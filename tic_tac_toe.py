#IMPORT LIBRARIES
import pygame
import sys
import numpy as np
import time
import random

#COLORS USED
white=(255,255,255)
black=(0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255,0)
dark = (6,2,28)

'''
We initialize a vector with 9 positions with 0, each of which represent a box on the tic-tac-toe grid going from left to
right, and from up to down. If player 1 (i.e. real person) marks a box, it will be filled with 1s. However, if is player2
(i.e. the AI bot), it will be filled with 2s.
'''
#GRID

grid = np.zeros(9)    

'''
We define a function which will be used to perform the minmax algorithm. The function will return None if the game has not
finished, 0 if it has finished in a draw, a positive value if player 1 won, and a negative one if it was the AI who was
victorious. Morever, this positive/negative values need to be scaled in order to inspect which end result is better. To do
so, the value +1(or -1) has been multiplied by the number of zeros there are at the grid +1. With this precedure, we are 
considering that victories with less moves are more valuable.
'''

def check(grid): 
    N=len([i for i, x in enumerate(grid) if x == 0])+1
    
    # HORIZTONTAL
    for i in range(3):
        if sum(grid[3*i:3*i+3]==1)==3:
            return 1*N
        elif sum(grid[3*i:3*i+3]==-1)==3:
            return -1*N
    # VERTICAL
    for i in range(3):
        if grid[i]==grid[3+i]==grid[6+i]==1:
            return 1*N
        if grid[i]==grid[3+i]==grid[6+i]==-1:
            return -1*N
    
    # DIAGONAL RIGHT
    if grid[0]==grid[4]==grid[8]==1:
        return 1*N
    if grid[0]==grid[4]==grid[8]==2:
        return -1*N
    
    # DIAGONAL LEFT
    if grid[2]==grid[4]==grid[6]==1:
        return 1*N
    if grid[2]==grid[4]==grid[6]==2:
        return -1*N
    
    # FULL GRID WITHOUT WINNER
    if 0 not in grid:
        return 0
    # KEEP GOING
    return None


'''
We define now a helper function that will be used to help with the user interfacte, which will return us the corresponding
position of the gird vector for the particular box we clicked on the tic-tac-toe game.
'''
def casella_click(pos):
    gap = d//3
    x,y = pos
    x = x-a
    y=y-a
    return x//gap+3*(y//gap)

'''
Function which will print on the screen the typical tic-tac-toe symbols 'X' and 'O', on their corresponding positions.
'''
def draw_grid(screen): 
    p1 = [i for i, x in enumerate(grid) if x == 1]
    p2 = [i for i, x in enumerate(grid) if x == 2]
    for c in p1:
        screen.blit(cross,list(reversed(positions[c])))
    for c in p2:
        screen.blit(circle,list(reversed(positions[c])))
 
'''Minmax function, which acts recursively and at the end it will return the next move for the AI'''

def minimax(maximizer,array,d):
    result = check(array)
    if result != None:  # If the game has ended with this placement we go back
        return result
    
    if maximizer:
        d += 1         #We keep track of the depth
        v = float('-inf')
        empty = [i for i, x in enumerate(array) if x == 0]  #Possible positions a move can occupy
        random.shuffle(empty)
        for spot in empty:
            array[spot] = 1
            MM = minimax(False,array,d)
            if v<MM:
                v = MM
                move = spot   
            array[spot] = 0
        if d == 1:                                        #If we backtracked till the end, we return the move
            return  move
        return v
    else:
        d += 1
        v = float('inf')
        empty = [i for i, x in enumerate(array) if x == 0]
        random.shuffle(empty)
        for spot in empty:
            array[spot] = 2
            MM=minimax(True,array,d)
            if v>MM:
                v = MM
                move = spot
            array[spot] = 0  
        if d == 1:
            return move
        return v
        
            
    
'''
We start ny defining some variables and initializing the pygame environment:
    · width = width of the display screen
    · height = height of the display  screen
    · a = number of pixel of the boder
    · d = playable screen
    · D = size of each tic-tac-toe box
    · screen = define the game window
    · game_font = define the font used
    · positions = dictionary which maps each tic-tac-toe box to each center.
    In cross and circle we load the png images used in the UI.
'''  
        
# VALUES 

pygame.init()
pygame.font.init()


width = 600
height = 600

a=50
d = height -2*a
D=d//3

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('TIC-TAC-TOE')
game_font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf',20)


positions = {0:[a,a],1:[a,a+D],2:[a,a+2*D],3:[a+D,a],4:[a+D,a+D],5:[a+D,a+2*D],6:[a+2*D,a],7:[a+2*D,a+D],8:[a+2*D,a+2*D]}

# OBJECTS
cross=pygame.image.load('cross.png')
cross=pygame.transform.scale(cross, (D,D))
circle=pygame.image.load('circle.png')
circle=pygame.transform.scale(circle, (D,D))


'''
Main loop, where the real player starts. First of all it is checked whether we want to stop the game. In case we want to play,
either the player makes its move or, if it is the AI turn, the minmax function is evaluated so that its chosen move is
calculated. Afer that the grid and the different objects are drown. If the game has ended, the grid empties and the game starts
all over again, and the first turn will be to the player that did not do the last move.
'''

jugador = True  

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0] and jugador: 
            pos=pygame.mouse.get_pos()
            number = casella_click(pos)
            if grid[number] == 0:
                grid[number] = 1
                jugador = False
        elif not jugador:
            darray = np.copy(grid)
            r=minimax(False,darray,0)
            grid[r] = 2
            jugador = True
            move = 10
            MM=0
   
    
    #DROWINGS
    
    screen.fill(dark)
    # BOXES
    pygame.draw.rect(screen,white,(a,a,d,d))
    pygame.draw.line(screen,black,(a+d//3,a),(a+d//3,a+d))
    pygame.draw.line(screen,black,(a+(d*2)//3,a),(a+(d*2)//3,a+d))
    pygame.draw.line(screen,black,(a,a+d//3),(a+d,a+d//3))
    pygame.draw.line(screen,black,(a,a+(d*2)//3),(a+d,a+(d*2)//3))
    
    # CIRCLES AND CROSS
    draw_grid(screen)
    
    
    pygame.display.update()   
    
    if check(grid) != None: #IF THE GAME HAS ENDED
        time.sleep(1)
        grid = np.zeros(9)
        array = np.zeros(9)
        move=10
        result = None