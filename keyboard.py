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

        # 单人键位
        if event.type == pygame.KEYDOWN and not common.two_player:
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
            elif event.key == pygame.K_o:
                common.difficulty = (common.difficulty + 1) % 4
            elif event.key == pygame.K_i:
                # 切换为双人模式
                common.two_player = True
                # 双人模式下禁用
                common.difficulty = 0
            return

        # 双人键位
        if event.type == pygame.KEYDOWN and common.two_player:
            if block.block_count % 2 == 0:
                if event.key == K_w:
                    cur_block.rotate()
                elif event.key == K_a:
                    cur_block.left()
                elif event.key == K_d:
                    cur_block.right()
                elif event.key == K_s:
                    cur_block.down()
                    block.reset_last_move()
            else:
                if event.key == K_UP:
                    cur_block.rotate()
                elif event.key == K_LEFT:
                    cur_block.left()
                elif event.key == K_RIGHT:
                    cur_block.right()
                elif event.key == K_DOWN:
                    cur_block.down()
                    block.reset_last_move()
            if event.key == pygame.K_p:
                common.open_predict = not common.open_predict
            elif event.key == pygame.K_i:
                # 切换为单人模式
                common.two_player = False


def quit_game():
    while True:
        for event in pygame.event.get():
            pygame.time.wait(100)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()
