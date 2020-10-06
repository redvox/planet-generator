import argparse
import math
import random

import noise
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=1500, type=int)
    parser.add_argument("--height", default=1500, type=int)
    parser.add_argument("-s", "--scale", default=200.0, type=float)
    parser.add_argument("-o", "--octaves", default=6, type=int)
    parser.add_argument("-p", "--persistence", default=.5, type=float)
    parser.add_argument("-l", "--lacunarity", default=2.0, type=float)
    parser.add_argument("-b", "--base", default=0, type=int)
    parser.add_argument("-md", "--max_distance", default=900.0, type=float)
    parser.add_argument("-a", "--alter", default=0, type=int)
    args = parser.parse_args()

    random.seed()
    offset = random.randint(1, 100) * random.randint(1, 1000)

    width, height = args.width, args.height
    octaves = args.octaves
    persistence = args.persistence
    lacunarity = args.lacunarity
    scale = args.scale
    base = args.base
    alter = args.alter
    max_distance = args.max_distance

    pil_image = Image.new('RGBA', (width, height))

    pixels = pil_image.load()

    cl = []
    r = lambda: random.randint(30, 235)
    for i in range(10):
        cl.append((r(), r(), r()))

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):

            # Generates a value from -1 to 1
            pixel_value = noise.pnoise2((offset + i) / scale,
                                        (offset + j) / scale,
                                        octaves,
                                        persistence,
                                        lacunarity,
                                        width,
                                        height,
                                        base)

            distance_from_center = math.sqrt(math.pow((i - width / 2), 2) + math.pow((j - height / 2), 2))
            gradient_perc = distance_from_center / max_distance
            pixel_value -= math.pow(gradient_perc, 3)

            if int(pixel_value * 100.0) > 40:
                pixels[i, j] = cl[5]
            elif int(pixel_value * 100.0) > 30:
                pixels[i, j] = cl[4]
            elif int(pixel_value * 100.0) > 20:
                pixels[i, j] = cl[3]
            elif int(pixel_value * 100.0) > 10:
                pixels[i, j] = cl[2]
            elif int(pixel_value * 100.0) > 0:
                pixels[i, j] = cl[1]
            elif int(pixel_value * 100.0) > -10:
                pixels[i, j] = cl[4]
            elif int(pixel_value * 100.0) > -20:
                pixels[i, j] = cl[3]
            elif int(pixel_value * 100.0) > -30:
                pixels[i, j] = cl[2]
            elif int(pixel_value * 100.0) > -40:
                pixels[i, j] = cl[1]
            else:
                pixels[i, j] = (20, 30, 35)
    pil_image.save('dist/color.png')


if __name__ == "__main__":
    main()
