from utils import write_data_to_json

TEAMNAMES_LINE = [None for _ in range(32)]
TEAMNAMES_LINE_ENTRY = [None for _ in range(22)]

def teamnames_to_team_objects(teamnames, team_id_prefix, competition):
    teams = []
    for i in range(len(teamnames)):
        id = team_id_prefix + " " + str(i+1)
        teams.append({ "teamId": id, "name": teamnames[i] if teamnames[i] else id, "competition": competition })
    return teams

teams_line = teamnames_to_team_objects(TEAMNAMES_LINE, "RL", "line")
teams_line_entry = teamnames_to_team_objects(TEAMNAMES_LINE_ENTRY, "RLE", "line-entry")

teams = []
for team in teams_line:
    teams.append(team)
for team in teams_line_entry:
    teams.append(team)

write_data_to_json(teams, "teams.json")
