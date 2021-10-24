import math
import random

import pygame


# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('images/bg7.jpeg')
background=pygame.transform.scale(background,(800,600))

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value=0



font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

#Token
token_value=0
font = pygame.font.Font('freesansbold.ttf', 32)

textX1 = 200
testY1= 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_token(x, y):
    token = font.render("Token : " + str(token_value), True, (255, 255, 255))
    screen.blit(token, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# It is better to make a function called insert_image which takes a image and x, y coordinate. That would reduce several lines. For enemy, the input image could just be enemyImg[i] rather than being a seperate function


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    
                   
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            
            
            bulletY = 480
            bullet_state = "ready"
            score_value += 100
            
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            if score_value>=100 and score_value<200:
               token_value +=15
            elif score_value>=200 and score_value<300:
                token_value +=15
            elif score_value>=300 and score_value<400:
                token_value +=15
            elif score_value>=400 and score_value<500:
                token_value +=15
            elif score_value>=500 and score_value<600:
                token_value =token_value+15+20*1   
            else:
                token_value+=15
            

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    player(playerX, playerY)
    show_score(textX, testY)
    show_token(textX1, testY1)
    pygame.display.update()