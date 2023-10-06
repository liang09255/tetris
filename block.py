import copy
import logging
import math
import random
import pygame
import common
import pierre_dellacherie
from brick import Brick
from common import is_legal, field_width, field_height

last_move = -1
block_count = 0


# 多个砖块组成的方块
class Block:
    def __init__(self, p_bricks_layout, p_direction, p_color, block_id: int = 0):
        self.bricks_layout = p_bricks_layout
        self.direction = p_direction
        self.cur_layout = self.bricks_layout[self.direction]
        self.position = common.cur_block_init_position
        self.bricks = []
        self.predict_bricks = []
        self.stopped = False
        self.move_interval = common.speed
        self.block_id = block_id
        for (x, y) in self.cur_layout:
            b = Brick(
                p_position=(self.position[0] + x, self.position[1] + y),
                p_color=p_color,
                block_id=block_id
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
        if common.open_predict:
            self.predict()
            for brick in self.predict_bricks:
                brick.draw()

    # 左移一格
    def left(self) -> bool:
        new_position = (self.position[0] - 1, self.position[1])
        if is_legal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bricks()
            return True
        return False

    # 右移一格
    def right(self) -> bool:
        new_position = (self.position[0] + 1, self.position[1])
        if is_legal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bricks()
            return True
        return False

    def predict(self):
        self.predict_bricks = [copy.copy(b) for b in self.bricks]
        (x, y) = (self.position[0], self.position[1] + 1)
        while is_legal(self.cur_layout, (x, y)):
            y += 1
        y -= 1
        for (brick, (x0, y0)) in zip(self.predict_bricks, self.cur_layout):
            brick.position = (x + x0, y + y0)
            brick.color = pygame.Color(140, 144, 148)
            brick.predict = True

    def down(self):
        (x, y) = (self.position[0], self.position[1] + 1)
        while is_legal(self.cur_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bricks()
            y += 1

    def up(self):
        (x, y) = (self.position[0], self.position[1] - 1)
        while is_legal(self.cur_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bricks()
            y -= 1

    def refresh_bricks(self):
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)

    def stop(self):
        self.stopped = True
        # 将这个形状的所有砖块加进砖块列表
        for brick in self.bricks:
            (col, row) = brick.position
            common.bricks[row][col] = brick
        calculate_game_score()

    # 更新当前方块的位置(自动下落)
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

    # 旋转
    def rotate(self) -> bool:
        new_direction = (self.direction + 1) % len(self.bricks_layout)
        new_layout = self.bricks_layout[new_direction]
        if not is_legal(new_layout, self.position):
            return False
        self.direction = new_direction
        self.cur_layout = new_layout
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)
        self.refresh_bricks()
        return True

    # 干扰块
    def interfere(self):
        while self.left():
            continue
        score_list = []
        min_score = -math.inf
        first = True
        while first or self.right():
            first = False
            rotate_count = 0
            first_rotate = True
            while first_rotate or (self.rotate() and rotate_count < 4):
                first_rotate = False
                rotate_count += 1
                self.down()
                now_score = self._add_and_cal_score()
                score_list.append(now_score)
                self.up()

        min_score = min(score_list, default=min_score)

        while self.left():
            continue
        first = True
        while first or self.right():
            first = False
            rotate_count = 0
            first_rotate = True
            while first_rotate or (self.rotate() and rotate_count < 4):
                first_rotate = False
                rotate_count += 1
                self.down()
                now_score = self._add_and_cal_score()
                if now_score == min_score:
                    return
                self.up()
        # 正常不会走到这里
        logging.warning("干扰块位置生成失败(仅可能在游戏结束出现一次)")
        self.down()

    def _add_and_cal_score(self) -> float:
        virtual_screen = [[0 for _ in range(field_width)] for _ in range(field_height)]
        # 将已有的砖块加入虚拟屏幕
        for line in common.bricks:
            for brick in line:
                if brick is not None:
                    (x, y) = brick.position
                    virtual_screen[y][x] = 1
        for brick in self.bricks:
            (x, y) = brick.position
            virtual_screen[y][x] = 2
        return pierre_dellacherie.cal_score(virtual_screen)


# 获取一个方块
def get_block() -> Block:
    block_type = rand_uint(6)
    global block_count
    block_count += 1
    return Block(
        p_bricks_layout=block_info[block_type][:-1],
        p_direction=rand_uint(len(block_info[block_type]) - 2),
        p_color=block_info[block_type][-1],
        block_id=block_count
    )


def reset_last_move():
    global last_move
    last_move = -1


def calculate_game_score():
    delete_line_num = 0
    for row in range(field_height):
        # 判断该行是否全部被填充
        if None in common.bricks[row]:
            continue
        delete_line_num += 1
        two_player_update_score(common.bricks[row])
        # 被消除行置空
        common.bricks[row] = [None for _ in range(common.field_width)]
        # 被消除行上面的所有行下移
        for r in range(row, 0, -1):
            for b in common.bricks[r]:
                if b is not None:
                    b.position = (b.position[0], b.position[1] + 1)
            common.bricks[r] = common.bricks[r - 1][:]
        common.bricks[0] = [None for _ in range(common.field_width)]
    # 单人模式更新得分
    update_score(delete_line_num)
    common.update_speed()


def update_score(delete_line: int):
    if common.two_player:
        return
    if delete_line == 4:
        common.current_score += 6
    elif delete_line == 3:
        common.current_score += 4
    else:
        common.current_score += delete_line
    if delete_line > 0:
        logging.info("消除%d行，当前得分：%d" % (delete_line, common.current_score))


def two_player_update_score(bricks: list):
    if not common.two_player:
        return
    player_one_bricks_count = 0
    player_two_bricks_count = 0
    for brick in bricks:
        if brick.block_id % 2 == 0:
            player_one_bricks_count += 1
        else:
            player_two_bricks_count += 1
    if player_one_bricks_count > player_two_bricks_count:
        common.player_one_score += 1
    else:
        common.player_two_score += 1


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
