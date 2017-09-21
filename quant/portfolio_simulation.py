from numba import jit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

@jit
def gen_return(ret = 0.01,risk = 1.0, sample_number = 1000):
    '''
    generate a asset's price history, ret and risk is the expected return rate and
    risk rate of the next price change on condition of the current price.
    '''
    Y = np.random.normal(loc=ret, scale=risk, size=sample_number)
    return np.cumsum(Y)

@jit
def portfolio_sim(assets_number,sample_number):
    '''
    print the price of a protfolio of some simulated assets, each asset is average weighted.
    And each asset's price is indenpendent, so the correlation coefficient is zero.
    '''
    yy = np.zeros(sample_number)
    for i in range(assets_number):
        yi = gen_return(sample_number=sample_number)
        yy = yy + yi
    yy = yy/assets_number
    pic = plt.plot(yy)
    plt.show(pic)


if __name__ == '__main__':
    portfolio_sim(10,2000)
    portfolio_sim(50,2000)
    portfolio_sim(200,2000)