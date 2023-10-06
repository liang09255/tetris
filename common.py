import copy
import logging
import pygame

field_width, field_height = 11, 21  # 游戏画面长宽
brick_width, brick_height = 30, 30  # 方块长宽
cur_block_init_position = (4, 0)  # 当前初始化位置
info_panel_width = 8  # 信息面板宽度
current_score = 0  # 总得分
player_one_score = 0  # 玩家一得分
player_two_score = 0  # 玩家二得分
open_predict = True  # 是否开启预测
difficulty = 0  # 困难模式
two_player = True  # 双人模式
bricks = [[None for _ in range(field_width)] for _ in range(field_height)]  # 整个游戏画面砖块矩阵
speed = 2000  # 移动间隔时间
min_speed = 200  # 最小移动间隔时间
max_speed = 2000  # 最大移动间隔时间
screen = pygame.display.set_mode(
    ((field_width + info_panel_width) * brick_width, field_height * brick_height),
    0,
    32
)


# 检查位置是否合法
def is_legal(layout, position) -> bool:
    (x0, y0) = position
    for (x, y) in layout:
        if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height or y + y0 < 0:
            return False
        if bricks[y + y0][x + x0] is not None:
            return False
    return True


def update_speed():
    global current_score, speed, min_speed, max_speed
    last_speed = copy.copy(speed)
    speed = min_speed + (max_speed - min_speed) // (1 + current_score / 5)
    if last_speed != speed:
        logging.info("当前速度：%.2f格/s" % (1000 / speed))
