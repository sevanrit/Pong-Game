import mainscript
from QL import Env
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = Env()
res = env.reset()
env.step(0)

steps = 10 * 10**3
model = PPO2(MlpPolicy, env, verbose=0) #verbose = 1 отображает на экран
model.learn(total_timesteps=steps)
model.save("models\\ppo2_1")

#model = PPO2.load("models\\PPO_001")
obs = env.reset()

while True:
  env.clock.tick(mainscript.FPS)
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()

