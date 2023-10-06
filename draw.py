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
    font = pygame.font.SysFont("simhei", 18)
    text_count = -1
    white = pygame.Color(255, 255, 255)
    # 双人/单人得分
    if common.two_player:
        text_count += 1
        score_text = font.render("蓝色得分:" + str(common.player_one_score), True, white)
        text_rect_score = score_text.get_rect()
        text_rect_score.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(score_text, text_rect_score)

        text_count += 1
        score_text = font.render("红色得分:" + str(common.player_two_score), True, white)
        text_rect_score = score_text.get_rect()
        text_rect_score.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(score_text, text_rect_score)
    else:
        text_count += 1
        score_text = font.render("总得分:" + str(common.current_score), True, white)
        text_rect_score = score_text.get_rect()
        text_rect_score.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(score_text, text_rect_score)
    # 历史最高得分
    if not common.two_player:
        text_count += 1
        history_score_text = font.render("历史最高:" + str(history_max.score), True, white)
        text_rect_history_score = history_score_text.get_rect()
        text_rect_history_score.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(history_score_text, text_rect_history_score)
    # 速度
    text_count += 1
    speed_text = font.render("速度:%.2f格/秒" % (1000 / common.speed), True, white)
    text_rect_speed = speed_text.get_rect()
    text_rect_speed.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
    common.screen.blit(speed_text, text_rect_speed)
    # 游戏时长
    if not common.two_player:
        text_count += 1
        time_text = font.render("用时:%ds" % (pygame.time.get_ticks() // 1000), True, white)
        text_rect_time = time_text.get_rect()
        text_rect_time.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(time_text, text_rect_time)
    # 干扰等级
    if not common.two_player:
        text_count += 1
        interfere_text = font.render("干扰等级:%d (按O切换)" % common.difficulty, True, white)
        text_rect_interfere = interfere_text.get_rect()
        text_rect_interfere.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
        common.screen.blit(interfere_text, text_rect_interfere)
    # 下落预测
    text_count += 1
    predict_text = font.render("按P开启或关闭下落预测", True, white)
    text_rect_predict = predict_text.get_rect()
    text_rect_predict.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
    common.screen.blit(predict_text, text_rect_predict)
    # 单/双人模式
    text_count += 1
    if common.two_player:
        player_t = "双人模式(按i切换单人)"
    else:
        player_t = "单人模式(按i切换双人)"
    player_text = font.render(player_t, True, white)
    text_rect_player = player_text.get_rect()
    text_rect_player.topleft = (field_width * brick_width + 10, 5 + text_count * 25)
    common.screen.blit(player_text, text_rect_player)


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
