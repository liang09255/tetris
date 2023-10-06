import pygame

import common
from common import brick_width, brick_height, screen


# 单个砖块
class Brick:
    brick_width: int = brick_width
    brick_height: int = brick_height
    blue = pygame.Color(28, 126, 214)
    red = pygame.Color(240, 62, 62)

    def __init__(self, p_position, p_color, block_id, predict=False):
        self.position = p_position
        self.color = p_color
        self.block_id = block_id
        self.predict = predict

    def draw(self):
        image = pygame.Surface([self.brick_width - 3, self.brick_height - 3])
        self.fill_color(image)
        screen.blit(image, (self.position[0] * self.brick_width, self.position[1] * self.brick_height))

    def fill_color(self, img: pygame.Surface):
        # 双人模式
        if common.two_player and not self.predict:
            if self.block_id % 2 == 0:
                img.fill(self.blue)
            else:
                img.fill(self.red)
        # 单人模式
        else:
            img.fill(self.color)
