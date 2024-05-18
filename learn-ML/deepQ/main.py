import gymnasium as gym
from qlearn import Agent
from myutils import plotLearning
import numpy as np
import torch
import pickle

# Load save

def save_agent(agent, filename):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

def load_agent(filename):
    with open(filename, 'rb') as f:
        agent = pickle.load(f)

    return agent

if __name__ == '__main__':
    env = gym.make('LunarLander-v2', render_mode='human')
    agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=4, eps_end=0.01, input_dims=[8], lr=0.001)
    scores, eps_history = [], []
    n_games = 50
    for i in range(n_games):
        score = 0
        done = False
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, truncated, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)

            agent.learn()
            observation = observation_

        scores.append(score)
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[-100:])

        print('episode', i,  'score %2f' % score,
              'avg score %.2f' % avg_score)

    x = [i + 1 for i in range(n_games)]
    save_agent(agent, 'agent_demo.pk1')
    filename = 'lunar_train.png'
    plotLearning(x, scores, eps_history, filename)