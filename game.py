import pygame
from pygame.locals import *
from sys import exit

# 定义窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 计数ticks
ticks = 0

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Plane Fight')

# 载入背景
background = pygame.image.load('./resources/images/background.png')

# 载入资源图片
shoot_img = pygame.image.load('./resources/images/shoot.png')
# 用subsurface剪切读入的图片
hero1_rect = pygame.Rect(0, 99, 102, 126)
hero2_rect = pygame.Rect(165, 360, 102, 126)
hero1 = shoot_img.subsurface(hero1_rect)
hero2 = shoot_img.subsurface(hero2_rect)
hero_pos = [200, 500]

# 定义一个字典
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    # 绘制背景
    screen.blit(background, (0, 0))
    # 绘制飞机
    
    if ticks % 50 < 25:
        screen.blit(hero1, hero_pos)
    else:
        screen.blit(hero2, hero_pos)
    ticks += 1

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # 处理键盘按下和松开事件
    if event.type == pygame.KEYDOWN:
        if event.key in offset:
            offset[event.key] = 3
    elif event.type == pygame.KEYUP:
        if event.key in offset:
            offset[event.key] = 0
    
    #　修改飞机坐标
    hero_pos = [hero_pos[0] + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT], hero_pos[1] + offset[pygame.K_DOWN] - offset[pygame.K_UP]]
    x = hero_pos[0] + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
    y = hero_pos[1] + offset[pygame.K_DOWN] - offset[pygame.K_UP]

    # 判断x坐标是否左边或右边越界
    if x < 0:
        x = 0
    elif x > SCREEN_WIDTH - hero1_rect.width:
        x = SCREEN_WIDTH - hero1_rect.width
    else:
        x = x

    # 判断y坐标是否上边或下边越界
    if y < 0:
        y = 0
    elif y > SCREEN_HEIGHT - hero1_rect.height:
        y = SCREEN_HEIGHT - hero1_rect.height
    else:
        y = y

    hero_pos[0] = x
    hero_pos[1] = y

