from os import PathLike
from typing import Union

import argparse
from PIL import Image

ASCII_CHARS = "@%#*+=-:. "


def pixels_to_ascii(image: Image, invert: bool) -> str:
    return ''.join(map(
        lambda p: ASCII_CHARS[p * len(ASCII_CHARS) // 256 if invert else (255 - p) * len(ASCII_CHARS) // 256],
        image.get_flattened_data()
    ))


def image_to_ascii(image: Union[PathLike, Image], ratio: float, new_width: int, invert: bool) -> str:

    if isinstance(image, str):
        try:
            image = Image.open(image)
        except Exception as e:
            print(f"Failed to open image: {e}")
            return

    def resize_image(image: Image, ratio: float, new_width: int) -> Image:
        width, height = image.size
        new_ratio = height / width / ratio
        new_height = int(new_width * new_ratio)
        return image.resize((new_width, new_height))

    def grayscale_image(image: Image) -> Image:
        return image.convert("L")

    ascii_str = pixels_to_ascii(grayscale_image(resize_image(image, ratio, new_width)), invert=invert)

    return "\n".join(ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width))


def main(args) -> None:
    print(image_to_ascii(args.image_path, args.ratio, args.width, args.invert))


if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('image_path')
    argparse.add_argument('--width', type=int, default=100, help='Width of ASCII art')
    argparse.add_argument('--ratio', type=float, default=2.0, help='Resize ratio of ASCII art')
    argparse.add_argument('--invert', action='store_true', help='Invert the ASCII art colors')
    main(argparse.parse_args())