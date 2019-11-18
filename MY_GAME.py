# import pygame and my functions file
import pygame
import functions

# initialise pygame module
pygame.init()

# main function that runs the game


def main():
    # start playing music indeffinetly
    pygame.mixer.music.play(-1)
    # call the main menu function to start the game
    functions.gameIntro()


# call the main function
main()
