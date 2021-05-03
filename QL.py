import gym, numpy, pygame, os
from mainscript import Plat
import numpy as np
import mainscript

class Env(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(np.array((0, 0, 0, 0, -6, -3), dtype=float), #Ракетки Мяч Скорость по X, Скорость по Y
                                                np.array((600, 600, 600, 600, 6, 3), dtype=float)#Ракетки Мяч Скорость по X, Скорость по Y
                                                )
        self.plat_1 = mainscript.table_1
        self.plat_2 = mainscript.table_1

    def step(self, action):
        if action == 0:
            Plat.move_up(self.plat_1)
        elif action == 1:
            Plat.move_down(self.plat_1)
        elif action == 2:
            pass
        self.last_observation = np.array([mainscript.table_1.x, mainscript.table_1.y, mainscript.table_2.x, mainscript.table_2.y, mainscript.ball.x, mainscript.ball.y], dtype=float)
        reward = 10
        done = False
        info = {}

        return (self.last_observation, reward, done, info)

    def reset(self):
        res = np.array([760, 240, 400, 300, 0, -1 * mainscript.ball_speed], dtype=float) #6 координат начальных значений
        self.last_observation = res

        return res

    def render():
        pass

