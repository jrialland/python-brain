#!/usr/bin/env python2
# -*- coding : utf-8 -*-

import logging
import math
import random


__author__ = "Julien Rialland"
__copyright__ = "Copyright 2015, J.Rialland"
__license__ = "Apache License 2.0"
__version__ = "0.2"
__maintainer__ = __author__
__email__ = "julien.rialland@gmail.com"
__status__ = "Production"

def flatten(lst):
    for x in lst:
        if isinstance(x, list):
            for x in flatten(x):
                yield x
        else:
            yield x

class NeuralNetwork:

    def __init__(self, learningRate=0.3, momentum=0.1, hiddenLayers=4, binaryThresh=0.5):
        self.learningRate = learningRate
        self.momentum = momentum
        self.hiddenSizes = hiddenLayers
        self.binaryThresh = binaryThresh

    def _initialize(self, sizes):
        self.sizes = sizes
        self.outputLayer = len(self.sizes) - 1
        self.biases = []  # weights for bias nodes
        self.weights = []
        self.outputs = []

        # state for training
        self.deltas = [[] for _ in xrange(self.outputLayer + 1)]
        self.changes = [[] for _ in xrange(self.outputLayer + 1)]
        self.errors = [[] for _ in xrange(self.outputLayer + 1)]
        self.outputs = [[] for _ in xrange(self.outputLayer + 1)]
        self.biases = [[] for _ in xrange(self.outputLayer + 1)]
        self.weights = [[] for _ in xrange(self.outputLayer + 1)]

        for layer in xrange(self.outputLayer + 1):
            size = self.sizes[layer]
            self.deltas[layer] = [0 for _ in xrange(size)]
            self.errors[layer] = [0 for _ in xrange(size)]
            self.outputs[layer] = [0 for _ in xrange(size)]

            if layer > 0:
                self.biases[layer] = [
                    random.random() * 0.4 - 0.2 for _ in xrange(size)]
                self.weights[layer] = [0 for _ in xrange(size)]
                self.changes[layer] = [0 for _ in xrange(size)]

                for node in xrange(size):
                    prevSize = self.sizes[layer - 1]
                    self.weights[layer][node] = [
                        random.random() * 0.4 - 0.2 for _ in xrange(prevSize)]
                    self.changes[layer][node] = [0 for _ in xrange(prevSize)]

    def train(self, data, inputSize=None, outputSize=None, iterations=20000, errorThresh=0.005, logLevel=logging.DEBUG, log=False, logPeriod=10, learningRate=0.3, callback=None, callbackPeriod=10):
        if inputSize is None:
		inputSize = len(data[0][0])
	if outputSize is None:
        	outputSize = len(data[0][1])
        hiddenSizes = self.hiddenSizes
        if not hiddenSizes:
            hiddenSizes = [math.max(3, math.floor(inputSize / 2))]
        self._initialize(list(flatten([inputSize, hiddenSizes, outputSize])))
        error = 1
        done = 0
        for i in xrange(iterations):
            done = i
            if error <= errorThresh:
                break
            sum = 0
            for d in data:                
		err = self.trainPattern(d[0], d[1], learningRate)
                sum = sum + err
            error = sum / len(data)
            if log and i % logPeriod == 0:
                logging.log(logLevel, "iterations:{0}, training error: {1}".format(i, error))
            if callback is not None and i % callbackPeriod == 0:
                callback(error=error, iterations=i)
        return (error, done)

    def trainPattern(self, input, target, learningRate):
        # forward propogate
        self.run(input)
        # back propogate
        self._calculateDeltas(target)
        self._adjustWeights(learningRate)
        return self._mse(self.errors[self.outputLayer])

    def run(self, input):
        output = self.outputs[0] = input  # set output state of input layer

        for layer in xrange(1, self.outputLayer + 1):
            for node in xrange(self.sizes[layer]):
                weights = self.weights[layer][node]
                sum = self.biases[layer][node]
                for k in xrange(len(weights)):
                    sum += weights[k] * input[k]
                self.outputs[layer][node] = 1 / (1 + math.exp(-sum))
            input = self.outputs[layer]
            output = input
        return output

    def _calculateDeltas(self, target):
        layer = self.outputLayer
        while layer >= 0:
            for node in xrange(self.sizes[layer]):
                output = self.outputs[layer][node]
                error = 0
                if layer == self.outputLayer:
                    error = target[node] - output
                else:
                    deltas = self.deltas[layer + 1]
                    for k in xrange(len(deltas)):
                        error += deltas[k] * self.weights[layer + 1][k][node]
                self.errors[layer][node] = error
                self.deltas[layer][node] = error * output * (1 - output)
            layer -= 1

    def _adjustWeights(self, learningRate):
        for layer in xrange(1, self.outputLayer + 1):
            incoming = self.outputs[layer - 1]
            for node in xrange(self.sizes[layer]):
                delta = self.deltas[layer][node]
                for k in xrange(len(incoming)):
                    change = self.changes[layer][node][k]
                    change = learningRate * delta * \
                        incoming[k] + (self.momentum * change)
                    self.changes[layer][node][k] = change
                    self.weights[layer][node][k] += change
                self.biases[layer][node] += learningRate * delta

    def _mse(self, errors):
        sum = 0
        for err in errors:
            sum += math.pow(err, 2)
        return sum / len(errors)

__all__ = ['NeuralNetwork']
