#!/usr/bin/env python3
"""
Slow wiki scraper for GitHub wikis.

Example:
  python scrape_wiki.py \
    --start "https://github.com/salutesh/DayZ-Expansion-Scripts/wiki" \
    --section-heading "Expansion Settings:" \
    --depth 2 \
    --delay 2.5 \
    --out ./custom_scripts/docs/output/expansion_wiki

Dependencies:
  pip install requests beautifulsoup4 markdownify
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass
from typing import Iterable, Optional
from urllib.parse import unquote, urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup, Tag

try:
    from markdownify import markdownify as html_to_md
except Exception:
    html_to_md = None


WIKI_DEFAULT_SELECTORS = [
    "#wiki-body",                # common
    "div.wiki-wrapper",          # sometimes present
    "div.markdown-body",         # GitHub markdown render
    "main",                      # fallback
]

# Selectors for sidebar content (used for finding section links)
WIKI_SIDEBAR_SELECTORS = [
    "div.wiki-custom-sidebar",   # GitHub wiki sidebar
    "div.gollum-markdown-content",
]

USER_AGENT = "local-doc-builder/1.0 (polite scraper; contact: andrew.box.81@gmail.com)"


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    html: str
    md: str
    link_label: str = ""  # The text of the link that led to this page


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:120] or "page"


def stable_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def title_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    tail = path.split("/")[-1] if path else ""
    tail = unquote(tail)
    tail = re.sub(r"^\[[^\]]+\][-_ ]*", "", tail)
    tail = tail.replace("-", " ").replace("_", " ").strip()
    tail = re.sub(r"\s+", " ", tail)
    return tail or "page"


def is_same_wiki(base_wiki_url: str, candidate: str) -> bool:
    """
    Only allow links that stay within the same wiki namespace:
      https://github.com/<owner>/<repo>/wiki/...
    """
    b = urlparse(base_wiki_url)
    c = urlparse(candidate)
    if c.scheme and c.scheme != b.scheme:
        return False
    if c.netloc and c.netloc != b.netloc:
        return False

    # Normalize paths
    base_path = b.path.rstrip("/")
    cand_path = c.path

    # base_path is .../wiki
    # allow .../wiki or .../wiki/<something>
    return cand_path.startswith(base_path)


def polite_sleep(base_seconds: float) -> None:
    jitter = random.uniform(0.3, 1.2)
    time.sleep(base_seconds * jitter)


def pick_main_content(soup: BeautifulSoup) -> Tag:
    for sel in WIKI_DEFAULT_SELECTORS:
        node = soup.select_one(sel)
        if node and isinstance(node, Tag):
            # prefer the most "content-like" node
            return node
    # as a last resort
    return soup.body if soup.body else soup


def pick_sidebar_content(soup: BeautifulSoup) -> Optional[Tag]:
    """Find sidebar content area (GitHub wikis have custom sidebars)."""
    for sel in WIKI_SIDEBAR_SELECTORS:
        node = soup.select_one(sel)
        if node and isinstance(node, Tag):
            return node
    return None


def extract_title(soup: BeautifulSoup) -> str:
    # GitHub's page header title is the most reliable for wiki pages.
    for sel in ["h1.gh-header-title", "#wiki-body h1", "div.markdown-body h1"]:
        h1 = soup.select_one(sel)
        if h1:
            t = h1.get_text(" ", strip=True)
            if t and len(t) < 100:  # Reasonable title length
                return t
    og_title = soup.select_one('meta[property="og:title"]')
    if og_title and og_title.get("content"):
        t = og_title["content"].strip()
        if t:
            return t
    # Fallback to any h1
    h1 = soup.select_one("h1")
    if h1:
        t = h1.get_text(" ", strip=True)
        if t and len(t) < 100:
            return t
    # Use page title, strip common suffixes
    if soup.title:
        t = soup.title.get_text(" ", strip=True)
        # Remove GitHub wiki suffix patterns
        for suffix in [" · Wiki · ", " - Wiki", " · salutesh/"]:
            if suffix in t:
                t = t.split(suffix)[0]
        if t:
            return t
    return "Untitled"


def html_to_markdown(html_fragment: str) -> str:
    if html_to_md is not None:
        # GitHub pages are already fairly clean HTML
        return html_to_md(html_fragment, heading_style="ATX").strip() + "\n"
    # fallback: very plain text
    soup = BeautifulSoup(html_fragment, "html.parser")
    return soup.get_text("\n", strip=True) + "\n"


def fetch(session: requests.Session, url: str, timeout: int = 30) -> str:
    # GitHub sometimes prefers no fragment; also avoid double-hits
    url, _frag = urldefrag(url)

    for attempt in range(1, 6):
        r = session.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.text

        # Backoff on rate limiting / transient blocks
        if r.status_code in (403, 429, 502, 503, 504):
            backoff = min(60.0, 2.0 ** attempt) + random.uniform(0.0, 1.5)
            print(f"[warn] {r.status_code} for {url} -> sleeping {backoff:.1f}s", file=sys.stderr)
            time.sleep(backoff)
            continue

        r.raise_for_status()

    raise RuntimeError(f"Failed to fetch after retries: {url}")


def find_section_links(main: Tag, section_heading: str, base_url: str) -> list[tuple[str, str]]:
    """
    Find links under an H1 heading with class heading-element and text == section_heading.
    Collect <a href> until the next H1.
    Returns list of (url, link_label) tuples.
    """
    heading = None
    for h in main.select("h1.heading-element, h1"):
        text = h.get_text(" ", strip=True)
        if text == section_heading:
            heading = h
            break

    if not heading:
        return []

    # GitHub wraps h1 in <div class="markdown-heading">, so start from parent if needed
    start_node = heading
    if heading.parent and heading.parent.name == "div":
        start_node = heading.parent

    links: list[tuple[str, str]] = []
    node = start_node.next_sibling
    while node:
        # Stop at next h1 (either direct or wrapped in markdown-heading div)
        if isinstance(node, Tag):
            if node.name == "h1":
                break
            if node.name == "div" and node.select_one("h1"):
                break
        if isinstance(node, Tag):
            for a in node.select("a[href]"):
                href = a.get("href")
                if not href:
                    continue
                abs_url = urljoin(base_url, href)
                abs_url, _ = urldefrag(abs_url)
                link_label = a.get_text(" ", strip=True)
                links.append((abs_url, link_label))
        node = node.next_sibling

    # de-dup by URL, preserve order
    seen = set()
    out = []
    for url, label in links:
        if url not in seen:
            seen.add(url)
            out.append((url, label))
    return out


def extract_internal_wiki_links(main: Tag, base_wiki_url: str, page_url: str) -> list[tuple[str, str]]:
    """
    Pull internal wiki links from the main content.
    Used for depth expansion.
    """
    links: list[tuple[str, str]] = []
    for a in main.select("a[href]"):
        href = a.get("href")
        if not href:
            continue
        abs_url = urljoin(page_url, href)
        abs_url, _ = urldefrag(abs_url)
        if is_same_wiki(base_wiki_url, abs_url):
            label = a.get_text(" ", strip=True)
            links.append((abs_url, label))

    # de-dup, preserve order
    seen = set()
    out = []
    for u, label in links:
        if u not in seen:
            seen.add(u)
            out.append((u, label))
    return out


_used_filenames: set[str] = set()


def save_page(outdir: str, page: Page) -> tuple[str, str]:
    os.makedirs(outdir, exist_ok=True)

    # Prefer link_label (from sidebar) over extracted title
    name_source = page.link_label if page.link_label else page.title
    if not name_source or name_source.strip().lower() == "expansion settings:":
        name_source = title_from_url(page.url)
    safe_name = slugify(name_source)

    # Find unique filename (add counter if needed)
    base = safe_name
    counter = 1
    while base in _used_filenames:
        counter += 1
        base = f"{safe_name}-{counter}"
    _used_filenames.add(base)

    html_path = os.path.join(outdir, base + ".html")
    md_path = os.path.join(outdir, base + ".md")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(page.html)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(page.md)

    return html_path, md_path


def build_combined_md(pages: list[Page], out_path: str) -> None:
    # Keep stable order as scraped
    lines: list[str] = []
    lines.append("# Local Wiki Documentation\n")
    lines.append("> Generated by scrape_wiki.py\n\n")
    lines.append("## Index\n")
    for p in pages:
        display_name = p.link_label if p.link_label else p.title
        anchor = slugify(display_name)
        lines.append(f"- [{display_name}](#{anchor})\n")
    lines.append("\n---\n\n")

    for p in pages:
        display_name = p.link_label if p.link_label else p.title
        lines.append(f"## {display_name}\n\n")
        lines.append(f"Source: {p.url}\n\n")
        lines.append(p.md)
        lines.append("\n---\n\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="Wiki landing page URL")
    ap.add_argument("--section-heading", required=True, help='Exact heading text, e.g. "Expansion Settings:"')
    ap.add_argument("--depth", type=int, default=2, help="Max depth (0=start only, 1=section links, 2=section links + their links)")
    ap.add_argument("--delay", type=float, default=2.5, help="Base delay between requests (seconds), jittered")
    default_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "local_wiki")
    ap.add_argument("--out", default=default_out, help="Output directory")
    ap.add_argument(
        "--extra-seed-url",
        action="append",
        default=[],
        help=(
            "Additional page URL to scrape as a depth-1 seed. "
            "Useful for hub pages that are missing from the main section crawl."
        ),
    )
    args = ap.parse_args()

    base_wiki_url = args.start.rstrip("/")
    outdir = args.out

    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
    })

    visited: set[str] = set()
    scraped_pages: list[Page] = []

    def scrape_one(url: str, link_label: str = "") -> Optional[Page]:
        url, _ = urldefrag(url)
        if url in visited:
            return None
        visited.add(url)

        polite_sleep(args.delay)
        html = fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")
        title = extract_title(soup)
        main_node = pick_main_content(soup)

        # Store only the main content fragment for MD conversion
        main_html = str(main_node)
        md = html_to_markdown(main_html)

        page = Page(url=url, title=title, html=html, md=md, link_label=link_label)
        save_page(outdir, page)
        display_name = link_label if link_label else title
        print(f"[ok] {display_name} <- {url}")
        return page

    # Depth 0: start page
    p0 = scrape_one(args.start)
    if p0:
        scraped_pages.append(p0)
    if args.depth <= 0 or not p0:
        build_combined_md(scraped_pages, os.path.join(outdir, "DOCUMENTATION.md"))
        return 0

    # Extract section links from the start page content (try main, then sidebar)
    soup0 = BeautifulSoup(p0.html, "html.parser")
    main0 = pick_main_content(soup0)
    section_links = find_section_links(main0, args.section_heading, base_url=args.start)

    # If not found in main content, try the sidebar
    if not section_links:
        sidebar0 = pick_sidebar_content(soup0)
        if sidebar0:
            section_links = find_section_links(sidebar0, args.section_heading, base_url=args.start)

    if not section_links:
        print(f"[warn] Could not find links under heading: {args.section_heading}", file=sys.stderr)
        print("[warn] Tip: confirm the heading text matches exactly (including colon).", file=sys.stderr)

    # Crawl seed links plus any explicit extra seed pages.
    frontier: list[tuple[str, str]] = []

    def scrape_seed(url: str, label: str = "") -> Optional[Page]:
        if not is_same_wiki(base_wiki_url, url):
            return None
        p = scrape_one(url, link_label=label)
        if p:
            scraped_pages.append(p)
            return p
        return None

    for url, label in section_links:
        frontier.append((url, label))

    for extra_url in args.extra_seed_url:
        frontier.append((extra_url, ""))

    if args.depth <= 1:
        for url, label in frontier:
            scrape_seed(url, label=label)
        build_combined_md(scraped_pages, os.path.join(outdir, "DOCUMENTATION.md"))
        return 0

    for current_depth in range(1, args.depth + 1):
        next_frontier: list[tuple[str, str]] = []
        for url, label in frontier:
            page_obj = scrape_seed(url, label=label)
            if current_depth >= args.depth or not page_obj:
                continue

            soup = BeautifulSoup(page_obj.html, "html.parser")
            main_node = pick_main_content(soup)
            internal_links = extract_internal_wiki_links(main_node, base_wiki_url=base_wiki_url, page_url=url)

            max_children_per_page = 30
            internal_links = internal_links[:max_children_per_page]
            next_frontier.extend(internal_links)

        frontier = next_frontier

    # Build combined documentation
    build_combined_md(scraped_pages, os.path.join(outdir, "DOCUMENTATION.md"))
    print(f"[done] Wrote combined file: {os.path.join(outdir, 'DOCUMENTATION.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
