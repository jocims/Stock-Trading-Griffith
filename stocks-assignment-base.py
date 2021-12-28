#!/usr/bin/python
#
# assignment that will get students to take the S&P 500 dataset and will apply numerical optimisation to it
# the objective here will be to generate the highest possible return on an initial investment in all stocks
# using the same provided weights.

# imports needed for this script to run
import struct
import math
from simanneal import Annealer
from deap import base
from deap import creator
from deap import tools
import random
import timeit


# class that will represent a stock frame
class StockFrame:
    # only constructor for this class
    def __init__(self, closing, volume, sma_ema, sma_ema_slope, sma_ema_curvature, profit_loss):
        self.closing = closing
        self.volume = volume
        self.sma_ema = sma_ema
        self.sma_ema_slope = sma_ema_slope
        self.sma_ema_curvature = sma_ema_curvature
        self.profit_loss = profit_loss

# helper function that will read in 8 floats and return a list containing them
# assumes that the file is already in the correct position for reading
def read8Floats(file):
    # return a list of 8 unpacked floats
    return list(struct.unpack('@8f', file.read(32)))

# function that will read in the preprocessed stock frames and will set them up in a list for access
def readPreprocessedData(filename):
    # the list of stock frames that will be returned
    stock_frames = []

    # open the file for reading and read in the number of stocks we have and the number of days
    # this will tell us how much data we will need to read
    to_read = open(filename, 'rb')
    num_days = struct.unpack('i', to_read.read(4))[0]
    num_stocks = struct.unpack('i', to_read.read(4))[0]

    # read in the stock frames. each stock has a frame for each day in the data
    for i in range(num_days):
        for j in range(num_stocks):
            # read in the closing value and volume traded of the stock on this day
            closing = struct.unpack('f', to_read.read(4))[0]
            volume = struct.unpack('i', to_read.read(4))[0]

            # read in the combined sma,ema values, their slope, and curvature
            sma_ema = read8Floats(to_read)
            sma_ema_slope = read8Floats(to_read)
            sma_ema_curvature = read8Floats(to_read)
            profit_loss = read8Floats(to_read)

            # generate a new stock frame and append it to the list
            stock_frames.append(StockFrame(closing, volume, sma_ema, sma_ema_slope, sma_ema_curvature, profit_loss))

    # close the file when we are finished and return the read in list of stock frames
    to_read.close()
    return stock_frames

# function that will read in the list of stock names and return it to the caller
def readStockNames():
    # open the file for reading, read in the lines, and close the file
    to_read = open('stock_names.txt', 'r')
    names = to_read.readlines()
    to_read.close()

    # go through each of the names in the list and remove the new line character at the end of it
    for i in range(len(names)):
        names[i] = names[i].rstrip()

    # return the list to the caller
    return names

# function that will be used for testing the portfolio itself to ensure it is working
# NOTE: uncomment for test to ensure your code is working correctly
def testPortfolio():
    # read in the stock data and the stock names
    start = timeit.default_timer()
    stock_frames = readPreprocessedData('preprocessed-stock-data-frames.dat')
    stock_names = readStockNames()
    elapsed = timeit.default_timer() - start
    print('Time taken to read in file (s)      :', elapsed)
    for i in range(10):
        print('Stock frames: ', stock_frames[i].profit_loss)

    # generate a portfolio. the values here are fixed as the data will not change
    #funds_per_stock = 2000.0
    #test_portfolio = Portfolio(505, 1259, funds_per_stock, stock_frames, stock_names, 10)
    #test_portfolio.updateBuyWeights([1.0] * 8)
    #test_portfolio.updateBuyThreshold(1.0)
    #test_portfolio.updateSellThreshold(0.0)

    # run the simulation and print out the total value of the portfolio before and after
    # start = timeit.default_timer()
    #test_portfolio.simulate()
    # elapsed = timeit.default_timer() - start
    # print('Time taken to simulate portfolio (s):', elapsed)
    #print('total of portfolio before simulation', funds_per_stock * 10)
    #print('total of portfolio after  simulation', test_portfolio.totalValue(1258))

# entry point ot the programme
if __name__ == '__main__':
    testPortfolio()
