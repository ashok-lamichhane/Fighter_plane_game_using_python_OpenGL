from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import time
import random

x = 0
y = 0
z = [(480,20),(520,20),(480,120),(520,120),(480,20),(480,120),(520,20),(520,120),(440,85),(480,85),(420,70),(480,70),
     (420,70),(440,85),(520,85),(560,85),(520,70),(580,70),(580,70),(560,85),
     (490,30),(510,30),(510,110),(490,110)]

fire = [(int(((z[2][0])+(z[3][0]))/2),int(((z[2][1])+(z[3][1]))/2))]
fire_moving = False
fire_target_y = 720
fire_target_x = 1020
fire_speed = 0
if fire_speed == 0:
    S = int(input("Set Speed: "))
    fire_speed = S
life = 2

square_position = [random.randint(50, 950), random.randint(350, 650)]  # Initial square position
score = 0
game = True
level = 0
level_up = 0
def find_zone(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if (dx >= 0) and (dy >= 0):
            return 0
        elif (dx >= 0) and (dy <= 0):
            return 7
        elif (dx <= 0) and (dy >= 0):
            return 3
        elif (dx <= 0) and (dy <= 0):
            return 4
    else:
        if (dx >= 0) and (dy >= 0):
            return 1
        elif (dx <= 0) and (dy >= 0):
            return 2
        elif (dx <= 0) and (dy <= 0):
            return 5
        elif (dx >= 0) and (dy <= 0):
            return 6

def ToZone0(x,y,zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def BackToOrigin(x,y,zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y,-x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_mld(x1,y1,x2,y2):
    glPointSize(1)
    glBegin(GL_POINTS)

    if x1 > x2:
        x1,y1,x2,y2 = x2,y2,x1,y1

    zone = find_zone(x1,y1,x2,y2)
    x1, y1 = ToZone0(x1, y1, zone)
    x2, y2 = ToZone0(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    NE = 2*(dy-dx)
    E = 2*dy

    x1_main, y1_main = BackToOrigin(x1,y1,zone)
    glVertex2f(abs(x1_main), abs(y1_main))

    while(x1 <= x2):
        if d <= 0:
            d += E
            x1 += 1
        else:
            d += NE
            x1 += 1
            y1 += 1

        x1_main, y1_main = BackToOrigin(x1, y1, zone)
        glVertex2f(abs(x1_main), abs(y1_main))
    glEnd()


def draw_mcd(org_x, org_y, r):
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(1,0,0)
    d = 5 - 4*r
    x = 0
    y = r
    while x <= y:
        if d < 0:
            d += 4 * (2 * x + 3)
            x += 1
        else:
            d += 4 * (2*x - 2*y + 5)
            x += 1
            y -= 1

        glVertex2f(y + org_x, x + org_y)
        glVertex2f(x + org_x, y + org_y)
        glVertex2f(-x + org_x, y + org_y)
        glVertex2f(-y + org_x, x + org_y)
        glVertex2f(-y + org_x, -x + org_y)
        glVertex2f(-x + org_x, -y + org_y)
        glVertex2f(x + org_x, -y + org_y)
        glVertex2f(y + org_x, -x + org_y)

    glEnd()

def plane(z):
    for i in range(0,len(z)-4,2):
        draw_mld(z[i][0], z[i][1], z[i+1][0], z[i+1][1])

    glColor3f(0, 0, 0.9)
    glBegin(GL_QUADS)
    glVertex2f(z[-4][0],z[-4][1])
    glVertex2f(z[-3][0],z[-3][1])
    glVertex2f(z[-2][0],z[-2][1])
    glVertex2f(z[-1][0],z[-1][1])
    glEnd()

    return z

def bullet(fire):
    draw_mcd(fire[-1][0],fire[-1][1],5)
    draw_mcd(fire[-1][0], fire[-1][1], 4)
    draw_mcd(fire[-1][0], fire[-1][1], 3)
    draw_mcd(fire[-1][0], fire[-1][1], 2)
    draw_mcd(fire[-1][0], fire[-1][1], 1)
    #print(fire[-1][0], fire[-1][1])

def left_translate(z):
    new = []
    for i in range(len(z)):
        x = z[i][0]
        y = z[i][1]
        tl = np.array([[1, 0, -10],
                       [0, 1, 0],
                       [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])
        v = np.matmul(tl, v1)
        new.append((v[0][0],v[1][0]))
    return new

def right_translate(z):
    new = []
    for i in range(len(z)):
        x = z[i][0]
        y = z[i][1]
        tl = np.array([[1, 0, 10],
                       [0, 1, 0],
                       [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])
        v = np.matmul(tl, v1)
        new.append((v[0][0],v[1][0]))
    return new

def left_rotate(z):
    a = math.cos(math.radians(35))
    b = math.sin(math.radians(35))
    new = []
    for i in range(len(z)):
        x = z[i][0]
        y = z[i][1]

        rt = np.array([[a, -b, 0],
                       [b, a, 0],
                       [0, 0, 1]])

        to_c = np.array([[1, 0, -(z[0][0]+20)],
                       [0, 1, -(z[0][1])],
                       [0, 0, 1]])

        bto_org = np.array([[1, 0,z[0][0]+20],
                       [0, 1, z[0][1]],
                       [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        f1 = np.matmul(bto_org,rt)
        f2 = np.matmul(f1,to_c)
        v = np.matmul(f2,v1)

        new.append((v[0][0],v[1][0]))
    return new

def right_rotate(z):
    a = math.cos(math.radians(-35))
    b = math.sin(math.radians(-35))
    new = []
    for i in range(len(z)):
        x = z[i][0]
        y = z[i][1]

        rt = np.array([[a, -b, 0],
                       [b, a, 0],
                       [0, 0, 1]])

        to_c = np.array([[1, 0, -(z[0][0]+20)],
                       [0, 1, -(z[0][1])],
                       [0, 0, 1]])

        bto_org = np.array([[1, 0,z[0][0]+20],
                       [0, 1, z[0][1]],
                       [0, 0, 1]])

        v1 = np.array([[x],
                       [y],
                       [1]])

        f1 = np.matmul(bto_org,rt)
        f2 = np.matmul(f1,to_c)
        v = np.matmul(f2,v1)

        new.append((v[0][0],v[1][0]))
    return new

# def shoot(fire):
#     x = fire[-1][0]
#     y = fire[-1][1]
#     tl = np.array([[1, 0, 0],
#                    [0, 1, 5],
#                    [0, 0, 1]])
#
#     v1 = np.array([[x],
#                    [y],
#                    [1]])
#     v = np.matmul(tl, v1)
#     m,n = v[0][0],v[1][0]
#     return m,n


def keyboard(key,X,Y):
    global x,y,z,fire, fire_moving, square_position,score,game,life
    if key == b'a' or key == b'A' or key == GLUT_KEY_LEFT:
        if z[0][0] >= 350:
            l = left_translate(z)
            z = l

    elif key == b'd' or key == b'D' or key == GLUT_KEY_RIGHT:
        if z[0][0] <= 550:
            l = right_translate(z)
            z = l

    elif key == b'q' or key == b'Q':
        if x>-1:# and fire[-1][1] <= square_position[-1]:
            l = left_rotate(z)
            z = l
            x -= 1

    elif key == b'e' or key == b'E':
        if x<1:# and fire[-1][1] <= square_position[-1]:
            l = right_rotate(z)
            z = l
            x += 1

    elif key == b' ':
        fire_moving = True
        glutTimerFunc(10, timer_func, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if fire_moving and fire[-1][1] >= (square_position[-1]+50): #fire_target_y:
        fire_moving = False
        life -= 1
        if life == 0:
            game = False
        #print("Game Over: Bullet missed the square")
        #print("Total Score:",score)
        #Optionally, you can reset the game by changing the bullet and square positions here.
    glutPostRedisplay()

    if fire_moving and fire[-1][1] >= (square_position[-1]+50):  # fire_target_y:
        fire_moving = False
        if life == 0:
            game = False

    if game == True:
        if fire_moving == False:
            fire = [(int(((z[2][0]) + (z[3][0])) / 2), int(((z[2][1]) + (z[3][1])) / 2))]

    glutPostRedisplay()


def timer_func(value):
    global fire, fire_moving,x,y,square_position,score,level_up,life

    if x == 0:
        if fire_moving and fire[-1][1] < fire_target_y:
            new_y = fire[-1][1] + fire_speed
            if new_y >= fire_target_y:
                new_y = fire_target_y
                fire_moving = False
            fire[-1] = (fire[-1][0], new_y)

        glutPostRedisplay()

        # Stop the animation if the ball reaches the target
        if fire_moving and fire[-1][1] == fire_target_y:
            fire_moving = False
            fire = [(int(((z[2][0])+(z[3][0]))/2), int(((z[2][1])+(z[3][1]))/2))]
            glutPostRedisplay()

        if fire_moving:
            glutTimerFunc(10, timer_func, 0)  # Continue the animation

    if x == -1:
        if fire_moving and fire[-1][1] < fire_target_y:
            new_y = fire[-1][1] + fire_speed
            new_x = fire[-1][0] - fire_speed
            if new_y >= fire_target_y:
                new_y = fire_target_y
                new_x = fire_target_x
                fire_moving = False
            fire[-1] = (new_x, new_y)

        glutPostRedisplay()

        # Stop the animation if the ball reaches the target
        if fire_moving and fire[-1][1] == fire_target_y:
            fire_moving = False
            fire = [(int(((z[2][0])+(z[3][0]))/2), int(((z[2][1])+(z[3][1]))/2))]
            glutPostRedisplay()

        if fire_moving:
            glutTimerFunc(10, timer_func, 0)  # Continue the animation

    if x == +1:
        if fire_moving and fire[-1][1] < fire_target_y:
            new_y = fire[-1][1] + fire_speed
            new_x = fire[-1][0] + fire_speed
            if new_y >= fire_target_y:
                new_y = fire_target_y
                new_x = fire_target_x
                fire_moving = False
            fire[-1] = (new_x, new_y)

        glutPostRedisplay()

        # Stop the animation if the ball reaches the target
        if fire_moving and fire[-1][1] == fire_target_y:

            fire_moving = False
            fire = [(int(((z[2][0])+(z[3][0]))/2), int(((z[2][1])+(z[3][1]))/2))]
            #glutPostRedisplay()

        if fire_moving:
            glutTimerFunc(10, timer_func, 0)  # Continue the animation

    if (
        square_position[0] <= fire[-1][0] <= square_position[0] + 50 and
        square_position[1] <= fire[-1][1] <= square_position[1] + 35
    ):
        # Bullet hit the square, change the square's position and reset bullet
        square_position = (random.randint(50, 950), random.randint(350, 650))
        fire_moving = False
        fire = [(int(((z[2][0]) + (z[3][0])) / 2), int(((z[2][1]) + (z[3][1])) / 2))]
        score += 1
        level_up +=1
        #print("Bullet hit the square! Continue playing...")
        #print("Current Score:",score)
        glutPostRedisplay()


def iterate():
    glViewport(0, 0, 1000, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global x,y,z,fire,score,level_up,level,fire_speed,life
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(0.1, 0.0, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(1000,700)
    glVertex2f(0,700)
    glVertex2f(0,0)
    glVertex2f(1000,0)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)
    z = plane(z)
    glColor3f(1.0, 0.0, 0.0)
    bullet(fire)


    glColor3f(0.3, 0.8, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(square_position[0] + 40, square_position[1] + 35)
    glVertex2f(square_position[0], square_position[1] + 35)
    glVertex2f(square_position[0], square_position[1])
    glVertex2f(square_position[0] + 40, square_position[1])
    glEnd()



    if game == True:
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(20, 650)  # Adjust position
        score_str = "Score: " + str(score)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(100, 650)  # Adjust position
        score_str = "Life: " + str(life)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(20, 620)  # Adjust position
        score_str = "Level: " + str(level)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        if level_up == 5:
            level += 1
            fire_speed += 1
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(450, 350)  # Adjust position
            lev = "Level Updated to " + str(level)
            for char in lev:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    else:
        glColor3f(1.0, 0, 0)
        glRasterPos2f(450, 350)  # Adjust position
        game_str = "Game Over"
        for char in game_str:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

        glColor3f(1.0, 1, 1)
        glRasterPos2f(450, 320)  # Adjust position
        score_str = "Total Score: " + str(score)
        for char in score_str:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


    glutSwapBuffers()
    if level_up == 5:
        level_up = 0
        time.sleep(1)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 700)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Fighter Plane")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboard)
glutTimerFunc(10, timer_func, 0)
glutMainLoop()