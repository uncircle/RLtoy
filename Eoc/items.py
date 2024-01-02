import time
import random
import numpy as np
from item_config import item_properties as props


class Items:
    def __init__(self, name, amount, price):
        self._timestamp = int(time.time())
        self._amount = amount
        self._price = price
        self._name = name
        # self.reset()

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def get_timestamp(self):
        return self._timestamp

    def add_amount(self, n):
        if self._amount + n <= 0:
            self._amount = 0
        self._amount += n

    def get_amount(self):
        return self._amount

    def add_price(self, n):
        if self._price + n <= 0:
            self._price = 0
        self._price += n

    def info(self):
        print(f'TS:{self.get_timestamp()}, '
              f'Name: {self.get_name()}, Amount: {self.get_amount()}, '
              f'Price:{self.get_price()}')
        return self.get_timestamp(), self.get_name(), self.get_amount(), self.get_price()


if __name__ == '__main__':

    items = [Items(*props) for props in props]

    while True:
        time.sleep(0.5)
        elapsed_time = 1
        for item in items:
            if item.get_amount() != 0:
                item.add_price((500 + random.randint(-5, 50) * elapsed_time) / item.get_amount())
            elapsed_time += 1
            # print(item.get_price())
        time_stamps = np.array([item.get_timestamp() for item in items]).reshape(-1, 1)
        quantities = np.array([item.get_amount() for item in items]).reshape(-1, 1)
        prices = np.array([item.get_price() for item in items]).reshape(-1, 1)
        obs = np.hstack((time_stamps,quantities, prices))
        print(obs)
        print('========')

