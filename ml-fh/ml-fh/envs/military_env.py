import gym
from gym import spaces
import numpy as np


class MilitaryEnv:
    def __init__(self):
        # 地图大小
        self.n_rows = 6
        self.n_cols = 9
        # 地图初始化
        self.map = np.full((self.n_rows, self.n_cols), '.', dtype=str)
        # 设置红方和蓝方基地
        self.red_bases = [(1, 2), (2, 1), (2, 2)]
        self.blue_bases = [(0, 6), (3, 7), (4, 6), (4, 7), (4, 8)]
        for base in self.red_bases:
            self.map[base] = '#'
        for base in self.blue_bases:
            self.map[base] = '*'
        # 战斗机初始位置和属性
        self.fighter_positions = [(0, 6), (3, 7), (4, 6)]
        self.fighter_fuel = [1000, 800, 900]  # 初始燃油
        self.fighter_missiles = [500, 300, 400]  # 初始导弹
        # 动作空间和状态空间
        self.action_space = ['up', 'down', 'left', 'right', 'attack', 'fuel', 'missile']
        self.state = self.map.copy()
        # 奖励
        self.score = 0

    def reset(self):
        # 重置环境状态
        self.__init__()
        return self.state

    def step(self, action):
        # 解析动作
        action_type, fighter_id, *params = action.split()
        fighter_id = int(fighter_id)
        done = False
        reward = 0
        info = {}

        if action_type == 'move':
            # 移动战斗机
            dir_map = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
            direction = params[0]
            if direction in dir_map:
                dx, dy = dir_map[direction]
                new_x = self.fighter_positions[fighter_id][0] + dx
                new_y = self.fighter_positions[fighter_id][1] + dy
                # 检查是否越界或进入敌方基地
                if 0 <= new_x < self.n_rows and 0 <= new_y < self.n_cols and self.map[new_x, new_y] != '#':
                    self.fighter_positions[fighter_id] = (new_x, new_y)
                    self.fighter_fuel[fighter_id] -= 1  # 假设每次移动消耗1单位燃油
                    reward += 1  # 假设每次移动获得1分奖励
                else:
                    info['error'] = 'Invalid move'
            else:
                info['error'] = 'Invalid direction'

        elif action_type == 'attack':
            # 攻击动作
            dir_map = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
            direction, missile_count = params
            missile_count = int(missile_count)
            if direction in dir_map and missile_count <= self.fighter_missiles[fighter_id]:
                dx, dy = dir_map[direction]
                target_x = self.fighter_positions[fighter_id][0] + dx
                target_y = self.fighter_positions[fighter_id][1] + dy
                # 检查是否攻击到敌方基地
                if (target_x, target_y) in self.red_bases:
                    self.fighter_missiles[fighter_id] -= missile_count
                    reward += missile_count * 10  # 假设每击中敌方基地获得10分奖励
                    # 这里可以添加更多逻辑，比如摧毁基地后的处理
                else:
                    info['error'] = 'Invalid attack target'
            else:
                info['error'] = 'Invalid attack parameters'

        elif action_type == 'fuel':
            # 加油动作
            fuel_amount = int(params[0])
            current_pos = self.fighter_positions[fighter_id]
            if self.map[current_pos] == '*':  # 检查是否在蓝方基地
                if fuel_amount <= self.blue_bases[current_pos]['fuel']:
                    self.fighter_fuel[fighter_id] += fuel_amount
                    self.blue_bases[current_pos]['fuel'] -= fuel_amount
                    reward += fuel_amount  # 假设加油也能获得奖励
                else:
                    info['error'] = 'Not enough fuel in base'
            else:
                info['error'] = 'Not at a blue base'

        elif action_type == 'missile':
            # 装弹动作
            missile_amount = int(params[0])
            current_pos = self.fighter_positions[fighter_id]
            if self.map[current_pos] == '*':  # 检查是否在蓝方基地
                if missile_amount <= self.blue_bases[current_pos]['missile']:
                    self.fighter_missiles[fighter_id] += missile_amount
                    self.blue_bases[current_pos]['missile'] -= missile_amount
                    reward += missile_amount * 2  # 假设装弹获得的奖励更高
                else:
                    info['error'] = 'Not enough missiles in base'
            else:
                info['error'] = 'Not at a blue base'

        else:
            pass
        # 更新状态
        self.state = self.map.copy()
        for pos in self.fighter_positions:
            self.state[pos] = 'F'

        # 检查游戏是否结束
        # ...

        return self.state, reward, done, info

    def render(self, mode='human'):
        # 可视化当前环境状态
        for row in self.map:
            print(' '.join(row))
        print()

    def close(self):
        # 清理环境资源（如果有的话）
        pass

