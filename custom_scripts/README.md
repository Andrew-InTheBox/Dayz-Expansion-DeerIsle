# Custom Scripts

Helper scripts are grouped by the kind of DayZ server configuration work they support. Each script category has an `output/` directory for generated reports, CSVs, plots, or transformed files.

## Folders

- `ai_patrols/`: AI patrol/location settings builders, reports, and map plots.
- `animals/`: Animal territory spawn-zone map plots.
- `roamers/`: Roamer heatmap, log, and animation plotting tools.
- `loadouts/`: Expansion loadout analysis and loadout mutation helpers.
- `market/`: Expansion market JSON pricing, threshold, and item helpers.
- `loot_types/`: `types.xml`, tier, nominal/minimum, and vehicle-spawn analysis helpers.
- `vehicles/`: Vehicle event spawn parsing and map plotting tools.
- `quests/`: Quest/NPC/objective analysis reports.
- `docs/`: Documentation scraping helpers.
- `maintenance/`: Broad server config maintenance and validation scripts.
- `assets/`: Shared static assets used by scripts, such as map background images.

Run Python scripts with `/home/acb/venv-dirs/venv-utils/bin/python` from the repo root unless a script says otherwise.
