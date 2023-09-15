import random
import pygame

field_width, field_height = 10, 15  # 游戏画面长宽
brick_width, brick_height = 30, 30  # 方块长宽
cur_block_init_position = (4, 0)  # 当前初始化位置
info_panel_width = 7  # 信息面板宽度
next_block_init_position = (field_width + 2, 5)  # 下一个形状初始化位置
score = 0  # 总得分
bricks = [[None for _ in range(field_width)] for _ in range(field_height)]  # 整个游戏画面砖块矩阵
last_move = -1  # 上次移动时间
speed = 800  # 移动间隔时间
screen = pygame.display.set_mode(((field_width + info_panel_width) * brick_width, field_height * brick_height), 0, 32)


# 随机正整数
def rand_uint(n: int) -> int:
    return random.randint(0, n)


# 检查位置是否合法
def is_legal(layout, position) -> bool:
    (x0, y0) = position
    for (x, y) in layout:
        if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height:
            return False
        if bricks[y + y0][x + x0] is not None:
            return False
    return True
