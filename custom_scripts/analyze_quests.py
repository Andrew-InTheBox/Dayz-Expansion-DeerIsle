import json
import os
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_positions(data):
    positions = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "Waypoints" and isinstance(value, list):
                positions.extend(value)
            elif isinstance(value, (dict, list)):
                positions.extend(extract_positions(value))
    elif isinstance(data, list):
        for item in data:
            positions.extend(extract_positions(item))
    return positions

def process_quests(quests_dir, objectives_dir, npcs_dir):
    quests = {}
    objectives = defaultdict(dict)
    npcs = {}

    # Load NPCs
    for npc_file in os.listdir(npcs_dir):
        if npc_file.endswith('.json'):
            npc_data = load_json(os.path.join(npcs_dir, npc_file))
            npcs[npc_data['ID']] = {
                'Name': npc_data['NPCName'],
                'Position': npc_data['Position']
            }

    # Load Objectives
    for obj_type in os.listdir(objectives_dir):
        obj_type_dir = os.path.join(objectives_dir, obj_type)
        if os.path.isdir(obj_type_dir):
            for obj_file in os.listdir(obj_type_dir):
                if obj_file.endswith('.json'):
                    obj_data = load_json(os.path.join(obj_type_dir, obj_file))
                    objectives[obj_type][obj_data['ID']] = {
                        'ObjectiveText': obj_data['ObjectiveText'],
                        'ID': obj_data['ID'],
                        'ObjectiveType': obj_data['ObjectiveType'],
                        'Positions': extract_positions(obj_data)
                    }

    # Load and process Quests
    for quest_file in os.listdir(quests_dir):
        if quest_file.endswith('.json'):
            quest_data = load_json(os.path.join(quests_dir, quest_file))
            quest_objectives = []
            for obj in quest_data['Objectives']:
                obj_type = next((t for t in objectives.keys() if objectives[t].get(obj['ID'])), None)
                if obj_type:
                    obj_info = objectives[obj_type][obj['ID']]
                    quest_objectives.append({
                        'Text': obj_info['ObjectiveText'],
                        'ID': obj_info['ID'],
                        'Type': obj_info['ObjectiveType'],
                        'Positions': obj_info['Positions']
                    })
                else:
                    quest_objectives.append({
                        'Text': f"Unknown Objective (Type: {obj['ObjectiveType']}, ID: {obj['ID']})",
                        'ID': obj['ID'],
                        'Type': obj['ObjectiveType'],
                        'Positions': []
                    })

            # Process rewards
            rewards = []
            for reward in quest_data.get('Rewards', []):
                rewards.append({
                    'ClassName': reward['ClassName'],
                    'Amount': reward['Amount'],
                    'Chance': reward.get('Chance', 1.0)
                })

            quests[quest_data['ID']] = {
                'Title': quest_data['Title'],
                'Objectives': quest_objectives,
                'QuestGiver': npcs.get(quest_data['QuestGiverIDs'][0], 'Unknown NPC') if quest_data['QuestGiverIDs'] else 'No Quest Giver',
                'Rewards': rewards
            }

    return quests

def generate_report(quests):
    report = []
    for quest_id, quest_data in quests.items():
        report.append(f"Quest ID: {quest_id}")
        report.append(f"Title: {quest_data['Title']}")
        report.append("Objectives:")
        for obj in quest_data['Objectives']:
            report.append(f"  - ID: {obj['ID']}, Type: {obj['Type']}")
            report.append(f"    Text: {obj['Text']}")
            if obj['Positions']:
                report.append("    Positions:")
                for pos in obj['Positions']:
                    report.append(f"      {pos}")
        quest_giver = quest_data['QuestGiver']
        if isinstance(quest_giver, dict):
            report.append(f"Quest Giver: {quest_giver['Name']} at position {quest_giver['Position']}")
        else:
            report.append(f"Quest Giver: {quest_giver}")
        report.append("Rewards:")
        if quest_data['Rewards']:
            for reward in quest_data['Rewards']:
                report.append(f"  - {reward['Amount']} x {reward['ClassName']} (Chance: {reward['Chance']})")
        else:
            report.append("  No rewards")
        report.append("")
    
    return "\n".join(report)

# Usage
quests_dir = './config/ExpansionMod/Quests/Quests'
objectives_dir = './config/ExpansionMod/Quests/Objectives'
npcs_dir = './config/ExpansionMod/Quests/NPCs'

quests = process_quests(quests_dir, objectives_dir, npcs_dir)
report = generate_report(quests)

# Print the report
print(report)

# Optionally, save the report to a file
with open('quest_report.txt', 'w') as f:
    f.write(report)
