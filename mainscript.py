import pygame, os, time, math
from random import randint

pygame.init()
pygame.font.init()

#Constants

disp_width = 800
disp_height = 600
display = pygame.display.set_mode((disp_width, disp_height))
myfont = pygame.font.SysFont('Arial', 30)
myfont_small = pygame.font.SysFont('Arial', 20)
FPS = 80
clock = pygame.time.Clock()
bg = pygame.image.load(os.path.join('Sprites\\bg.png')).convert_alpha()
vectorY = 0
vectorX = 1
ball_speed = 10 #6
ball_plus = 0.2
points_1 = 0
points_2 = 0
table_speed = 5 #3
start_pos = 240
y_cof = 1.0 # Угол отскока
r = 1

render = True
gameRunning = True
GameLvl = 2

class Plat:
    def __init__(self, img, x, y, size_x, size_y, points, speed, reb_counter, max_reb):
        self.img = img
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.points = points
        self.speed = speed
        self.reb_counter = reb_counter
        self.max_reb = max_reb

    def move_up(self):
        if (self.y ) >= 0:
            self.y += -self.speed

    def move_down(self):
        if (self.y + self.size_y) <= disp_height:
            self.y += self.speed
        
class Ball:
    def __init__(self, img, x, y, size_x, size_y, vectorX, vectorY, speed, table_1, table_2, IsAway, Wait):
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
        self.Wait = Wait
        self.max_speed = 0

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
        #print(ball_speed*self.vectorX, ball_speed*self.vectorY)
        self.IsAway = False
        self.Wait = False

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
        if self.speed > self.max_speed: self.max_speed = self.speed
        self.speed = ball_speed
        self.vectorY = 0
        self.table_1.y = start_pos
        self.table_2.y = start_pos

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
        display.blit(myfont_small.render("rebounds:  "+ str(self.table_1.reb_counter), False, (255, 0, 0)), (560, 5))
        display.blit(myfont_small.render("max:  " + str(self.table_1.max_reb), False, (255, 0, 0)), (700, 5))
        display.blit(myfont_small.render("speed:  " + str(round(self.speed, 2)), False, (255, 0, 0)), (560, 25))
        display.blit(myfont_small.render("max:  " + str(round(self.max_speed, 2)), False, (255, 0, 0)), (700, 25))
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
            self.NoCorrect = True
            self.correct = 300
            self.ball.IsAway = False
            self.ball.Wait = True

        elif self.ball.Wait:
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

                        #Коррекция
                        for i in range(10):
                            if self.correct > disp_height:
                                self.correct = abs(1200 - self.correct)

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

        #Deffence
        s = randint(-70, 70)
        if plat.y + plat.size_y/2 + s >= self.correct:
            plat.move_up()
        elif plat.y + plat.size_y/2 + s < self.correct:
            plat.move_down()

    def low_ai_main(self, plat, character):
        k = randint(-40, 40)
        #k = 0
        if plat.y + plat.size_y/2 + k >= self.ball.y: plat.move_up()
        elif plat.y + plat.size_y/2 + k < self.ball.y:  plat.move_down()
