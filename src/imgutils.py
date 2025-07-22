from PIL import Image
from PIL import UnidentifiedImageError
from pathlib import Path


def trim_transparent_pixel(img: str):
    imfile = Path(img)
    if not imfile.exists():
        raise FileNotFoundError(f"path {img} doesnt exist")
    if imfile.suffix.upper() != ".PNG":
        raise UnidentifiedImageError(
            f"invalid image extension. allowed extension is .PNG only"
        )

    image = Image.open(img).convert("RGBA")
    cropped_image = image.crop(image.getbbox())
    return cropped_image


if __name__ == "__main__":
    path = "/home/rudy/Downloads/firefox/FreeDinoSprite/png/Dead (6).png"
    x = trim_transparent_pixel(path)
    x.show()
