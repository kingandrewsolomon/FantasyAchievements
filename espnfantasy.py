import requests
from team_colors import NFL_TEAMS


class FantasyLeague:
    """
    ESPN Fantasy Football League class for pulling data from the ESPN API
    """

    POSITION_MAPPING = {
        0: "QB",
        2: "RB",
        4: "WR",
        6: "TE",
        16: "D/ST",
        17: "K",
        23: "FLEX",
        20: "Bench",
        21: "IR",
        "": "NA",
    }

    POSITION_CODES = {1: "QB", 2: "RB", 3: "WR", 4: "TE", 16: "D/ST", 5: "K", "": "NA"}

    STAT_MAPPING = {
        "0": "Pass Attempts",
        "1": "Completions",
        "3": "Pass Yards",
        "4": "Pass Touchdowns",
        "20": "Interceptions",
        "23": "Rushing Attempts",
        "24": "Rushing Yards",
        "25": "Rushing Touchdowns",
        "41": "Receptions",
        "42": "Receiving Yards",
        "43": "Receiving Touchdowns",
        "58": "Targets",
        "83": "Field Goals Made",
        "84": "Field Goals Attempted",
        "86": "Extra Points Made",
        "87": "Extra Points Attempted",
        "214": "Yards1",
        "216": "Yards2",
    }

    def __init__(self, league_id, year, espn_s2, swid):
        self.league_id = league_id
        self.year = year
        self.espn_s2 = espn_s2
        self.swid = swid
        self.base_url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{self.year}/segments/0/leagues/{self.league_id}"
        self.cookies = {"swid": self.swid, "espn_s2": self.espn_s2}
        self.default_params = {"leagueId": self.league_id, "seasonId": self.year}

        self.league_json = {}
        self.teams_dict = {}

        self.player_dict = {}

        self.matchup_df = None
        self.team_df = None

    def make_request(self, week, view="", views=[], params=None):
        """
        Initiate a request to the ESPN API
        """
        url = self.base_url
        if len(view) > 0:
            self.default_params["view"] = view
        elif len(views) > 0:
            view_str = "&view=".join(views)
            url = self.base_url + "?view=" + view_str
        else:
            raise ValueError("Must have a view or views option")

        self.default_params["matchupPeriodId"] = week
        if params:
            self.default_params.update(params)
        return requests.get(
            url, params=self.default_params, cookies=self.cookies, timeout=30
        ).json()

    def load_league(self, week):
        """
        Load the league JSON from the ESPN API
        """
        return self.make_request(
            week=week,
            views=["mMatchup", "mMatchupScore"],
            params={"scoringPeriodId": week},
        )

    def load_player_data(self, week):
        """
        Load the player data from the league JSON
        """

        # Loop through each team
        for team in self.league_json["teams"]:
            team_name = self.teams_dict[team["name"]]["team_name"]
            self.player_dict[team_name] = []
            # Loop through each roster slot in each team
            for slot in team["roster"]["entries"]:
                player_info = {}
                # Append the week number to a list for each entry for each team

                # Append player name, player fantasy team, and player ro
                temp_info = slot["playerPoolEntry"]["player"]
                player_info["id"] = temp_info["id"]
                player_info["player_name"] = temp_info["fullName"]
                player_info["Position"] = self.POSITION_CODES[
                    temp_info["defaultPositionId"]
                ]
                player_info["Slot"] = self.POSITION_MAPPING[slot["lineupSlotId"]]
                player_info["proTeamId"] = temp_info["proTeamId"]
                player_info["proTeamColorScheme"] = NFL_TEAMS[temp_info["proTeamId"]]

                # Initialize the variables before using them
                player_info["stats"] = {}
                for statMap in self.STAT_MAPPING:
                    statName = self.STAT_MAPPING[statMap]
                    player_info["stats"][statName] = 0

                player_info["stats"]["Actual Total"] = 0

                # Loop through each statistic set for each roster slot for each team
                # to get projected and actual scores
                for stat in slot["playerPoolEntry"]["player"]["stats"]:
                    if stat["scoringPeriodId"] == week:
                        if stat["statSourceId"] == 0:
                            for statMap in self.STAT_MAPPING:
                                statName = self.STAT_MAPPING[statMap]
                                if statMap in stat["stats"]:
                                    player_info["stats"][statName] = stat["stats"][
                                        statMap
                                    ]

                            player_info["stats"]["Actual Total"] = stat["appliedTotal"]
                self.player_dict[team_name].append(player_info)

    def load_team_names(self, week):
        """
        Load the team names from the league JSON
        """
        # Define the URL with our parameters

        team_json = self.make_request(week, view="mTeam")

        # Loop through each team in the JSON
        for team in team_json["teams"]:
            # Append the team id and team name to the list
            team_name = team["name"]
            self.teams_dict[team_name] = {}
            team_dict = self.teams_dict[team_name]
            team_dict["team_primary_owner"] = team["primaryOwner"]
            team_dict["team_location"] = team["location"]
            team_dict["team_nickname"] = team["nickname"]
            team_dict["team_name"] = team["name"]
            team_dict["profile"] = team["logo"]
            for member in team_json["members"]:
                if member["id"] == team["primaryOwner"]:
                    team_dict["owner_first_name"] = member["firstName"]
                    team_dict["owner_last_name"] = member["lastName"]
                    team_dict["team_cookie"] = member["id"]
                    break

    def get_league_data(self, week):
        self.league_json = self.load_league(week)
        self.load_player_data(week)
        self.load_team_names(week)

    def get_matchup_data(self, week):
        return self.make_request(week, "mMatchup")

    def _get_receiving_yards(self):
        team_reception = {}
        for team in self.player_dict:
            team_reception[team] = 0
            for player in self.player_dict[team]:
                team_reception[team] += player["stats"]["Receiving Yards"]
        return team_reception

    def get_most_receiving_yards(self, detailed=False):
        team_reception = self._get_receiving_yards()
        if not detailed:
            return item(team_reception, "max")
        else:
            return sorted_zip(team_reception, "max")

    def get_least_receiving_yards(self, detailed=False):
        team_reception = self._get_receiving_yards()
        if not detailed:
            return item(team_reception, "min")
        else:
            return sorted_zip(team_reception, "min")

    def _get_rushing_yards(self):
        team_rushing = {}
        for team in self.player_dict:
            team_rushing[team] = 0
            for player in self.player_dict[team]:
                team_rushing[team] += player["stats"]["Rushing Yards"]
        return team_rushing

    def get_most_rushing_yards(self, detailed=False):
        team_rushing = self._get_rushing_yards()
        if not detailed:
            return item(team_rushing, "max")
        else:
            return sorted_zip(team_rushing, "max")

    def get_most_rushing_yards(self, detailed=False):
        team_rushing = self._get_rushing_yards()
        if not detailed:
            return item(team_rushing, "min")
        else:
            return sorted_zip(team_rushing, "min")

    def _get_throwing_yards(self):
        team_throwing = {}
        for team in self.player_dict:
            team_throwing[team] = 0
            for player in self.player_dict[team]:
                team_throwing[team] += player["stats"]["Pass Yards"]
        return team_throwing

    def get_most_throwing_yards(self, detailed=False):
        team_throwing = self._get_throwing_yards()
        if not detailed:
            return item(team_throwing, "max")
        else:
            return sorted_zip(team_throwing, "max")

    def get_least_throwing_yards(self, detailed=False):
        team_throwing = self._get_throwing_yards()
        if not detailed:
            return item(team_throwing, "min")
        else:
            return sorted_zip(team_throwing, "min")

    def _get_PAT(self, state):
        team_PAT = {}
        for team in self.player_dict:
            team_PAT[team] = ("name", 0)
            for player in self.player_dict[team]:
                if player["Slot"] == "K":
                    if state == "made":
                        team_PAT[team] = (
                            player["player_name"],
                            player["stats"]["Extra Points Made"],
                        )
                    else:
                        PAT_made = player["stats"]["Extra Points Made"]
                        PAT_attempted = player["stats"]["Extra Points Attempted"]
                        made_attempt = PAT_made - PAT_attempted
                        if team_PAT[team][1] > made_attempt:
                            team_PAT[team] = (player["player_name"], made_attempt)
        return team_PAT

    def get_most_made_PAT(self, detailed=False):
        team_PAT = self._get_PAT("made")
        if not detailed:
            return max_item(team_PAT)
        else:
            return sorted_zip(team_PAT, "max")

    def get_most_missed_PAT(self, detailed=False):
        team_PAT = self._get_PAT("missed")
        if not detailed:
            return min_item(team_PAT)
        else:
            return sorted_zip(team_PAT, "min")

    def _get_rb_rushing(self, state):
        team_rb = {}
        for team in self.player_dict:
            val = 0 if state == "max" else 1000
            team_rb[team] = ("name", val)
            for player in self.player_dict[team]:
                if player["Position"] == "RB" and player["Slot"] != "Bench":
                    rushing_yards = player["stats"]["Rushing Yards"]
                    if state == "max":
                        if team_rb[team][1] <= rushing_yards:
                            team_rb[team] = (player["player_name"], rushing_yards)
                    else:
                        if team_rb[team][1] > rushing_yards:
                            team_rb[team] = (player["player_name"], rushing_yards)
        return team_rb

    def get_strongest_rb(self, detailed=False):
        team_rb = self._get_rb_rushing("max")
        if not detailed:
            return max_item(team_rb)
        else:
            return sorted_zip(team_rb, "max")

    def get_weakest_rb(self, detailed=False):
        team_rb = self._get_rb_rushing("min")
        if not detailed:
            return min_item(team_rb)
        else:
            return sorted_zip(team_rb, "min")

    def get_blindest_qb(self, detailed=False):
        if not hasattr(self, "team_interceptions"):
            self.team_interceptions = {}
            for team in self.player_dict:
                self.team_interceptions[team] = ("name", 0, 0)
                for player in self.player_dict[team]:
                    if player["Slot"] == "QB" and player["Position"] != "BENCH":
                        interceptions = player["stats"]["Interceptions"]
                        pct_completions = (
                            player["stats"]["Completions"]
                            / player["stats"]["Pass Attempts"]
                        )
                        if (
                            self.team_interceptions[team][1] <= interceptions
                            and self.team_interceptions[team][2] <= pct_completions
                        ):
                            self.team_interceptions[team] = (
                                player["player_name"],
                                interceptions,
                                pct_completions,
                            )

            self.sorted_team_interceptions = sorted(
                self.team_interceptions.items(), key=self.blind_qb_sort
            )

        if not detailed:
            return self.sorted_team_interceptions[0]
        else:
            return self.sorted_team_interceptions

    def blind_qb_sort(self, item):
        return (-item[1][1], item[1][2])

    def _get_qb_rush(self):
        if not hasattr(self, "team_qb_rush"):
            self.team_qb_rush = {}
            for team in self.player_dict:
                self.team_qb_rush[team] = ("name", 0)
                for player in self.player_dict[team]:
                    if player["Slot"] == "QB":
                        self.team_qb_rush[team] = (
                            player["player_name"],
                            player["stats"]["Rushing Yards"],
                        )
            self.sorted_team_qb_rush = sorted(
                self.team_qb_rush.items(), key=self.qb_rush
            )
        return self.sorted_team_qb_rush

    def qb_rush(self, item):
        return item[1][1]

    def get_fastest_qb(self, detailed=False):
        team_qb = self._get_qb_rush()
        if not detailed:
            return team_qb[-1]
        else:
            return team_qb

    def get_slowest_qb(self, detailed=False):
        team_qb = self._get_qb_rush()
        if not detailed:
            return team_qb[0]
        else:
            return team_qb

    def _get_kicker_score(self):
        team_k = {}
        for team in self.player_dict:
            team_k[team] = ("name", 0)
            for player in self.player_dict[team]:
                if player["Slot"] == "K":
                    attempts = player["stats"]["Field Goals Attempted"]
                    team_k[team] = (player["player_name"], attempts)
        return team_k

    def get_fire_kicker(self, detailed=False):
        team_k = self._get_kicker_score()
        if not detailed:
            return max_item(team_k)
        else:
            return sorted_zip(team_k, "max")

    def get_frozen_kicker(self, detailed=False):
        team_k = self._get_kicker_score()
        if not detailed:
            return min_item(team_k)
        else:
            return sorted_zip(team_k, "min")

    def _get_team_touchdowns(self):
        team_touchdowns = {}
        for team in self.player_dict:
            team_touchdowns[team] = 0
            team_set = set()
            qb_stats = {}
            for player in self.player_dict[team]:
                stats = player["stats"]
                if player["Position"] == "QB" and player["Slot"] != "Bench":
                    qb_stats["proTeamId"] = player["proTeamId"]
                    qb_stats["Pass Touchdowns"] = stats["Pass Touchdowns"]
                    qb_stats["Rushing Touchdowns"] = stats["Rushing Touchdowns"]
                    qb_stats["Receiving Touchdowns"] = stats["Receiving Touchdowns"]

                elif player["Slot"] != "Bench":
                    team_set.add(player["proTeamId"])
                    team_touchdowns[team] += stats["Pass Touchdowns"]
                    team_touchdowns[team] += stats["Rushing Touchdowns"]
                    team_touchdowns[team] += stats["Receiving Touchdowns"]

            if qb_stats["proTeamId"] not in team_set:
                team_touchdowns[team] += qb_stats["Pass Touchdowns"]
            team_touchdowns[team] += qb_stats["Rushing Touchdowns"]
            team_touchdowns[team] += qb_stats["Receiving Touchdowns"]

        return team_touchdowns

    def get_most_touchdowns(self, detailed=False):
        team_touchdowns = self._get_team_touchdowns()
        return (
            max(team_touchdowns, key=team_touchdowns.get),
            max(team_touchdowns.values()),
        )

    def get_least_touchdowns(self, detailed=False):
        team_touchdowns = self._get_team_touchdowns()
        return (
            min(team_touchdowns, key=team_touchdowns.get),
            min(team_touchdowns.values()),
        )

    def _get_flex(self, state):
        team_flexes = {}
        for team in self.player_dict:
            val = 0 if state == "max" else 1000
            team_flexes[team] = ("name", val)
            for player in self.player_dict[team]:
                if player["Slot"] == "FLEX":
                    player_name = player["player_name"]
                    if state == "max":
                        if team_flexes[team][1] <= player["stats"]["Actual Total"]:
                            team_flexes[team] = (
                                player_name,
                                player["stats"]["Actual Total"],
                            )
                    elif state == "min":
                        if team_flexes[team][1] > player["stats"]["Actual Total"]:
                            team_flexes[team] = (
                                player_name,
                                player["stats"]["Actual Total"],
                            )
        return team_flexes

    def get_best_flex(self, detailed=False):
        flexes = self._get_flex("max")
        if not detailed:
            return max_item(flexes)
        else:
            return sorted_zip(flexes, "max")

    def get_worst_flex(self, detailed=False):
        flexes = self._get_flex("min")
        if not detailed:
            return min_item(flexes)
        else:
            return sorted_zip(flexes, "min")

    def _get_receptions(self, position, state):
        team_receptions = {}
        for team in self.player_dict:
            targets = 0 if state == "max" else 1000
            team_receptions[team] = ("name", targets, 1)
            for player in self.player_dict[team]:
                if player["Position"] == position and player["Slot"] != "Bench":
                    if state == "max":
                        if targets < player["stats"]["Targets"]:
                            player_name = player["player_name"]
                            targets = player["stats"]["Targets"]
                            receptions = player["stats"]["Receptions"]
                            rec_tar = (
                                team_receptions[team][1] / team_receptions[team][2]
                            )
                            if rec_tar <= receptions / targets:
                                team_receptions[team] = (
                                    player_name,
                                    receptions,
                                    targets,
                                )

                    elif state == "min":
                        if targets > player["stats"]["Targets"]:
                            player_name = player["player_name"]
                            targets = player["stats"]["Targets"]
                            receptions = player["stats"]["Receptions"]
                            if team_receptions[team][1] > receptions / targets:
                                team_receptions[team] = (
                                    player_name,
                                    receptions,
                                    targets,
                                )
        return team_receptions

    def get_stickiest_rb(self, detailed=False):
        rb_receptions = self._get_receptions("RB", "max")
        if not detailed:
            return max_item(rb_receptions)
        else:
            return sorted_zip(rb_receptions, "max")

    def get_butter_rb(self, detailed=False):
        rb_receptions = self._get_receptions("RB", "min")
        if not detailed:
            return min_item(rb_receptions)
        else:
            return sorted_zip(rb_receptions, "min")

    def get_stickiest_wr(self, detailed=False):
        wr_receptions = self._get_receptions("WR", "max")
        if not detailed:
            return max_item(wr_receptions)
        else:
            return sorted_zip(wr_receptions, "max")

    def get_butter_wr(self, detailed=False):
        wr_receptions = self._get_receptions("WR", "min")
        if not detailed:
            return min_item(wr_receptions)
        else:
            return sorted_zip(wr_receptions, "min")

    def _get_defense(self):
        team_defense = {}
        for team in self.player_dict:
            team_defense[team] = 0
            for player in self.player_dict[team]:
                if player["Slot"] == "D/ST":
                    team_defense[team] = player["stats"]["Actual Total"]
        return team_defense

    def get_strongest_defense(self, detailed=False):
        team_defense = self._get_defense()
        if not detailed:
            return item(team_defense, "max")
        else:
            return sorted_zip(team_defense, "max")

    def get_weakest_defense(self, detailed=False):
        team_defense = self._get_defense()
        if not detailed:
            return item(team_defense, "min")
        else:
            return sorted_zip(team_defense, "min")

    def get_most_injuries(self, detailed=False):
        team_injury_count = {}
        for team in self.player_dict:
            team_injury_count[team] = 0
            for player in self.player_dict[team]:
                if player["injuryStatus"] != "ACTIVE":
                    team_injury_count[team] += 1
        return item(team_injury_count, "max")


def item(vals: dict, state):
    if state == "max":
        return (max(vals, key=vals.get), max(vals.values()))
    elif state == "min":
        return (min(vals, key=vals.get), min(vals.values()))


def sorted_zip(vals: dict, reverse: str):
    r = reverse == "max"
    return zip(sorted(vals, key=vals.get, reverse=r), sorted(vals.values(), reverse=r))


def max_item(vals: dict):
    t = -1
    to = {}
    for item in vals.items():
        if t < item[1][1]:
            t = item[1][1]
            to = item
    return to


def min_item(vals: dict):
    t = 1000
    to = ()
    for item in vals.items():
        if t > item[1][1]:
            t = item[1][1]
            to = item
    return to
