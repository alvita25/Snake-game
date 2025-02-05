import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

# initialize game window
screen_width=500
screen_height=600
gameWindow=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Snake game')
pygame.display.update()

# background image
bgimg=pygame.image.load("background.jpg")
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

food_sound = pygame.mixer.Sound("food.mp3")  # Load food eating sound

clock=pygame.time.Clock()
font=pygame.font.SysFont(None,35)

# function to display text
def display_score(text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

# function to draw snake
def plot_snake(Window,color,snake_list,size):
    for x,y in snake_list:
        pygame.draw.rect(Window,color,[x,y,size,size])

# welcome function
def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.fill(white)
        display_score("Welcome to snakes",black,140,250)
        display_score("Press space to play",black,140,280)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("background.mp3")
                    pygame.mixer.music.play(-1)

                    gameLoop()

        pygame.display.update()
        clock.tick(60)
        

# game loop function
def gameLoop():
    # game specific variables
    exit_game=False
    game_over=False
    snake_x=55
    snake_y=65
    velocity_x=0
    velocity_y=0
    snake_size=20
    fps=30
    score=0
    init_velocity=5

    # get random coordinames of food
    food_x=random.randint(20,screen_width-20)
    food_y=random.randint(20,screen_height-20)
    food_size=20
    snake_list=[]
    snake_length=1

    # create highscore file if it does not exist
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt","w") as f:
            f.write("0")
    # read highScore
    with open("high_score.txt","r") as f:
        highScore=f.read()

    # game loop 
    while not exit_game:
        if game_over:
            # write highScore into the file 
            with open("high_score.txt","w") as f:
                f.write(str(highScore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0)) # display background img

            display_score("Game over...Press Enter to play again",red,10,screen_height/2)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN: # start new game
                        pygame.mixer.music.load("background.mp3")
                        pygame.mixer.music.play(-1)
                        gameLoop()

        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True

                
                # check pressed key 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
                    # cheat code
                    if event.key == pygame.K_q: # press 'q' to increase score
                        score+=5
            # eat food
            if abs(snake_x-food_x)<20 and abs(snake_y-food_y)<20:
                food_sound.play()

                score+=10
                # random food coordinates
                food_x=random.randint(20,screen_width-20)
                food_y=random.randint(20,screen_height-20)
                while [food_x,food_y] in snake_list[:-1]:
                    food_x=random.randint(20,screen_width-20)
                    food_y=random.randint(20,screen_height-20)
                snake_length+=5 # increase length of snake
                if score>int(highScore): # check highscore
                    highScore=score

            # move snake            
            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            # display game window
            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            display_score("Score: "+str(score) +"  Highscore: "+str(highScore),red,5,5)

            # make list of new snake coordinates and append it to list
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            # delete tail of snake 
            if len(snake_list)>snake_length:
                del(snake_list[0])

            # check if head of snake collides with its body 
            if head in snake_list[:-1]:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                game_over=True

            # check if snake goes out of game window 
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load("crash.mp3")
                pygame.mixer.music.play()
                game_over=True
                

            plot_snake(gameWindow,black,snake_list,snake_size) # draw snake
            pygame.draw.rect(gameWindow,red,[food_x,food_y,food_size,food_size]) # draw food
        pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()

welcome()