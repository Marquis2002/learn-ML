from envs.military_env import MilitaryEnv  # 假设这是你的环境类
from agents.rl_agent import DQNAgent  # 假设这是你的DQN智能体类


def main():
    # 环境和智能体的初始化
    env = MilitaryEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)

    episodes = 1000  # 总训练回合数
    batch_size = 32  # 经验回放的批次大小

    for e in range(episodes):
        state = env.reset()  # 重置环境状态
        state = np.reshape(state, [1, state_size])

        while True:
            action = agent.act(state)  # 根据当前状态选择动作
            next_state, reward, done, _ = env.step(action)  # 执行动作并获得新状态和奖励
            next_state = np.reshape(next_state, [1, state_size])

            agent.remember(state, action, reward, next_state, done)  # 存储经验

            state = next_state  # 更新状态

            if done:
                print(f"Episode: {e+1}/{episodes}, score: {reward}")
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)  # 经验回放

if __name__ == "__main__":
    main()
