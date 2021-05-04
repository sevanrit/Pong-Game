import mainscript
from QL import Env
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

env = Env()

res = env.reset()
env.step(0)
#model = PPO2(MlpPolicy, env, verbose=1)
#model.learn(total_timesteps=10000)
#model.save("models\\ppo2_1")
model = PPO2.load("models\\ppo2_1")
obs = env.reset()

while True:
  env.clock.tick(mainscript.FPS)
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()

