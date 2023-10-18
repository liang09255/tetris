import logging
import pygame
import common
import score
from common import field_width, field_height, brick_width, brick_height

history_max = score.get_max_score()


def update_screen():
    common.screen.fill((44, 62, 80))
    draw_frame()
    draw_field()
    draw_info_panel()


def draw_field():
    for line in common.bricks:
        for brick in line:
            if brick is not None:
                brick.draw()


def draw_info_panel():
    text_count = -1
    # 双人/单人得分
    if common.two_player:
        text_count += 1
        _draw_text("蓝色得分:" + str(common.player_one_score), 5 + text_count * 25)

        text_count += 1
        _draw_text("红色得分:" + str(common.player_two_score), 5 + text_count * 25)
    else:
        text_count += 1
        _draw_text("总得分:" + str(common.current_score), 5 + text_count * 25)
    # 历史最高得分
    if not common.two_player:
        text_count += 1
        _draw_text("历史最高:" + str(history_max.score), 5 + text_count * 25)
    # 速度
    text_count += 1
    _draw_text("速度:%.2f格/秒" % (1000 / common.speed), 5 + text_count * 25)
    # 游戏时长
    if not common.two_player:
        text_count += 1
        _draw_text("用时:%ds" % (pygame.time.get_ticks() // 1000), 5 + text_count * 25)
    # 干扰等级
    if not common.two_player:
        text_count += 1
        _draw_text("干扰等级:%d (按O切换)" % common.difficulty, 5 + text_count * 25)
    # 下落预测
    text_count += 1
    _draw_text("按p开启或关闭下落预测", 5 + text_count * 25)
    # 单/双人模式
    text_count += 1
    if common.two_player:
        player_t = "双人模式(按i切换单人)"
    else:
        player_t = "单人模式(按i切换双人)"
    _draw_text(player_t, 5 + text_count * 25)
    # 操作提示
    if common.two_player:
        text_count += 1
        _draw_text("红方：WASD", 5 + text_count * 25)
        text_count += 1
        _draw_text("蓝方：↑←↓→", 5 + text_count * 25)


def _draw_text(t: str, height: int):
    font = pygame.font.SysFont("simhei", 18)
    white = pygame.Color(255, 255, 255)
    text = font.render(t, True, white)
    text_rect = text.get_rect()
    text_rect.topleft = (field_width * brick_width + 10, height)
    common.screen.blit(text, text_rect)


# 绘制分界线
def draw_frame():
    frame_color = pygame.Color(200, 200, 200)
    pygame.draw.line(common.screen, frame_color, (field_width * brick_width, field_height * brick_height),
                     (field_width * brick_width, 0), 2)


def draw_game_over():
    game_over_img = pygame.image.load("resources/images/game_over.png")  # 游戏结束图标
    common.screen.blit(game_over_img, (field_width / 2 * brick_width, (field_height / 2 - 2) * brick_height))
    logging.info("游戏结束，总得分：%d" % common.current_score)
    # 记录到文件
    score.Score(score=common.current_score, t=pygame.time.get_ticks() // 1000).record()
