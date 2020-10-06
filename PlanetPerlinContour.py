import math
import random

import noise
from PIL import Image


def main():
    width, height = 1500, 1500
    random.seed()

    planet_image = Image.new('RGBA', (width, height))
    planet_pixel = planet_image.load()

    planetary_terrain = generate_terrain(width, height)
    draw_map(width, height, planet_pixel, planetary_terrain)

    urban_terrain = generate_cities(width, height, planetary_terrain)
    draw_map(width, height, planet_pixel, urban_terrain)

    # cloud_image = Image.new('RGBA', (width, height))
    # cloud_pixel = cloud_image.load()
    # cloud_terrain = generate_cloud(width, height)
    # draw_map(width, height, cloud_pixel, cloud_terrain)
    # planet_image.paste(cloud_image, (0, 0), cloud_image)

    planet_image.save('dist/planet_contour.png')


def generate_terrain(width, height):
    planetary_terrain = [[None for i in range(width)] for j in range(height)]
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    scale = 200.0
    base = 0
    max_distance = 500.0
    offset = random.randint(1, 100) * random.randint(1, 1000)

    terrain = {
        30: 'MT',
        20: 'M',
        4: 'G',
        0: 'B'
    }
    default_terrain = 'W'

    for i in range(width):
        for j in range(height):
            pixel_value = noise.pnoise2((offset + i) / scale,
                                        (offset + j) / scale,
                                        octaves,
                                        persistence,
                                        lacunarity,
                                        width,
                                        height,
                                        base)
            pixel_normalised_value = int(pixel_value * 100.0)
            distance_from_center = math.sqrt(math.pow((i - width / 2), 2) + math.pow((j - height / 2), 2))

            if distance_from_center < max_distance:
                for terrain_probability, terrain_code in terrain.items():
                    if pixel_normalised_value > terrain_probability:
                        planetary_terrain[i][j] = terrain_code
                        break
                    planetary_terrain[i][j] = default_terrain
            elif distance_from_center < (max_distance + .03 * max_distance):
                planetary_terrain[i][j] = 'BLACK'
    return planetary_terrain


def generate_cities(width, height, planetary_terrain):
    urban_terrain = [[None for i in range(width)] for j in range(height)]
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    scale = 150.0
    base = 0
    max_distance = 500.0
    offset = random.randint(1, 100) * random.randint(1, 1000)

    for i in range(width):
        for j in range(height):
            pixel_value = noise.pnoise2((offset + i) / scale,
                                        (offset + j) / scale,
                                        octaves,
                                        persistence,
                                        lacunarity,
                                        width,
                                        height,
                                        base)
            pixel_normalised_value = int(pixel_value * 100.0)
            distance_from_center = math.sqrt(math.pow((i - width / 2), 2) + math.pow((j - height / 2), 2))

            if distance_from_center < max_distance:
                if pixel_normalised_value > 17 and planetary_terrain[i][j] in ['G']:
                    urban_terrain[i][j] = 'C'
    return urban_terrain


def generate_cloud(width, height):
    cloud_terrain = [[None for i in range(width)] for j in range(height)]
    octaves = 6
    persistence = 0.6
    lacunarity = 7.0
    scale = 150.0
    base = 0
    max_distance = 500.0
    offset = random.randint(1, 100) * random.randint(1, 1000)

    for i in range(width):
        for j in range(height):
            pixel_value = noise.pnoise2((offset + i) / scale,
                                        (offset + j) / scale,
                                        octaves,
                                        persistence,
                                        lacunarity,
                                        width,
                                        height,
                                        base)
            pixel_normalised_value = int(pixel_value * 100.0)
            distance_from_center = math.sqrt(math.pow((i - width / 2), 2) + math.pow((j - height / 2), 2))

            if distance_from_center < max_distance:
                if pixel_normalised_value > 5:
                    cloud_terrain[i][j] = 'CLOUD1'
                if pixel_normalised_value > 0:
                    cloud_terrain[i][j] = 'CLOUD2'
    return cloud_terrain


def draw_map(width, height, pixels, data):
    color_codes = {
        'MT': (240, 240, 240),
        'M': (200, 200, 200),
        'G': (134, 164, 114),
        'B': (236, 212, 184),
        'W': (153, 162, 157),
        'C': (15, 15, 15),
        'L': (255, 241, 118),
        'CLOUD1': (224, 224, 224, 200),
        'CLOUD2': (189, 189, 189, 200),
        'BLACK': (15, 15, 15),
    }
    for i in range(width):
        for j in range(height):
            if data[i][j]:
                pixels[i, j] = color_codes[data[i][j]]
    return pixels


if __name__ == "__main__":
    main()
