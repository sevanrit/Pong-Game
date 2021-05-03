import pygame, os, time, math
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

render = True
gameRunning = True
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

    def move_up(self):
        if (self.y ) >= 0:
            self.y += -self.speed

    def move_down(self):
        if (self.y + self.size_y) <= disp_height:
            self.y += self.speed
        
class Ball:
    def __init__(self, img, x, y, size_x, size_y, vectorX, vectorY, speed, table_1, table_2, IsAway):
        self.img = img
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.vectorX = vectorX
        self.vectorY = vectorY
        self.speed = speed
        self.table_1 = table_1
        self.table_2 = table_2
        self.IsAway = IsAway


    def correction_speed(vector_x, vector_y):
        if vector_y > 1:
            vector_x *= 1/vector_y
            vector_y = 1
        if vector_y < -1:
            vector_x *= 1/abs(vector_y)
            vector_y = -1
        
        return vector_x, vector_y
    
    def correction_sqrt(self, vector_x, vector_y):
        t = 1
        if vector_x < 0: t = -1
        vector_x = math.sqrt(abs(1**2 - vector_y**2)) * t

        return vector_x, vector_y

    def collision_plat(self, vectorX_num, plat):
        global IsAway
        
        IsAway = False
        self.vectorX = vectorX_num
        if GameLvl == 2:
            self.speed += ball_plus
        else:
            self.speed = ball_speed
        ball_center = self.y + self.size_y/2
        #ball.vectorY = (((ball.y - plat.y) / 50) - 1)*y_cof
        cf = ball_center - plat.y
        self.vectorY = (cf - 50) * 0.01
        self.vectorX, self.vectorY = self.correction_sqrt(self.vectorX, self.vectorY)
        print(ball_speed*self.vectorX, ball_speed*self.vectorY)

    def collision_wall(self):
        self.vectorY = self.vectorY * -1
        #ball.speed += ball_plus

    def away(self, direction):
        if direction == "right":
            self.x = 100
            self.vectorX = 1
            self.table_1.points += 1
        elif direction == "left":
            self.x = 700
            self.vectorX = -1
            self.table_2.points += 1
        self.y = 300
        self.speed = ball_speed
        self.vectorY = 0
        self.table_1.y = start_pos
        self.table_2.y = start_pos
        self.IsAway = False

    def reset(self):
        self.x = 400
        self.vectorX = -1
        self.y = 300
        self.speed = ball_speed
        self.vectorY = 0
        self.table_1.y = start_pos
        self.table_2.y = start_pos


    def render(self):
        display = pygame.display.set_mode((disp_width, disp_height))
        display.blit(bg, (0, 0))
        display.blit(self.table_1.img, (self.table_1.x, self.table_1.y))
        display.blit(self.table_2.img, (self.table_2.x, self.table_2.y))
        display.blit(self.img, (self.x, self.y))
        display.blit(myfont.render(str(self.table_1.points), False, (255, 255, 255)), (360, 10))
        display.blit(myfont.render(str(self.table_2.points), False, (255, 255, 255)), (440, 10))
        pygame.display.update()
    
class AI:
    def __init__(self, ball):
        self.size_y = None
        self.y = None
        self.t = 0
        self.frames_dif = [[400, 300]]
        self.predict = []
        self.NoCorrect = True
        self.correct = 300
        self.ball = ball

    def trend(self):
        if self.ball.IsAway:
            print(1)
            self.NoCorrect = True
            self.correct = 300
        
        elif self.ball.vectorX < 0:
            
            if time.perf_counter() - self.t >= 0.01:
                self.frames_dif.append([self.ball.x, self.ball.y])
                x = self.frames_dif[1][0] - self.frames_dif[0][0]
                y = self.frames_dif[1][1] - self.frames_dif[0][1]
                
                if len(self.predict) < 2:
                    self.predict.append([x, y])
                else:
                    y = self.predict[1][1]
                    x = self.predict[1][0]
                    if self.NoCorrect:
                        if x == 0: x = 1
                        ball_way = abs((self.ball.x-40)/x)
                        ball_const_y = self.ball.y
                        self.correct = abs(ball_const_y + ball_way * y)
                        #print(ai.corect, ball_way, ball_const_y, y, x)

                        #Коррекция
                        for i in range(10):
                            if self.correct > disp_height:
                                self.correct = abs(1200 - self.correct)
                        
 
                        #print(ai.corect)
                        self.NoCorrect = False
                        return self.correct

                self.t = time.perf_counter()
                self.frames_dif = [[self.ball.x, self.ball.y]]
                
        else:
            self.predict = []
            self.NoCorrect = True
            self.correct = 300

    def main(self, plat, character):
        AI.trend(character)

        # Attack
        """
        if (self.ball.x < 100) and (plat.y + plat.size_y > self.ball.y > plat.y):
            if not Strategy:
                #r = randint(1, 3)
                r = 3
                Strategy = True
            if plat.y + plat.size_y/2 + 50 >= self.correct and r == 1: plat.move_up()
            if plat.y + plat.size_y / 2 - 50 >= self.correct and r == 2: plat.move_up()
            if plat.y + plat.size_y / 2 >= self.correct and r == 3: plat.move_up()
        """

        #Deffence
        if plat.y + plat.size_y/2 >= self.correct: plat.move_up()
        elif plat.y + plat.size_y/2 < self.correct:  plat.move_down()

#                       #

#table_1 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 760, start_pos, 20, 100, points_1, table_speed)
#table_2 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 20, start_pos, 20, 100, points_2, table_speed)
#ball = Ball(pygame.image.load(os.path.join('Sprites\\ball.png')).convert_alpha(), 400, 300, 16, 16, vectorX, vectorY, ball_speed)
#ai = AI()

#                       #
"""
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
        Ball.render()
    pygame.display.update()

while gameRunning:
    main_loop()
    #print("ball:  ", ball.x, ball.y, "table_1:  ", table_1.x, table_1.y, "table_2:  ", table_2.x, table_2.y)

pygame.quit()

"""
