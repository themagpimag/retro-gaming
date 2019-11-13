import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660

player = Actor("piman_o") # Load in the player Actor image
player.score = 0
player.lives = 3
level = 0
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
            if piDots[a].status == 0:
                if piDots[a].type == 2:
                    for g in range(len(flames)): flames[g].status = 1200
                else:
                    player.score += 10
            piDots[a].status = 1
    if piDotsLeft == 0: player.status = 2
    drawFlames()
    getPlayerImage()
    player.draw()
    drawLives()
    screen.draw.text("LEVEL "+str(level) , topleft=(10, 10), owidth=0.5, ocolor=(0,0,255), color=(255,255,0) , fontsize=40)
    screen.draw.text(str(player.score) , topright=(590, 20), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    if player.status == 3: drawCentreText("GAME OVER")
    if player.status == 2: drawCentreText("LEVEL CLEARED!\nPress Enter or Button A\nto Continue")
    if player.status == 1: drawCentreText("CAUGHT!\nPress Enter or Button A\nto Continue")
        

def drawCentreText(t):
    screen.draw.text(t , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)

def update(): # Pygame Zero update function
    global player, moveFlamesFlag, flames
    if player.status == 0:
        if moveFlamesFlag == 4: moveFlames()
        for g in range(len(flames)):
            if flames[g].status > 0: flames[g].status -= 1
            if flames[g].collidepoint((player.x, player.y)):
                if flames[g].status > 0:
                    player.score += 100
                    animate(flames[g], pos=(290, 370), duration=1/SPEED, tween='linear', on_finished=flagMoveFlames)
                else:
                    player.lives -= 1
                    sounds.pi2.play()
                    if player.lives == 0:
                        player.status = 3
                        music.fadeout(3)
                    else:
                        player.status = 1
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                sounds.pi1.play()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)
    if player.status == 1:
        i = gameinput.checkInput(player)
        if i == 1:
            player.status = 0
            player.x = 290
            player.y = 570
    if player.status == 2:
        i = gameinput.checkInput(player)
        if i == 1:
            init()

def init():
    global player, level
    initDots()
    initFlames()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()
    level += 1
    music.play("pm1")
    music.set_volume(0.2)

def drawLives():
    for l in range(player.lives): screen.blit("piman_o", (10+(l*32),40))

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
            if flames[g].status > 200 or (flames[g].status > 1 and flames[g].status%2 == 0):
                flames[g].image = "flame"+str(g+1)+"-"
            else:
                flames[g].image = "flame"+str(g+1)+"r"
        else:
            if flames[g].status > 200 or (flames[g].status > 1 and flames[g].status%2 == 0):
                flames[g].image = "flame"+str(g+1)+"-"
            else:
                flames[g].image = "flame"+str(g+1)
        flames[g].draw()

def moveFlames():
    global moveFlamesFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveFlamesFlag = 0
    for g in range(len(flames)):
        dirs = gamemaps.getPossibleDirection(flames[g])
        if inTheCentre(flames[g]):
            flames[g].dir = 3
        else:
            if g == 0: followPlayer(g, dirs)
            if g == 1: ambushPlayer(g, dirs)
        
        if dirs[flames[g].dir] == 0 or randint(0,50) == 0:
            d = -1
            while d == -1:
                rd = randint(0,3)
                if aboveCentre(flames[g]) and rd == 1:
                    rd = 0
                if dirs[rd] == 1:
                    d = rd
            flames[g].dir = d
        animate(flames[g], pos=(flames[g].x + dmoves[flames[g].dir][0]*20, flames[g].y + dmoves[flames[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveFlames)

def followPlayer(g, dirs):
    d = flames[g].dir
    if d == 1 or d == 3:
        if player.x > flames[g].x and dirs[0] == 1: flames[g].dir = 0
        if player.x < flames[g].x and dirs[2] == 1: flames[g].dir = 2
    if d == 0 or d == 2:
        if player.y > flames[g].y and dirs[1] == 1 and not aboveCentre(flames[g]): flames[g].dir = 1
        if player.y < flames[g].y and dirs[3] == 1: flames[g].dir = 3


def ambushPlayer(g, dirs):
    d = flames[g].dir
    if player.movex > 0 and dirs[0] == 1: flames[g].dir = 0
    if player.movex < 0 and dirs[2] == 1: flames[g].dir = 2

    if player.movey > 0 and dirs[1] == 1 and not aboveCentre(flames[g]): flames[g].dir = 1
    if player.movey < 0 and dirs[3] == 1: flames[g].dir = 3

def inTheCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 320 and ga.y < 420:
        return True
    return False

def aboveCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 300 and ga.y < 320:
        return True
    return False

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
            d = gamemaps.checkDotPoint(10+x*20, 10+y*20)
            if d == 1:
                piDots.append(Actor("dot",(10+x*20, 90+y*20)))
                piDots[a].status = 0
                piDots[a].type = 1
                a += 1
            if d == 2:
                piDots.append(Actor("power",(10+x*20, 90+y*20)))
                piDots[a].status = 0
                piDots[a].type = 2
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
        flames[g].status = 0
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
