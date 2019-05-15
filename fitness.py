import numpy as np


def sphere(X):
    return np.sum([x**2 for x in X])

def rastrigin(X):
    sum_i = np.sum([x**2 - 10*np.cos(2 * np.pi * x) for x in X])
    return 10 * len(X) + sum_i

def rosenbrock(X):
    f = 0
    for i in range(1, len(X)-1):
        f += ((100 * ((X[i + 1] - (X[i]) ** 2) ** 2)) + (X[i] - 1) ** 2)
    return f