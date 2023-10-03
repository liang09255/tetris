import copy
import logging
import random
import pygame
import common
from brick import Brick
from common import is_legal, open_predict

last_move = -1


# 多个砖块组成的方块
class Block:
    def __init__(self, p_bricks_layout, p_direction, p_color):
        self.bricks_layout = p_bricks_layout
        self.direction = p_direction
        self.cur_layout = self.bricks_layout[self.direction]
        self.position = common.cur_block_init_position
        self.bricks = []
        self.predict_bricks = []
        self.stopped = False
        self.move_interval = common.speed
        for (x, y) in self.cur_layout:
            b = Brick(
                p_position=(self.position[0] + x, self.position[1] + y),
                p_color=p_color,
            )
            self.bricks.append(b)

    def set_position(self, position):
        self.position = position
        self.refresh_bricks()

    # 绘制到屏幕上
    def draw(self):
        for brick in self.bricks:
            brick.draw()

    def draw_predict(self):
        if open_predict:
            self.predict()
            for brick in self.predict_bricks:
                brick.draw()

    # 左移一格
    def left(self):
        new_position = (self.position[0] - 1, self.position[1])
        if is_legal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bricks()

    # 右移一格
    def right(self):
        new_position = (self.position[0] + 1, self.position[1])
        if is_legal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bricks()

    def predict(self):
        self.predict_bricks = [copy.copy(b) for b in self.bricks]
        (x, y) = (self.position[0], self.position[1] + 1)
        while is_legal(self.cur_layout, (x, y)):
            y += 1
        y -= 1
        for (brick, (x0, y0)) in zip(self.predict_bricks, self.cur_layout):
            brick.position = (x + x0, y + y0)
            brick.color = pygame.Color(140, 144, 148)

    def down(self):
        (x, y) = (self.position[0], self.position[1] + 1)
        while is_legal(self.cur_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bricks()
            y += 1

    def refresh_bricks(self):
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)

    def stop(self):
        self.stopped = True
        row_nums = []  # 记录有方块的行号
        # 将这个形状的所有砖块加进砖块列表，并把相应位置赋值为1
        for brick in self.bricks:
            (col, row) = brick.position
            common.bricks[row][col] = brick
            if row not in row_nums:
                row_nums.append(row)

        row_nums.sort()  # 保证行更新顺序
        delete_line_num = 0
        for row in row_nums:
            # 判断该行是否全部被填充
            if None in common.bricks[row]:
                continue
            delete_line_num += 1
            # 被消除行置空
            common.bricks[row] = [None for _ in range(common.field_width)]
            # 被消除行上面的所有行下移
            for r in range(row, 0, -1):
                for b in common.bricks[r]:
                    if b is not None:
                        b.position = (b.position[0], b.position[1] + 1)
                common.bricks[r] = common.bricks[r - 1][:]
            common.bricks[0] = [None for _ in range(common.field_width)]
        common.update_score(delete_line_num)
        common.update_speed()

    def update(self):
        self.draw_predict()
        self.draw()
        global last_move
        t = pygame.time.get_ticks()
        if last_move == -1 or t - last_move >= self.move_interval:
            new_position = (self.position[0], self.position[1] + 1)
            if is_legal(self.cur_layout, new_position):
                self.position = new_position
                self.refresh_bricks()
                last_move = t
            else:
                self.stop()

    def rotate(self):
        new_direction = (self.direction + 1) % len(self.bricks_layout)
        new_layout = self.bricks_layout[new_direction]
        if not is_legal(new_layout, self.position):
            return
        self.direction = new_direction
        self.cur_layout = new_layout
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)
        self.refresh_bricks()
        self.draw_predict()
        self.draw()


# 获取一个方块
def get_block() -> Block:
    block_type = rand_uint(6)
    return Block(
        p_bricks_layout=block_info[block_type][:-1],
        p_direction=rand_uint(len(block_info[block_type]) - 2),
        p_color=block_info[block_type][-1],
    )


# 随机正整数
def rand_uint(n: int) -> int:
    return random.randint(0, n)


# 砖块构成形状的布局和颜色
block_info = (
    # 0: oooo
    (
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 1), (1, 1), (2, 1), (3, 1)),
        pygame.Color(188, 45, 117)
    ),
    # 1: oo
    #    oo
    (
        ((1, 0), (2, 0), (1, 1), (2, 1)),
        pygame.Color(0, 137, 255)
    ),
    # 2: o
    #   ooo
    (
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 1), (1, 0), (1, 1), (1, 2)),
        ((1, 2), (0, 1), (1, 1), (2, 1)),
        ((2, 1), (1, 0), (1, 1), (1, 2)),
        pygame.Color(155, 89, 182)
    ),
    # 3: o
    #    oo
    #     o
    (
        ((0, 1), (1, 1), (1, 0), (2, 0)),
        ((0, 0), (0, 1), (1, 1), (1, 2)),
        pygame.Color(140, 73, 92)
    ),
    # 4:  o
    #    oo
    #    o
    (
        ((0, 0), (1, 0), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (0, 1), (0, 2)),
        pygame.Color(241, 196, 15)
    ),
    # 5: ooo
    #    o
    (
        ((0, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 2), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (1, 2), (2, 2)),
        ((2, 0), (2, 1), (1, 1), (0, 1)),
        pygame.Color(231, 76, 60)
    ),
    # 6: ooo
    #      o
    (
        ((2, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (1, 1), (1, 0)),
        ((2, 2), (2, 1), (1, 1), (0, 1)),
        pygame.Color(138, 201, 255)
    )
)
