try:
    import os
    import sys

    import pygame
    import requests
    import time
except ImportError as err:
    print("Could't load module. %s" % (err))
    sys.exit(2)


def get_map(coord, delta="0.5"):
    # get map screen
    search_api_server = "https://static-maps.yandex.ru/1.x/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "ll": coord,
        "spn": ",".join([delta, delta]),
        'l': 'map'
    }
    response = requests.get(search_api_server, params=search_params)
    map_file = "map.png"
    # recording a screenshot to a file
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def draw_map(coord, map_file, map_size=0.5):
    # create pygame window
    pygame.init()
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    during_size = 0
    while running:
        screen.blit(pygame.image.load(map_file), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # key pressed, change size
                if event.key == pygame.K_PAGEUP:
                    during_size += 0.1
                elif event.key == pygame.K_PAGEDOWN:
                    during_size -= 0.1
        if during_size != 0:
            if map_size + during_size <= 0 or map_size + during_size >= 10:
                # checking for restrictions
                print("Error, Incorrect scale")
            else:
                map_size += during_size
            during_size = 0
            # create map with new size
            get_map(coord, str(map_size))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


def main():
    # coord = input("Введите координаты через запятую: ")
    coord = "29.914783,59.891574"
    draw_map(coord, get_map(coord))


if __name__ == '__main__':
    main()
