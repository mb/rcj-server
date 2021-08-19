from utils import write_data_to_json, get_data_from_json
import datetime

# TODO: log warning if first_day or second_day matches today

"""
WARNING: SCHEDULE MUST NOT BE RECREATED DURING COMPETITION! RUN_IDS AND TIMES DEPEND ON NUMBER OF TEAMS!

This script will create the schedule for RCJ Berlin.
A few things can be configured, but other things are just assumed and hard-coded.

Assumptions / hard-coded decisions:
- two days, two arenas per competition (line / line-entry)
- two runs on first day, one on second day (per team)
- first day: teams will have a run of each of the arenas for their competition, each arena has distinct map
- second day: both arenas for a competition have the same map
- first team on first day will be last team on second day
- there will be a break on first day; referees will switch to another arena of another competition during this break
  -> effective length of break is average of the breaks of each competition/arenas
- there will probably be a shorter and a longer block among both competitions
  -> they will be aligned so that the shorter block has empty blocks before and after it (centered / same average)
  -> in case number of empty blocks is odd, ealier start for shorter block is preferred
- if odd number of teams in competition, prefer to start at same time and end shifted by one slot
"""

EVENT = "2022-berlin"
COMPETITIONS = ["line-entry", "line"]
ARENA_IDS = { "line-entry": ["A", "B"], "line": ["C", "D"] }

# dates need to be in "YYYY-MM-DD" format and times in "HH.mm" format
COMPETITION_START_TIME_FIRST_DAY = "11.30"
MINIMUM_BREAK_LENGTH_PER_ARENA_IN_MINUTES = 20 # needed for possible delays + new referees can familiarize themselves with arena
MINIMUM_BREAK_LENGTH_FOR_REFEREES_IN_MINUTES = 50
COMPETITION_END_TIME_SECOND_DAY = "13.10"
FIRST_DAY = "2022-04-01"
SECOND_DAY = "2022-04-02"
TIMEZONE = "+02"
SLOT_LENGTH_IN_MINUTES = 10

time_format_string = "%Y-%m-%dT%H:%M:%S" + TIMEZONE

teams = get_data_from_json("teams.json")
teams_per_competition = { "line-entry": [], "line": [] }
for team in teams:
    teams_per_competition[team["competition"]].append(team)

schedule = []
MAX_NUMBER_OF_SLOTS = int(max(len(teams_per_competition["line-entry"]), len(teams_per_competition["line"])) / 2 + 0.5)

# day 1
MIN_NUMBER_OF_SLOTS = int(min(len(teams_per_competition["line-entry"]), len(teams_per_competition["line"])) / 2 + 0.5)
empty_slots_in_shorter_competition_block_used_for_break = int((MAX_NUMBER_OF_SLOTS - MIN_NUMBER_OF_SLOTS) / 2 + 0.5)
effective_break_length_for_referees_when_using_min_break_length_on_longer_competition_block = empty_slots_in_shorter_competition_block_used_for_break * SLOT_LENGTH_IN_MINUTES + MINIMUM_BREAK_LENGTH_PER_ARENA_IN_MINUTES
break_length_on_longer_competition_block = MINIMUM_BREAK_LENGTH_PER_ARENA_IN_MINUTES + max(0, MINIMUM_BREAK_LENGTH_FOR_REFEREES_IN_MINUTES - effective_break_length_for_referees_when_using_min_break_length_on_longer_competition_block)
number_of_slots_for_break_on_longer_competition_block = break_length_on_longer_competition_block // SLOT_LENGTH_IN_MINUTES + (1 if break_length_on_longer_competition_block % SLOT_LENGTH_IN_MINUTES else 0)
start_time = datetime.datetime(*[int(x) for x in (FIRST_DAY.split("-") + COMPETITION_START_TIME_FIRST_DAY.split("."))])
for competition in COMPETITIONS:
    number_of_slots = int(len(teams_per_competition[competition]) / 2 + 0.5)
    slot_offset_from_start = int((MAX_NUMBER_OF_SLOTS - number_of_slots) / 2)
    empty_slots_at_end_of_first_block = MAX_NUMBER_OF_SLOTS - number_of_slots - slot_offset_from_start
    slots_for_break = 2 * empty_slots_at_end_of_first_block + number_of_slots_for_break_on_longer_competition_block
    current_slot_start_time = start_time + datetime.timedelta(minutes=slot_offset_from_start * SLOT_LENGTH_IN_MINUTES)
    for i in range(number_of_slots):
        second_slot_start_time = current_slot_start_time + datetime.timedelta(minutes=(number_of_slots + slots_for_break) * SLOT_LENGTH_IN_MINUTES)
        schedule.append({
            "competition": competition,
            "teamId": teams_per_competition[competition][i]["teamId"],
            "time": current_slot_start_time.strftime(time_format_string),
            "arenaId": ARENA_IDS[competition][0],
            "round": 1
        })
        schedule.append({
            "competition": competition,
            "teamId": teams_per_competition[competition][i]["teamId"],
            "time": second_slot_start_time.strftime(time_format_string),
            "arenaId": ARENA_IDS[competition][1],
            "round": 2
        })
        # if odd number of teams: prefer free slot in last slot (ignore when i=number_of_slots-1)
        if (i != number_of_slots-1 or len(teams_per_competition[competition]) % 2 == 0):
            schedule.append({
                "competition": competition,
                "teamId": teams_per_competition[competition][int(i + len(teams_per_competition[competition]) / 2 + 0.5)]["teamId"],
                "time": current_slot_start_time.strftime(time_format_string),
                "arenaId": ARENA_IDS[competition][1],
                "round": 1
            })
            schedule.append({
                "competition": competition,
                "teamId": teams_per_competition[competition][int(i + len(teams_per_competition[competition]) / 2 + 0.5)]["teamId"],
                "time": second_slot_start_time.strftime(time_format_string),
                "arenaId": ARENA_IDS[competition][0],
                "round": 2
            })
        current_slot_start_time += datetime.timedelta(minutes=SLOT_LENGTH_IN_MINUTES)

# day 2
# go backwards from end-time in slot_length-timesteps (teams should be in reversed order on this day -> go through teams from 0 to n)
end_time = datetime.datetime(*[int(x) for x in (SECOND_DAY.split("-") + COMPETITION_END_TIME_SECOND_DAY.split("."))])
for competition in COMPETITIONS:
    number_of_slots = int(len(teams_per_competition[competition]) / 2 + 0.5)
    slot_offset_from_end = int((MAX_NUMBER_OF_SLOTS - number_of_slots) / 2 + 0.5)
    current_slot_start_time = end_time - datetime.timedelta(minutes=slot_offset_from_end * SLOT_LENGTH_IN_MINUTES)
    for i in range(number_of_slots):
        current_slot_start_time -= datetime.timedelta(minutes=SLOT_LENGTH_IN_MINUTES)
        schedule.append({
            "competition": competition,
            "teamId": teams_per_competition[competition][i]["teamId"],
            "time": current_slot_start_time.strftime(time_format_string),
            "arenaId": ARENA_IDS[competition][0],
            "round": 3
        })
        # if odd number of teams: prefer free slot in last slot (ignore when i=0 coz we are going backwards)
        if (i != 0 or len(teams_per_competition[competition]) % 2 == 0):
            schedule.append({
                "competition": competition,
                "teamId": teams_per_competition[competition][i + len(teams_per_competition[competition]) // 2]["teamId"],
                "time": current_slot_start_time.strftime(time_format_string),
                "arenaId": ARENA_IDS[competition][1],
                "round": 3
            })

# add event and runId for all scheduled runs
run_id = 0
for scheduled_run in schedule:
    run_id += 1
    scheduled_run["event"] = EVENT
    scheduled_run["runId"] = run_id

write_data_to_json(schedule, "scheduled-runs.json")
