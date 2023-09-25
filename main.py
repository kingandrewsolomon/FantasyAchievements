from espnfantasy import FantasyLeague
import pprint
import os

with open(".env", "r") as f:
    for line in f:
        env_name, env_value = line.split(" = ")
        os.environ[env_name] = env_value.strip()

year = 2023
league_id = os.environ["LEAGUE_ID"]
swid = os.environ["SWID"]
espn_s2 = os.environ["ESPN_S2"]

cookies = {"swid": swid, "espn_s2": espn_s2}

league = FantasyLeague(league_id, year, espn_s2, swid)

week = 3
data = league.get_matchup_data(week)
league.load_team_names(week)

league.get_league_data(week)

print(f"WEEK {week} RESULTS:")

if week == 1:
    print("get_weakest_rb")
    print(league.get_weakest_rb())
    pprint.pprint(list(league.get_weakest_rb(detailed=True)))
if week == 2:
    print("get_worst_flex")
    print(league.get_worst_flex())
    pprint.pprint(list(league.get_worst_flex(detailed=True)))
if week == 3:
    print("get_stickiest_wr")
    print(league.get_stickiest_wr())
    pprint.pprint(list(league.get_stickiest_wr(detailed=True)))
if week == 4:
    print("get_most_interceptions")
    print(league.get_most_interceptions())
    pprint.pprint(list(league.get_most_interceptions(detailed=True)))
if week == 5:
    print("get_slowest_qb")
    print(league.get_slowest_qb())
    pprint.pprint(list(league.get_slowest_qb(detailed=True)))
if week == 6:
    print("get_fire_kicker")
    print(league.get_fire_kicker())
    pprint.pprint(list(league.get_fire_kicker(detailed=True)))
if week == 7:
    print("get_strongest_defense")
    print(league.get_strongest_defense())
    pprint.pprint(list(league.get_strongest_defense(detailed=True)))
if week == 8:
    print("get_most_made_PAT")
    print(league.get_most_made_PAT())
    pprint.pprint(list(league.get_most_made_PAT(detailed=True)))
if week == 9:
    print("get_butter_wr")
    print(league.get_butter_wr())
    pprint.pprint(list(league.get_butter_wr(detailed=True)))
if week == 10:
    print("get_frozen_kicker")
    print(league.get_frozen_kicker())
    pprint.pprint(list(league.get_frozen_kicker(detailed=True)))
if week == 11:
    print("get_most_throwing_yards")
    print(league.get_most_throwing_yards())
    pprint.pprint(list(league.get_most_throwing_yards(detailed=True)))
if week == 12:
    print("get_strongest_rb")
    print(league.get_strongest_rb())
    pprint.pprint(list(league.get_strongest_rb(detailed=True)))
if week == 13:
    print("get_least_touchdowns")
    print(league.get_least_touchdowns())
    pprint.pprint(list(league.get_least_touchdowns(detailed=True)))
if week == 14:
    print("get_weakest_defense")
    print(league.get_weakest_defense())
    pprint.pprint(list(league.get_weakest_defense(detailed=True)))
if week == 15:
    print("get_stickiest_rb")
    print(league.get_stickiest_rb())
    pprint.pprint(list(league.get_stickiest_rb(detailed=True)))
if week == 16:
    print("get_most_touchdowns")
    print(league.get_most_touchdowns())
    pprint.pprint(list(league.get_most_touchdowns(detailed=True)))
if week == 17:
    print("get_butter_rb")
    print(league.get_butter_rb())
    pprint.pprint(list(league.get_butter_rb(detailed=True)))
if week == 18:
    print("get_most_rushing_yards")
    print(league.get_most_rushing_yards())
    pprint.pprint(list(league.get_most_rushing_yards(detailed=True)))

# with open("stats.json", "w") as f:
#     json.dump(league.player_dict, f)
