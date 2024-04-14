import gymnasium as gym
from stable_baselines3 import A2C, PPO
env = gym.make('LunarLander-v2', render_mode='human')

# model = A2C('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps = 100)

model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps = 100)

episodes = 10
vec_env = model.get_env()
obs = vec_env.reset()

for ep in range(episodes):
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = vec_env.step(action)
        env.render()
        print(rewards)

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