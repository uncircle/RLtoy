import gymnasium as gym

def foo1(arg=[]):
    arg.append(1)
    print(arg)

def foo2(arg=None):
    env = gym.make('CartPole-v1')
    print(type(env))




if __name__ == '__main__':
    foo2()

