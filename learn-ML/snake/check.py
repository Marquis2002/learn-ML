from stable_baselines3 import PPO
from snakeenv import SnekEnv

env  = SnekEnv()
episodes = 50
# model = PPO ('MlpPolicy', env, verbose=1)
# model.learn(total_timesteps = 100)
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


for episodes in range(episodes):
    done = False
    obs = env.reset()
    while True:
        random_action = env.action_space.sample()
        print('action', random_action)
        obs, reward, done, info = env.step(random_action)
        print('reward', reward)


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