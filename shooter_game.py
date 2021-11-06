# Create your own shooter
from pygame import *
from random import randint

# mixer.music.load('')
# mixer.music.play()

#create game window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

font.init()
font_1 = font.SysFont("Arial", 36)
font_2 = font.SysFont("Arial", 80)

win_text = font_2.render("VICTORY", True, (255, 255, 255))
lose_text = font_2.render("GAME OVER", True, (255, 255, 255))

# GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.ast_speed = randint(2, 3)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
score = 0
ammo = 5
lives = 3

class Enemy(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       global lost
       #disappears upon reaching the screen edge
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost += 1

enemys = sprite.Group()

for i in range(5):
    enemy = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    enemys.add(enemy)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.ast_speed 
        if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0

asteroids = sprite.Group()

for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

rocket = Rocket('rocket.png', 5, win_height - 80, 80, 100, 4)

clock = time.Clock()
# timer for 3 seconds
time.set_timer(USEREVENT, 1000 * 3)

game = True

state = "start"

while game:
    keys_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo > 0:
                    rocket.fire()
                    ammo -= 1
                
        elif e.type == USEREVENT:
            if ammo < 5:
                ammo += 1
    if state == "start":
        window.blit(background, (0, 0))

        start_text = font_2.render("Shooter Game", True, (255, 255, 255))
        window.blit(start_text, (150, 140))

        instruction_text = font_2.render("CLICK P TO PLAY", True, (255, 255, 255))
        window.blit(instruction_text, (110, 260))

        if keys_pressed[K_p]:
            score = 0
            lost = 0
            lives = 3
            ammo = 5

            for a in asteroids:
                a.kill()
            for b in bullets:
                b.kill()
            for e in enemys:
                e.kill()
            
            for i in range(3):
                asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
                asteroids.add(asteroid)

            for i in range(5):
                enemy = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
                enemys.add(enemy)

            rocket = Rocket('rocket.png', 5, win_height - 80, 80, 100, 4)
            state = "play"

    elif state == "play":  
        window.blit(background, (0, 0))

        text_lost = font_1.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 20))

        text_score = font_1.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 50))

        text_ammo = font_1.render("Ammo: " + str(ammo), 1, (255, 255, 255))
        window.blit(text_ammo, (10, 80))

        text_lives = font_1.render("Lives: " + str(lives), 1, (255, 255, 255))
        window.blit(text_lives, (10, 110))

        rocket.update()
        enemys.update()
        bullets.update()
        for asteroid in asteroids:
            asteroid.reset()
            asteroid.update()


        rocket.reset()

        enemys.draw(window)
        bullets.draw(window)


        collisions = sprite.groupcollide(enemys, bullets, True, True)

        # asteroid_col = sprite.groupcollide(asteroids, bullets, True, True)

        for c in collisions:
            score = score + 1
            enemy = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            enemys.add(enemy)

        for asteroid in asteroids:
            for bullet in bullets:
                if sprite.collide_rect(asteroid, bullet):
                    bullet.kill()
            if sprite.collide_rect(asteroid, rocket):
                if lives >= 1:
                    lives -= 1
                    asteroid.kill()
                    if lives <= 0:
                        state = "gameover"
                        status = "lost"
        for enemy in enemys:
            if sprite.collide_rect(rocket, enemy):
                if lives >= 1:
                    lives -= 1
                    enemy.kill()
                    if lives <= 0:
                        state = "gameover"
                        status = "lost"
                        
        if lost >= 10:
            state = "gameover"
            status = "lost"
        if score >= 15:
            state = "gameover"
            staus = "win"

    elif state == "gameover":
        window.blit(background, (0, 0))
        if status == "lost":
            window.blit(lose_text, (170, 140))
        elif status == "win":
            window.blit(win_text, (200, 140))
        
        text_over = font_2.render("PRESS M", 1, (255, 255, 255))
        window.blit(text_over, (230, 260))

        if keys_pressed[K_m]:
            state = "start"
        
    display.update()

    clock.tick(60)