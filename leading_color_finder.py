from PIL import Image
from typing import Tuple, List
from collections import Counter
import argparse
import sty


def get_cli_args()-> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A pixel value counter, used to get leading color of a image')
    parser.add_argument('filename',  nargs=1, type=str,  metavar='Filename',
                        help='A filepath to desired image')
    parser.add_argument('-n', nargs=1, type=int, default=[10],
                        help='A number of outputted colors')

    return parser.parse_args()


def get_rgb_values_counter_from_image(img: Image) -> Counter:
    rgb_values = Counter()
    loaded_img = img.load()
    width, height = img.size
    for row in range(height):
        for pixel in range(width):
            rgb_values[loaded_img[pixel, row]] += 1
    return rgb_values


def get_top_n_colors(counter: Counter, n: int) -> List:
    return counter.most_common(n)


def rgba_to_hex_str(rgba: Tuple[int, int, int, int])->str:
    return "#"+"".join([hex(x)[2:] for x in rgba])


def print_rgba_as_hex_with_color(rgba_values: Tuple[int, int, int, int])->None:
    for rgba in rgba_values:
        print(sty.fg(*rgba[:-1]) + rgba_to_hex_str(rgba) +
              sty.fg.rs)

def main():
    args = get_cli_args()
    filename = args.filename[0]
    n = args.n[0]

    with Image.open(filename).convert('RGBA') as img:
        values = get_rgb_values_counter_from_image(img)
        counted = get_top_n_colors(values, n)
        print_rgba_as_hex_with_color([x[0] for x in counted])


main()
