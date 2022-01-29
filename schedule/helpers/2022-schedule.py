from utils import write_data_to_json, get_data_from_json
import datetime


EVENT = "2022-berlin"
COMPETITIONS = ["line-entry", "line"]
ARENA_ID = { "line-entry": "B", "line": "A" }

# dates need to be in "YYYY-MM-DD" format and times in "HH.mm" format
COMPETITION_DAY = "2022-03-19"
COMPETITION_START_TIME = "10.00"
TIMEZONE = "+01"
SLOT_LENGTH_IN_MINUTES = 10
BREAKS = [["11.00","11.10"], ["12.20","13.10"]]

time_format_string = "%Y-%m-%dT%H:%M:%S" + TIMEZONE

teams = []
for e in [1, 2, 11, 5, 3, 13, 6, 4, None, 8, 14, 10, 9, 15, 7, None, 12]:
    teams.append({ "competition": "line", "teamId": "RL " + str(e) if e else None })
for e in [3, 7, 1, 10, 8, 5, 13, 11, 6, 14, 15, 12, 16, 9, 4, None, 2]:
    teams.append({ "competition": "line-entry", "teamId": "RLE " + str(e) if e else None })

teams_per_competition = { "line-entry": [], "line": [] }
for team in teams:
    teams_per_competition[team["competition"]].append(team)

schedule = []

def to_dt(day, time):
    return datetime.datetime(*[int(x) for x in (day.split("-") + time.split("."))])

for competition in COMPETITIONS:
    current_slot_start_time = to_dt(COMPETITION_DAY, COMPETITION_START_TIME)
    break_id = 0
    next_break = to_dt(COMPETITION_DAY, BREAKS[break_id][0])
    for i in range(len(teams_per_competition[competition])):
        team = teams_per_competition[competition][i]["teamId"]
        if (team):
            schedule.append({
                "competition": competition,
                "teamId": team,
                "time": current_slot_start_time.strftime(time_format_string),
                "arenaId": ARENA_ID[competition],
                "round": 1
            })
        current_slot_start_time += datetime.timedelta(minutes=SLOT_LENGTH_IN_MINUTES)
        if (current_slot_start_time >= next_break):
            current_slot_start_time = to_dt(COMPETITION_DAY, BREAKS[break_id][1])
            break_id += 1
            next_break = to_dt(*([COMPETITION_DAY, BREAKS[break_id][0]] if break_id < len(BREAKS) else ["9999-12-31", "23.59"]))

# add event and runId for all scheduled runs
run_id = 0
for scheduled_run in schedule:
    run_id += 1
    scheduled_run["event"] = EVENT
    scheduled_run["runId"] = run_id

write_data_to_json(schedule, "scheduled-runs.json")
