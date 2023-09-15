import logging
import pygame
import time
import common
from block import get_block
from pygame.locals import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT
from common import field_width, field_height, brick_width, brick_height, is_legal


def draw_field():
    for line in common.bricks:
        for brick in line:
            if brick is not None:
                brick.draw(screen=common.screen)


def draw_info_panel():
    font = pygame.font.Font("resources/fonts/MONACO.TTF", 18)
    score_text = font.render("score:" + str(common.score), True, (255, 255, 255))
    history_score_text = font.render("history:" + str(0), True, (255, 255, 255))
    text_rect_score = score_text.get_rect()
    text_rect_score.topleft = (field_width * brick_width + 10, 5)
    common.screen.blit(score_text, text_rect_score)
    text_rect_history_score = history_score_text.get_rect()
    text_rect_history_score.topleft = (field_width * brick_width + 10, 30)
    common.screen.blit(history_score_text, text_rect_history_score)
    next_block.draw()


# 绘制分界线
def draw_frame():
    frame_color = pygame.Color(200, 200, 200)
    pygame.draw.line(common.screen, frame_color, (field_width * brick_width, field_height * brick_height),
                     (field_width * brick_width, 0), 2)


logging.basicConfig(
    level=logging.DEBUG,
    format="{\"dateTime\":\"%(asctime)s\", \"level\":\"%(levelname)s\", \"message\":\"%(message)s\"}"
)
logging.info("开始运行俄罗斯方块")
pygame.init()
pygame.display.set_caption('俄罗斯方块')
pygame.display.set_icon(pygame.image.load("resources/images/icon.png"))
game_over_img = pygame.image.load("resources/images/game_over.png")  # 游戏结束图标
logging.info("初始化完成")
next_block = get_block()
next_block_init_position = (field_width + 2, 5)  # 下一个形状初始化位置

# 开始运行游戏
while True:
    # 显示一个方块
    cur_block = next_block
    cur_block.set_position(common.cur_block_init_position)
    logging.info("新方块开始下落")
    next_block = get_block()
    next_block.set_position(next_block_init_position)

    if not is_legal(cur_block.cur_layout, cur_block.position):
        cur_block.draw()
        break
    # 判定
    while not cur_block.stopped:
        common.screen.fill((44, 62, 80))
        draw_frame()
        draw_field()
        draw_info_panel()
        cur_block.update()
        pygame.display.update()

        # 防死循环
        time.sleep(0.05)

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
                    last_move = -1

# 游戏结束
common.screen.blit(game_over_img, (field_width / 2 * brick_width, (field_height / 2 - 2) * brick_height))
logging.info("游戏结束，总得分：%d" % common.score)
while True:
    for event in pygame.event.get():
        time.sleep(0.1)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.update()
