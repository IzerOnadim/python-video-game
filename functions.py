# import all mod les that I need
import pygame
import random
import time
import shelve
from os import path
from datetime import datetime as dt

# initialise pygame
pygame.init()
# define clock to control frames per second
clock = pygame.time.Clock()

# define colours I will need through RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
QUITRED = (130, 0, 0)
GREEN = (0, 255, 0)
STARTGREEN = (0, 130, 0)
BLUE = (0, 0, 255)
MUTEBLUE = (0, 0, 130)
YELLOW = (255, 255, 0)
MUTEYELLOW = (130, 130, 0)
ORANGE = (255, 69, 0)
PRESSORANGE = (180, 50, 0)
PURPLE = (255, 0, 255)
PRESSPURPLE = (128, 0, 128)

# initialise some global variable
level = 1
lives = 3
Score = 0
Pass = True
rep = True

# import my classes file
import classes
# import player from classes file
from classes import player

# give the player a certain amount of ammo depending on whether it is a boss level or not
if (level % 5) == 0:
    magLeft = 14
else:
    magLeft = 10
# shoot cooldown prevents player from firing many consecutive bullets - gun is semi-automatic not fully automatic
shootCooldown = 0

# define dimensions of the screen
windowWidth = 700
windowSize = (windowWidth, windowWidth)
# create the window
window = pygame.display.set_mode(windowSize)

# initialise all the lists that I use as empty
boats = []
speeds = []
invincibles = []
nukes = []
skips = []
randxs = []
starts = []
randHxs = []
randHys = []
healths = []
scores = []
randSxs = []
randSys = []
bullets = []
enemies = []
bosses = []
ceilingBlocks = []

# define the file that contains the highscore
HSfile = ("highscore.txt")

# define the file that contains the highest level reached
HLfile = ("highlevel.txt")

# define all the fonts that I will need
font1 = pygame.font.SysFont("comicsans", 25)
font2 = pygame.font.SysFont("comicsans", 100)
font3 = pygame.font.SysFont("comicsans", 70)
font4 = pygame.font.SysFont("comicsans", 45)

# import all of the images that I will need
beach = pygame.image.load("beach.png")
waves = pygame.image.load("waves.png")
sea = pygame.image.load("sea.jpg")
lightningBolt = pygame.image.load("lightningBolt.png")
infinity = pygame.image.load("infinity.png")
explosion = pygame.image.load("explosion.png")

# scale the images to the correct size
background = pygame.transform.scale(beach, (windowSize))
pauseBackground = pygame.transform.scale(waves, (windowSize))
explosion = pygame.transform.scale(explosion, (windowSize))
introBackground = pygame.transform.scale(sea, (windowSize))
lightningBolt = pygame.transform.scale(lightningBolt, (45, 45))
infinity = pygame.transform.scale(infinity, (70, 40))

# import music
music = pygame.mixer.music.load('music.mp3')

# import sound effects
moneySound = pygame.mixer.Sound('money.wav')
bulletSound = pygame.mixer.Sound('bullet.wav')
explosionSound = pygame.mixer.Sound('explosionSound.wav')

# boolean to control whether music is playing
mute = False

# boolean to determine whether we are in timed mode or in normal
timed = False

# function to allow music to be muted


def music():

    global mute
    # when mute button is pressed, checks if music was already muted, if so unmutes, if not mutes the music
    if mute:
        pygame.mixer.music.unpause()
        mute = False
    else:
        pygame.mixer.music.pause()
        mute = True

# creating my own delay function to allow the user to exit the game during a delay


def delay(period):
    i = 0
    while i < 100:
        pygame.time.delay(period)
        i += 1
        # checks if the user is exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 101
                pygame.quit()

# function to create random coordinates for power ups without clashes


def randomise():

    repetition = True

    while repetition:
        repetition = False
        xVal = random.randint(50, 650)
        for randSx in randSxs:
            # check against x values of scores to prevent collisions
            if randSx - 30 < xVal < randSx + 30:
                repetition = True
        for randHx in randHxs:
            # checks against x values of healths to prevent collisions
            if randHx - 30 < xVal < randHx + 30:
                repetition = True

    repetition = True

    while repetition:
        repetition = False
        yVal = random.randint(50, 600)
        for randSy in randSys:
            # check against x values of scores to prevent collisions
            if randSy - 30 < yVal < randSy + 30:
                repetition = True
        for randHy in randHys:
            # checks against x values of healths to prevent collisions
            if randHy - 30 < yVal < randHy + 30:
                repetition = True

    # return random coordinates
    return (xVal, yVal)

# create all lists and set all variables between levels
# called after every level to reset/increment values


def createNextLevel():

    global timeLimit
    global timeLeft
    global rep
    global magLeft

    # reset the position of the player at the start of every level
    player.x = 337
    player.y = 650

    if timed:
        # time given in milliseconds
        if level > 9:
            timeLimit = 1860
        elif level > 4:
            timeLimit = 1560
        else:
            timeLimit = 1260
        timeLeft = timeLimit

    # define how many bullets that the player will have
    if (level % 5) == 0:
        # 14 bulltes for every boss level
        magLeft = 14
    else:
        # 10 bullets for every normal level
        magLeft = 10

    # write the hints that the player will see before each level
    if level == 1:
        hint = "hint: collect all the treasure to pass"
    elif level == 2:
        hint = "hint: collect all the treasure to get firepower"
    elif level == 3:
        hint = "hint: torpedos can be shot down"
    elif level == 5:
        hint = "hint: release the kraken"
    elif level == 10:
        hint = "hint: double trouble"
    else:
        hint = ""

    # blit the background for the transition between levels onto the screen
    window.blit(pauseBackground, (0, 0))

    # define the stats to show the user in between each level
    textMinus = font2.render("Level: " + str(level), 1, BLUE)
    textScoreUpdate = font4.render("Score: " + str(Score), 1, BLACK)
    textLivesUpdate = font4.render("Lives: " + str(lives), 1, BLACK)

    # create the hint
    hintText = font4.render(hint, 1, RED)

    # blit the text onto the screen in between levels
    window.blit(textMinus, (230, windowWidth/2))
    window.blit(textScoreUpdate, (300, 420))
    window.blit(textLivesUpdate, (303, 455))
    window.blit(hintText, (20, 650))
    # refresh the display with the writing on it
    pygame.display.update()

    # delay so that the user has a chance to read the hint
    delay(23)

    # clear all of the lists at the start of each level
    healths.clear()
    scores.clear()
    speeds.clear()
    invincibles.clear()
    nukes.clear()
    skips.clear()
    randHxs.clear()
    randHys.clear()
    randSxs.clear()
    randSys.clear()
    randxs.clear()
    boats.clear()
    bullets.clear()
    ceilingBlocks.clear()
    enemies.clear()
    bosses.clear()

    rep = True

    # creates random x positions for the all of the boats, making sure that they don't line up
    for i in range(15):

        repetition = True
        # loop while repeat so that boats do not overlap - repeat until varient x values are found
        while repetition:
            repetition = False
            currentVal = random.randint(0, 650)
            for randx in randxs:
                # checks each new x value with all other x values to make sure that none are the same
                if randx - 25 < currentVal < randx + 25:
                    repetition = True
        # place x value in a list of x values
        randxs.append(currentVal)
        starts.append(i*40 + 40)
        # instantiate boats with random x values and place them into a list that contains all boats
        boats.append(classes.obstacles(randxs[i], starts[i], 40, 20, 660))

    # create random x and y coordinates for the health points, and make sure they don't clash with any others
    for i in range(2):

        repetition = True
        while repetition:
            repetition = False
            currentVal = random.randint(50, 650)
            for randHx in randHxs:
                # check if clash in x value is occuring
                if randHx - 30 < currentVal < randHx + 30:
                    repetition = True
        # place x value in a list of x values
        randHxs.append(currentVal)

        repetition = True
        while repetition:
            repetition = False
            currentVal = random.randint(50, 600)
            for randHy in randHys:
                # check if clash in y value is occuring
                if randHy - 30 < currentVal < randHy + 30:
                    repetition = True
        # place y value in list of y values
        randHys.append(currentVal)

        # instantiate healthPoints with generated x and y values and place them all into a list
        healths.append(classes.healthPoints(randHxs[i], randHys[i]))

    # create random x and y values for the score points, making sure they don't overlap with either themselves or the healthpoints
    for i in range(7):

        repetition = True
        while repetition:
            repetition = False
            currentVal = random.randint(50, 650)
            for randSx in randSxs:
                # check against x values of other scores
                if randSx - 30 < currentVal < randSx + 30:
                    repetition = True
            for randHx in randHxs:
                # checks against x values of healths
                if randHx - 30 < currentVal < randHx + 30:
                    repetition = True
        # append new x value to list of x values for scores
        randSxs.append(currentVal)

        repetition = True
        while repetition:
            repetition = False
            currentVal = random.randint(50, 600)
            for randSy in randSys:
                # check against y values of other scores
                if randSy - 30 < currentVal < randSy + 30:
                    repetition = True
            for randHy in randHys:
                # check against y values of healths
                if randHy - 30 < currentVal < randHy + 30:
                    repetition = True
        # append new y value to list of y values for scores
        randSys.append(currentVal)

        # instantiate scorePoints with generated x and y values and place them all into a list
        scores.append(classes.scorePoints(randSxs[i], randSys[i]))

    for i in range(18):
        # instantiate ceiling from blocks class
        ceiling = classes.blocks(BLUE, i*40, 0)
        # append ceiling to list containing cailingblocks - all elemnts in the list will appear on the screen
        ceilingBlocks.append(ceiling)

    # design what enemies/bosses will be created every level, by instantiating them and appending them to lists
    # whatever is contained in the lists will be drawn to the screen
    if level == 3:
        # append 1 enemy
        enemies.append(classes.chasers(350, -50, 15, 40))
    if level == 4:
        # append 2 enemies
        for i in range(2):
            enemies.append(classes.chasers(
                (i+1)*(windowWidth/(3)), -50, 15, 40))
    if level == 5:
        # append 1 boss
        bosses.append(classes.bigBoss(350, -150, 140, 140))
    if 5 < level < 8:
        # append 3 enemies
        for i in range(3):
            enemies.append(classes.chasers(
                (i+1)*(windowWidth/(4)), -50, 15, 40))
    if 7 < level < 10:
        # append 4 enemies
        for i in range(4):
            enemies.append(classes.chasers(
                (i+1)*(windowWidth/(5)), -50, 15, 40))
    if level > 7 and (level % 5) == 0:
        # append 2 bosses
        for i in range(2):
            bosses.append(classes.bigBoss(
                (i+1)*(windowWidth/(3)), -150, 140, 140))
    if level > 10 and (level % 5) != 0:
        # append 5 enemies
        for i in range(5):
            enemies.append(classes.chasers(
                (i+1)*(windowWidth/(6)), -50, 15, 40))

    # generate random number which will determine whether a power up will appear that round
    p = random.randint(0, 11)

    # must be one of 4 numbers out of 12, so there is a 33.3% chance of a speed powerup appearing each round
    if level > 1 and (p == 0 or p == 1 or p == 2 or p == 3):
        # use randomise to generate random coordinates
        (xVal, yVal) = randomise()
        # instantiate an object of the speedUp class with generated x and y values and add to speeds list
        speeds.append(classes.speedUp(xVal, yVal))

    # must be one of 3 numbers out of 12, so there is a 25% chance of an invincibility power up appearing each round
    elif level > 1 and (p == 4 or p == 5 or p == 6):
        # use randomise to generate random coordinates
        (xVal, yVal) = randomise()
        # instantiate an object of the invincibility class with generated x and y values and add to invincibles list
        invincibles.append(classes.invincibility(xVal, yVal))

    # must be one of 2 numbers out of 12, so there is a 16.7% chance nuke power up will appear each round
    elif level > 2 and (p == 7 or p == 8):
        # use randomise to generate random coordinates
        (xVal, yVal) = randomise()
        # instantiate an object of the nuke class with generated x and y values and add to invincibles list
        nukes.append(classes.bomb(xVal, yVal))

    # must be one number out of 12, so there is an 8.3% chance skip power up will appear each round
    elif level > 2 and p == 9:
        # use randomise to generate random coordinates
        (xVal, yVal) = randomise()
        # instantiate an object of the invincibility class with generated x and y values and add to invincibles list
        skips.append(classes.roundSkip(xVal, yVal))

# defines what will happen before the first level when play is pressed


def levelOne():
    # a background is drawn, as well as ready? and go!
    window.blit(introBackground, (0, 0))
    window.blit(pauseBackground, (0, 0))
    textMinus = font2.render("READY?", 1, BLUE)
    window.blit(textMinus, (230, windowWidth/2))
    pygame.display.update()
    # delay so that the player can see the writing
    delay(8)
    createNextLevel()

    window.blit(pauseBackground, (0, 0))
    textMinus = font2.render("GO!", 1, BLUE)
    window.blit(textMinus, (290, windowWidth/2))
    pygame.display.update()
    # delay so that the player can see the writing
    delay(5)
    # start game loop
    gameLoop()

# draw the screen and everything on it


def drawGameWindow():

    global speedTimer
    global invincibilityTimer
    global playerInv
    #global timeLeft
    #global timed

    # drawing scorePoints/treasure
    for score in scores:
        score.draw(window)
    # drawing healthpoints
    for health in healths:
        health.draw(window)
    # draw speed power ups
    for speed in speeds:
        speed.draw(window)
    # draw invincibility power ups
    for invincible in invincibles:
        invincible.draw(window)
    # draw nuke power ups
    for nuke in nukes:
        nuke.draw(window)
    # draw round skip powerps
    for skip in skips:
        skip.draw(window)
    # drawing player
    player.draw(window)
    # drawing obstacle boats
    for boat in boats:
        boat.draw(window)
    # draw bullets whenever there are bullets in the list
    for bullet in bullets:
        bullet.draw(window)
    # draw all the blocks blocking the players exit
    for ceilingBlock in ceilingBlocks:
        ceilingBlock.draw(window)
    # in levels 3 and 4, wait for the player to get scorePoints, then draw enemies
    if 2 < level < 5 and not scores:
        for enemy in enemies:
            enemy.draw(window)
    # level 5 and later draw enemies straight away
    if level > 4:
        for enemy in enemies:
            enemy.draw(window)
    # draw bosses after player has a gun; after all scorePointsare collected
    if not scores:
        for boss in bosses:
            boss.draw(window)

    if speedTimer != 0:
        window.blit(lightningBolt, (10, 20))

    if invincibilityTimer != 0:
        window.blit(infinity, (60, 20))

    # creating lives and level count to display in bottom right corner
    textLevel = font1.render("Level: " + str(level), 1, RED)
    textScore = font1.render("Score: " + str(Score), 1, RED)
    if playerInv:
        textLives = font1.render("Lives: *", 1, RED)
    else:
        textLives = font1.render("Lives: " + str(lives), 1, RED)
    # adjust bullet count colour depending on how many bullets are left
    if magLeft > 3:
        bulletColour = BLACK
    else:
        bulletColour = RED
    # create ammo count
    textMagLeft = font4.render("AMMO: " + str(magLeft), 1, bulletColour)

    # blit text to bottom right corner
    window.blit(textLevel, (620, 620))
    window.blit(textLives, (620, 640))
    window.blit(textScore, (620, 660))
    # if the player has a gun blit bullet count to bottom left corner
    if level > 1 and not scores:
        window.blit(textMagLeft, (10, 660))

    # if timed mode active, blit time left to top left corner
    if timed:
        if timeLeft > 360:
            textTime = font4.render(str(int(timeLeft/60)), 1, BLACK)
        else:
            textTime = font4.render(str(int(timeLeft/60)), 1, RED)
        window.blit(textTime, (660, 30))

    # refresh display
    pygame.display.update()

# what happens when player's life count hit zero


def gameOver():
    global highscore
    global highlevel
    global level
    global Score

    # screen goes black
    window.fill(BLACK)
    # game over, level reached and final score are displayed
    textOver = font2.render("GAME OVER", 1, RED)

    if Score > highscore:
        highscore = Score
        FINALSCORE = "NEW HIGHSCORE: " + str(Score)
        dir = path.dirname(__file__)
        with open(path.join(dir, HSfile), 'r+') as f:
            f.write(str(Score))
    else:
        FINALSCORE = "Final Score: " + str(Score)

    if level > highlevel:
        highlevel = level
        FINALLEVEL = "NEW MAX LEVEL: " + str(level)
        dir = path.dirname(__file__)
        with open(path.join(dir, HLfile), 'r+') as f:
            f.write(str(Score))

    else:
        FINALLEVEL = "Level Reached: " + str(level)

    textFinalScore = font4.render(FINALSCORE, 1, WHITE)
    textLevelReached = font4.render(FINALLEVEL, 1, WHITE)

    window.blit(textOver, (150, windowWidth/2))
    window.blit(textFinalScore, ((windowWidth/2), 420))
    window.blit(textLevelReached, (235, 455))

    pygame.display.update()

    delay(20)

    reset()
    gameIntro()

# reads the highscores from a local textfile


def loadData():
    # make highscore and highest level global so they can be changed and used by other parts of the program
    global highscore
    global highlevel

    # set path to file
    dir = path.dirname(__file__)

    # open the file in read and write mode
    with open(path.join(dir, HSfile), 'r+') as f:
        # try to read the data in file
        try:
            highscore = int(f.read())
        # if no data in file, the above line returns an error, so instead highscore is set to zero.
        except:
            highscore = 0

    # same process as above but for highest level reached
    with open(path.join(dir, HLfile), 'r+') as f:
        try:
            highlevel = int(f.read())
        except:
            highlevel = 0

# save the level that a player got to so they can resume


def saveGame():
    global lives
    global level
    global Score
    global timed
    global timeLeft

    #playerState = [lives, level, Score]
    #gameState = [boats, speeds, invincibles, nukes, skips, starts, healths, scores, bullets, enemies, bosses, ceilingBlocks]

    shelfFile = shelve.open('savedgame')

    shelfFile['livesVariable'] = lives
    shelfFile['levelVariable'] = level
    shelfFile['scoreVariable'] = Score
    shelfFile['timedVariable'] = timed
    shelfFile['timedLeftVariable'] = timeLeft

    shelfFile.close()

# resume the game from the level that a player saved


def loadGame():
    global lives
    global level
    global Score
    global timed
    global timeLeft

    shelfFile = shelve.open('savedgame')

    lives = shelfFile['livesVariable']
    level = shelfFile['levelVariable']
    Score = shelfFile['scoreVariable']
    timed = shelfFile['timedVariable']
    timeLeft = shelfFile['timedLeftVariable']

    shelfFile.close()

    createNextLevel()
    gameLoop()

# reset values of player for a new game


def reset():
    global lives
    global level
    global Score

    # reset players speed
    player.vel = 3.5

    lives = 3
    level = 1
    Score = 0

# called to start the game


def gameIntro():

    global mute
    global timed
    global highscore
    global highlevel

    intro = True

    loadData()

    # intro loop
    while intro:

        # draw background
        window.blit(introBackground, (0, 0))

        # create all the buttons
        normalMode = classes.button(GREEN, 100, 350, 220, 100, "NEW GAME")
        resumePrevious = classes.button(
            PURPLE, 400, 350, 220, 100, "SAVED GAME")
        timedMode = classes.button(ORANGE, 100, 500, 220, 100, "TIMED MODE")
        quitButton = classes.button(RED, 400, 500, 220, 100, "QUIT")
        muteButton = classes.button(BLUE, 615, 10, 75, 50, "MUTE")

        # define a tuple that represents mouse postion
        pos = pygame.mouse.get_pos()

        # if mouse is over a button, change the colour of the button to indicate that it can be pressed
        # draw the buttons selected colour
        if normalMode.isOver(pos):
            normalMode.colour = STARTGREEN
        normalMode.draw(window)

        if timedMode.isOver(pos):
            timedMode.colour = PRESSORANGE
        timedMode.draw(window)

        if quitButton.isOver(pos):
            quitButton.colour = QUITRED
        quitButton.draw(window)

        if resumePrevious.isOver(pos):
            resumePrevious.colour = PRESSPURPLE
        resumePrevious.draw(window)

        # if mute already, mute button is yellow, if not mute, mute button is blue
        # button changes shade when mouse is over it
        if mute:
            if muteButton.isOver(pos):
                muteButton.colour = MUTEYELLOW
            else:
                muteButton.colour = YELLOW
        else:
            if muteButton.isOver(pos):
                muteButton.colour = MUTEBLUE
            else:
                muteButton.colour = BLUE

        muteButton.draw(window)

        for event in pygame.event.get():
            # close window if user quits
            if event.type == pygame.QUIT:
                pygame.quit()

            # if the mouse button is pressed, we check where it was pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse was over a button, the action of that button is carried out
                if normalMode.isOver(pos):
                    intro = False
                    timed = False
                    levelOne()

                if timedMode.isOver(pos):
                    intro = False
                    timed = True
                    levelOne()

                if resumePrevious.isOver(pos):
                    intro = False
                    loadGame()

                if quitButton.isOver(pos):
                    pygame.quit()

                if muteButton.isOver(pos):
                    music()

        keys = pygame.key.get_pressed()

        # player can also use keyboard shortcuts
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        if keys[pygame.K_RETURN]:
            intro = False
            levelOne()

        if keys[pygame.K_m]:
            music()

        if keys[pygame.K_l]:
            loadGame()

        pygame.time.delay(15)

        # display game title for the duration of the intro
        title = font2.render("BOAT WAR", 1, WHITE)
        HIGHSCORE = font4.render("Highscore: " + str(highscore), 1, RED)
        HIGHLEVEL = font4.render("Max Level: " + str(highlevel), 1, RED)

        window.blit(title, (175, 150))
        window.blit(HIGHSCORE, (250, 230))
        window.blit(HIGHLEVEL, (250, 270))

        pygame.display.update()

# will be called during the game loop - interupts the game, which can be carried on when you resume


def pause():
    pause = True
    global mute

    # loop runs whilst game is paused
    while pause:

        window.fill(BLACK)
        # draw pause background
        window.blit(pauseBackground, (0, 0))

        # create buttons
        resumeButton = classes.button(GREEN, 100, 350, 220, 100, "RESUME")
        mainMenuButton = classes.button(
            ORANGE, 400, 350, 220, 100, "MAIN MENU")
        saveButton = classes.button(PURPLE, 100, 500, 220, 100, "SAVE GAME")
        quitButton = classes.button(RED, 400, 500, 220, 100, "QUIT")
        muteButton = classes.button(BLUE, 615, 10, 75, 50, "MUTE")

        # mouse position tuple
        pos = pygame.mouse.get_pos()

        # change shade of buttons to indicate that the mouse is over them
        if resumeButton.isOver(pos):
            resumeButton.colour = STARTGREEN
        resumeButton.draw(window)

        if mainMenuButton.isOver(pos):
            mainMenuButton.colour = PRESSORANGE
        mainMenuButton.draw(window)

        if saveButton.isOver(pos):
            saveButton.colour = PRESSPURPLE
        saveButton.draw(window)

        if quitButton.isOver(pos):
            quitButton.colour = QUITRED
        quitButton.draw(window)

        # mute from main menu can also be controlled from here
        if mute:
            if muteButton.isOver(pos):
                muteButton.colour = MUTEYELLOW
            else:
                muteButton.colour = YELLOW
        else:
            if muteButton.isOver(pos):
                muteButton.colour = MUTEBLUE
            else:
                muteButton.colour = BLUE

        muteButton.draw(window)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            # checking if a button is pressed and putting the action into effect
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resumeButton.isOver(pos):
                    pause = False

                if quitButton.isOver(pos):
                    pygame.quit()

                if muteButton.isOver(pos):
                    mute != mute
                    music()

                # allow player to go back to main menu
                if mainMenuButton.isOver(pos):
                    pause = False
                    reset()
                    gameIntro()

                if saveButton.isOver(pos):
                    saveGame()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        if keys[pygame.K_RETURN]:
            pause = False

        if keys[pygame.K_s]:
            saveGame()

        pygame.time.delay(15)
        # write paused on screen
        enterToResume = font2.render("PAUSED", 1, WHITE)
        window.blit(enterToResume, (220, 200))
        pygame.display.update()

# called when player presses play


def gameLoop():

    # define all the global variables
    global level
    global lives
    global Score
    global timed
    global timeLeft
    global timeLimit
    global rep
    global magLeft
    global shootCooldown
    global speedTimer
    global invincibilityTimer
    global playerInv

    run = True

    # indicates whether or not player is invincible at given time
    playerInv = False

    # start is the amount of time that has passed since the player has picked up a power up
    speedTimer = 0
    invincibilityTimer = 0

    # loop cycles through whilst the game is being played
    while run:
        # run at sixty frames per second
        clock.tick(60)

        # pass variable allows player to go forward if true - prevents them from getting through the wall
        Pass = True
        # prevents on bullet from colliding with two enemies or bosses
        bulletDestroyed = False
        # prevents one boat from colliding with two bosses
        boatDestroyed = False

        # draw background
        window.blit(background, (0, 0))

        # if player has no lives left
        if lives == 0:
            # breaks out of game loop
            gameOver()

        # ends game if time runs out
        if timed:
            if timeLeft < 1:
                run = False
                gameOver()
            timeLeft -= 1

        # sets the amount of time between the firing of consecutive bullets
        if shootCooldown > 0:
            shootCooldown += 1
            if shootCooldown > 20:
                shootCooldown = 0

        # causes game to end if 'X' is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # checks for collisions between player and boat obstacles
        for boat in boats:
            # checks if player and boat y values overlap
            if player.y <= boat.y <= player.y + player.height or boat.y <= player.y <= boat.y + boat.height:
                # checks if player and boat x values overlap
                if player.x <= boat.x <= player.x + player.width or boat.x <= player.x <= boat.x + boat.width:
                    # call player's hit method to reset player
                    player.hit()

            # checks for collisions between boss and boats
            for boss in bosses:
                if boss.y <= boat.y <= boss.y + boss.height or boat.y <= boss.y <= boat.y + boat.height:
                    if boss.x <= boat.x <= boss.x + boss.width or boat.x <= boss.x <= boat.x + boat.width:
                        if not boatDestroyed:
                            # remove boat from list
                            boats.pop(boats.index(boat))
                            # prevent two collisions from happening with the same boat
                            # so the game doesn't try to remove the same boat twice and give an error
                            boatDestroyed = True

        # checks for collisions between boss and player
        for boss in bosses:
            if boss.y <= player.y <= boss.y + boss.height or player.y <= boss.y <= player.y + player.height:
                if boss.x <= player.x <= boss.x + boss.width or player.x <= boss.x <= player.x + player.width:
                    player.hit()

        # checks for collisions between player and health points
        for health in healths:
            if player.y <= health.y <= player.y + player.height or health.y <= player.y <= health.y + health.height:
                if player.x <= health.x <= player.x + player.width or health.x <= player.x <= health.x + health.width:
                    # remove health point from list
                    healths.remove(health)
                    # increase player lives
                    lives += 1

        # checks for collisions between player and score points
        for score in scores:
            if player.y <= score.y <= player.y + player.height or score.y <= player.y <= score.y + score.height:
                if player.x <= score.x <= player.x + player.width or score.x <= player.x <= score.x + score.width:
                    # play money sound effect
                    moneySound.play()
                    # remove score from list
                    scores.remove(score)
                    # increase score
                    Score += 1

        # check for a collision between the player and the speed power up
        for speed in speeds:
            if speed.y - speed.radius < player.y + player.height and speed.y + speed.radius > player.y:
                if speed.x - speed.radius < player.x + player.width and speed.x + speed.radius > player.x:
                    # if a speed power up is not already in effect the player can pick one up
                    if speedTimer == 0:
                        # speed power up is removed when picked up
                        speeds.remove(speed)
                        # players velocity is increased by 35%
                        player.vel = player.vel * 1.35
                        # timer is started to time the effect of the power up
                        speedTimer = dt.now()

        # if a power up has been picked up, the timer is running so not zero
        if speedTimer != 0:
            # seconds is how long it has been since the player picked up the power up
            seconds = (dt.now() - speedTimer).total_seconds()
            # once the power up has been in effect for 10 seconds, the player's speed is returned to normal
            if seconds >= 10:
                player.vel = player.vel / 1.35
                # start is set to zero so the player's speed won't be decreased again unless another power up is picked up
                speedTimer = 0

        # check for a collision between the player and the invincible power up
        for invincible in invincibles:
            if invincible.y - invincible.radius < player.y + player.height and invincible.y + invincible.radius > player.y:
                if invincible.x - invincible.radius < player.x + player.width and invincible.x + invincible.radius > player.x:
                    # if the power up is not already in effect the player can pick one up
                    if invincibilityTimer == 0:
                        # power up is removed when pick up
                        invincibles.remove(invincible)
                        # make player invincible
                        playerInv = True
                        # start timer on invincibility
                        invincibilityTimer = dt.now()

        # if a power up has been picked up, the timer is running so not zero
        if invincibilityTimer != 0:
            # seconds is how long it has been since the player picked up the power up
            seconds = (dt.now() - invincibilityTimer).total_seconds()
            # once the power up has been in effect for 10 seconds, the player's speed is returned to normal
            if seconds >= 15:
                playerInv = False
                # start is set to zero so the player's speed won't be decreased again unless another power up is picked up
                invincibilityTimer = 0

        # check for a collision between the player and the nuke power up
        for nuke in nukes:
            if nuke.y - nuke.radius < player.y + player.height and nuke.y + nuke.radius > player.y:
                if nuke.x - nuke.radius < player.x + player.width and nuke.x + nuke.radius > player.x:
                    # power up is removed when pick up
                    nukes.remove(nuke)
                    boats.clear()
                    bullets.clear()
                    ceilingBlocks.clear()
                    enemies.clear()
                    bosses.clear()
                    explosionSound.play()
                    window.blit(explosion, (0, 0))
                    pygame.display.update()
                    delay(10)

        # check for a collision between the player and the skip power up
        for skip in skips:
            if skip.y - skip.radius < player.y + player.height and skip.y + skip.radius > player.y:
                if skip.x - skip.radius < player.x + player.width and skip.x + skip.radius > player.x:
                    # power up is removed when pick up
                    skips.remove(skip)
                    level += 1
                    createNextLevel()

        # checks for collisions between ceiling and player, and stops the player from passing if there is
        for ceilingBlock in ceilingBlocks:
            if player.y <= ceilingBlock.height:
                if ceilingBlock.x <= player.x <= ceilingBlock.x + ceilingBlock.width or ceilingBlock.x <= player.x + player.width <= ceilingBlock.x + ceilingBlock.width:
                    # stops player from passing to next level
                    Pass = False
            else:
                Pass = True

        # if its level 1 a door opens up in the wall allowing player to pass through to the next level
        # rep prevents this from being repeated every frame
        if level == 1 and rep == True and not scores:
            ceilingBlocks.remove(ceilingBlocks[8])
            ceilingBlocks.remove(ceilingBlocks[8])
            rep = False

        # checks for all collisions between bullets and everything else
        for bullet in bullets:
            # checks if bullet is still on screen
            if bullet.y > 0:
                # moves bullet forward
                bullet.y -= bullet.vel
            else:
                # removes bullet from list
                bullets.remove(bullet)

            # checks for collisions between bullets and boats
            for boat in boats:
                if bullet.y <= boat.y <= bullet.y + bullet.height or boat.y <= bullet.y <= boat.y + boat.height:
                    if bullet.x <= boat.x <= bullet.x + bullet.width or boat.x <= bullet.x <= boat.x + boat.width:
                        # increment score
                        Score += 1
                        # remove both boat and bullets from lists
                        boats.remove(boat)
                        bullets.remove(bullet)

            # collisions between ceiling and bullets
            for ceilingBlock in ceilingBlocks:
                if bullet.y <= ceilingBlock.y <= bullet.y + bullet.height or ceilingBlock.y <= bullet.y <= ceilingBlock.y + ceilingBlock.height:
                    if bullet.x <= ceilingBlock.x <= bullet.x + bullet.width or ceilingBlock.x <= bullet.x <= ceilingBlock.x + ceilingBlock.width:
                        # increment score
                        Score += 1
                        # remove ceiling block and bullet from lists
                        ceilingBlocks.remove(ceilingBlock)
                        bullets.remove(bullet)

            # collisions between enemies and bullets
            for enemy in enemies:
                if bullet.y <= enemy.y <= bullet.y + bullet.height or enemy.y <= bullet.y <= enemy.y + enemy.height:
                    if bullet.x <= enemy.x <= bullet.x + bullet.width or enemy.x <= bullet.x <= enemy.x + enemy.width:
                        Score += 1
                        # make sure that the same bullets does not collide with multiple enemies to prevent error
                        if not bulletDestroyed:
                            # remove enemy and bullet from lists
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                            bulletDestroyed = True

            # collisions between boss and bullet
            for boss in bosses:
                if bullet.y <= boss.y <= bullet.y + bullet.height or boss.y <= bullet.y <= boss.y + boss.height:
                    if bullet.x <= boss.x <= bullet.x + bullet.width or boss.x <= bullet.x <= boss.x + boss.width:
                        # increase score by 5
                        Score += 5
                        # make sure same bullet does not collide with two bosses
                        if not bulletDestroyed:
                            # remove bullet from list
                            bullets.remove(bullet)
                            bulletDestroyed = True
                            # decrease boss life
                            if boss.lives > 1:
                                # if lives left, take 1 life away from boss
                                boss.lives -= 1
                            else:
                                # if no lives, remove boss from list; kill boss
                                bosses.remove(boss)

        # collisions between enemies and player
        for enemy in enemies:
            if player.y <= enemy.y <= player.y + player.height or enemy.y <= player.y <= enemy.y + enemy.height:
                if player.x <= enemy.x <= player.x + player.width or enemy.x <= player.x <= enemy.x + enemy.width:
                    # player is hit, decrease lives
                    player.hit()
                    enemies.remove(enemy)

            # collisions between enemy and boats
            for boat in boats:
                if enemy.y <= boat.y <= enemy.y + enemy.height or boat.y <= enemy.y <= boat.y + boat.height:
                    if enemy.x <= boat.x <= enemy.x + enemy.width or boat.x <= enemy.x <= boat.x + boat.width:
                        # remove boat from list
                        boats.remove(boat)

        # telling pygame what to do when a key is pressed - allows character to move continuosly whilst key is being pressed.
        keys = pygame.key.get_pressed()
        # esc to quit
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        # p to pause
        if keys[pygame.K_p]:
            pause()
        # space to shoot, if the player has a gun and bullets haven't run out, and gun isn't cooling down
        if keys[pygame.K_SPACE] and shootCooldown == 0 and level > 1 and not scores and magLeft > 0:
            # play bullet shooting sound effect
            bulletSound.play()
            # add bullet to list
            bullets.append(classes.projectile(player.x + 5, player.y, 15, 40))
            # start cooldown cycle
            shootCooldown = 1
            # decrease bullets left in magazine
            magLeft -= 1

        # give the user control of the player and prevent player from leaving the screen through the bottom or the sides
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player.vel
        if keys[pygame.K_RIGHT] and player.x < windowWidth - player.width:
            player.x += player.vel
        if keys[pygame.K_DOWN] and player.y < windowWidth - player.height:
            player.y += player.vel
        # only allow the player to pass if pass is true, so if there is no wall
        if keys[pygame.K_UP] and player.y > 0 and Pass == True:
            player.y -= player.vel
        # when player reaches the end, moves onto next level
        if player.y <= 0:
            level += 1
            if timed:
                timeLeft = timeLimit
            createNextLevel()

        # draw the game window at the end of each frame
        drawGameWindow()

    # end game
    pygame.quit()
