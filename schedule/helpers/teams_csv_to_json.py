from utils import write_data_to_json, get_data_from_csv

csv_rows = get_data_from_csv("helpers/teams-2022", delim="\t", includes_header=False)

teams = []

for team in csv_rows:
    team_id = team[0]
    teamname = team[1]
    teams.append({
        "teamId": team_id,
        "name": teamname,
        "competition": "line-entry" if team_id.startswith("RLE") else "line"
    })

write_data_to_json(teams, "teams.json")
