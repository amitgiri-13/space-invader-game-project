import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()
#create a screen
screen = pygame.display.set_mode((600,600))
background = pygame.image.load('data/images/sky.jpg')

#background sound
mixer.music.load("data/sounds/spacebg1.wav")
mixer.music.play(1)
    
mixer.music.load("data/sounds/spacebg.wav")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("EXO ENEMY")
icon = pygame.image.load('data/images/ufo.png')
pygame.display.set_icon(icon)

#start of the game 
start_image = pygame.image.load('data/images/play.jpg')
start_font = pygame.font.Font('freesansbold.ttf',100)
start_x = 0
start_y = 0
start = False
#end of the game 
end_image = pygame.image.load('data/images/playagain.jpg')
end_x = 0
end_y = 0
end = False
gameover = False

#player
player_image = pygame.image.load('data/images/spaceship1.png')
player_x = 270
player_y = 500
player_xchange = 0

#alien enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []



num_of_enemy = 5
for i in range(num_of_enemy):
    enemy_image.append(pygame.image.load('data/images/alien.png'))
    enemy_x.append(random.randint(0,540))
    enemy_y.append(random.randint(0,0))
    enemy_image.append(pygame.image.load('data/images/alien1.png'))
    enemy_x.append(random.randint(0,540))
    enemy_y.append(random.randint(0,0))
    enemy_xchange.append(.3)
    enemy_ychange.append(50)
  
#bullet
bullet_image = pygame.image.load('data/images/bullet1.png')
bullet_x = 0
bullet_y = 500
bullet_xchange = .3
bullet_ychange = .9
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',25)
text_x = 10
text_y = 10
high_score = 0
hscore_font = pygame.font.Font('freesansbold.ttf',25)
#game over
over_font = pygame.font.Font('freesansbold.ttf',100)

def start_game(x,y):
    screen.blit(start_image,(start_x,start_y))
    start_text = font.render("START !",True,(20,0,99))
    screen.blit(start_text,(260,570))

def end_game(x,y):
    screen.blit(end_image,(end_x,end_y))


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
    score = font.render("Score : "+ str(score_value),True,(255,25,250))
    screen.blit(score,(y,y))

def show_highscore(x,y):
    h_score = font.render("High Score : "+ str(high_score),True,(90,255,190))
    screen.blit(h_score,(x,y))

def game_over():
    over_text = font.render("MISSION FAILED !",True,(255,0,0))
    screen.blit(over_text,(170,350))

    

#game loop
running = True
while running:
    
    screen.blit(background,(0,0))
    if not start:
        start_game(0,0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if keyboard is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                start = True
                end = False
            if event.key==pygame.K_LEFT:
                player_xchange = -0.5
            if event.key==pygame.K_RIGHT:
                player_xchange = 0.5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('data/sounds/bullet.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x,bullet_y)
                      
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_xchange = 0
            if event.key==pygame.K_SPACE:
                load = True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and gameover:
                end = False
                gameover = False
                
                 
                #initial position of player
                player_x = 270
                player_y = 500
                player_xchange = 0
                #initial position of bullet
                bullet_x = 0
                bullet_y = 500
                bullet_xchange = .3
                bullet_ychange = .6
                bullet_state = "ready"
                #initial position of enemy
                enemy_image = []
                enemy_x = []
                enemy_y = []
                enemy_xchange = []
                enemy_ychange = []
                num_of_enemy = 3
                for i in range(num_of_enemy):
                    enemy_image.append(pygame.image.load('data/images/alien1.png'))
                    enemy_x.append(random.randint(0,540))
                    enemy_y.append(random.randint(0,10))
                    enemy_xchange.append(.3)
                    enemy_ychange.append(50)
                #initial score
                score_value = 0
                restart_sound = mixer.Sound('data/sounds/restart.wav')
                restart_sound.play()
                        
    if start and not end:    
        player_x += player_xchange
        if player_x <= 0:
            player_x = 0
        elif player_x >= 540:
            player_x = 540
        #enemy movement
        for i in range(num_of_enemy):
            #game over
            if enemy_y[i]>400:
                for j in range(num_of_enemy):
                    
                    enemy_y[j]= 2000
                    gameover = True
                    end = True
                    gameover_sound = mixer.Sound('data/sounds/missionfail.wav')
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
                bullet_y =  500
                bullet_state = "ready"
                score_value += 1
                if high_score<score_value:
                    high_score = score_value
                enemy_x[i] = random.randint(0,540)
                enemy_y[i] = 0
                enemy_sound_2 = mixer.Sound('data/sounds/dead.wav')
                enemy_sound_2.play()
            enemy(enemy_x[i],enemy_y[i],i)

        #bullet movement
        if bullet_y <=0:
            bullet_y = 500
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bullet_x,bullet_y)
            bullet_y -= bullet_ychange
        
   

    if end:
        
        end_game(0,0)
        game_over()
        show_highscore(text_x,text_y-5)
    
    
        

    player(player_x,player_y)
    if start and not end:
        show_score(text_x,text_y)
    
    
    pygame.display.update() 