from espnfantasy import FantasyLeague
import pprint
import os
from graphic import FFGraphic

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

week = 9
data = league.get_matchup_data(week)
league.load_team_names(week)

league.get_league_data(week)

print(f"WEEK {week} RESULTS:")
achievement_title = ""
achievement_result = 0
achievement_list = []
achievement_unit = ""

if week == 1:
    achievement_title = "Weakest RB"
    achievement_result = league.get_weakest_rb()
    achievement_list = league.get_weakest_rb(detailed=True)
    achievement_unit = "Yards"
elif week == 2:
    achievement_title = "Worst Flex"
    achievement_result = league.get_worst_flex()
    achievement_list = league.get_worst_flex(detailed=True)
    achievement_unit = "Points"
elif week == 3:
    achievement_title = "Stickiest WR"
    achievement_result = league.get_stickiest_wr()
    achievement_list = league.get_stickiest_wr(detailed=True)
    achievement_unit = "%"
elif week == 4:
    achievement_title = "Blindest QB"
    achievement_result = league.get_blindest_qb()
    achievement_list = league.get_blindest_qb(detailed=True)
    achievement_unit = "Int"
elif week == 5:
    achievement_title = "Slowest QB"
    achievement_result = league.get_slowest_qb()
    achievement_list = league.get_slowest_qb(detailed=True)
    achievement_unit = "Yards"
elif week == 6:
    achievement_title = "Fire Kicker"
    achievement_result = league.get_fire_kicker()
    achievement_list = league.get_fire_kicker(detailed=True)
    achievement_unit = "Points"
elif week == 7:
    achievement_title = "Strongest Defense"
    achievement_result = league.get_strongest_defense()
    achievement_list = league.get_strongest_defense(detailed=True)
    achievement_unit = "Points"
elif week == 8:
    achievement_title = "Most Made PAT"
    achievement_result = league.get_most_made_PAT()
    achievement_list = league.get_most_made_PAT(detailed=True)
    achievement_unit = "Extra Points"
elif week == 9:
    achievement_title = "Butter WR"
    achievement_result = league.get_butter_wr()
    achievement_list = league.get_butter_wr(detailed=True)
    achievement_unit = "%"
elif week == 10:
    achievement_title = "Frozen Kicker"
    achievement_result = league.get_frozen_kicker()
    achievement_list = league.get_frozen_kicker(detailed=True)
    achievement_unit = "Points"
elif week == 11:
    achievement_title = "Most Throwing Yards"
    achievement_result = league.get_most_throwing_yards()
    achievement_list = league.get_most_throwing_yards(detailed=True)
    achievement_unit = "Yards"
elif week == 12:
    achievement_title = "Strongest RB"
    achievement_result = league.get_strongest_rb()
    achievement_list = league.get_strongest_rb(detailed=True)
    achievement_unit = "Yards"
elif week == 13:
    achievement_title = "Least Touchdowns"
    achievement_result = league.get_least_touchdowns()
    achievement_list = league.get_least_touchdowns(detailed=True)
    achievement_unit = "Touchdowns"
elif week == 14:
    achievement_title = "Weakest Defense"
    achievement_result = league.get_weakest_defense()
    achievement_list = league.get_weakest_defense(detailed=True)
    achievement_unit = "Points"
elif week == 15:
    achievement_title = "Stickiest RB"
    achievement_result = league.get_stickiest_rb()
    achievement_list = league.get_stickiest_rb(detailed=True)
    achievement_unit = "%"
elif week == 16:
    achievement_title = "Most Touchdowns"
    achievement_result = league.get_most_touchdowns()
    achievement_list = league.get_most_touchdowns(detailed=True)
    achievement_unit = "Touchdowns"
elif week == 17:
    achievement_title = "Butter RB"
    achievement_result = league.get_butter_rb()
    achievement_list = league.get_butter_rb(detailed=True)
    achievement_unit = "%"
elif week == 18:
    achievement_title = "Most Rushing Yards"
    achievement_result = league.get_most_rushing_yards()
    achievement_list = league.get_most_rushing_yards(detailed=True)
    achievement_unit = "Yards"

team_name = achievement_result[0]
player_name, *result = achievement_result[1]

achievement_team = league.teams_dict[team_name]
achievement_player = {}
for player in league.player_dict[team_name]:
    if player["player_name"] == player_name:
        achievement_player = player
        break

print(achievement_title)
print(achievement_result)
pprint.pprint(list(achievement_list))

FFGraphic(
    achievement_team,
    achievement_player,
    achievement_title,
    result,
    achievement_unit,
)
# with open("stats.json", "w") as f:
#     json.dump(league.player_dict, f)
