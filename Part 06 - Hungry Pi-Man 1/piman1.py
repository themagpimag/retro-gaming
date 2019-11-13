import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660

player = Actor("piman_o") # Load in the player Actor image
SPEED = 3

def draw(): # Pygame Zero draw function
    global piDots, player
    screen.blit('header', (0, 0))
    screen.blit('colourmap', (0, 80))
    piDotsLeft = 0
    for a in range(len(piDots)):
        if piDots[a].status == 0:
            piDots[a].draw()
            piDotsLeft += 1
        if piDots[a].collidepoint((player.x, player.y)):
            piDots[a].status = 1
    if piDotsLeft == 0: player.status = 2
    drawFlames()
    getPlayerImage()
    player.draw()
    if player.status == 1: screen.draw.text("GAME OVER" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)
    if player.status == 2: screen.draw.text("YOU WIN!" , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=40)

def update(): # Pygame Zero update function
    global player, moveFlamesFlag, flames
    if player.status == 0:
        if moveFlamesFlag == 4: moveFlames()
        for g in range(len(flames)):
            if flames[g].collidepoint((player.x, player.y)):
                player.status = 1
                pass
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)

def init():
    global player
    initDots()
    initFlames()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "piman_c"
        else:
            player.image = "piman_cr"
    else:
        if a != 180:
            player.image = "piman_o"
        else:
            player.image = "piman_or"
    player.angle = a

def drawFlames():
    for g in range(len(flames)):
        if flames[g].x > player.x:
            flames[g].image = "flame"+str(g+1)+"r"
        else:
            flames[g].image = "flame"+str(g+1)
        flames[g].draw()

def moveFlames():
    global moveFlamesFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveFlamesFlag = 0
    for g in range(len(flames)):
        dirs = gamemaps.getPossibleDirection(flames[g])
        if flameCollided(flames[g],g) and randint(0,3) == 0: flames[g].dir = 3
        if dirs[flames[g].dir] == 0 or randint(0,50) == 0:
            d = -1
            while d == -1:
                rd = randint(0,3)
                if dirs[rd] == 1:
                    d = rd
            flames[g].dir = d
        animate(flames[g], pos=(flames[g].x + dmoves[flames[g].dir][0]*20, flames[g].y + dmoves[flames[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveFlames)

def flagMoveFlames():
    global moveFlamesFlag
    moveFlamesFlag += 1

def flameCollided(ga,gn):
    for g in range(len(flames)):
        if flames[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global piDots
    piDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            if gamemaps.checkDotPoint(10+x*20, 10+y*20):
                piDots.append(Actor("dot",(10+x*20, 90+y*20)))
                piDots[a].status = 0
                a += 1
            y += 1
        x += 1

def initFlames():
    global flames, moveFlamesFlag
    moveFlamesFlag = 4
    flames = []
    g = 0
    while g < 4:
        flames.append(Actor("flame"+str(g+1),(270+(g*20), 370)))
        flames[g].dir = randint(0, 3)
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()
