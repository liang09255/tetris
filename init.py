import logging
import pygame


def init():
    logging.info("开始运行俄罗斯方块")
    logging_init()
    pygame_init()
    logging.info("初始化完成")


def logging_init():
    logging.basicConfig(
        level=logging.DEBUG,
        format="{\"dateTime\":\"%(asctime)s\", \"level\":\"%(levelname)s\", \"message\":\"%(message)s\"}"
    )


def pygame_init():
    pygame.init()
    pygame.display.set_caption('俄罗斯方块')
    pygame.display.set_icon(pygame.image.load("resources/images/icon.png"))

