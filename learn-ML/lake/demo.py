import numpy as np
import gymnasium as gym
import random
import imageio
import os
from tqdm import tqdm
import pickle
from tqdm.notebook import tqdm

env = gym.make("FrozenLake-v1", map_name='4x4', is_slippery=False, render_mode="human")
desc = ["SFFF", "FHFH", "FFFH", "HFFG"]
gym.make("FrozenLake-v1", desc=desc, is_slippery=False)

# Q-learning
state_space = env.observation_space.n
action_space = env.action_space.n


# print(state_space,action_space)

def initialize_q_table(state_space, action_space):
    Qtable = np.zeros((state_space, action_space))
    # Qtable = np.random.randint(4, size=(state_space, action_space))
    return Qtable


def greedy_policy(Qtable, state):
    action = np.argmax(Qtable[state][:])
    return action


def epsilon_greedy_policy(Qtable, state, epsilon):
    random_num = random.uniform(0, 1)
    if random_num > epsilon:
        # action = env.action_space.sample()

        action = greedy_policy(Qtable, state)
    else:
        action = env.action_space.sample()
        # print(action)
    return action


n_training_episodes = 100
learning_rate = 0.7
n_eval_episodes = 100
env_id = "FrozenLake-v1"
max_steps = 99
eval_seed = []

max_epsilon = 1.0
min_epsilon = 0.05
decay_rate = 0.0005


def train(n_training_episode, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable):
    """
    0-left 1-down 2-right 3-up
    """
    for episode in tqdm(range(n_training_episode)):
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        state, info = env.reset()
        step = 0
        terminated = False
        truncated = False

        for step in range(max_steps):
            action = epsilon_greedy_policy(Qtable, state, epsilon)
            new_state, reward, terminated, truncated, info = env.step(action)
            Qtable[state][action] = Qtable[state][action] + learning_rate * (
                    reward + np.max(Qtable[new_state]) - Qtable[state][action]
            )
            if terminated or truncated:
                break
            state = new_state
    return Qtable

def evaluate_agent(env, max_steps, n_eval_episode, Q, seed):
    episode_rewards = []
    for episode in tqdm(range(n_eval_episode)):
        if seed:
            state, info = env.reset(seed=seed[episode])
        else:
            state, info = env.reset()

        step = 0
        terminated = False
        truncated = False
        total_rewards_ep = 0

        for step in range(max_steps):
            action = greedy_policy(Q, state)
            new_state, reward, terminated, truncated, info = env.step(action)
            total_rewards_ep += reward

            if terminated or truncated:
                break
            state = new_state
        episode_rewards.append(total_rewards_ep)
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    return mean_reward, std_reward


Qtable_frozenlake = initialize_q_table(state_space, action_space)
Qtable_frozenlake = train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable_frozenlake)
mean_reward, std_reward = evaluate_agent(env, max_steps, n_eval_episodes, Qtable_frozenlake, eval_seed)

# print("obs space \n")
# print("obs space", env.observation_space)
# print("obs space sample", env.observation_space.sample())
#
# print("action space \n")
# print("action space", env.action_space)
# print("action space sample", env.action_space.sample())


#
# episodes = 10
# for episode in range(episodes):
#     done = False
#     obs = env.reset()
#     while True:
#         random_action = env.action_space.sample()
#         print('action', random_action)
#         obs, reward, done, info, _ =env.step(random_action)
#         print('reward', reward)
#         if done:
#           break

