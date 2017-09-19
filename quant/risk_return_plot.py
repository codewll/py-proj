import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import random
import math
'''
Assume there is no correlation between any of two assets
'''

def getms(assets,weight):
    means = assets['means']
    stds = assets['stds']
    m = sum([ means[i]*weight[i] for i in range(len(means))])
    s = math.sqrt(sum([ (weight[i]**2)*(stds[i]**2) for i in range(len(means))]))
    return m,s

def gen_weight(sample_size, asset_num):
    random_weights = np.random.rand(sample_size,asset_num)
    weights = [[t for t in i] / sum(i) for i in random_weights]
    return weights

def rrplot(assets = None, sample_size = 1000):
    if assets == None:
        print("assets should contains at least one asset!")
        return
    else:
        weights = gen_weight(sample_size,len(assets['means']))
        mean = []
        std = []
        for i in range(sample_size):
            m,s = getms(assets,weights[i])
            mean.append(m)
            std.append(s)
        img = plt.scatter(std,mean)
        plt.xlabel('std')
        plt.ylabel('mean')
        plt.show(img)


if __name__ == '__main__':
    assets = {
        'means': [5,    15,     25,     35],
        'stds':  [15,    20,     25,    30]
    }
    rrplot(assets = assets, sample_size = 20000)