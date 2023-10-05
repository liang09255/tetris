import pygame

import block
import common
from block import Block
from pygame.locals import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT


def listen(cur_block: Block):
    # 按键操作
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                cur_block.rotate()
            elif event.key == K_a or event.key == K_LEFT:
                cur_block.left()
            elif event.key == K_d or event.key == K_RIGHT:
                cur_block.right()
            elif event.key == K_s or event.key == K_DOWN:
                cur_block.down()
                block.reset_last_move()
            elif event.key == pygame.K_p:
                common.open_predict = not common.open_predict


def quit_game():
    while True:
        for event in pygame.event.get():
            pygame.time.wait(100)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()
