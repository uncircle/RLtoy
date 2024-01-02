import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time
import random

from items import Items
from item_config import item_properties as props


class EconomicEnv(gym.Env):
    def __init__(self, item_properties, total_duration=600):
        self.items = [Items(*p) for p in props]
        self.previous_prices = np.array([item.get_price() for item in self.items])
        self.inflation_threshold = 0.2
        # Box[i] means item i. Box[i][0] means time  Box[i][1] means amount, Box[i][2] means price
        self.observation_space = spaces.Box(low=0, high=float('inf'), shape=(len(self.items), 3), dtype=np.float32)
        # increase or decrease the amount of items, max 50
        self.action_space = spaces.Box(low=-50, high=50, shape=(len(self.items),), dtype=np.float32)

        self.total_duration = total_duration
        self.elapsed_time = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.elapsed_time = 0
        self.items = [Items(*p) for p in props]
        self.previous_prices = np.array([item.get_price() for item in self.items])
        return self._get_obs(), 0

    def _calculate_inflation(self, obs_pre, obs_cur):
        inflation = [False] * len(self.items)
        inflation_num = 0

        for i, item in enumerate(self.items):
            prev_price = obs_pre[i][2]
            cur_price = obs_cur[i][2]

            if int(prev_price) > 0:
                inflation_rate = (cur_price - prev_price) / prev_price
                if abs(inflation_rate) > self.inflation_threshold:
                    inflation[i] = True
                    inflation_num += 1
        return inflation, inflation_num

    def _get_obs(self):
        time_stamps = np.array([item.get_timestamp() for item in self.items]).reshape(-1, 1)
        quantities = np.array([item.get_amount() for item in self.items]).reshape(-1, 1)
        prices = np.array([item.get_price() for item in self.items]).reshape(-1, 1)
        obs = np.hstack((time_stamps, quantities, prices))
        return obs

    def _update(self):
        # time.sleep(1)
        self.elapsed_time += 1
        for item in self.items:
            if item.get_amount() != 0:
                item.set_price((500 + random.randint(-5, 50) * self.elapsed_time) / item.get_amount())

    def step(self, action):
        obs_prev = self._get_obs()
        print(obs_prev[:, -2:])
        # action
        print(action)
        for i, item in enumerate(self.items):
            if item.get_amount() > -action[i]:
                item.add_amount(action[i])
        self._update()
        obs_cur = self._get_obs()
        print(obs_cur[:, -2:])

        inflation, inflation_num = self._calculate_inflation(obs_prev, obs_cur)

        reward = -inflation_num if inflation_num > 0 else 1
        print(reward)
        done = self.elapsed_time >= self.total_duration
        return self._get_obs(), reward, done, False, {}


if __name__ == '__main__':
    env = EconomicEnv(props)
    print(env._get_obs()[:, -2:])
    env.reset()
    env.step(env.action_space.sample())
    print(env._get_obs())
    env.step(env.action_space.sample())
    print(env._get_obs())
    env.step(env.action_space.sample())
    print(env._get_obs())

