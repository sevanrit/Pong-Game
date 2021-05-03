import mainscript, gym
from QL import Env
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = Env()

res = env.reset()
env.step(0)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=200000)
obs = env.reset()
for i in range(1000000):
  env.clock.tick(mainscript.FPS)
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()

