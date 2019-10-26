
import pygame, random, sys, time
from pygame.locals import *

#set screen size
WINDOWWIDTH = 1024
WINDOWHEIGHT = 600
FPS = 60

MAXGOTTENPASS = 20
EnemiesIZE = 70
ADDNEWEnemyRATE = 30
ADDNEWKINDEnemy = ADDNEWEnemyRATE

NORMALEnemiesPEED = 2
NEWKINDEnemiesPEED = NORMALEnemiesPEED / 2

PLAYERMOVERATE = 15
BULLETSPEED = 10
ADDNEWBULLETRATE = 15

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN:
                    return

def terminate():
    pygame.quit()
    sys.exit()

def playerHasHitEnemy(playerRect, Enemies):
    for z in Enemies:
        if playerRect.colliderect(z['rect']):
            return True
    return False

def bulletHasHitEnemy(bullets, Enemies):
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

def bulletHasHitCrawler(bullets, newKindEnemies):
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False

def displayText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Goku Uses Rasengan')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)

gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('Naruto-SpinAndBurst.mp3')

playerImage = pygame.image.load('goku.gif')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('rasengan.gif')
bulletRect = bulletImage.get_rect()

EnemyImage = pygame.image.load('deidara.png')
newKindEnemyImage = pygame.image.load('obito.gif')

backgroundImage = pygame.image.load('background.png')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# show the "Start" screen
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
displayText('Goku Uses Rasengan on Akatsuki', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
displayText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()
while True:

    Enemies = []
    newKindEnemies = []
    bullets = []

    akatsukiGottenPast = 0
    score = 0

    playerRect.topleft = (50, WINDOWHEIGHT /2)
    moveLeft = moveRight = False
    moveUp=moveDown = False
    shoot = False

    EnemyAddCounter = 0
    newKindEnemyAddCounter = 0
    bulletAddCounter = 40
    pygame.mixer.music.play(-1, 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False

        EnemyAddCounter += 1
        if EnemyAddCounter == ADDNEWKINDEnemy:
            EnemyAddCounter = 0
            Enemiesize = EnemiesIZE       
            newEnemy = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-Enemiesize-10), Enemiesize, Enemiesize),
                        'surface':pygame.transform.scale(EnemyImage, (Enemiesize, Enemiesize)),
                        }

            Enemies.append(newEnemy)

        newKindEnemyAddCounter += 1
        if newKindEnemyAddCounter == ADDNEWEnemyRATE:
            newKindEnemyAddCounter = 0
            newKindEnemiesize = EnemiesIZE
            newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindEnemiesize-10), newKindEnemiesize, newKindEnemiesize),
                        'surface':pygame.transform.scale(newKindEnemyImage, (newKindEnemiesize, newKindEnemiesize)),
                        }
            newKindEnemies.append(newCrawler)

        bulletAddCounter += 1
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
                         'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
                        }
            bullets.append(newBullet)

        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0,-1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
            playerRect.move_ip(0,PLAYERMOVERATE)

        for z in Enemies:
            z['rect'].move_ip(-1*NORMALEnemiesPEED, 0)

        for c in newKindEnemies:
            c['rect'].move_ip(-1*NEWKINDEnemiesPEED,0)

        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

        # Delete Enemies that have fallen past the bottom.
        for z in Enemies[:]:
            if z['rect'].left < 0:
                Enemies.remove(z)
                akatsukiGottenPast += 1

        for c in newKindEnemies[:]:
            if c['rect'].left <0:
                newKindEnemies.remove(c)
                akatsukiGottenPast += 1

        for b in bullets[:]:
            if b['rect'].right>WINDOWWIDTH:
                bullets.remove(b)

        for z in Enemies:
            if bulletHasHitEnemy(bullets, Enemies):
                score += 1
                Enemies.remove(z)
    
        for c in newKindEnemies:
            if bulletHasHitCrawler(bullets, newKindEnemies):
                score += 1
                newKindEnemies.remove(c)      

        # Draw the game world on the window.
        windowSurface.blit(rescaledBackground, (0, 0))

        windowSurface.blit(playerImage, playerRect)

        for z in Enemies:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindEnemies:
            windowSurface.blit(c['surface'], c['rect'])

        # draw each bullet
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        displayText('Akatsuki gotten past: %s' % (akatsukiGottenPast), font, windowSurface, 10, 20)
        displayText('score: %s' % (score), font, windowSurface, 10, 50)

        # update the display
        pygame.display.update()
            
        # Check if any of the Enemies has hit the player.
        if playerHasHitEnemy(playerRect, Enemies):
            break
        if playerHasHitEnemy(playerRect, newKindEnemies):
           break
        
        # check if score is over MAXGOTTENPASS which means game over
        if akatsukiGottenPast >= MAXGOTTENPASS:
            break

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    if akatsukiGottenPast >= MAXGOTTENPASS:
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        displayText('score: %s' % (score), font, windowSurface, 10, 30)
        displayText('GAME OVER....!!!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        displayText('YOU LET KONOHA BE OVERRUN', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 100)
        displayText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    if playerHasHitEnemy(playerRect, Enemies):
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        displayText('score: %s' % (score), font, windowSurface, 10, 30)
        displayText('GAME OVER....!!!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        displayText('YOU GOT REKT BY THE AKATSUKI', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 100)
        displayText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    gameOverSound.stop()