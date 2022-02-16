try:
    import os
    import sys

    import pygame
    import requests
    import time
except ImportError as err:
    print("Could't load module. %s" % (err))
    sys.exit(2)


def get_map(coord, delta="0.5") -> str:
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


def get_input(keys, size) -> (int, int, int):
    # take input from keyboard
    x, y, xy = 0, 0, 0
    if keys[pygame.K_UP]:
        y = size * 0.01
    elif keys[pygame.K_DOWN]:
        y = -size * 0.01
    elif keys[pygame.K_LEFT]:
        x = size * 0.01
    elif keys[pygame.K_RIGHT]:
        x = -size * 0.01
    elif keys[pygame.K_PAGEUP]:
        xy += 0.1
    elif keys[pygame.K_PAGEDOWN]:
        xy -= 0.1

    return x, y, xy


def change_size(direction, size, coord):
    if direction == 0:
        return
    if size + direction <= 0 or size + direction >= 10:
        # checking for restrictions
        print("Error, Incorrect scale")
    else:
        size += direction
    # create map with new size
    get_map(coord, str(size))


def change_coord(coord, direction, change, size) -> str:
    x, y = map(float, coord.split(','))
    if direction:
        x -= change
    else:
        y += change
    coord = str(x) + ',' + str(y)
    get_map(coord, str(size))
    return coord


def draw_map(coord, map_file, map_size=0.5):
    # create pygame window
    pygame.init()
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.blit(pygame.image.load(map_file), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # take input
        direction_x, direction_y, direction_size \
            = get_input(pygame.key.get_pressed(), map_size)

        # change size
        if direction_size != 0:
            change_size(direction_size, map_size, coord)

        # change coord
        if direction_y != 0:
            coord = change_coord(coord, False, direction_y, map_size)
        if direction_x != 0:
            coord = change_coord(coord, True, direction_x, map_size)

        # change
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
