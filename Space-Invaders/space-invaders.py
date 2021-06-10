import random
import pygame
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
pygame.joystick.init()
# define fps
joysticks = []
motion = [0, 0]
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

# define fonts
font30 = pygame.font.SysFont('constantia', 30)
font40 = pygame.font.SysFont('constantia', 40)

# load sounds
bg_sound = pygame.mixer.Sound("img/spaceinvaders1.wav")
bg_sound.set_volume(0.5)
bg_sound.play(-1)

explosion_fx = pygame.mixer.Sound("img/img_explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/img_explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/img_laser.wav")
laser_fx.set_volume(0.25)

# define game variables
rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shoot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0  # 0 means no game over, 1 player win, -1 player lost

# load image
bg = pygame.image.load("img/bg.png")

# define clours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


def draw_bg():
    screen.blit(bg, (0, 0))


# creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create spaceship class
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # set movement speed
        speed = 5
        # set cooldown
        cooldown = 500  # milliseconds
        game_over = 0

        for i in range(pygame.joystick.get_count()):
            joysticks.append((pygame.joystick.Joystick(i)))
            joysticks[-1].init()

        if abs(motion[0]) < 0.2:
            motion[0] = 0

        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 0.7:
                motion[event.axis] = event.value
                self.rect.x += motion[0] * speed

            if event.axis > 0.7:
                motion[event.axis] = event.value
                self.rect.x -= motion[0] * speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 and time_now - self.last_shot > cooldown:
                laser_fx.play()
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width *
                                                          (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


# create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


# Create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_direction = 1
        self.move_count = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_count += 1

        if abs(self.move_count) > 75:
            self.move_direction *= -1
            self.move_count *= self.move_direction


# create Alien_Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.bottom > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            # reduce spaceship health
            spaceship.health_remaining -= 10
            self.kill()
            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# create explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3

        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if animation complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter > explosion_speed:
            self.kill()


# create a sprite group
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullets_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()

# create player
spaceship = SpaceShip(int(screen_width / 2), screen_height - 100, 50)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    # draw background
    draw_bg()

    if countdown == 0:
        # create random alien bullets
        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if time_now - last_alien_shoot > alien_cooldown and len(alien_bullets_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullets_group.add(alien_bullet)
            last_alien_shoot = time_now
        if len(alien_group) == 0:
            game_over = 1
        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()

            # update sprite groups
            bullet_group.update()
            alien_group.update()
            alien_bullets_group.update()
        else:
            if game_over == -1:
                draw_text("GAME OVER!", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text("YOU WIN!", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
    if countdown > 0:
        draw_text("GET READY!", font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    explosion_group.update()

    # draw sprite group
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullets_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update()
    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
