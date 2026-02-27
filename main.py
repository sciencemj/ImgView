import argparse
import shutil

from PIL import Image
from PIL.ImageFile import ImageFile
from rich.console import Console
from rich.style import Style


def get_resized_image(image: ImageFile, custom_width=None) -> ImageFile:
    size = shutil.get_terminal_size(fallback=(80, 24))
    width = size.columns if not custom_width else custom_width
    height = size.lines
    org_width, org_height = image.size
    ratio = org_height / org_width
    new_width = width
    new_height = int(new_width * ratio * 0.5)
    if new_height > height - 1:
        new_height = height - 1
        new_width = int(new_height / (ratio * 0.5))
    return image.resize((new_width, new_height))


def printImage(file: str, cutom_width=None):
    try:
        image = Image.open(file)
    except Image.UnidentifiedImageError as e:
        print(f"Error trying to open {file}: {e}")
    except FileNotFoundError as e:
        print(f"Error trying to open {file}: {e}")
    else:
        resized_image = get_resized_image(image, custom_width=cutom_width)
        width, height = resized_image.size
        pixels = list(resized_image.get_flattened_data())
        console = Console()
        for h in range(height):
            for w in range(width):
                if len(pixels[0]) == 4:
                    r, g, b, a = pixels[h * width + w]
                else:
                    r, g, b = pixels[h * width + w]
                    a = 255
                style = Style(color=f"rgb({r}, {g}, {b})")
                if a > 0:
                    console.print("█", style=style, end="")
                else:
                    console.print(" ", end="")
            console.print("")


def main():
    parser = argparse.ArgumentParser(description="View image in treminal!")
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="manually set the width of image output.",
    )
    parser.add_argument("files", type=str, nargs="*")
    args = parser.parse_args()
    if len(args.files) <= 0:
        print("You need at least one file input!")
        return
    files = args.files
    width = args.width
    for file in files:
        printImage(file, width)


if __name__ == "__main__":
    main()
