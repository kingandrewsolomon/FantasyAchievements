from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from team_colors import *
import requests
import cairosvg

PLAYER_ICON_WIDTH = 285
PLAYER_ICON_HEIGHT = 214

TEAM_LOGO_WIDTH = TEAM_LOGO_HEIGHT = 66


class FFGraphic:
    WIDTH = HEIGHT = 500
    FONT_URL = "/Users/123ad30/Documents/Fonts/25028_memphi31.ttf"
    ACHIEVEMENT_FONT_SIZE = 55
    PLAYER_NAME_FONT_SIZE = 38
    TEAM_NAME_FONT_SIZE = 12
    PLAYER_URL = "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/{player_id}.png&w={player_width}&h={player_height}&cb=1"
    TEAM_DEFENSE_URL = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{team_name}.png&w={team_width}&h={team_height}&cb=1"

    def add_player(self, player_img, player_name, team_color_scheme):
        padding = 15
        # Add the player name
        player_font = ImageFont.truetype(self.FONT_URL, self.PLAYER_NAME_FONT_SIZE)
        txt_width, _ = player_font.getsize(player_name)
        if txt_width > PLAYER_ICON_WIDTH:
            # we place the text in its spot and move the icon
            y = 452
            x = self.WIDTH - txt_width - padding
            self.drawer.text(
                (x + 1.5, y + 2),
                player_name,
                team_color_scheme.secondary,
                font=player_font,
            )
            self.drawer.text(
                (x, y), player_name, team_color_scheme.tertiary, font=player_font
            )
            txt_midpoint = x + txt_width // 2
            img_x = (txt_midpoint - PLAYER_ICON_WIDTH // 2) - padding

            # Add the player image
            img_height = self.HEIGHT - PLAYER_ICON_HEIGHT

            self.img.paste(
                player_img,
                (
                    img_x,
                    img_height - 60,
                ),
                player_img,
            )
            pass
        else:
            # we place the icon in its spot and move the text

            # Add the player image
            img_width = self.WIDTH - PLAYER_ICON_WIDTH - 15
            img_height = self.HEIGHT - PLAYER_ICON_HEIGHT

            self.img.paste(
                player_img,
                (
                    img_width,
                    img_height - 60,
                ),
                player_img,
            )

            img_midpoint = img_width + PLAYER_ICON_WIDTH / 2

            y = 452
            x = img_midpoint - txt_width / 2

            self.drawer.text(
                (x + 1.5, y + 2),
                player_name,
                team_color_scheme.secondary,
                font=player_font,
            )
            self.drawer.text(
                (x, y), player_name, team_color_scheme.tertiary, font=player_font
            )

    def add_team_icon(self, team_img, team_name, team_color_scheme):
        team_font = ImageFont.truetype(self.FONT_URL, self.TEAM_NAME_FONT_SIZE)
        txt_width, _ = team_font.getsize(team_name)

        txt_x, txt_y = (8, 80)

        img_x, img_y = (26, 8)

        # Add the LM name (team name)
        self.drawer.text(
            (txt_x + 1, txt_y + 1),
            team_name,
            team_color_scheme.secondary,
            font=team_font,
        )
        self.drawer.text(
            (txt_x, txt_y), team_name, team_color_scheme.tertiary, font=team_font
        )

        # Add the LM image (team profile pic)
        bigsize = (team_img.size[0] * 5, team_img.size[1] * 5)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(team_img.size, Image.ANTIALIAS)
        team_img.putalpha(mask)

        txt_midpoint = txt_x + txt_width // 2
        img_x = txt_midpoint - team_img.size[0] // 2
        self.img.paste(team_img, (img_x, img_y), team_img)

    def add_achievement(self, achievement_title, result, unit, team_color_scheme):
        # Add the achievement title
        achievement_font = ImageFont.truetype(self.FONT_URL, self.ACHIEVEMENT_FONT_SIZE)
        x, y = 26, 165
        achvmt_width, achvmt_height = achievement_font.getsize(achievement_title)

        if achvmt_width + x > self.WIDTH:
            achievement_title = achievement_title.replace(" ", "\n")
            y = y - achvmt_height

        self.drawer.text(
            (x + 3, y + 3),
            achievement_title,
            team_color_scheme.secondary,
            font=achievement_font,
        )
        self.drawer.text(
            (x, y), achievement_title, team_color_scheme.tertiary, font=achievement_font
        )

        # Add the achievement result
        x, y = 27, 227
        if unit == "%":
            result = round((result[0] / result[1]) * 100)
        else:
            result = result[0]
        achievement_result = f"{result} {unit.upper()}"
        self.drawer.text(
            (x + 3, y + 3),
            achievement_result,
            team_color_scheme.secondary,
            font=achievement_font,
        )
        self.drawer.text(
            (x, y),
            achievement_result,
            team_color_scheme.tertiary,
            font=achievement_font,
        )
        pass

    def __init__(
        self,
        team_data: dict,
        player_data: dict,
        achievement_title: str,
        result,
        unit: str,
    ) -> None:
        if player_data["Position"] != "D/ST":
            player_id = player_data["id"]
            player_url = self.PLAYER_URL.format(
                player_id=player_id,
                player_width=PLAYER_ICON_WIDTH,
                player_height=PLAYER_ICON_HEIGHT,
            )
        else:
            team_name = player_data["team_abbr"]
            player_url = self.TEAM_DEFENSE_URL.format(
                team_name=team_name,
                team_width=PLAYER_ICON_WIDTH,
                team_height=PLAYER_ICON_HEIGHT,
            )
        player_name = player_data["player_name"]

        team_url = team_data["profile"]
        team_name = team_data["team_name"].strip().upper()

        achievement_title = achievement_title.upper()

        r = requests.get(player_url, stream=True)
        player_img = Image.open(r.raw)

        if ".svg" in team_url:
            # For SVGs
            r = requests.get(team_url, stream=True)
            team_img = cairosvg.svg2png(bytestring=r.content)
            team_img = Image.open(BytesIO(team_img))
        else:
            # For regular PNGS
            headers = {
                "User-Agent": "FantasyFootballBot/0.0 (andrewsolomon610@gmail.com)"
            }
            r = requests.get(team_url, stream=True, headers=headers)
            print(team_url)
            team_img = Image.open(r.raw)

        team_img = team_img.resize((TEAM_LOGO_WIDTH, TEAM_LOGO_HEIGHT), Image.ANTIALIAS)

        team_color_scheme: TeamColor = player_data["proTeamColorScheme"]

        self.img = Image.new("RGB", (self.WIDTH, self.HEIGHT))
        self.drawer = ImageDraw.Draw(self.img)

        # Add the background color
        self.img.paste(
            team_color_scheme.primary,
            (0, 0, self.WIDTH, self.HEIGHT),
        )

        self.add_player(player_img, player_name, team_color_scheme)

        self.add_team_icon(team_img, team_name, team_color_scheme)

        self.add_achievement(achievement_title, result, unit, team_color_scheme)

        self.img.save("image.png")
