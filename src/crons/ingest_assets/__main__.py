from __future__ import annotations

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from src.shared.bot_api.api import get_bot_api
from src.shared.config import PROJECT_ROOT

ASSET_FOLDER = PROJECT_ROOT / "src" / "assets"


def main() -> None:
    bot_api = get_bot_api()

    for participant in bot_api.get_participants():
        image_name = f"spiderman-{participant.first_name}.jpg"
        image_path = ASSET_FOLDER / "rendered_assets" / image_name
        if image_path.exists():
            return
        else:
            spiderman_image = Image.open(str(ASSET_FOLDER / "spiderman.jpg"))
            draw = ImageDraw.Draw(spiderman_image)
            font = ImageFont.truetype(str(ASSET_FOLDER / "OpenSans-Bold.ttf"), 64)
            draw.text((100, 175), participant.first_name, (0, 0, 0), font=font)
            draw.text((520, 225), participant.first_name, (0, 0, 0), font=font)
            spiderman_image.save(str(image_path))


if __name__ == "__main__":
    main()
