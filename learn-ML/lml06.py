import gymnasium as gym
from stable_baselines3 import A2C, PPO
import  os
import pickletools

models_dir = "models/PPO"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

env = gym.make('LunarLander-v2', render_mode='human')
env.reset()
model_path = f"{models_dir}/30.zip"
model = PPO.load(model_path, env=env)

vec_env = model.get_env()

episodes = 5
for ep in range(episodes):
    obs = vec_env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = vec_env.step(action)
        env.render()
        print(rewards)
#
#
# model = PPO('MlpPolicy', env, verbose=1)
# TIMESTEPS = 10
# iters = 0
# while True:
#     iters += 1
#
#     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
#     model.save(f"{models_dir}/{TIMESTEPS*iters}")

# model = A2C('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps = 100)

# model.learn(total_timesteps = 100)
#
# episodes = 10
# vec_env = model.get_env()
# obs = vec_env.reset()
#
# for ep in range(episodes):
#     done = False
#     while not done:
#         action, _states = model.predict(obs)
#         obs, rewards, done, info = vec_env.step(action)
#         env.render()
#         print(rewards)

# env.reset()
#
# for step in range(400):
#     env.render()
#
#     observation, reward, terminated, truncate, info = env.step(env.action_space.sample())
#     print(reward, terminated)
    # env.step(env.action_space.sample())


# print('sample action', env.action_space.sample())
#
# print('observation space shape', env.observation_space.shape)
#
# print('sample observation', env.observation_space.sample())

env.close()