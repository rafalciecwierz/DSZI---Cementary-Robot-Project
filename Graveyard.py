import math, pygame, sys, os, numpy
from astar import *





# Variables
block = 32  # constant for moving and grid
# Positions of each graveplace held in this array
tombsArray = numpy.array([[6, 1], [12, 1], [17, 1], [23, 1],
                         [1, 6], [6, 6], [12, 6], [17, 6], [23, 6], [28, 6],
                         [1, 11], [6, 11], [12, 11], [17, 11], [23, 11], [28, 11],
                         [1, 16], [6, 19], [23, 19], [28, 16]])

clock = pygame.time.Clock()

# Character
posX = 15
posY = 22
left = False
right = False
up = False
down = False
walkCount = 0
rawX = 4 * block
rawY = 4 * block

# Loading Textures
walkRight = [pygame.image.load(os.path.join('img', 'wr1.png')), pygame.image.load(os.path.join('img', 'wr2.png')), pygame.image.load(os.path.join('img', 'wr3.png'))]
walkLeft = [pygame.image.load(os.path.join('img', 'wl1.png')), pygame.image.load(os.path.join('img', 'wl2.png')), pygame.image.load(os.path.join('img', 'wl3.png'))]
walkUp = [pygame.image.load(os.path.join('img', 'wu1.png')), pygame.image.load(os.path.join('img', 'wu2.png')), pygame.image.load(os.path.join('img', 'wu3.png'))]
walkDown = [pygame.image.load(os.path.join('img', 'wd1.png')), pygame.image.load(os.path.join('img', 'wd2.png')), pygame.image.load(os.path.join('img', 'wd3.png'))]
bg = pygame.image.load(os.path.join('img', 'map.png'))
tomb = [pygame.image.load(os.path.join('img', 'grave.png')), pygame.image.load(os.path.join('img', 'graveb.png')), pygame.image.load(os.path.join('img', 'gravey.png')), pygame.image.load(os.path.join('img', 'graver.png')), pygame.image.load(os.path.join('img', 'gravedown.png'))]
flower = [pygame.image.load(os.path.join('img', 'f1.png')), pygame.image.load(os.path.join('img', 'f2.png')), pygame.image.load(os.path.join('img', 'f3.png')), pygame.image.load(os.path.join('img', 'f4.png')), pygame.image.load(os.path.join('img', 'f5.png'))]
torch = [pygame.image.load(os.path.join('img', 'torch1a.png')), pygame.image.load(os.path.join('img', 'torch1b.png')), pygame.image.load(os.path.join('img', 'torch2a.png')), pygame.image.load(os.path.join('img', 'torch2b.png')), pygame.image.load(os.path.join('img', 'torch3a.png')), pygame.image.load(os.path.join('img', 'torch3b.png')), pygame.image.load(os.path.join('img', 'torch4.png'))]
screen = pygame.display.set_mode((1024,768))      # Display settings to 1024x768, it is equal to 32x24 block 32x32px each
pygame.display.set_caption("A.I. TOMB RIPPER ")     # Window title set


# parameters (position, type of tomb[0-4], type of flower [0-4], level of torch[0-6])
def tombsDraw(position, x, y,z):
    screen.blit(tomb[x], ((tombsArray[position-1, 0]+1) * block, (tombsArray[position-1, 1]) * block))
    screen.blit(flower[y], ((tombsArray[position - 1, 0]) * block, (tombsArray[position - 1, 1]+2) * block))
    screen.blit(torch[z], ((tombsArray[position - 1, 0]+2) * block, (tombsArray[position - 1, 1] + 2) * block))
def drewCementary():
    tombsDraw(1,1,0,1)
    tombsDraw(2,2,1,3)
    tombsDraw(3, 3, 2, 5)
    tombsDraw(4, 4, 3, 6)
    tombsDraw(5, 0, 4, 0)
    tombsDraw(6, 2, 1, 1)
    tombsDraw(7, 4, 3, 2)
    tombsDraw(20, 2, 4, 3)

def checkFunction():
    global posY, posX
    #maze jest obrocony czyli x to y a y to x
    maze = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   #0 row
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   #1
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   #2
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],   #3
            [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1],                           #4
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #5
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #6
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #7
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #8
            [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1],                           #9
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #10
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #11
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #12
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],       #13
            [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1],                           #14
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #15
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #16
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #17
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #18
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #19
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #20
            [-1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],         #21
            [-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1],                           #22
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]   #23
    start = (posY, posX)
    end = (4, 4)
    path = astar(maze, start, end)
    before = start
    after = (0,0)
    for i in path:
        if i == start:
            print('ELDOKA')
            after = i
        else:
            before = after
            after = i
            if (after[0] - before[0]) > 0:
                print("DOWN")
            elif(after[0] - before[0]) < 0:
                print("UP")
            else:
                if (after[1] - before[1]) > 0:
                    print("Right")
                else:
                    print("Left")



checkFunction()

# Refreshing game window
def redrawGameWidnow():

    global walkCount, rawX, rawY
    screen.blit(bg, (0, 0))
    drewCementary()

    if left:
        screen.blit(walkLeft[walkCount % 3], (posX*block, posY*block))
        if walkCount < 3:
            walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount % 3], (posX * block, posY * block))
        if walkCount < 3:
            walkCount += 1
    elif up:
        screen.blit(walkUp[walkCount % 3], (posX * block, posY * block))
        if walkCount < 3:
            walkCount += 1
    elif down:
        screen.blit(walkDown[walkCount % 3], (posX * block, posY * block))
        if walkCount < 3:
            walkCount += 1
    else:
        screen.blit(walkDown[walkCount % 3], (posX * block, posY * block))


    pygame.display.update()

run = True
while run:
    clock.tick(16) # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and posY > 0:
            walkCount = 0
            posY -= 1
            left = False
            right = False
            up = True
            down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and  posY < 23:
            walkCount = 0
            posY += 1
            left = False
            right = False
            up = False
            down = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and posX < 31:
            walkCount = 0
            posX += 1
            left = False
            right = True
            up = False
            down = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and posX > 0:
            walkCount = 0
            posX -= 1
            left = True
            right = False
            up = False
            down = False

    redrawGameWidnow()
pygame.quit()

