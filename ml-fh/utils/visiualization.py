import gym
from agents.rl_agent import RLAgent
import time


def visualize(agent, env, num_episodes):
    """可视化智能体的表现"""
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        step = 0

        while not done:
            env.render()  # 渲染环境
            time.sleep(0.05)  # 控制渲染速度
            action = agent.choose_action(state)
            state, reward, done, _ = env.step(action)
            total_reward += reward
            step += 1

        print(f"Episode: {episode + 1}, Total Reward: {total_reward}, Steps: {step}")
        time.sleep(1)  # 在每个回合之间暂停

    env.close()


def main():
    env = gym.make('CartPole-v1')  # 创建环境
    agent = RLAgent(env.action_space)  # 初始化智能体

    # 假设agent已经训练好了，这里我们只是演示可视化
    # 如果需要，可以在这里加载智能体的状态

    num_episodes = 5  # 设置可视化的回合数
    visualize(agent, env, num_episodes)  # 开始可视化


if __name__ == "__main__":
    main()
