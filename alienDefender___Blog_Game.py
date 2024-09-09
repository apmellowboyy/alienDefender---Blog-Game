
#IMPORTING * IS A NECESSITY, TIME DEALS WITH MOVEMENT, RANDOM HELPS ALIEN SPAWNS
#PYGAME IS USED FOR THE MUSIC
from ursina import *
import random
import time
import pygame

#THIS IS THE URSINA GAME WINDOW, IT WILL BE USED LATER TO RUN THE GAME
spaceShooterGame = Ursina()

# SPEED AND SPAWN VARIABLES, CHANGING THESE EFFECTS GAME LOGIC
bulletSpeed = 100
enemySpeed = 4.5
spawnRate = 0.7
dropEnemy = 0
score = 0

#WIN AND LOSS VARIABLES, LOSE IF ALIEN HTIS THE BOTTOM OR WIN IF YOU DEFEAT 100 ALIENS
game_over = False
winScreen = False

#INITIALIZER FOR PY GAME SOUND
pygame.mixer.init()

#BACKGROUND MUSIC AND LASER BEAM SOUND WITH PYGAME
#YOU ARE ABLE TO SET VOLUME, MUSIC IS LOUDER THN THE LASER OF COURSE
peterGriffinDeathNote = pygame.mixer.Sound('ursinaGames/song.wav') 
peterGriffinDeathNote.set_volume(1.0)
peterGriffinDeathNote.play(-1) 
laser = pygame.mixer.Sound('ursinaGames/laser.mp3')
laser.set_volume(0.3)

#THIS IS THE PLAYER ENTITY. WITH A MODEL, COLOR, SIZE, POSITION AND SPEED. ROTATION WAS NEEDED FOR THE PLANE TO FACE UPWARDS
player = Entity(model='plane.obj', color=color.black, scale=(1, 1, 1), position=(0, -4, 0), speed=5, rotation=(0, 0, 90))


#BULLETS ARE HANDLED AS A LIST
bullets = []


#SHOOT FUNCTION KEEPS THE BULLET COUNT TO 1, CHANGING THE NUMBER CAPS THE BULLET COUNT TO THAT NUMBER
#APPEND TRACKS THAT NUMBER IN THE BULLETS LIST ABOVE
#LASER SOUND IS PLAYED EVERY SHOT
def shoot():
    if len(bullets) <1:
        bullet = Entity(model='cube', color=color.pink, scale=(0.2, 0.3, 1), position=player.position + (0, 0.5, 0), collider='box')
        bullets.append(bullet)
        laser.play()

# ENEMIES ARE A LIST
enemies = []
#SPAWNS AN ENEMY AND TRACKS IT IN THE LIST ABOVE
def enemyMake():
    alienShip = Entity(model='UFO.obj', texture='alien.jpg', scale=0.03, position=(random.uniform(-7, 7), 10, 0), collider='box')
    enemies.append(alienShip)

#END GAME IF 100 INVADERS ELIMINATED
def exitGame():
    time.sleep(4)  
    application.quit()  

#UPDATES THE GAME
def update():
    #GLOBAL ACCESSES OUTSIDE OF THE UPDATE FUNCTION
    global dropEnemy, score, game_over, winScreen
    
    #GAME STOPS IF EITHER HAPPEN
    if game_over or winScreen:
        return

    # LEFT AND RIGHT CONTROLS
    if held_keys['a']:
        player.x -= 0.3
    if held_keys['d']:
        player.x += 0.3

    #KEEPS THE PLAYER WITHIN A CERTAIN AREA AND GOING OFF SCREEN
    player.x = clamp(player.x, -8, 8)

    # SHOOT BUTTON
    if held_keys['space']:
        shoot()

    #BULLET UP SPEED AND DESPAWN AT 5 (Y)
    for bullet in bullets[:]:
        bullet.y += 30 * time.dt
        if bullet.y > 5:
            bullet.disable()
            bullets.remove(bullet)

    # ALIEN FALL SPEED AND GAME OVER IF THEY REACH THE BOTTOM
    for enemy in enemies[:]:
        enemy.y -= enemySpeed * time.dt
        if enemy.y < -5:
            game_over = True

            #GAME OVER TEXT AND EXIT FROM URSINA
            Text("Invaders have landed!", position = (-0.25, 0.05, 0), scale = 2)
            Text("Game Over!", position=(-0.15, 0, 0), scale=2)
            Text(f'Score: {score}', position=(-0.13, -0.10, 0), scale=2, color=color.blue)
            invoke(exitGame, delay=1)

    # BULLET AND ALIEN COLLISION
    #IF BULLET AND AN ALIEN COLLIDE THEY BOTH DISAPPEAR 
    #AND A POINT IS ADDED TO THE SCORE
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.intersects().hit and enemy.intersects().hit:
                bullet.disable()
                enemy.disable()
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break  

    #ALIEN SPAWN
    dropEnemy += time.dt
    if dropEnemy >= spawnRate:
        enemyMake()
        dropEnemy = 0
    
    #WIN SCREEN!
    # IF SCORE HITS 100 YOU WIN
    if score == 100:
        winScreen = True
        #WIN TEXT
        Text("After a lengthy battle", position = (-0.30, 0,0), scale = 2)
        Text("You defeated the invaders!", position=(-0.30, -0.05, 0), scale=2)
        Text("Thank you for playing!", position = (-0.30,-0.10,0),scale = 2)
        invoke(exitGame, delay=1)

    #2D LOOK
    camera.orthographic = True
    camera.fov = 10
    camera.z = -2

#RUNS THE GAME
spaceShooterGame.run()
