# DayZ-Expansion-DeerIsle

This repository contains the configuration files for a DayZ server setup using the DeerIsle expansion. The files are located in the `./config` and `./mpmissions/Expansion.deerisle` directories.

The setup includes:
- The Expansion bundle
- Several quests
- Multiple market traders

> **Note:** MMG equipment is integrated, but the category for market items can be removed if necessary.

## Startup Note

The startup batch file identifies any directory starting with "@" as a mod. Consequently, server-side mods must not start with "@" in their names. In this setup, server-side mods are denoted with "_XYZ". Add the ones you are using manually to the startup batch.

## AI Configuration

LoootingBehavior can have the options described here:

eAILootingBehavior
NONE
WEAPONS_FIREARMS 
WEAPONS_LAUNCHERS
WEAPONS_MELEE
WEAPONS
BANDAGES
CLOTHING
UPGRADE 
DEFAULT
ALL

DEFAULT is synonymous to WEAPONS (but may be subject to change)
WEAPONS is shorthand for WEAPONS_FIREARMS | WEAPONS_LAUNCHERS | WEAPONS_MELEE

You can combine options like this:
    "LootingBehaviour": "WEAPONS_MELEE | CLOTHING"

## Mods Used

The setup utilizes the following mods:

- **DeerIsle**
- **BulletStacksPlusEnhanced**
- **CF**
- **COT**
- **DabsFramework**
- **DayZ-Editor-Loader**
- **Dayz-Expansion-Animations**
- **DayZ-Expansion-Bundle**
- **DayZ-Expansion-Licensed**
- **MMG-MightysMilitaryGear**
- **PvZmoD_CustomizableZombies**
- **NoForceWeaponRaise**
- **RedFalconHelis**
- **SNAFUWeapons**
- **InventoryRevert**
- **MetroWatchPack-OG**
- **_DayZ-Dynamic-AI-Addon** (server-side)

MMG mod types.xml files are set for military & all tiers *except* tiers 2 and 3.   Meaning, no MMG gear should spawn on starting islands.
