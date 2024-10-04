import pygame
import math
from datetime import datetime
import random 

## Define colors ##
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

## Define radius of the watch ##
radius = 200

## Define screen size ##
width= 700
height=700

## Establish screen and center of the screen ##
screen= pygame.display.set_mode((width, height))
center= pygame.Vector2(width // 2, height // 2)

## Function to get random colors ##
def get_colors():

    ## Establish list for colors ##
    colors = []

    ## Generate 60 random colors for the 60 ticks + 1 for the background ##
    for _ in range (61):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        ## Append the colors to the list ##
        colors.append(color)

    ## Return the list of colors ##
    return colors

## Function to get the radians of the hands ##
def get_radians():

    ## Ensure we update the time ##
    time= datetime.now()

    ## Get the radians for the hands ##
    hour_radians = math.radians((time.hour + time.minute / 60) * 30-90)
    minute_radians= math.radians(time.minute * 6-90 )  
    second_radians= math.radians(time.second * 6-90)   

    ## Return the radians for each hand ##
    return hour_radians, minute_radians, second_radians 

## Function to draw the hands ##
def draw_hand(radians, length):

    ## Calculate the end position of the hands, based on centerpoint, radians and length ##
    end_pos= center + pygame.math.Vector2(math.cos(radians)* length, math.sin(radians)*length)

    ## Draw the hands##
    pygame.draw.aaline(screen, white, center, end_pos)

## Function to draw the ticks ##
def draw_ticks(colors):

    ## Loop through the 60 ticks ##
    for i in range (60):

        ## Make every 5th tick longer ##
        if i % 5 == 0:
            length = 20
        else:
            length = 10
       
        ## Get the random color of each tick ##
        color = colors[i]
        
        ## Calculate the angle for each tick ##
        angle = math.radians(i * 6 - 90)
        
        ## Calculate the start and end position of each tick ##
        start_pos = center + pygame.math.Vector2(math.cos(angle) * radius, math.sin(angle) * radius)
        end_pos = center + pygame.math.Vector2(math.cos(angle) * (radius - length), math.sin(angle) * (radius - length))
        
        ## Draw the ticks ##
        pygame.draw.aaline(screen, color, start_pos, end_pos)

## Function to draw the numbers ##
def draw_numbers(colors):

    ## Loop through the 12 numbers ##
    for i in range(1, 13):

        ## Get the random color of each number ##
        color = colors[i]

        ## Calculate the angle for each number ##
        angle = math.radians(i * 30 - 90)

        ## Render the number ##
        number = font.render(str(i), True, (color))

        ## Define the text box ##
        text_rect = number.get_rect(center=(center + pygame.math.Vector2(math.cos(angle) * (radius - 40), math.sin(angle) * (radius - 40))))
        
        ## Draw the number ##
        screen.blit(number, text_rect)

## Initialize pygame, mixer and font ##
pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans", 24)

## Get the random colors ##
colors = get_colors()

## Main loop ##
while True:

    ## Event handling ##
    for event in pygame.event.get():
        
        ## Ensure program can be quit ##
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        ## Change colors when space is pressed ##
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                colors = get_colors()

                ## Play confirmation sound for color change ##
                ## Ensures user knows colors changed even if they, by chance, did not change much ##
                sound = pygame.mixer.Sound('sound.mp3')
                pygame.mixer.Sound.play(sound)

    ## Draw the constant elements ##
    pygame.Surface.fill(screen, colors[60])
    watch_edge = pygame.draw.circle(screen, (white), (center), radius + 2)
    watch_face= pygame.draw.circle(screen, (black), (center), radius)
    ticks = draw_ticks(colors)
    numbers = draw_numbers(colors)

    ## Draw watch hands ##
    hour_radians, minute_radians, second_radians = get_radians()
    draw_hand(hour_radians, radius * 0.65)
    draw_hand(minute_radians, radius * 0.80)
    draw_hand(second_radians, radius * 0.90)

    ## Ensure screen gets updated ##
    pygame.display.flip()