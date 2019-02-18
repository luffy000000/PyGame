import pygame
from pygame.locals import *
from sys import exit
from random import randint

# 定义窗口大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕上方，则销毁子弹
        if self.rect.top <= -self.rect.height:
            self.kill()
# 玩家类
class Hero(pygame.sprite.Sprite):
    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.is_hit = False
        self.bullets = pygame.sprite.Group()

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
        
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

    def shoot(self, bullet_surface):
        # 子弹初始位置在我方飞机的上方居中位置
        bullet = Bullet(bullet_surface, self.rect.midtop)
        # 将子弹添加到子弹组
        self.bullets.add(bullet)

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 2
        # 爆炸画面索引
        self.explode_index = 0
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 定义画面帧率
FRAME_TATE = 60

# 定义动画帧数
ANIMATE_CYCLE = 30

ticks = 0
clock = pygame.time.Clock()
offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}

# 玩家坠毁图片索引
hero_down_index = 1

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Plane Fight')

# 载入背景图
background = pygame.image.load('./resources/images/background.png')
# 游戏结束图
gameover = pygame.image.load('./resources/images/gameover.png')
# 载入资源图片
shoot_img = pygame.image.load('./resources/images/shoot.png')
# 剪切读入的图片
# Hero图片
hero_surface = []
hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 234, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)))
hero_pos = [200, 500]

# 子弹图片
bullet_surface = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))

# 敌机图片
enemy_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))
enemy_hit_surface = []
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_hit_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))

# 创建玩家
hero = Hero(hero_surface[0], hero_pos)
# 创建敌机组
enemy_group = pygame.sprite.Group()
# 创建击毁敌机组
enemy_hit_group = pygame.sprite.Group()
# 被击中敌机字典
enemy_hit_dict = {}
score = 0 # 得分
# 击落敌机得分
ENEMY_SCORE = 100
game_font = pygame.font.SysFont('arial', 16, True) # 字体

# 事件循环
while True:

    # 控制游戏最大帧率
    clock.tick(FRAME_TATE)

    # 绘制背景
    screen.blit(background, (0, 0))

    # 改变飞机图片制造动画
    if ticks >= ANIMATE_CYCLE:
        ticks = 0

    if hero.is_hit:
        if ticks % (ANIMATE_CYCLE // 2) == 0:
            hero_down_index += 1
        hero.image = hero_surface[hero_down_index]
        if hero_down_index == 5:
            break
    else:
        hero.image = hero_surface[ticks // (ANIMATE_CYCLE // 2)]

    # 我方飞机发射子弹,每10帧发射1次子弹
    if ticks % 10 == 0:
        hero.shoot(bullet_surface)
    hero.bullets.update()
    # 绘制子弹
    hero.bullets.draw(screen)

    # 每30帧产生一个敌方飞机
    # 敌方飞机的x坐标用随机函数生成
    if ticks % 30 == 0:
        enemy = Enemy(enemy_surface, [randint(0, SCREEN_WIDTH - enemy_surface.get_width()), -enemy_surface.get_height()])
        enemy_group.add(enemy)
    # 敌机移动
    enemy_group.update()
    # 绘制敌机
    enemy_group.draw(screen)
    # 检测敌机与子弹的碰撞
    #enemy_hit_group.add(pygame.sprite.groupcollide(enemy_group, hero.bullets, True, True))
    enemy_hit_dict = pygame.sprite.groupcollide(enemy_group, hero.bullets, True, True )
    score += len(enemy_hit_dict) * ENEMY_SCORE
    enemy_hit_group.add(enemy_hit_dict)
    for enemy_hit in enemy_hit_group:
        screen.blit(enemy_hit_surface[enemy_hit.explode_index], enemy_hit.rect)
        if ticks % (ANIMATE_CYCLE // 2) == 0:
            if enemy_hit.explode_index < 3:
                enemy_hit.explode_index += 1
            else:
                enemy_hit_group.remove(enemy_hit)
    # 检测敌机与玩家碰撞
    enemy_down_list = pygame.sprite.spritecollide(hero, enemy_group, True)
    if len(enemy_down_list) > 0:
        enemy_hit_group.add(enemy_down_list)
        hero.is_hit = True

    # 绘制飞机
    screen.blit(hero.image, hero.rect)
    ticks += 1
    # 绘制游戏得分
    screen.blit(game_font.render('SCORE  %d' % score, True, [255, 0, 0]), [20, 20])

    # 更新屏幕
    pygame.display.update()

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 控制方向
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = hero.speed
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
    # 移动飞机
    hero.move(offset)
# 跳出主循环
screen.blit(gameover, (0, 0))
# 玩家坠机后退出游戏
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
