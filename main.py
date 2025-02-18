import io
import sys
import pygame
from io import BytesIO
from PIL import Image
from yandex_map_library import *
from distance import lonlat_distance


class MapApp:
    DELTA_LON = 200
    DELTA_LAT = 90

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.z = 1
        self.coord = [0, 0]
        self.update_map()

    def update_map(self):
        bytes_img = get_static_map(ll=','.join(map(str, self.coord)), z=self.z)
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
            self.update_map()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                self.process_keys(event)

            pygame.display.flip()


if __name__ == '__main__':
    app = MapApp((600, 450))
    app.run()
