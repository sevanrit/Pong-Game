import pygame, os, time, math, random
from random import randint

pygame.init()
pygame.font.init()

#Constants

disp_width = 800
disp_height = 600
display = pygame.display.set_mode((disp_width, disp_height))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
FPS = 60
clock = pygame.time.Clock()
bg = pygame.image.load(os.path.join('Sprites\\bg.png')).convert_alpha()
vectorY = 0
vectorX = 1
ball_speed = 6
ball_plus = 0.2
points_1 = 0
points_2 = 0
table_speed = 3
start_pos = 240
y_cof = 1.0 # Угол отскока
r = 1

IsAway = False
render = True
gameRunning = True
Strategy = False
GameLvl = 1

class Plat:
    def __init__(self, img, x, y, size_x, size_y, points, speed):
        self.img = img
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.points = points
        self.speed = speed

    def move_up(table):
        if (table.y ) >= 0:
            table.y += -table.speed

    def move_down(table):
        if (table.y + table.size_y) <= disp_height: table.y += table.speed
        
class Ball:
    def __init__(self, img, x, y, size_x, size_y, vectorX, vectorY, speed):
        self.img = img
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.vectorX = vectorX
        self.vectorY = vectorY
        self.speed = speed

    def correction_speed(vector_x, vector_y):
        if vector_y > 1:
            vector_x *= 1/vector_y
            vector_y = 1
        if vector_y < -1:
            vector_x *= 1/abs(vector_y)
            vector_y = -1
        
        return vector_x, vector_y
    
    def correction_sqrt(vector_x, vector_y):
        t = 1
        if vector_x < 0: t = -1
        vector_x = math.sqrt(abs(1**2 - vector_y**2)) * t

        return vector_x, vector_y

    def collision_plat(vectorX_num, plat):
        global IsAway
        
        IsAway = False
        ball.vectorX = vectorX_num
        if GameLvl == 2:
            ball.speed += ball_plus
        else:
            ball.speed = ball_speed
        ball_center = ball.y + ball.size_y/2
        #ball.vectorY = (((ball.y - plat.y) / 50) - 1)*y_cof
        cf = ball_center- plat.y
        ball.vectorY = (cf - 50) * 0.01
        ball.vectorX, ball.vectorY = Ball.correction_sqrt(ball.vectorX, ball.vectorY)
        print(ball_speed*ball.vectorX, ball_speed*ball.vectorY)

    def collision_wall():
        ball.vectorY = ball.vectorY * -1
        #ball.speed += ball_plus

    def away(direction):
        if direction == "right":
            ball.x = 100
            ball.vectorX = 1
            table_1.points += 1
        elif direction == "left":
            ball.x = 700
            ball.vectorX = -1
            table_2.points += 1
        ball.y = 300
        ball.speed = ball_speed
        ball.vectorY = 0
        table_1.y = start_pos
        table_2.y = start_pos

    def reset(self):
        ball.x = 400
        ball.vectorX = -1
        ball.y = 300
        ball.speed = ball_speed
        ball.vectorY = 0
        table_1.y = start_pos
        table_2.y = start_pos

def render():
    display = pygame.display.set_mode((disp_width, disp_height))
    display.blit(bg, (0, 0))
    display.blit(table_1.img, (table_1.x, table_1.y))
    display.blit(table_2.img, (table_2.x, table_2.y))
    display.blit(ball.img, (ball.x, ball.y))
    display.blit(myfont.render(str(table_1.points ), False, (255, 255, 255)), (360, 10))
    display.blit(myfont.render(str(table_2.points), False, (255, 255, 255)), (440, 10))
    
class AI:
    def __init__(self):
        self.size_y = None
        self.y = None
        self.t = 0
        self.frames_dif = [[400, 300]]
        self.predict = []
        self.NoCorrect = True
        self.correct = 300

    def trend(plat, ai):
        if IsAway:
            ai.NoCorrect = True
            ai.correct = 300
        
        elif ball.vectorX < 0:
            
            if time.perf_counter() - ai.t >= 0.01:
                ai.frames_dif.append([ball.x, ball.y])
                x = ai.frames_dif[1][0] - ai.frames_dif[0][0]
                y = ai.frames_dif[1][1] - ai.frames_dif[0][1]
                
                if len(ai.predict) < 2:
                    ai.predict.append([x, y])
                else:
                    y = ai.predict[1][1]
                    x = ai.predict[1][0] 
                    if ai.NoCorrect:
                        if x == 0: x = 1
                        ball_way = abs((ball.x-40)/x)
                        ball_const_y = ball.y
                        ai.correct = abs(ball_const_y + ball_way * y)
                        #print(ai.corect, ball_way, ball_const_y, y, x)

                        #Коррекция
                        for i in range(10):
                            if ai.correct > disp_height:
                                ai.correct = abs(1200 - ai.correct)
                        
 
                        #print(ai.corect)
                        ai.NoCorrect = False
                        return ai.correct

                ai.t = time.perf_counter()
                ai.frames_dif = [[ball.x, ball.y]]
                
        else:
            ai.predict = []
            ai.NoCorrect = True
            ai.correct = 300

    def main(plat, character):
        global Strategy, r
        AI.trend(plat, character)

        # Attack
        if (ball.x < 100) and (plat.y + plat.size_y > ball.y > plat.y):
            if not Strategy:
                r = randint(1, 3)
                Strategy = True
            if plat.y + plat.size_y/2 + 50 >= ai.correct and r == 1: Plat.move_up(plat)
            if plat.y + plat.size_y / 2 - 50 >= ai.correct and r == 2: Plat.move_up(plat)
            if plat.y + plat.size_y / 2 >= ai.correct and r == 3: Plat.move_up(plat)
            
        #Deffence
        elif plat.y + plat.size_y/2 >= ai.correct: Plat.move_up(plat)
        elif plat.y + plat.size_y/2 < ai.correct:  Plat.move_down(plat)
        if ball.vectorX > 0: Strategy = False

#                       #

table_1 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 760, start_pos, 20, 100, points_1, table_speed)
table_2 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 20, start_pos, 20, 100, points_2, table_speed)
ball = Ball(pygame.image.load(os.path.join('Sprites\\ball.png')).convert_alpha(), 400, 300, 16, 16, vectorX, vectorY, ball_speed)
ai = AI()

#                       #

def main_loop():
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
    #       KEYS        #
    keys = pygame.key.get_pressed()

    if keys[pygame.K_o] and (table_1.y ) >= 0:
        Plat.move_up(table_1)
    if keys[pygame.K_l] and (table_1.y + table_1.size_y) <= disp_height:
        Plat.move_down(table_1)

    if keys[pygame.K_w] and (table_2.y ) >= 0:
        Plat.move_up(table_2)
    if keys[pygame.K_s] and (table_2.y + table_2.size_y) <= disp_height:
        Plat.move_down(table_2)

    if keys[pygame.K_q]: print(" Вектор X = ", ball.vectorX," Вектор Y = ", ball.vectorY," Позиция мяча X = ", ball.x," Позиция мяча Y = ", ball.y)

    #       Collisions      #

    if ball.y + ball.size_y > disp_height and ball.vectorY > 0:
        Ball.collision_wall()
    if ball.y < 0 and ball.vectorY <= 0:
        Ball.collision_wall()

    if ( table_1.y + table_1.size_y - ball.size_x/2 >= ball.y >= table_1.y - ball.size_x/2 ) and (ball.x + ball.size_x >= 760):
        Ball.collision_plat(-1, table_1)

    if ( table_2.y + table_2.size_y - ball.size_x/2 >= ball.y >= table_2.y - ball.size_x/2 ) and (ball.x <= 40):
        Ball.collision_plat(1, table_2)

    elif (ball.x + ball.size_x >= 760) and not( table_1.y + table_1.size_y - ball.size_x/2 >= ball.y >= table_1.y - ball.size_x/2 ): #МИМО ПРАВО
        IsAway = True
        Ball.away("right")

    elif (ball.x <= 40) and not( table_2.y + table_2.size_y - ball.size_x/2 >= ball.y >= table_2.y - ball.size_x/2 ): #МИМО ЛЕВО
        IsAway = True
        Ball.away("left")


    #       Ball        #
    ball.y += ball.speed * ball.vectorY
    ball.x += ball.speed * ball.vectorX
    #       AI          #
    AI.main(table_2, ai)
    #AI(table_1)
    #       Blits       #
    if render:
        render()
    pygame.display.update()

while gameRunning:
    main_loop()
    #print("ball:  ", ball.x, ball.y, "table_1:  ", table_1.x, table_1.y, "table_2:  ", table_2.x, table_2.y)

pygame.quit()


