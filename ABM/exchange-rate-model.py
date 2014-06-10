__author__ = 'lfi'

import matplotlib.pyplot as plt
from numpy import mean


def extrapolative_expectations():
    g = 0.05
    s = list()
    s.append(1.0)
    s.append(1.1)
    for i in range(2, 100):
        s.append((1-g) * s[-1] + g * s[-2])
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    ax.plot(s, 'ok')
    ax.set_xlabel("Time")
    ax.set_ylabel("s")
    plt.show()


def mean_reverting_expectations():
    g = 0.05
    s = list()
    s.append(1.0)
    s.append(1.1)
    for i in range(2, 100):
        s.append((1-g) * s[-1] + g * mean(s))
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    ax.plot(s, 'ok')
    ax.set_xlabel("Time")
    ax.set_ylabel("s")
    plt.show()

if __name__ == '__main__':
    extrapolative_expectations()
