import pygame
import score

field_width, field_height = 10, 15  # 游戏画面长宽
brick_width, brick_height = 30, 30  # 方块长宽
cur_block_init_position = (4, 0)  # 当前初始化位置
info_panel_width = 7  # 信息面板宽度
current_score = 0  # 总得分
open_predict = True  # 是否开启预测
bricks = [[None for _ in range(field_width)] for _ in range(field_height)]  # 整个游戏画面砖块矩阵
speed = 1000  # 移动间隔时间
min_speed = 200  # 最小移动间隔时间
max_speed = 1000  # 最大移动间隔时间
screen = pygame.display.set_mode(
    ((field_width + info_panel_width) * brick_width, field_height * brick_height),
    0,
    32
)


# 检查位置是否合法
def is_legal(layout, position) -> bool:
    (x0, y0) = position
    for (x, y) in layout:
        if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height:
            return False
        if bricks[y + y0][x + x0] is not None:
            return False
    return True


def update_score(delete_line: int):
    global current_score
    if delete_line == 4:
        current_score += 6
    elif delete_line == 3:
        current_score += 4
    else:
        current_score += delete_line


def update_speed():
    global current_score, speed, min_speed, max_speed
    speed = min_speed + (max_speed - min_speed) // (1 + current_score)
