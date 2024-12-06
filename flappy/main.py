import pygame
import os
import random

pygame.init()

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # 设置绿色
WIDTH, HEIGHT = 1200, 600
PIPE_WIDTH, PIPE_GAP = 80, 150

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# 加载小鸟图片
bird_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'bird.jpg')).convert(), (20, 35))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.bottom = HEIGHT / 2
        self.upbeat = -10

    def update(self):
        self.rect.bottom += 3  # 重力
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self.rect.bottom += self.upbeat
        # 保证小鸟不出屏幕外
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        pygame.sprite.Sprite.__init__(self)
        
        # Create a full surface for the pipe
        self.image = pygame.Surface((PIPE_WIDTH, HEIGHT))  # Create a surface for the pipe
        self.image.fill(GREEN)  # Fill the pipe with green color

        if is_top:
            # Top pipe part: height is 'y'
            self.image = self.image.subsurface((0, 0, PIPE_WIDTH, y))
        else:
            # Bottom pipe part: starts at 'y + PIPE_GAP' and goes down to the bottom
            self.image = self.image.subsurface((0, y + PIPE_GAP, PIPE_WIDTH, HEIGHT - y - PIPE_GAP))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.top = 0 if is_top else y + PIPE_GAP

    def update(self):
        self.rect.x -= 8  # Move to the left
        if self.rect.right < 0:  # If the pipe goes out of screen, remove it
            self.kill()


def spawn_pipes():
    pipe_y = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = Pipe(WIDTH, pipe_y, True)
    bottom_pipe = Pipe(WIDTH, pipe_y, False)
    pipes.add(top_pipe, bottom_pipe)
    all_sprites.add(top_pipe, bottom_pipe)

bird = Player()
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
all_sprites.add(bird)

running = True
spawn_timer = 0

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 每120帧生成一个新的水管
    spawn_timer += 1
    if spawn_timer > 120:
        spawn_pipes()
        spawn_timer = 0

    # 检查碰撞
    if pygame.sprite.spritecollideany(bird, pipes):
        running = False
    if bird.rect.top == 0 or bird.rect.bottom == HEIGHT:
        running = False
    # 更新所有精灵
    all_sprites.update()

    # 清屏并绘制所有内容
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
