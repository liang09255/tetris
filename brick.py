import pygame
from common import brick_width, brick_height, screen


# 单个砖块
class Brick:
    brick_width: int = brick_width
    brick_height: int = brick_height

    def __init__(self, p_position, p_color):
        self.position = p_position
        self.color = p_color

    def draw(self):
        image = pygame.Surface([self.brick_width - 3, self.brick_height - 3])
        image.fill(self.color)
        screen.blit(image, (self.position[0] * self.brick_width, self.position[1] * self.brick_height))
