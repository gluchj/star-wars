###############################################################################
# "Star Wars.py" is a 2-D scrolling game based on the popular Star Wars movie
# series. It is written in Python and utilizes the pygame module.
#
# 9/21/17
# Joel Gluch
###############################################################################

import pygame
import sys
import os
import time
import random
import json
import operator
import inputbox
pygame.init()

# game sound definitions
crash_sound = pygame.mixer.Sound("sounds\explosion-02.wav")
laser_sound = pygame.mixer.Sound("sounds\LASER.wav")
laser_hit_sound = pygame.mixer.Sound("sounds\Explosion_01.wav")

# game display and options definitions
display_width = 800
display_height = 600
ship_width = 120
MAX_STARS = 100
STAR_SPEED = 2

# color definitions
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
yellow = (240,250,10)
green = (0,200,0)
bright_green = (0,255,0)
blue = (0,0,200)

pause = False

# load game images, initialize pygame clock, set window size
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Save the Republic")
clock = pygame.time.Clock()
shipImg = pygame.image.load(os.path.join("images", "falcon.png"))
gameIcon = pygame.image.load(os.path.join("images", "falcon-icon.png"))
badshipImg = pygame.image.load(os.path.join("images", "tieFighter.png"))
deathstarImg = pygame.image.load(os.path.join("images", "Death_Star.png"))
pygame.display.set_icon(gameIcon)

#load our ship blowing up images
explosion = []
for i in range(8):
    explosion.append(pygame.image.load(os.path.join("images", "Falcon_Explosion", "regularExplosion0" + str(i) + ".png")))

#load small laser/death star explosion images
explosion2 = []
for i in range(1,90):
    if i < 10:
        explosion2.append(pygame.image.load(os.path.join("images", "64x48", "explosion1_000" + str(i) + ".png")))
    else:
        explosion2.append(pygame.image.load(os.path.join("images", "64x48", "explosion1_00" + str(i) + ".png")))

#load large explosion for death star!!!
explosion3 = []
for i in range(1,90):
    if i < 10:
        explosion3.append(pygame.image.load(os.path.join("images", "640x480", "explosion1_000" + str(i) + ".png")))
    else:
        explosion3.append(pygame.image.load(os.path.join("images", "640x480", "explosion1_00" + str(i) + ".png")))

####################These 2 globals control Normal Mode or Hard Mode########################
num_hits_to_kill_deathstar = 20 # changes to 10 for "normal mode"
ships_passed = 20 # changes to 10 for "normal mode"


#---------------------------------------------------------------------
# create_stars() makes a global list and via a 'for' loop populates it
# with randomly generated x and y coordinates
#---------------------------------------------------------------------
def create_stars():
    global stars
    stars = []
    for i in range(MAX_STARS):
        star = [random.randrange(0,display_width-1), random.randrange(0,display_height-1)]
        stars.append(star)

#---------------------------------------------------------------------
# move_and_draw_stars() puts the stars on the screen and continusously
# updates their location to create movement
#---------------------------------------------------------------------
def move_and_draw_stars():
    global stars
    for star in stars:
        star[1] += STAR_SPEED
        #once star reaches bottom of screen recreate it at top
        if star[1] > display_height:
            star[1] = 0
            star[0] = random.randrange(0, display_width-1)
        gameDisplay.set_at(star,(white))

#---------------------------------------------------------------------
# laser_beam(screen, color, (x,y,w,h)) will be the lasers from good
# and bad guy ships
#---------------------------------------------------------------------
def laser_beam(color,x,y,w,h):
    pygame.draw.rect(gameDisplay, color,(x,y,w,h))

#---------------------------------------------------------------------
# ship(x,y) reloads the ship image at the specified coordinates (which
# will show on screen when the next pygame.display.update() is called)
#---------------------------------------------------------------------
def ship(x,y):
    gameDisplay.blit(shipImg, (x,y))

#---------------------------------------------------------------------
# badguy(x,y) reloads the bad guy ship image at the specified coordinates
# which will show on screen when the next pygame.display.update() is called)
#---------------------------------------------------------------------
def badguy(x,y):
    gameDisplay.blit(badshipImg, (x,y))

#---------------------------------------------------------------------
# deathstar(x,y) reloads the bad guy ship image at the specified coordinates
# which will show on screen when the next pygame.display.update() is called)
#---------------------------------------------------------------------
def deathstar(x,y):
    gameDisplay.blit(deathstarImg, (x,y))

#---------------------------------------------------------------------
# explode(x,y) will create an explosion at the given (x,y) point for
# our game.
#---------------------------------------------------------------------
def explode(x,y):
    #display our 8 explosion images
    for i in range(8):
        clock.tick(12)
        gameDisplay.blit(explosion[i], (x,y))
        pygame.display.update()

#---------------------------------------------------------------------
# laser_hit(x,y) will create an explosion at the given (x,y) point for
# our game.
#---------------------------------------------------------------------
def laser_hit(x,y):
    #display our 90 explosion2 images
    pygame.mixer.Sound.play(laser_hit_sound)
    for item in explosion2:
        gameDisplay.blit(item, (x,y))
        pygame.display.update()

#---------------------------------------------------------------------
# deathstar_explosion(x,y) will create an explosion at the given (x,y)
# point for our game.
#---------------------------------------------------------------------
def deathstar_explosion(x,y,count):
    #display our 90 explosion2 images
    pygame.mixer.Sound.play(crash_sound)
    for item in explosion3:
        clock.tick(20)
        item = pygame.transform.scale(item, (1280,720))
        gameDisplay.blit(item, (x,y))
        pygame.display.update()
    highScores = new_high_score(count)
    pygame.mixer.music.load("sounds\End_Credits.mid")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("comicsansms", 65)
        TextSurf = largeText.render("VICTORY!", True, yellow)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        show_high_scores(highScores)
        button("Play Again?", 200, 400, 110, 40, bright_green, green, game_loop)
        button("QUIT", 500, 400, 110, 40, bright_red, red, quitgame)
        pygame.display.update()

#---------------------------------------------------------------------
# crash() is called when the user hits something with the ship. 
#---------------------------------------------------------------------
def crash(x,y,count):
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    explode(x,y)
    highScores = new_high_score(count)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("comicsansms", 65)
        TextSurf = largeText.render("You Crashed!", True, red)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        show_high_scores(highScores)

        button("Try Again?", 200, 400, 110, 40, bright_green, green, game_loop)
        button("QUIT", 500, 400, 110, 40, bright_red, red, quitgame)
        
        pygame.display.update()
        clock.tick(15)

#---------------------------------------------------------------------
# new_high_score(count) is a loop that will check if count is a new
# high score. If not, return current scores. If so, prompt the user for
# a name and save the new score with name to the file then return this
#---------------------------------------------------------------------
def new_high_score(count):
    highScores = []
    count = count * 100
    with open("high_score.dat", "r") as f:
        for i in f.read().splitlines():
            tmp = i.split(",")
            highScores.append((tmp[0],int(tmp[1])))
        f.close()
    sorted_highScores = sorted(highScores, key=operator.itemgetter(1))
    if count > sorted_highScores[0][1]:
        pygame.mixer.music.load("sounds\Cantina_Band.mid")
        pygame.mixer.music.play(-1)
        sorted_highScores.pop(0)
        name = inputbox.ask(gameDisplay, "Name")
        sorted_highScores.append((name, count))
        with open("high_score.dat", "w") as f:
            for item in sorted_highScores:
                f.write(str(item[0]) + "," + str(item[1]) + "\n")
    return sorted_highScores
    
#---------------------------------------------------------------------
# show_high_scores() displays the top 3 scores from our json file.
# Takes the dictionary highScores as a paramater (our opened json)
#---------------------------------------------------------------------
def show_high_scores(highScores):
    scores = sorted(highScores, key=operator.itemgetter(1))
    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render("High Scores:", True, yellow)
    text2 = font.render(str(scores[2][0])+": "+str(str(scores[2][1])), True, yellow)
    text3 = font.render(str(scores[1][0])+": "+str(str(scores[1][1])), True, yellow)
    text4 = font.render(str(scores[0][0])+": "+str(str(scores[0][1])), True, yellow)
    gameDisplay.blit(text,((display_width/3),20))
    gameDisplay.blit(text2, ((display_width/3),70))
    gameDisplay.blit(text3, ((display_width/3),120))
    gameDisplay.blit(text4, ((display_width/3),170))

#---------------------------------------------------------------------
# things_dodged(count) will display the paramater "count" which are
# blocks we have dodged in the upper left of our screen
#---------------------------------------------------------------------
def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 30)
    text = font.render("Score: " + str(count*100), True, white) #count * 100 to make score bigger
    gameDisplay.blit(text,(20,20))

#---------------------------------------------------------------------
# button() draws our button and tracks mouse movements over it.
# parameters: msg=button text, x,y=coordinates w,h=button width/height
# i = button inactive color, a = button active color
#---------------------------------------------------------------------
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y < mouse[1] < y+h:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h)) #mouse ON bttn
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h)) #mouse NOT on bttn
    # Creates text on button
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf = smallText.render(msg, True, black)
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

#---------------------------------------------------------------------
# quitgame() terminates the game and exits Python
#---------------------------------------------------------------------
def quitgame():
    pygame.quit()
    sys.exit()

#---------------------------------------------------------------------
# unpause() sets the global pause variable to false breaking us out of
# the pause() while look below and resuming the game_loop()
#---------------------------------------------------------------------
def unpause():
    global pause
    pygame.mixer.music.play(-1)
    pause = False
    
#---------------------------------------------------------------------
# game_pause() is a loop that will pause the game
#---------------------------------------------------------------------
def game_pause():
    pygame.mixer.music.stop()
    largeText = pygame.font.SysFont("comicsansms", 85)
    TextSurf = largeText.render("Paused", True, yellow)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    unpause()
        gameDisplay.fill(black)
        button("Continue", 200, 400, 90, 40, bright_green, green, unpause)
        button("QUIT", 500, 400, 90, 40, bright_red, red, quitgame)
        
        pygame.display.update()
        clock.tick(15)

def set_mode_normal():
    global num_hits_to_kill_deathstar
    num_hits_to_kill_deathstar = 10
    global ships_passed
    ships_passed = 10
    game_loop()

def set_mode_hard():
    global num_hits_to_kill_deathstar
    num_hits_to_kill_deathstar = 20
    global ships_passed
    ships_passed = 20
    game_loop()

#---------------------------------------------------------------------
# get_instructions() is a loop that displays some dialog between our
# two heroes for the purpose of telling the user how to play.
#---------------------------------------------------------------------
def get_instructions():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.fill(black)
        instructions = pygame.image.load(os.path.join("images", "Han_Chewy.png"))
        gameDisplay.blit(instructions, (144, 50))    
        button("Normal", 200, 500, 90, 40, bright_green, green, set_mode_normal)
        button("Hard", 500, 500, 90, 40, bright_green, green, set_mode_hard)
        pygame.display.update()
        clock.tick(15)

#---------------------------------------------------------------------
# get_intro() is an intro loop that will tick until the user starts
# the game. It will display a nice splash screen at program startup.
#---------------------------------------------------------------------
def game_intro():
    intro = True
    pygame.mixer.music.load("sounds\Main_Title.mid")
    pygame.mixer.music.play(-1)

    highScores = []
    with open("high_score.dat", "r") as f:
        for i in f.read().splitlines():
            tmp = i.split(",")
            highScores.append((tmp[0],int(tmp[1])))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.fill(black)
        show_high_scores(highScores)
        largeText = pygame.font.SysFont("comicsansms", 85)
        TextSurf = largeText.render("STAR WARS", True, yellow)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("PLAY", 200, 400, 90, 40, bright_green, green, get_instructions)
        button("QUIT", 500, 400, 90, 40, bright_red, red, quitgame)
        
        pygame.display.update()
        clock.tick(15)

#---------------------------------------------------------------------
# game_loop() is our main logic loop for catching user input and
# excuting the game's logic.
#---------------------------------------------------------------------
def game_loop():
    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.7)
    x_change = 0
    y_change = 0
    ship_speed = 0
    badguy_speed = 5
    badguy_max_speed = 10
    badguy_width = 164
    badguy_height = 160
    badguy_x = random.randrange(0, (display_width - badguy_width))
    badguy_y = -600
    deathstar_width = 600
    deathstar_height = 594
    deathstar_x = random.randrange(-50, (display_width - deathstar_width))
    deathstar_y = -600
    deathstar_x_change = 1
    deathstar_y_change = 1
    deathstar_hits = 0
    count = 0
    create_stars()
    pygame.mixer.music.load("sounds\Into_the_Trap.mid")
    pygame.mixer.music.play(-1)
    music_switch = True
    laser_x = []
    laser_y = []
    deathstar_laser_y = []
    deathstar_laser_x = []
    laser_height = 40
    laser_weight = 5
    good_laser_color = blue
    bad_laser_color = red
    laser_speed = 8
    NUM_BEAMS = 0
    NUM_BAD_BEAMS = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
#====================code start for left and right movement===============#
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    game_pause()
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(laser_sound)
                    NUM_BEAMS += 1
                    laser_x.append(x+97)
                    laser_y.append(y-5)
                if event.key == pygame.K_LEFT:
                    x_change = -8
                elif event.key == pygame.K_RIGHT:
                    x_change = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
#============ code for up and down movement - currently unused ===========#
#        if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_UP:
#                    y_change = -5
#                elif event.key == pygame.K_DOWN:
#                    y_change = 5
#        if event.type == pygame.KEYUP:
#                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#                    y_change = 0
#        y += y_change
#=========================================================================#    
        gameDisplay.fill(black)
        move_and_draw_stars()
        ship(x,y)

        #tieFighters continue to come until x have passed starting the boss fight
        if count < ships_passed:
            badguy(badguy_x, badguy_y)
            badguy_y += badguy_speed
        else:
            if music_switch is True:
                pygame.mixer.music.load("sounds\Vaders_Theme.mid")
                pygame.mixer.music.play(-1)
                music_switch = False
            deathstar(deathstar_x, deathstar_y) #display deathstar
            if deathstar_y > -370: #if deathstar hits floor of y start subtracting 1 from y coordinate
                deathstar_y_change = -1
            if deathstar_y < -500: #if deathstar hits ceiling of y start adding 1 from y coordinate
                deathstar_y_change = 1
            if deathstar_x < -50: #if deathstar hits wall of y limits reverse course
                deathstar_x_change = 1
            if deathstar_x + deathstar_width > display_width + 50:
                deathstar_x_change = -1
            deathstar_x += deathstar_x_change
            deathstar_y += deathstar_y_change

            # DeathStar laser beam generation
            if NUM_BAD_BEAMS < 2:
                deathstar_laser_x.append(random.randrange(deathstar_x + 50, deathstar_x + deathstar_width - 50))
                deathstar_laser_y.append(deathstar_y + 300)
                NUM_BAD_BEAMS += 1
            for i in range(NUM_BAD_BEAMS-1, -1, -1):
                laser_beam(bad_laser_color,deathstar_laser_x[i],deathstar_laser_y[i],laser_weight, laser_height + 25)

                #Deathstar laser beam hit detection with the Falcon
                if deathstar_laser_y[i] + 65 >= y:
                    if x <= deathstar_laser_x[i] <= x + ship_width:
                        deathstar_laser_y[i] = display_height
                        crash(x, y, count + deathstar_hits)
                deathstar_laser_y[i] += laser_speed
                
                if deathstar_laser_y[i] > display_height:
                    del deathstar_laser_y[i]
                    del deathstar_laser_x[i]
                    NUM_BAD_BEAMS -= 1              

        #displays all laser shots for player
        for i in range(NUM_BEAMS-1, -1, -1): #using range function to iterate list in reverse order
            laser_beam(good_laser_color,laser_x[i],laser_y[i],laser_weight,laser_height)

            #Laser beam hit detection with death star exhause hole (355,370) and (425,445) are the
            #rect coordinates of the exhaust hole on the death star
            if deathstar_y + 370 <= laser_y[i] <= deathstar_y + 445:
                if deathstar_x + 355 <= laser_x[i] <= deathstar_x + 425:
                    laser_y[i] = -1
                    laser_hit(laser_x[i], laser_y[i])
                    deathstar_hits += 1
                    #print(str(deathstar_hits))   
            laser_y[i] -= laser_speed

            if deathstar_hits > num_hits_to_kill_deathstar: #Deathstar has been destroyed
                deathstar_explosion(deathstar_x - 300,deathstar_y + 100, count + deathstar_hits)

            #remove beam coordinates from coordinates lists after it leaves screen
            if laser_y[i] < 0:
                del laser_y[i]
                del laser_x[i]
                NUM_BEAMS -= 1
        
        ###if ship hits a side wall
        if x > display_width - ship_width or x < 0:    
            crash(x,y,count + deathstar_hits)
  
        #if a bad guy ship passes our y coordinate (not necessarily our x though)
        if y < badguy_y + badguy_height:
            #checks if x coordinate and x+width coordinate of BOTH Falcon and bad guy ship falls within range of the other, ie crashed into each other
            if x > badguy_x and x < (badguy_x + badguy_width) or (x + ship_width) > badguy_x and (x + ship_width) < (badguy_x + badguy_width) or badguy_x >= x and badguy_x <= x+ship_width or badguy_x + badguy_width >= x and badguy_x + badguy_width <= x+ship_width:
                  crash(x,y,count + deathstar_hits)
        #once bad guy leaves screen, change it's x,y to be at the top of screen again
        if badguy_y > display_height:
            count += 1
            if badguy_speed < badguy_max_speed:
                badguy_speed += .5
            badguy_y = 0 - badguy_height
            badguy_x = random.randrange(0, (display_width - badguy_width))

        things_dodged(count + deathstar_hits) #displays score on screen
        pygame.display.update()
        clock.tick(60)
#==========================End of Game Loop====================================

game_intro()
game_loop()
pygame.quit()
sys.exit()