import math, pygame, sys, os, numpy, random, time
from astar import *
from decisiontree import * #My algs #Maciek

# Positions of each graveplace held in this array
# Positions 0-19 #Maciek
tombsArray = numpy.array([
                            [6, 1], [12, 1], [17, 1], [23, 1],
                            [1, 6], [6, 6], [12, 6], [17, 6], [23, 6], [28, 6],
                            [1, 11], [6, 11], [12, 11], [17, 11], [23, 11], [28, 11],
                            [1, 16], [6, 19], [23, 19], [28, 16]
                        ])

tombsArrayStopingPlaces = [
                            (4, 7, 1), (4, 13, 1), (4, 18, 1), (4, 24, 1),
                            (7, 4, 3), (9, 7, 1), (9, 13, 1), (9, 18, 1), (9, 24, 1), (7, 27, 2),
                            (12, 4, 3), (14, 7, 1), (14, 13, 1), (14, 18, 1), (14, 24, 1), (12, 27, 2),
                            (17, 4, 3), (22, 7, 1), (22, 24, 1), (17, 27, 2)
                        ]

#Beggining states of every tomb #Maciek
tombs = []
for i in range (0, 20):
    tombs.append([random.randint(0,2), random.randint(0,0), random.randint(0,3)])

tombs[0] = [5, 5, 7]

# Constants
clock = pygame.time.Clock()     #clock for FPS
block = 32                      # constant for moving and grid
# Character
posX = 4
posY = 4
posZ = 1                        #Rotation
left = False
right = False
up = False
down = False
start = False
walkCount = 0
moves = []
where = 'S'
positionX = posX * block
positionY = posY * block


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

# Loading Textures
#Pozmieniałem zgodnie z zasadą 0 - najgorsze, max - najlepsze
walkRight = [pygame.image.load(os.path.join('img', 'wr1.png')), pygame.image.load(os.path.join('img', 'wr2.png')), pygame.image.load(os.path.join('img', 'wr3.png'))]
walkLeft = [pygame.image.load(os.path.join('img', 'wl1.png')), pygame.image.load(os.path.join('img', 'wl2.png')), pygame.image.load(os.path.join('img', 'wl3.png'))]
walkUp = [pygame.image.load(os.path.join('img', 'wu1.png')), pygame.image.load(os.path.join('img', 'wu2.png')), pygame.image.load(os.path.join('img', 'wu3.png'))]
walkDown = [pygame.image.load(os.path.join('img', 'wd1.png')), pygame.image.load(os.path.join('img', 'wd2.png')), pygame.image.load(os.path.join('img', 'wd3.png'))]
bg = pygame.image.load(os.path.join('img', 'map.png'))
tomb = [pygame.image.load(os.path.join('img', 'graveabsent.png')), pygame.image.load(os.path.join('img', 'gravedown.png')), pygame.image.load(os.path.join('img', 'grave.png')), pygame.image.load(os.path.join('img', 'graveb.png')), pygame.image.load(os.path.join('img', 'gravey.png')), pygame.image.load(os.path.join('img', 'graver.png'))]
flower = [pygame.image.load(os.path.join('img', 'f0.png')), pygame.image.load(os.path.join('img', 'f1.png')), pygame.image.load(os.path.join('img', 'f2.png')), pygame.image.load(os.path.join('img', 'f3.png')), pygame.image.load(os.path.join('img', 'f4.png')), pygame.image.load(os.path.join('img', 'f5.png'))]
torch = [pygame.image.load(os.path.join('img', 'torch0.png')), pygame.image.load(os.path.join('img', 'torch1.png')), pygame.image.load(os.path.join('img', 'torch2a.png')), pygame.image.load(os.path.join('img', 'torch2b.png')), pygame.image.load(os.path.join('img', 'torch3a.png')), pygame.image.load(os.path.join('img', 'torch3b.png')), pygame.image.load(os.path.join('img', 'torch4a.png')), pygame.image.load(os.path.join('img', 'torch4b.png'))]
screen = pygame.display.set_mode((1024,768))      # Display settings to 1024x768, it is equal to 32x24 block 32x32px each
pygame.display.set_caption("A.I. TOMB RIPPER ")     # Window title set


# parameters (position[0-19], type of tomb[0-5], type of flower [0-5], level of torch[0-7])
#Maciek:
#types of tombs: 0 - nothing, 1 - half, 2 - normal, 3-5 - coloured
#flowers: 0 - nothing, 1-5 - coloured
#torches: 0 - nothing, 1 - extinguished, 2-3 - small, 4-5 - medium, 6-7 - full
def tombsDraw(position, x, y,z):
    screen.blit(tomb[x], ((tombsArray[position, 0]+1) * block, (tombsArray[position, 1]) * block))
    screen.blit(flower[y], ((tombsArray[position, 0]) * block, (tombsArray[position, 1]+2) * block))
    if torchBlinking == -1:
        if z == 2 or z == 4 or z == 6:
            z += 1
        elif z == 3 or z == 5 or z == 7:
            z -= 1
    screen.blit(torch[z], ((tombsArray[position, 0]+2) * block, (tombsArray[position, 1] + 2) * block))

#Rysuje wszystkie groby, a nie tylko kilka #Maciek
def drewCementary():
    for i in range(0,20):
        tombsDraw(i, tombs[i][0], tombs[i][1], tombs[i][2])

#Dodane argumenty skąd dokąd idzie #Maciek
def checkFunction(orig, dest):
    global moves, end, posY, posX, posZ
    start = orig
    # ( Y , X )
    end = dest
    path = astar(maze, start, end)
    print(path)
    after = (0,0)
    for i in path:
        if i == start:
            print('Start')
            after = i
        else:
            before = after
            after = i
            if (after[0] - before[0]) > 0:
                print("DOWN")
                moves.append('D')
            elif(after[0] - before[0]) < 0:
                print("UP")
                moves.append('U')
            else:
                if (after[1] - before[1]) > 0:
                    print("Right")
                    moves.append('R')
                elif (after[1] - before[1]) < 0:
                    print("Left")
                    moves.append('L')
                else:
                    print("Obrót")
    moves.reverse()
    print(moves)
    #Po zakończeniu algorytmu przypisuje aktualne położenie na koniec ścieżki #Maciek
    posX = end[1]
    posY = end[0]
    posZ = end[2]


#setting maze grid and routing path to follow
#Pierwsza ścieżka #Maciek
checkFunction((4, 4, 1), (5, 4, 1))

# Refreshing game window
def redrawGameWidnow():

    global walkCount, where, positionX, positionY, start, end, posY, posX, posZ
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
        screen.blit(walkDown[walkCount % 3], (positionX, positionY))
    if start:
        pygame.draw.rect(screen, (255, 255, 255), (end[1]*block, end[0]*block, 32, 32))
        if where == 'S':
            where = moves.pop()
        elif where == 'U':
            screen.blit(walkUp[walkCount % 3], (positionX, positionY))
            if walkCount < 32:
                positionY += -8
                walkCount += 8
            else:
                print('Moves up')
                walkCount = 0
                if moves:
                    where = moves.pop()
                else:
                    where = 'N'
                    start = False
        elif where == 'L':
            screen.blit(walkLeft[walkCount % 3], (positionX, positionY))
            if walkCount < 32:
                positionX += -8
                walkCount += 8
            else:
                print('Moves Left')
                walkCount = 0
                if moves:
                    where = moves.pop()
                else:
                    where = 'N'
                    start = False
        elif where == 'R':
            screen.blit(walkRight[walkCount % 3], (positionX, positionY))
            if walkCount < 32:
                positionX += 8
                walkCount += 8
            else:
                print('Moves Right')
                walkCount = 0
                if moves:
                    where = moves.pop()
                else:
                    where = 'N'
                    start = False
        elif where == 'D':
            screen.blit(walkDown[walkCount % 3], (positionX, positionY))
            if walkCount < 32:
                positionY += 8
                walkCount += 8
            else:
                print('Moves Down')
                walkCount = 0
                if moves:
                    where = moves.pop()
                else:
                    where = 'N'
                    start = False

    pygame.display.update()

run = True

#Od razu po uruchomieniu zacznij chodzić #Maciek
start = True

#Używane gdy podejdzie do grobu aby go naprawić
toFill = False

gettingOlderTimer = 0
torchBlinking = 1

while run:
    clock.tick(32) # FPS

    gettingOlderTimer += 1
    if gettingOlderTimer > 8:
        torchBlinking *= -1
        gettingOlderTimer = 0
        for i in range(1,20):
            if tombs[i][0] > 0 and random.randint(0,20) == 0:
                tombs[i][0] -= 1
            if tombs[i][1] > 0 and random.randint(0,10) == 0:
                tombs[i][1] -= 1
            if tombs[i][2] > 0 and random.randint(0,5) == 0:
                tombs[i][2] -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        '''
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

        #Generowanie losowego następnego miejsca i przejście do niego #Maciek
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            randY = random.randint(4,22)
            randX = random.randint(4,27)

            while maze[randY][randX] == -1:
                randY = random.randint(4,22)
                randX = random.randint(4,27)

            checkFunction((posY, posX, posZ), (randY, randX, 1))
            where = 'S'
            start = True
        '''
    if start == False:
        if toFill != False:
            tombs[indexOfBest] = [random.randint(3,5), random.randint(1,5), 7]
            toFill = False
            time.sleep(0.1)

        tombPriorities = []
        for i in range(0,20):
            tombPriorities.append(getPriority(tombs[i]))

        maxPriority = 0
        for i in range(0,20):
            if tombPriorities[i] > maxPriority:
                maxPriority = tombPriorities[i]
        minDistance = 100
        for i in range(0,20):
            if tombPriorities[i] == maxPriority:
                print("Current position:")
                print((posY, posX, posZ))
                print("Destination:")
                print((tombsArrayStopingPlaces[i][0], tombsArrayStopingPlaces[i][1], 1))
                print("Astar distance:")
                tempDist = len(astar(maze, (posY, posX, posZ), tombsArrayStopingPlaces[i]))
                print(tempDist)
                if tempDist < minDistance and tempDist > 1:
                    minDistance = tempDist
                    indexOfBest = i

        checkFunction((posY, posX, posZ), tombsArrayStopingPlaces[indexOfBest])
        toFill = indexOfBest
        where = 'S'
        start = True


    redrawGameWidnow()
pygame.quit()

