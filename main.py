import io
import sys
import pygame
import pygame_gui
from io import BytesIO
from PIL import Image

from yandex_map_library import *
from distance import lonlat_distance


class GUI:
    def __init__(self, size, theme):
        self.manager = pygame_gui.UIManager(size)
        self.theme_toggle = pygame_gui.elements.UIDropDownMenu(
            MapApp.THEMES,
            MapApp.THEMES[theme],
            pygame.rect.Rect(10, 10, 100, 30),
            self.manager,
        )

    def update(self, td):
        self.manager.update(td)

    def draw_ui(self, surf):
        self.manager.draw_ui(surf)

    def process_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_elemrnt == self.theme_toggle:
                print('Тема')


class MapApp:
    DELTA_LON = 200
    DELTA_LAT = 90
    THEMES = ['light', 'dark']

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.z = 1
        self.coord = [0, 0]
        self.theme = 0
        self.update_map()
        self.clock = pygame.time.Clock()
        self.gui = GUI(size, self.theme)

    def update_map(self):
        bytes_img = get_static_map(ll=','.join(map(str, self.coord)), z=self.z, theme=MapApp.THEMES[self.theme])
        img = pygame.image.load(BytesIO(bytes_img))
        self.screen.blit(img, (0, 0))

    def process_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                self.z = min(21, self.z + 1)
            if event.key == pygame.K_PAGEDOWN:
                self.z = max(1, self.z - 1)
            if event.key == pygame.K_LEFT:
                self.coord[0] = (self.coord[0] - MapApp.DELTA_LON * 2 ** -self.z + 180) % 360 - 180
            if event.key == pygame.K_RIGHT:
                self.coord[0] = (self.coord[0] + MapApp.DELTA_LON * 2 ** -self.z + 180) % 360 - 180
            if event.key == pygame.K_UP:
                self.coord[1] = min((self.coord[1] + MapApp.DELTA_LAT * 2 ** -self.z), 85)
            if event.key == pygame.K_DOWN:
                self.coord[1] = max((self.coord[1] - MapApp.DELTA_LAT * 2 ** -self.z), -85)
            if event.key == pygame.K_t:
                self.theme = 1 - self.theme
            self.update_map()

    def run(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                self.gui.process_event(event)
                self.process_keys(event)

            self.gui.update(time_delta)
            self.gui.draw_ui(self.screen)

            pygame.display.flip()


if __name__ == '__main__':
    app = MapApp((600, 450))
    app.run()
