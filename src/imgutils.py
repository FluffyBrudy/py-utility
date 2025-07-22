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
    cropped_image = image.getchannel("A").crop(image.getbbox())
    return cropped_image
