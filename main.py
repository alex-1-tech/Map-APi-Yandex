import os
import sys

import pygame
import requests
import time


def get_map(coord, delta="0.5"):
    search_api_server = "https://static-maps.yandex.ru/1.x/"
    api_key = "..."
    search_params = {
        "apikey": api_key,
        "ll": coord,
        "spn": ",".join([delta, delta]),
        'l': 'map'
    }
    response = requests.get(search_api_server, params=search_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

def draw_map(map_file):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    os.remove(map_file)


def main():
    coord = input("Введите координаты через запятую: ")
    # coord = "29.914783,59.891574"
    draw_map(get_map(coord))


if __name__ == '__main__':
    main()
