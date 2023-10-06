import logging
import pygame
import block
import common
import draw
import keyboard
import init
from block import get_block
from common import field_width, is_legal

# 初始化日志及pygame
init.init()
# 获取第一个方块
next_block = get_block()
# 下一个形状初始化位置
next_block_init_position = (field_width + 2, 7)

# 开始运行游戏
while True:
    logging.info("新方块开始下落")
    # 显示一个方块
    cur_block = next_block
    cur_block.set_position(common.cur_block_init_position)
    if (
            (common.difficulty == 1 and block.block_count % 8 == 0) or
            (common.difficulty == 2 and block.block_count % 5 == 0) or
            (common.difficulty == 3 and block.block_count % 3 == 0)
    ):
        cur_block.interfere()

    next_block = get_block()
    next_block.set_position(next_block_init_position)
    # 判断是否合法
    if not is_legal(cur_block.cur_layout, cur_block.position):
        cur_block.draw()
        break

    # 当前方块下落过程
    while not cur_block.stopped:
        # 监听键盘事件
        keyboard.listen(cur_block)
        # 绘制游戏画面
        draw.update_screen()
        next_block.draw()
        cur_block.update()
        pygame.display.flip()
        # 等待下次判定
        pygame.time.wait(10)

# 游戏结束
draw.draw_game_over()
# 等待退出信号
keyboard.quit_game()
