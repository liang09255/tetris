import pygame
from common import brick_width, brick_height


# 单个砖块
class Brick:
    brick_width: int = brick_width
    brick_height: int = brick_height

    def __init__(self, p_position, p_color):
        self.position = p_position
        self.color = p_color
        self.image = pygame.Surface([self.brick_width - 3, self.brick_height - 3])
        self.image.fill(self.color)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.position[0] * self.brick_width, self.position[1] * self.brick_height))