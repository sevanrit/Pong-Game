import gym, pygame, os
from mainscript import Plat, Ball, AI
import numpy as np
import mainscript

class Env(gym.Env):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(np.array((0, 0, 0, 0, -6, -3), dtype=float), #Ракетки Мяч Скорость по X, Скорость по Y
                                                np.array((600, 600, 600, 600, 6, 3), dtype=float)#Ракетки Мяч Скорость по X, Скорость по Y
                                                )
        self.plat_1 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 760, mainscript.start_pos, 20, 100, mainscript.points_1, mainscript.table_speed)
        self.plat_2 = Plat(pygame.image.load(os.path.join('Sprites\\table.png')).convert_alpha(), 20, mainscript.start_pos, 20, 100, mainscript.points_2, mainscript.table_speed)
        self.ball = Ball(pygame.image.load(os.path.join('Sprites\\ball.png')).convert_alpha(), 400, 300, 16, 16, mainscript.vectorX, mainscript.vectorY, mainscript.ball_speed, self.plat_1, self.plat_2, False)
        self.ai = AI(self.ball)

    def step(self, action):

        reward = 0

        if action == 1 and (self.plat_1.y) >= 0:
            self.plat_1.move_up()
        if action == 2 and (self.plat_1.y + self.plat_1.size_y) <= mainscript.disp_height:
            self.plat_1.move_down()

        #       Collisions      #

        if self.ball.y + self.ball.size_y > mainscript.disp_height and self.ball.vectorY > 0:
            self.ball.collision_wall()
        if self.ball.y < 0 and self.ball.vectorY <= 0:
            self.ball.collision_wall()

        if (self.plat_1.y + self.plat_1.size_y - self.ball.size_x / 2 >= self.ball.y >= self.plat_1.y - self.ball.size_x / 2) and (
                self.ball.x + self.ball.size_x >= 760):
            self.ball.collision_plat(-1, self.plat_1)
            reward = 10

        if (self.plat_2.y + self.plat_2.size_y - self.ball.size_x / 2 >= self.ball.y >= self.plat_2.y - self.ball.size_x / 2) and (self.ball.x <= 40):
            self.ball.collision_plat(1, self.plat_2)
            reward = -20

        elif (self.ball.x + self.ball.size_x >= 760) and not (
                self.plat_1.y + self.plat_1.size_y - self.ball.size_x / 2 >= self.ball.y >= self.plat_1.y - self.ball.size_x / 2):  # МИМО ПРАВО
            self.ball.IsAway = True
            self.ball.away("right")
            reward = -100

        elif (self.ball.x <= 40) and not (
                self.plat_2.y + self.plat_2.size_y - self.ball.size_x / 2 >= self.ball.y >= self.plat_2.y - self.ball.size_x / 2):  # МИМО ЛЕВО
            self.ball.IsAway = True
            self.ball.away("left")
            reward = 10000

        self.last_observation = np.array(
            [self.plat_1.x, self.plat_1.y, self.plat_2.x, self.plat_2.y, self.ball.x, self.ball.y],
            dtype=float)
        done = False
        info = {}

        #       Ball        #
        self.ball.y += self.ball.speed * self.ball.vectorY
        self.ball.x += self.ball.speed * self.ball.vectorX
        #       AI          #
        self.ai.main(self.plat_2, self.ai)

        return (self.last_observation, reward, done, info)

    def reset(self):
        self.ball.reset()
        res = np.array([self.plat_1.y, self.plat_2.y, self.ball.x, self.ball.y, self.ball.vectorX * mainscript.ball_speed, self.ball.vectorY * mainscript.ball_speed], dtype=float) #Ракетка 1 Y Ракетка 2 Y
        self.last_observation = res

        return res

    def render(self, mode='human'):
        self.ball.render()

