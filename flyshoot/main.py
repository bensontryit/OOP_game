import pygame
import random
import os
# game initialize
pygame.init()
# capital is used to deifine the variable which will not be changed.
FPS=60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGH = 500, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption('flyshoot')    #difine the window name

#load image
background_img = pygame.image.load(os.path.join('img', 'harry_potter_background.jpg')).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGH))
player_img = pygame.image.load(os.path.join('img', 'player.jpg')).convert()
badguy_img = pygame.image.load(os.path.join('img', 'badguy.jpg')).convert()
explo_list = []
for i in range(1, 3):
    file_path = os.path.join("img", f"explosion{i}.png")
    if os.path.exists(file_path):
        image = pygame.image.load(file_path).convert()
        image.set_colorkey(WHITE)
        image = pygame.transform.scale(image, (30, 30))
        explo_list.append(image)
    else:
        print(f"Missing file: {file_path}")
        explo_list.append(None)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGH - 10
        self.speedx= 8
        self.health = 100
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprite.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 隨機生成敵人的寬度和高度
        self.rock_width = random.randint(40, 80)  # 設定寬度的隨機範圍
        self.rock_height = random.randint(60, 120)  # 設定高度的隨機範圍
        
        # 根據隨機尺寸調整圖片
        self.image = pygame.transform.scale(badguy_img, (self.rock_width, self.rock_height))
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGH or self.rect.left < 0 or self.rect.right > WIDTH:
            # 重新生成敵人的位置和大小
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
            rock_width = random.randint(40, 80)
            rock_height = random.randint(60, 120)
            self.image = pygame.transform.scale(badguy_img, (rock_width, rock_height))



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explo_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame == len(explo_list):
                self.kill()

            else:
                self.image = explo_list[self.frame] 
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENTH = 100
    BAR_HEIGHT = 10 
    fill = (hp / 100) * BAR_LENTH
    outline_rect = pygame.Rect(x, y, BAR_LENTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def new_rock():
    r = Rock()
    all_sprite.add(r)
    rocks.add(r)

all_sprite = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprite.add(player)    #add the player in to the sprite


for i in range(8):
    new_rock()

font_name = pygame.font.match_font('arial')

running = True
score = 0
while running:
    clock.tick(FPS)
    #get the user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #update game 
    all_sprite.update() #this method will execute the update of all the objects in all sprite
    hit = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hit:
        score += (hit.rock_width / 2 + hit.rock_height / 2)
        expl = Explosion(hit.rect.center) 
        all_sprite.add(expl)
        new_rock()
    hits = pygame.sprite.spritecollide(player, rocks, True)
    for hit in hits:
        new_rock()
        player.health -= round((hit.rock_width / 10))
        if player.health <= 0:
            running = False

    #display on the screen
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprite.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    pygame.display.update()
pygame.quit()



