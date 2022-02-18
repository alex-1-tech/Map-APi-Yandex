try:
    import os
    import sys
    import pygame
    import requests
    import time

    from math import sqrt, pow
    from button import Button
except ImportError as err:
    print("Could't load module. %s" % (err))
    sys.exit(2)


class Api_map:
    # create Map class
    def __init__(self, coord):
        self.coord = coord
        self.zoom = 12
        self.map_file = "map.png"
        self.type = "map"
        self.map_layer_buttons = []

    def get_map(self):
        # get map screen
        search_api_server = "https://static-maps.yandex.ru/1.x/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        search_params = {
            "apikey": api_key,
            "ll": self.coord,
            "z": self.zoom,
            'l': self.type,
        }
        response = requests.get(search_api_server, params=search_params)

        # recording a screenshot to a file
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def get_input(self, keys) -> (int, int):
        # take input from keyboard
        x, y = 0, 0

        if keys[pygame.K_UP]:
            y = 0.008
        elif keys[pygame.K_DOWN]:
            y = -0.008
        elif keys[pygame.K_LEFT]:
            x = 0.008
        elif keys[pygame.K_RIGHT]:
            x = - 0.008
        elif keys[pygame.K_PAGEUP]:
            if self.zoom < 19:
                self.zoom += 1
        elif keys[pygame.K_PAGEDOWN]:
            if self.zoom > 1:
                self.zoom -= 1

        return x, y

    def change_coord(self, direction, change):
        x, y = map(float, self.coord.split(','))
        if direction:
            x -= change * pow(2, 15 - self.zoom)
        else:
            y += change * pow(2, 15 - self.zoom)
        coord = str(x) + ',' + str(y)
        self.coord = coord

    def pressed(self):
        for t, button in enumerate(self.buttons):
            if button.pressed(pygame.mouse.get_pos()):
                if t == 0:
                    self.type = "map"
                elif t == 1:
                    self.type = "sat"
                elif t == 1:
                    self.type = "skl"

    def create_buttons(self, screen, size) -> [Button, Button, Button]:
        scheme = Button()
        satellite = Button()
        hybrid = Button()
        self.buttons = [scheme, satellite, hybrid]
        self.map_layer_buttons.append(scheme.create_button(screen, (0, 0, 0),
                                                           size[0] - 135, 20, 120, 50, 100, 'Scheme', (255, 255, 255)))
        self.map_layer_buttons.append(satellite.create_button(screen, (0, 0, 0),
                                                              size[0] - 135, 100, 120, 50, 100, 'Satellite',
                                                              (255, 255, 255)))
        self.map_layer_buttons.append(hybrid.create_button(screen, (0, 0, 0),
                                                           size[0] - 135, 180, 120, 50, 100, 'Hybrid', (255, 255, 255)))


def draw_map(y_map):
    # create pygame window
    pygame.init()
    size = width, height = 750, 450
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    y_map.create_buttons(screen, size)

    while running:
        y_map.get_map()
        screen.blit(pygame.image.load(y_map.map_file), (0, 0))
        # draw buttons
        for button in y_map.map_layer_buttons:
            screen.blit(button, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                y_map.pressed()
        # take input
        direction_x, direction_y \
            = y_map.get_input(pygame.key.get_pressed())

        # change coord
        if direction_y != 0:
            y_map.change_coord(False, direction_y)
        if direction_x != 0:
            y_map.change_coord(True, direction_x)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    os.remove(y_map.map_file)


def main():
    # coord = input("Введите координаты через запятую: ")
    coord = "29.914783,59.891574"
    y_map = Api_map(coord)
    draw_map(y_map)


if __name__ == '__main__':
    main()
