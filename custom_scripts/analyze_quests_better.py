import os
import json
import glob

# Get the path to the parent directory of custom_scripts
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Function to create the correct path
def get_config_path(*args):
    return os.path.join(base_path, 'config', 'ExpansionMod', 'Quests', *args)

def find_positions_and_waypoints(data):
    positions = []
    waypoints = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "Position" and isinstance(value, list) and len(value) == 3:
                positions.append(value)
            elif key == "Waypoints" and isinstance(value, list):
                waypoints.extend(value)
            elif isinstance(value, (dict, list)):
                pos, way = find_positions_and_waypoints(value)
                positions.extend(pos)
                waypoints.extend(way)
    elif isinstance(data, list):
        for item in data:
            pos, way = find_positions_and_waypoints(item)
            positions.extend(pos)
            waypoints.extend(way)
    return positions, waypoints

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def find_objective_file(objective_id, objective_type):
    for obj_file in glob.glob(get_config_path('Objectives', '**', '*.json'), recursive=True):
        data = load_json(obj_file)
        if data.get('ID') == objective_id and data.get('ObjectiveType') == objective_type:
            return data
    return None

def find_npc_file(npc_id):
    for npc_file in glob.glob(get_config_path('NPCs', '*.json')):
        data = load_json(npc_file)  # Changed obj_file to npc_file
        if data.get('ID') == npc_id:
            return data
    return None


def analyze_quests():
    report = []
    
    for quest_file in glob.glob(get_config_path('Quests', '*.json')):
        quest_data = load_json(quest_file)
        quest_id = quest_data.get('ID')
        quest_title = quest_data.get('Title', 'Untitled')  # Get the title, default to 'Untitled' if not found
        
        report.append(f"Quest ID: {quest_id} - Title: {quest_title}")  # Add title to the report
        
        # NPC information
        npc_ids = quest_data.get('QuestGiverIDs', [])
        for npc_id in npc_ids:
            npc_data = find_npc_file(npc_id)
            if npc_data:
                npc_name = npc_data.get('NPCName', 'Unknown')
                npc_position = npc_data.get('Position', [])
                report.append(f"NPC Name: {npc_name}")
                report.append(f"NPC Position: {npc_position}")
        
        # Objective information
        for objective in quest_data.get('Objectives', []):
            obj_id = objective.get('ID')
            obj_type = objective.get('ObjectiveType')
            
            obj_data = find_objective_file(obj_id, obj_type)
            if obj_data:
                report.append(f"Objective ID: {obj_id}")
                report.append(f"Objective Type: {obj_type}")
                
                positions, waypoints = find_positions_and_waypoints(obj_data)
                for pos in positions:
                    report.append(f"Position: X={pos[0]}, Y={pos[1]}, Z={pos[2]}")
                
                if waypoints:
                    report.append("Waypoints:")
                    for i, wp in enumerate(waypoints, 1):
                        report.append(f"  Waypoint {i}: X={wp[0]}, Y={wp[1]}, Z={wp[2]}")
        
        report.append("\n")  # Add a blank line between quests
    
    # Write report to file
    with open(os.path.join(base_path, 'custom_scripts', 'quest_analysis_report.txt'), 'w') as f:
        f.write('\n'.join(report))


analyze_quests()
