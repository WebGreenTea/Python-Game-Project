import pgzrun
import random
import pygame

def start_game():
    global gamescreen,lchek,lchekOammo,itemC,ammo,health,Time,TimeOver,startOtime,score,damage
    gamescreen = 1
    lchek = 1
    lchekOammo = 1
    itemC = 0
    ammo = 100
    health = 4
    Time = 0
    TimeOver = 5
    startOtime = 1
    score = 0
    damage = 0
    ship.pos = WIDTH/2,700
    shiphit.pos = WIDTH/2,708
    clock.schedule_interval(spawnMeteo,0.3)
    clock.schedule_interval(timeCount,1.0)
    clock.schedule_interval(timeOcount,1.0)

def end_game():
    global gamescreen
    laser.clear()
    laser1.clear()
    laser2.clear()
    meteo.clear()
    meteo1.clear()
    meteo2.clear()
    meteo3.clear()
    ammoI.clear()
    bufI.clear()
    healI.clear()
    BomEff.clear()
    clock.unschedule(spawnMeteo)
    clock.unschedule(timeCount)
    clock.unschedule(timeOcount)
    gamescreen = 2


WIDTH = 700
HEIGHT = 750
bg = Actor('galaxy',topleft=(0,0))
bg2 = Actor('galaxy',topleft=(0,-3000))
ship = Actor('ship')
shiphit = Actor('shiphit')
healthBar = Actor('he4',topright=(690,20))
Ibar = Actor('ibar0',topright=(690,50))
gamescreen = 0
FullSC = 0
laser = []
laser1 = []
laser2 = []
meteo = []
meteo1 = []
meteo2 = []
meteo3 = []
BomEff = []
ammoI = []
bufI = []
healI = []
lchek = 1
lchekOammo = 1
itemC = 0
ammo = 100
health = 4
Time = 0
TimeOver = 5
startOtime = 1
score = 0
damage = 0

def draw():
    global lchek,lchekOammo,itemC,Time,ammo,TimeOver,startOtime
    screen.fill((201,0,0))
    bg.draw()
    bg2.draw()
    if gamescreen == 0:
        screen.blit('mainmenu',(0,0))
        screen.blit('1',((WIDTH/2)-125,530))
        screen.blit('4',((WIDTH/2)-179,700))
    if gamescreen == 1:
        #draw BomEff
        for i in BomEff:
            i.draw()
        shiphit.draw()
        ship.draw()
        #pass space
        keySPACE()
        #draw laser
        for i in laser: 
            i.draw()
        for i in laser1: #draw laser ( use item)[1]
            i.draw()
        for i in laser2: #draw laser ( use item)[2]
           i.draw()
        #draw meteor
        for i in meteo:
            i.draw()
        for i in meteo1:
            i.draw()
        for i in meteo2:
            i.draw()
        for i in meteo3:
            i.draw()
        #draw ITEM
        for i in ammoI:
            i.draw()
        for i in bufI:
            i.draw()
        for i in healI:
            i.draw()
        screen.draw.text("Your Score: "+str(score),topleft=(10,30),fontsize=30,color=(255,255,255))
        screen.draw.text("Ammo: "+str(ammo),topleft=(10,10),fontsize=30,color="red")
        healthBar.draw()
        Ibar.draw()
        if ammo == 0 :
            startOtime = 0
            screen.draw.text("!!Out of Ammo!!",midtop=(WIDTH/2,10),fontsize=50,color="yellow")
            screen.draw.text("GameOver in "+str(TimeOver),midtop=(WIDTH/2,50),fontsize=50,color="yellow")
        else:
            TimeOver = 10
            startOtime = 1
    if gamescreen == 2:
        screen.draw.text("GameOver",midtop=(WIDTH/2,150),fontsize=100,color="cyan")
        screen.draw.text("Your Score : "+str(score),midtop=(WIDTH/2,250),fontsize=100,color="cyan")
        screen.blit('2',((WIDTH/2)-142.5,470))
        screen.blit('3',((WIDTH/2)-87.5,620))

#in draw     
def keySPACE():
    global ammo,lchek,lchekOammo,itemC
    if keyboard.space:
        if lchek == 1 and ammo > 0:
            if itemC == 0: #no item
                sounds.laser.play()
                laser.append(Actor('mylaser',(ship.x,ship.y-55)))
                ammo -= 1
            elif itemC == 1: # have item
                laser1.append(Actor('mylaser',(ship.x-40,ship.y-20)))
                laser2.append(Actor('mylaser',(ship.x+40,ship.y-20)))
                sounds.laser.play()
                if ammo == 1:
                    ammo -= 1
                else:
                    ammo -= 2
            lchek = 0
            clock.schedule(lasercreate,0.5)
        elif lchekOammo == 1 and ammo == 0:
            sounds.out_ammo.play()
            lchekOammo = 0
            clock.schedule(outAmScreate,0.5)

#in keySPACE
def lasercreate():
    global lchek
    lchek = 1
def outAmScreate():
    global lchekOammo
    lchekOammo = 1

def on_key_down(key):
    global gamescreen,FullSC
    if key == keys.F and FullSC == 0:
        FullSC = 1
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    elif key == keys.F and FullSC == 1:
        FullSC = 0
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT))
    if gamescreen == 0:
        if key == keys.RETURN:
            start_game()
    if gamescreen == 2:
        if key == keys.RETURN:
            start_game()
        if key == keys.ESCAPE:
            quit()

def update():
    global ammo,itemC,Time,health,startOtime,damage
    if gamescreen == 1:
        #Item Control
        ItemControl()
        #check to normal laser
        Lasernormal()
        #meteor move
        meteorControl()
        #UupdateHealthBar
        updateHealth()
        #updateItemBar
        updateITEM()         
        #laser move
        laserControl()
        #ship control
        shipControl()
        if health <= 0 or TimeOver <= 0 :
            end_game() 
    #background
    bgControl()
    #DEBUG
    '''print("laser"+str(len(laser))+str(len(laser1))+str(len(laser2))+" meteo"+str(len(meteo))+str(len(meteo1))+str(len(meteo2))+str(len(meteo3))
    +" Eff"+str(len(BomEff))+" Item"+str(len(ammoI))+str(len(bufI))+str(len(healI)))'''

#inUpdate
def ItemControl():
    global ammo,itemC,Time,health
    for i in ammoI:
        if i.colliderect(shiphit):
            sounds.get_ammo.play()
            ammoI.remove(i)
            ammo+=10
        if i.y <= HEIGHT:
            i.y += 1
        else:
            ammoI.remove(i)
    for i in bufI:
        if i.colliderect(shiphit):
            sounds.get_up.play()
            bufI.remove(i)
            itemC = 1
            Time = 10
        if i.y <= HEIGHT:
            i.y += 1
        else:
            bufI.remove(i)
    for i in healI:
        if i.colliderect(shiphit):
            sounds.get_heal.play()
            healI.remove(i)
            if health < 4:
                health += 1
        if i.y <= HEIGHT:
            i.y += 1
        else:
            healI.remove(i)

def Lasernormal():
    global itemC,Time
    if Time == 0:
        itemC = 0

def meteorControl():
    global damage,health,KEEP,meteoType
    for i in meteo:
        if i.colliderect(shiphit):
            sounds.hit.play()
            damage = 1
            ship.image = 'shipdamage'
            meteo.remove(i)
            health -= 1
            clock.schedule(shipNormal,0.1)
        c = meteoRemove(i)
        if c:
            BomEff.append(Actor('m0b',center=(i.x,i.y)))
            meteo.remove(i)
            clock.schedule(removeEff,0.1)
        elif i.y <= HEIGHT:
            i.y += 7
        else:
            meteo.remove(i)
    for i in meteo1:
        if i.colliderect(shiphit):
            sounds.hit.play()
            damage = 1
            ship.image = 'shipdamage'
            meteo1.remove(i)
            health -= 1
            clock.schedule(shipNormal,0.1)
        c = meteoRemove(i)
        if c:
            BomEff.append(Actor('m1b',center=(i.x,i.y)))
            meteo1.remove(i)
            clock.schedule(removeEff,0.1)
        elif i.y <= HEIGHT:
            i.y += 6
        else:
            meteo1.remove(i)
    for i in meteo2:
        if i.colliderect(shiphit):
            sounds.hit.play()
            damage = 1
            ship.image = 'shipdamage'
            meteo2.remove(i)
            health -= 1
            clock.schedule(shipNormal,0.1)
        c = meteoRemove(i)
        if c:
            BomEff.append(Actor('m2b',center=(i.x,i.y)))
            meteo2.remove(i)
            clock.schedule(removeEff,0.1)
        elif i.y <= HEIGHT:
            i.y += 5
        else:
            meteo2.remove(i)
    for i in meteo3:
        if i.colliderect(shiphit):
            sounds.hit.play()
            damage = 1
            ship.image = 'shipdamage'
            meteo3.remove(i)
            health -= 1
            clock.schedule(shipNormal,0.1)
        c = meteoRemove(i)
        if c:
            BomEff.append(Actor('m3b',center=(i.x,i.y)))
            meteo3.remove(i)
            clock.schedule(removeEff,0.1)
        elif i.y <= HEIGHT:
            i.y += 4
        else:
            meteo3.remove(i)

def updateHealth():
    if health == 4:
        healthBar.image = 'he4'
    elif health == 3:
        healthBar.image = 'he3'
    elif health == 2:
        healthBar.image = 'he2'
    elif health == 1:
        healthBar.image = 'he1'
    elif health == 0:
        healthBar.image = 'he0'

def updateITEM():
    if Time == 10:
        Ibar.image = 'ibar10'
    elif Time == 9:
        Ibar.image = 'ibar9'
    elif Time == 8:
        Ibar.image = 'ibar8'
    elif Time == 7:
        Ibar.image = 'ibar7'
    elif Time == 6:
        Ibar.image = 'ibar6'
    elif Time == 5:
        Ibar.image = 'ibar5'
    elif Time == 4:
        Ibar.image = 'ibar4'
    elif Time == 3:
        Ibar.image = 'ibar3'
    elif Time == 2:
        Ibar.image = 'ibar2'
    elif Time == 1:
        Ibar.image = 'ibar1'
    else:
        Ibar.image = 'ibar0'

def laserControl():
    #if itemC = 0 #laser no item
    for i in range(len(laser)):
        laser[i].y -= 7
    for i in range(len(laser)):
        if laser[i].y < -10 :
            laser.pop(i)
            break
    #if itemC = 1
        #laser use item [1]
    for i in range(len(laser1)):
        laser1[i].y -= 5
    for i in range(len(laser1)):
        if laser1[i].y < -10 :
            laser1.pop(i)
            break
        #laser use item [2]
    for i in range(len(laser2)):
        laser2[i].y -= 5
    for i in range(len(laser2)):
        if laser2[i].y < -10 :
            laser2.pop(i)
            break

def bgControl():
    bg.y += 0.5
    bg2.y += 0.5
    if bg.top > HEIGHT:
        bg.top = -3000
    if bg2.top > HEIGHT:
        bg2.top = -3000

def shipControl():
    if (keyboard.left or keyboard.a) and (keyboard.up or keyboard.w):
        if ship.left > 0 and ship.top > 0:
            ship.x -= 5
            ship.y -= 5
            shiphit.x -= 5
            shiphit.y -= 5
            if damage == 0:
                ship.image = 'shipfor'
        elif ship.left > 0:
            ship.x -= 5
            shiphit.x -= 5
            if damage == 0:
                ship.image = 'ship'
        elif ship.top > 0:
            ship.y -= 5
            shiphit.y -= 5
            if damage == 0:
                ship.image = 'shipfor'
        else:
            if damage == 0:
                ship.image = 'ship'
    elif (keyboard.left or keyboard.a) and (keyboard.down or keyboard.s):
        if ship.left > 0 and ship.bottom < HEIGHT:
            ship.x -= 5
            ship.y += 5
            shiphit.x -= 5
            shiphit.y += 5
            if damage == 0:
                ship.image = 'shipba'
        elif ship.bottom < HEIGHT:
            ship.y += 5
            shiphit.y += 5
            if damage == 0:
                ship.image = 'shipba'
        elif ship.left > 0:
            ship.x -= 5
            shiphit.x -= 5
            if damage == 0:
                ship.image = 'ship'
        else:
            if damage == 0:
                ship.image = 'ship'
    elif (keyboard.right or keyboard.d) and (keyboard.up or keyboard.w):
        if ship.right < WIDTH and ship.top > 0:
            ship.x += 5
            ship.y -= 5
            shiphit.x += 5
            shiphit.y -= 5
            if damage == 0:
                ship.image = 'shipfor'
        elif ship.right < WIDTH:
            ship.x += 5
            shiphit.x += 5
            if damage == 0:
                ship.image = 'ship'
        elif ship.top > 0:
            ship.y -= 5
            shiphit.y -= 5
            if damage == 0:
                ship.image = 'shipfor'
        else:
            if damage == 0:
                ship.image = 'ship'
    elif (keyboard.right or keyboard.d) and (keyboard.down or keyboard.s):
        if ship.right < WIDTH and ship.bottom < HEIGHT:
            ship.x += 5
            ship.y += 5
            shiphit.x += 5
            shiphit.y += 5
            if damage == 0:
                ship.image = 'shipba'
        elif ship.right < WIDTH:
            ship.x += 5
            shiphit.x += 5
            if damage == 0:
                ship.image = 'ship'
        elif ship.bottom < HEIGHT:
            ship.y += 5
            shiphit.y += 5
            if damage == 0:
                ship.image = 'shipba'
        else:
            if damage == 0:
                ship.image = 'ship'
    elif keyboard.left or keyboard.a:
        if ship.left > 0:
            ship.x -= 5
            shiphit.x -= 5
    elif keyboard.right or keyboard.d:
        if ship.right < WIDTH:
            ship.x += 5
            shiphit.x += 5
    elif keyboard.up or keyboard.w:
        if ship.top > 0:
            ship.y -= 5
            shiphit.y -= 5
            if damage == 0:
                ship.image = 'shipfor'
    elif keyboard.down or keyboard.s:
        if ship.bottom < HEIGHT:
            ship.y += 5
            shiphit.y += 5
            if damage == 0:
                ship.image = 'shipba'
    else:
        if damage == 0:
            ship.image = 'ship'
    
#in meteorControl
def removeEff():
    BomEff.remove(BomEff[0])

def shipNormal():
    global damage
    damage = 0
    ship.image = 'ship'

def meteoRemove(i):
    global score
    for n in laser:
        if n.colliderect(i):
            sounds.lhm.play()
            laser.remove(n)
            randomItem(i)
            score += 1
            return(True)
    for n2 in laser1:
        if n2.colliderect(i):
            sounds.lhm.play()
            laser1.remove(n2)
            randomItem(i)
            score += 1
            return(True)
    for n3 in laser2:
        if n3.colliderect(i):
            sounds.lhm.play()
            laser2.remove(n3)
            randomItem(i)
            score += 1
            return(True)
    return(False) 

#in meteo Remove
def randomItem(i):
    R = random.randint(1,100)
    if R >= 1 and R <= 10:
        ammoI.append(Actor('ammo',(i.x,i.y)))
    elif R >= 11 and R <= 15:
        bufI.append(Actor('buf',(i.x,i.y)))
    elif R ==97 or R == 98:
        healI.append(Actor('heal',(i.x,i.y)))

#in Clock before game start
def timeCount():
    global Time,itemC
    if Time > 0:
        Time -= 1
    else:
        pass
def timeOcount():
    global TimeOver
    if startOtime == 0:
        if TimeOver > 0:
            TimeOver -= 1
def spawnMeteo():
    global gamescreen
    if gamescreen == 1:
        R = random.randint(1,4)
        if R == 1:
            meteo.append(Actor('meteor',midbottom=(random.randint(100,650),0)))
        elif R == 2:
            meteo1.append(Actor('meteor1',midbottom=(random.randint(100,650),0)))
        elif R == 3:
            meteo2.append(Actor('meteor2',midbottom=(random.randint(100,650),0)))
        elif R == 4:
            meteo3.append(Actor('meteor3',midbottom=(random.randint(100,650),0)))

pgzrun.go()