from io import BytesIO, StringIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from team_colors import *
import urllib.request
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

    def __init__(self, team_data, player_data, achievement_title, result, unit) -> None:
        player_id = player_data["id"]
        player_url = self.PLAYER_URL.format(
            player_id=player_id,
            player_width=PLAYER_ICON_WIDTH,
            player_height=PLAYER_ICON_HEIGHT,
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
            r = requests.get(team_url, stream=True)
            team_img = Image.open(r.raw)

        team_img = team_img.resize((TEAM_LOGO_WIDTH, TEAM_LOGO_HEIGHT), Image.ANTIALIAS)

        team_color_scheme: TeamColor = player_data["proTeamColorScheme"]

        img = Image.new("RGB", (self.WIDTH, self.HEIGHT))
        drawer = ImageDraw.Draw(img)

        img.paste(
            team_color_scheme.primary,
            (0, 0, self.WIDTH, self.HEIGHT),
        )

        img.paste(
            player_img,
            (
                self.WIDTH - PLAYER_ICON_WIDTH - 15,
                self.HEIGHT - PLAYER_ICON_HEIGHT - 60,
            ),
            player_img,
        )

        bigsize = (team_img.size[0] * 5, team_img.size[1] * 5)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(team_img.size, Image.ANTIALIAS)
        team_img.putalpha(mask)

        img.paste(team_img, (26, 8), team_img)

        team_font = ImageFont.truetype(self.FONT_URL, self.TEAM_NAME_FONT_SIZE)
        drawer.text(
            (8 + 1, 80 + 1), team_name, team_color_scheme.secondary, font=team_font
        )
        drawer.text((8, 80), team_name, team_color_scheme.tertiary, font=team_font)

        player_font = ImageFont.truetype(self.FONT_URL, self.PLAYER_NAME_FONT_SIZE)
        x, y = 194, 452
        drawer.text(
            (x + 1.5, y + 2),
            player_name,
            team_color_scheme.secondary,
            font=player_font,
        )
        drawer.text((x, y), player_name, team_color_scheme.tertiary, font=player_font)

        achievement_font = ImageFont.truetype(self.FONT_URL, self.ACHIEVEMENT_FONT_SIZE)
        x, y = 26, 165
        drawer.text(
            (x + 3, y + 3),
            achievement_title,
            team_color_scheme.secondary,
            font=achievement_font,
        )
        drawer.text(
            (x, y), achievement_title, team_color_scheme.tertiary, font=achievement_font
        )

        x, y = 27, 227
        if unit == "%":
            result = (result[0] / result[1]) * 100
        else:
            result = result[0]
        achievement_result = f"{result} {unit.upper()}"
        drawer.text(
            (x + 3, y + 3),
            achievement_result,
            team_color_scheme.secondary,
            font=achievement_font,
        )
        drawer.text(
            (x, y),
            achievement_result,
            team_color_scheme.tertiary,
            font=achievement_font,
        )
        img.save("image.png")
