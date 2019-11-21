# import all necessary modules
import pygame
import math
# import my functions file
import functions as fn

# initialise pygame module
pygame.init()

# define colours I will need through RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# define dimensions of the screen
windowWidth = 700
windowSize = (windowWidth, windowWidth)

# create the window
window = pygame.display.set_mode(windowSize)

# define fonts I will need
font1 = pygame.font.SysFont("comicsans", 25)
font2 = pygame.font.SysFont("comicsans", 100)
font3 = pygame.font.SysFont("comicsans", 70)
font4 = pygame.font.SysFont("comicsans", 45)

# import sound effect
hitSound = pygame.mixer.Sound('hit.wav')

# import all the images I will to draw my objects/sprites
mainBoat = pygame.image.load("mainboat.png")
sailBoat = pygame.image.load("sailboat.png")
torpedo = pygame.image.load("torpedo.png")
treasure = pygame.image.load("treasure.png")
bulletFire = pygame.image.load("bullet.png")
fence = pygame.image.load("fence.png")
heart = pygame.image.load("heart.png")
kraken = pygame.image.load("kraken.png")
lightning = pygame.image.load("lightning.png")
star = pygame.image.load("star.png")
nuke = pygame.image.load("nuke.png")
skip = pygame.image.load("skip.png")

# scale, flip, and rotate all the images to the correct format
mainBoat = pygame.transform.scale(mainBoat, (25, 50))
sailBoatRight = pygame.transform.scale(sailBoat, (40, 20))
sailBoatLeft = pygame.transform.flip(sailBoatRight, True, False)
torpedo = pygame.transform.scale(torpedo, (15, 40))
treasure = pygame.transform.scale(treasure, (28, 28))
bulletFire = pygame.transform.rotate(bulletFire, 270)
bulletFire = pygame.transform.scale(bulletFire, (15, 40))
fence = pygame.transform.scale(fence, (40, 20))
heart = pygame.transform.scale(heart, (30, 30))
kraken = pygame.transform.scale(kraken, (150, 150))
lightning = pygame.transform.scale(lightning, (30, 30))
star = pygame.transform.scale(star, (40, 40))
nuke = pygame.transform.scale(nuke, (40, 40))
skip = pygame.transform.scale(skip, (40, 40))

# initialise boolean that determines which way the sailBoat obstacles are facing
sailRight = True

# create the character super class
class Character(object):
    def __init__(self, x, y, width, height):
        # these parameters are set during instantiation
        self.x = x
        self.y = y
        self.width = width
        self.height = height

# create boat sub class, from character class


class Player(Character):
    def __init__(self, x, y, width, height):
        # inherit attributes of character class
        super(). __init__(x, y, width, height)
        # set the player's speed - this is how many pixels the player can move by per frame
        # player's speed will incrementaly increase each round until level 20
        if fn.level < 20:
            self.vel = 3 * (1.05 ** fn.level)
        else:
            self.vel = 3 * (1.05 ** 20)

        # initial coordinates of player
        self.xInit = 337
        self.yInit = 650
        # other attributes
        self.image = mainBoat

    # draw boat
    def draw(self, window):
        # blit the image of the boat to the size and the coordinates of the player
        window.blit(self.image, (self.x, self.y))

    # this method is called when the player is hit
    def hit(self):
        # play a sound effect that indicates that the player has been hit
        hitSound.play()
        # if player is not invinsible
        if not fn.playerInv:
            # decrease player's life count by 1
            fn.lives = fn.lives - 1
            # render a '-1' onto the  screen to indicate that the player has lost a life
            textMinus = font2.render("-1", 1, RED)
            window.blit(textMinus, (windowWidth/2, windowWidth/2))
            # update the display to show all of the changes
            pygame.display.update()
            # delay of a second to give the user a chance to see the text on the screen
            fn.delay(10)
        # reset the player to its original position
        self.x = self.xInit
        self.y = self.yInit

# create obstacles sub class, from character class


class obstacles(Character):
    def __init__(self, x, y, width, height, end):
        # inherit attributes of character class
        super(). __init__(x, y, width, height)
        # define end value where obstacles must switch direction
        self.end = end
        self.path = [self.x, self.end]
        # define the obstacles starting speed
        self.vel = 1
        # multiplication by this will cause the obstacles to switch direction
        self.direction = -1

        # increase the speed of the obstacles
        if fn.level < 10:
            self.vel = 1.15 ** fn.level
        else:
            self.vel = (1.15 ** 9) * (1.05 ** (fn.level - 9))

    # draw the obstacle
    def draw(self, window):
        # call move function so the obstacles will always move once inbetween getting drawn
        self.move()
        # draw the image facing right or left depending on which direction the obstacle is heading in
        if sailRight == True:
            # set right facing image as self.image
            self.image = sailBoatRight
        else:
            # set left facing image as self.image
            self.image = sailBoatLeft

        # blit image to obstacle's coordinates
        window.blit(self.image, (self.x, self.y))

    # move function defines how the obstacle will move in each frame
    def move(self):
        # global boolean that indicates which way the obstacle is heading
        global sailRight
        # if vel is positive the obstacle is heading to the right
        if self.vel > 0:
            # set bool to true so image is drawn facing right
            sailRight = True
            # if the is still space to the right, move the obstacle to the right
            if self.x <= self.path[1]:
                # move by incrementing the x value by vel
                self.x += self.vel
            else:
                # if there is no more space, multiply vel by direction to change the obstacle's direction
                self.vel = self.vel * self.direction
        # if vel is negative, the object is heading to the left
        else:
            # set bool to false so image is drawn facing left
            sailRight = False
            # same movement mechanics as before, but facing left
            if self.x > 0:
                self.x += self.vel
            else:
                self.vel = self.vel * self.direction

# create chasers sub class, from character class


class chasers(Character):
    def __init__(self, x, y, width, height):
        # inherit attributes of character class
        super(). __init__(x, y, width, height)
        # velocity defined, set to increase as the levels increase
        if fn.level < 15:
            self.vel = 1.5 * (1.05 ** (fn.level - 2))
        else:
            self.vel = 1.5 * (1.05 ** 13)

    def draw(self, window):
        self.move()
        # define the torpedo by rotating the image by the correct angle so that it always faces the player
        torpedoFace = pygame.transform.rotate(torpedo, angle)
        # blit torpedo to the correct coordinates
        window.blit(torpedoFace, (self.x, self.y))

    def move(self):
        # global variable that holds the angle that the torpedo needs to face in order to face the player
        global angle

        # algorithm to track and chase the player
        # if the player is to the left of the torpedo;
        # use round function to find the centre of the player and the torpedo
        if round(player.x + player.width // 2) < round(self.x + self.width // 2):
            # the torpedo moves left
            self.x -= self.vel
            diffX = self.x - player.x
        else:
            # else the torpedo moves right
            self.x += self.vel
            diffX = player.x - self.x

        # if the player is above the torpedo;
        if round(player.y + player.height // 2) < round(self.y + self.height // 2):
            # the torpedo moves up
            self.y -= self.vel
            diffY = self.y - player.y
        else:
            # else the torpedo moves down
            self.y += self.vel
            diffY = player.y - self.y

        # diffX and diffY are the differences between the x and y values of the player and the torpedo
        # algorithm to work out the angle that the torpedo needs to be rotated through to face the player
        # use arctan function from math module to work out the angle of the player from the torpedo, depending on which quadrant the player is in
        if player.x < self.x and player.y < self.y:
            angle = 90 - math.degrees(math.atan(diffY/diffX))
        elif player.x < self.x and player.y > self.y:
            angle = 90 + math.degrees(math.atan(diffY/diffX))
        elif player.x > self.x and player.y < self.y:
            angle = 270 + math.degrees(math.atan(diffY/diffX))
        elif player.x > self.x and player.y > self.y:
            angle = 270 - math.degrees(math.atan(diffY/diffX))

# create bigBoss sub class, from character class


class bigBoss(Character):
    def __init__(self, x, y, width, height):
        # inherit attributes of character class
        super(). __init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # define bosses speed
        self.vel = 1.5
        # give boss multiple lives
        self.lives = 5

    def draw(self, window):
        self.move()
        # blit the image of the kraken onto the boss's position
        window.blit(kraken, (self.x, self.y))
        # create a health bar
        # draw a green bar on top of a red bar, and make the green bar smaller to reveal the red bar every time the boss losses a life
        pygame.draw.rect(window, RED, ((self.x + 30), (self.y - 10), 100, 15))
        pygame.draw.rect(window, GREEN, ((self.x + 30),
                                         (self.y - 10), (self.lives*20), 15))

    def move(self):
        # algorithm to make the boss track and chase the player
        if round(player.x + player.width // 2) < round(self.x + self.width // 2):
            self.x -= self.vel
        else:
            self.x += self.vel
        if round(player.y + player.height // 2) < round(self.y + self.height // 2):
            self.y -= self.vel
        else:
            self.y += self.vel

# powerup super class


class Powerup(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

# construct class for lives


class healthPoints(Powerup):
    def __init__(self, x, y):
        # inherit from powerup
        super(). __init__(x, y)
        # set size for collisions
        self.width = 29
        self.height = 29

    def draw(self, window):
        # blit image of a heart onto coordinates
        window.blit(heart, (self.x, self.y))

# construct class for treasure / score


class scorePoints(Powerup):
    def __init__(self, x, y):
        # inherit from powerup
        super(). __init__(x, y)
        # set size for collisions
        self.width = 28
        self.height = 28

    def draw(self, window):
        # blit image of treasure onto coordinates
        window.blit(treasure, (self.x, self.y))

# construct class for a powerup that will give the player increases speed for a short time


class speedUp(Powerup):
    def __init__(self, x, y):
        # inherit from powerup
        super(). __init__(x, y)
        # set size of powerup for collisions
        self.radius = 15

    def draw(self, window):
        # blit image on to specified coordinates
        window.blit(lightning, ((self.x - self.radius),
                                (self.y - self.radius)))

# construct class for a power up that will make player invincible for a short time


class invincibility(Powerup):
    def __init__(self, x, y):
        # inherit from powerup class
        super(). __init__(x, y)
        # set radius for collisions
        self.radius = 15

    def draw(self, window):
        # blit image on to coordinates
        window.blit(star, ((self.x - self.radius), (self.y - self.radius)))


class bomb(Powerup):
    def __init__(self, x, y):
        # inherit from powerup class
        super(). __init__(x, y)
        # set radius for collisions
        self.radius = 15

    def draw(self, window):
        # blit image on to coordinates
        window.blit(nuke, ((self.x - self.radius), (self.y - self.radius)))


class roundSkip(Powerup):
    def __init__(self, x, y):
        # inherit from powerup class
        super(). __init__(x, y)
        # set radius for collisions
        self.radius = 15

    def draw(self, window):
        # blit image on to coordinates
        window.blit(skip, ((self.x - self.radius), (self.y - self.radius)))

# create a class for buttons for use in the main and pause menus


class button(object):
    def __init__(self, colour, x, y, width, height, text=''):
        # attributes of the button
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):

        # button is a rectangle of set dimensions
        pygame.draw.rect(window, self.colour,
                         (self.x, self.y, self.width, self.height), 0)

        # if text is entered in the parameters, this is rendered onto the centre of button
        if self.text != '':
            text = font1.render(self.text, 1, BLACK)
            # centre and blit the text
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                               self.y + (self.height/2 - text.get_height()/2)))

    # method that returns whether the mouse is over the button at any given time
    def isOver(self, pos):
        # pos is the mouse position; tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

# create blocks that prevent player from leaving


class blocks(object):
    def __init__(self, colour, x, y):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20

    def draw(self, window):
        # blit image of fence to screen
        window.blit(fence, (self.x, self.y))

# create bullets that the player can fire


class projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # set the bullets speed
        if fn.level < 20:
            self.vel = 6 * (1.03 ** fn.level)
        else:
            self.vel = 6 * (1.03 ** 20)

    def draw(self, window):
        # blit bullet to screen
        window.blit(bulletFire, (self.x, self.y))


# instantiate player using Player class
player = Player(337, 650, 25, 50)
