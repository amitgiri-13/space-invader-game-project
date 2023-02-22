import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()
#create a screen
screen = pygame.display.set_mode((600,800))
background = pygame.image.load('sky.jpg')

#background sound
mixer.music.load("spacebg1.wav")
mixer.music.play(1)
    
mixer.music.load("spacebg.wav")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("space invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
player_image = pygame.image.load('spaceship1.png')
player_x = 270
player_y = 700
player_xchange = 0

#alien enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemy_image.append(pygame.image.load('alien1.png'))
    enemy_x.append(random.randint(0,540))
    enemy_y.append(random.randint(0,10))
    enemy_xchange.append(.3)
    enemy_ychange.append(50)
  
#bullet
bullet_image = pygame.image.load('bullet1.png')
bullet_x = 0
bullet_y = 700
bullet_xchange = .3
bullet_ychange = .9
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y = 10
#game over
over_font = pygame.font.Font('freesansbold.ttf',64)
def player(x,y):
    screen.blit(player_image,(player_x,player_y))
    
def enemy(x,y,i):
    screen.blit(enemy_image[i],(enemy_x[i],enemy_y[i]))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image,(x+14,y))

def iscollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow(enemy_x-bullet_x,2)+math.pow(enemy_y-bullet_y,2))
    if distance < 30:
        return True
    else:
        return False
def show_score(x,y):
    score = font.render("Score : "+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over():
    over_text = font.render("MISSION FAILED !",True,(255,0,255))
    screen.blit(over_text,(160,400))

#game loop
running = True
while running:
    screen.fill((50,25,112))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keyboard is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_xchange = -0.3
            if event.key==pygame.K_RIGHT:
                player_xchange = 0.3
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x,bullet_y)
                
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_xchange = 0
            if event.key==pygame.K_SPACE:
                load = True
        
    player_x += player_xchange
    if player_x <= 0:
        player_x = 0
    elif player_x >= 540:
        player_x = 540
    #enemy movement
    for i in range(num_of_enemy):
        #game over
        if enemy_y[i]>500:
            for j in range(num_of_enemy):
                enemy_y[j]= 2000
            game_over()
            gameover_sound = mixer.Sound('missionfail.wav')
            gameover_sound.play()
            break

        enemy_x[i]+= enemy_xchange[i]
        if enemy_x[i] <= 0:
            enemy_xchange[i] = 0.3
            enemy_y[i] += enemy_ychange[i]
        elif enemy_x[i] >= 540:
            enemy_xchange[i] = -.3
            enemy_y[i] += enemy_ychange[i]
        
         #collision
        collision = iscollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)  
        if collision:
            bullet_y =  700
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0,540)
            enemy_y[i] = 10
            enemy_sound = mixer.Sound('die.wav')
            enemy_sound.play()
            enemy_sound_2 = mixer.Sound('dead.wav')
            enemy_sound_2.play()
        enemy(enemy_x[i],enemy_y[i],i)

    #bullet movement
    if bullet_y <=0:
        bullet_y = 700
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_ychange
    
   
        



      
    player(player_x,player_y)
    show_score(text_x,text_y)
   
    pygame.display.update() 