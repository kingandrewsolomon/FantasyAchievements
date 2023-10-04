class TeamColor:
    def __init__(self, team_name, primary, secondary, tertiary):
        self.team_name = team_name
        self.primary = primary
        self.secondary = secondary
        self.tertiary = tertiary

    def __str__(self) -> str:
        return self.team_name


ARIZONA_CARDINALS = TeamColor("Arizona Cardinals", "#97233F", "#000000", "#FFB612")
ATLANTA_FALCONS = TeamColor("Atlanta Falcons", "#a71930", "#000000", "#a5acaf")
BALTIMORE_RAVENS = TeamColor("Baltimore Ravens", "#241773", "#000000", "#9E7C0C")
BUFFALO_BILLS = TeamColor("Buffalo Bills", "#00338D", "#C60C30", "#FFFFFF")
CAROLINA_PANTHERS = TeamColor("Carolina Panthers", "#0085CA", "#101820", "#BFC0BF")
CHICAGO_BEARS = TeamColor("Chicago Bears", "#0B162A", "#c83803", "#FFFFFF")
CINCINNATI_BENGALS = TeamColor("Cincinnati Bengals", "#fb4f14", "#000000", "#FFFFFF")
CLEVELAND_BROWNS = TeamColor("Cleveland Browns", "#311D00", "#ff3c00", "#FFFFFF")
DALLAS_COWBOYS = TeamColor("Dallas Cowboys", "#041E42", "#003594", "#FFFFFF")
DENVER_BRONCOS = TeamColor("Denver Broncos", "#FB4F14", "#002244", "#FFFFFF")
DETROIT_LIONS = TeamColor("Detroit Lions", "#0076b6", "#B0B7BC", "#FFFFFF")
GREEN_BAY_PACKERS = TeamColor("Green Bay Packers", "#203731", "#FFB612", "#FFFFFF")
HOUSTON_TEXANS = TeamColor("Houston Texans", "#03202f", "#A71930", "#FFFFFF")
INDIANAPOLIS_COLTS = TeamColor("Indianapolis Colts", "#002C5F", "#A2AAAD", "#FFFFFF")
JACKSONVILLE_JAGUARS = TeamColor(
    "Jacksonville Jaguars", "#101820", "#D7A22A", "#006778"
)
KANSAS_CITY_CHIEFS = TeamColor("Kansas City Chiefs", "#E31837", "#FFB81C", "#FFFFFF")
LOS_ANGELES_CHARGERS = TeamColor(
    "Los Angeles Chargers", "#0080C6", "#FFC20E", "#ffffff"
)
LOS_ANGELES_RAMS = TeamColor("Los Angeles Rams", "#003594", "#ffa300", "#ffffff")
MIAMI_DOLPHINS = TeamColor("Miami Dolphins", "#008E97", "#FC4C02", "#005778")
MINNESOTA_VIKINGS = TeamColor("Minnesota Vikings", "#4F2683", "#FFC62F", "#FFFFFF")
NEW_ENGLAND_PATRIOTS = TeamColor(
    "New England Patriots", "#002244", "#C60C30", "#B0B7BC"
)
NEW_ORLEANS_SAINTS = TeamColor("New Orleans Saints", "#D3BC8D", "#101820", "#FFFFFF")
NEW_YORK_GIANTS = TeamColor("New York Giants", "#0B2265", "#a71930", "#a5acaf")
NEW_YORK_JETS = TeamColor("New York Jets", "#125740", "#000000", "#FFFFFF")
LAS_VEGAS_RAIDERS = TeamColor("Las Vegas Raiders", "#000000", "#A5ACAF", "#FFFFFF")
PHILADELPHIA_EAGLES = TeamColor("Philadelphia Eagles", "#004C54", "#A5ACAF", "#FFFFFF")
PITTSBURGH_STEELERS = TeamColor("Pittsburgh Steelers", "#FFB612", "#101820", "#FFFFFF")
SAN_FRANCISCO_49ERS = TeamColor("San Francisco 49ers", "#AA0000", "#B3995D", "#FFFFFF")
SEATTLE_SEAHAWKS = TeamColor("Seattle Seahawks", "#002244", "#69BE28", "#A5acaf")
TAMPA_BAY_BUCCANEERS = TeamColor(
    "Tampa Bay Buccaneers", "#D50A0A", "#FF7900", "#0A0A08"
)
TENNESSEE_TITANS = TeamColor("Tennessee Titans", "#0C2340", "#4B92DB", "#C8102E")
WASHINGTON_COMMANDERS = TeamColor(
    "Washington Commanders", "#5A1414", "#FFB612", "#FFFFFF"
)

NFL_TEAMS = {
    0: "FREE AGENT",
    1: ATLANTA_FALCONS,
    2: BUFFALO_BILLS,
    3: CHICAGO_BEARS,
    4: CINCINNATI_BENGALS,
    5: CLEVELAND_BROWNS,
    6: DALLAS_COWBOYS,
    7: DENVER_BRONCOS,
    8: DETROIT_LIONS,
    9: GREEN_BAY_PACKERS,
    10: TENNESSEE_TITANS,
    11: INDIANAPOLIS_COLTS,
    12: KANSAS_CITY_CHIEFS,
    13: LAS_VEGAS_RAIDERS,
    14: LOS_ANGELES_RAMS,
    15: MIAMI_DOLPHINS,
    16: MINNESOTA_VIKINGS,
    17: NEW_ENGLAND_PATRIOTS,
    18: NEW_ORLEANS_SAINTS,
    19: NEW_YORK_GIANTS,
    20: NEW_YORK_JETS,
    21: PHILADELPHIA_EAGLES,
    22: ARIZONA_CARDINALS,
    23: PITTSBURGH_STEELERS,
    24: LOS_ANGELES_CHARGERS,
    25: SAN_FRANCISCO_49ERS,
    26: SEATTLE_SEAHAWKS,
    27: TAMPA_BAY_BUCCANEERS,
    28: WASHINGTON_COMMANDERS,
    29: CAROLINA_PANTHERS,
    30: JACKSONVILLE_JAGUARS,
    33: BALTIMORE_RAVENS,
    34: HOUSTON_TEXANS,
}
