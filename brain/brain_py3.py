# -*- coding:utf-8 -*-

import logging
import math
import random
import pickle
import zlib
import base64


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
        self.deltas = [[]] * (self.outputLayer + 1)
        self.changes = [[]] * (self.outputLayer + 1)
        self.errors = [[]] * (self.outputLayer + 1)
        self.outputs = [[]] * (self.outputLayer + 1)
        self.biases = [[]] * (self.outputLayer + 1)
        self.weights = [[]] * (self.outputLayer + 1)

        for layer in range(self.outputLayer + 1):
            size = self.sizes[layer]
            self.deltas[layer] = [0] * size
            self.errors[layer] = [0] * size
            self.outputs[layer] = [0] * size

            if layer > 0:
                self.biases[layer] = [
                    random.random() * 0.4 - 0.2 for _ in range(size)]
                self.weights[layer] = [0] * size
                self.changes[layer] = [0] * size

                for node in range(size):
                    prevSize = self.sizes[layer - 1]
                    self.weights[layer][node] = [
                        random.random() * 0.4 - 0.2 for _ in range(prevSize)]
                    self.changes[layer][node] = [0] * prevSize

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
        for i in range(iterations):
            done = i
            if error <= errorThresh:
                break
            sum = 0
            for d in data:
                err = self.trainPattern(d[0], d[1], learningRate)
                sum = sum + err
            error = sum / len(data)
            if log and i % logPeriod == 0:
                logging.log(
                    logLevel, "iterations:{0}, training error: {1}".format(i, error))
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
        for layer in range(1, self.outputLayer + 1):
            for node in range(self.sizes[layer]):
                weights = self.weights[layer][node]
                sum = self.biases[layer][node]
                for k in range(len(weights)):
                    sum += weights[k] * input[k]
                self.outputs[layer][node] = 1 / (1 + math.exp(-sum))
            input = self.outputs[layer]
            output = input
        return output

    def dump(self):
        return base64.b64encode(zlib.compress(pickle.dumps(self), 9))

    @staticmethod
    def load(s):
        return pickle.loads(zlib.decompress(base64.b64decode(s)))

    def _calculateDeltas(self, target):
        layer = self.outputLayer
        while layer >= 0:
            for node in range(self.sizes[layer]):
                output = self.outputs[layer][node]
                error = 0
                if layer == self.outputLayer:
                    error = target[node] - output
                else:
                    deltas = self.deltas[layer + 1]
                    for k in range(len(deltas)):
                        error += deltas[k] * self.weights[layer + 1][k][node]
                self.errors[layer][node] = error
                self.deltas[layer][node] = error * output * (1 - output)
            layer -= 1

    def _adjustWeights(self, learningRate):
        for layer in range(1, self.outputLayer + 1):
            incoming = self.outputs[layer - 1]
            for node in range(self.sizes[layer]):
                delta = self.deltas[layer][node]
                for k in range(len(incoming)):
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

    def _indent(self, txt, chars):
        result = ''
        d = ' ' * chars
        for line in txt.split('\n'):
            result += d + line + '\n'
        return result

    def to_function(self, fnname='nn_run', indent=0):
        fn = 'def {fnname}(i):\n'.format(fnname=fnname)
        for l in range(1, self.outputLayer + 1):
            if l < self.outputLayer:
                fn += '    o = [\n'
            else:
                fn += '    return [\n'
            size = self.sizes[l]
            for n in range(size):
                term = str(-self.biases[l][n])
                length = len(self.weights[l][n])
                for k in range(length):
                    w = self.weights[l][n][k]
                    term = term + ('-' if w > 0 else '+') + \
                        str(abs(w)) + '*i[' + str(k) + ']'
                fn += '        1/(1+math.exp(' + term + '))' + \
                    (',' if n != size - 1 else '') + '\n'
            fn += '    ]\n'
            if l != self.outputLayer:
                fn += '    i = o\n'
        return self._indent(fn, indent)

    def to_java_method(self, fnname='nn_run', static=False, scope='protected', indent=4):
        fn = scope + (' static ' if static else ' ') + \
            'double[] {fnname}(double[] i)'.format(fnname=fnname) + '{\n'
        fn += '    double[] o;\n'
        for l in range(1, self.outputLayer + 1):
            if l < self.outputLayer:
                fn += '    o = new double[]{\n'
            else:
                fn += '    return new double[]{\n'
            size = self.sizes[l]
            for n in range(size):
                term = str(-self.biases[l][n])
                length = len(self.weights[l][n])
                for k in range(length):
                    w = self.weights[l][n][k]
                    term = term + ('-' if w > 0 else '+') + \
                        str(abs(w)) + '*i[' + str(k) + ']'
                fn += '        1/(1+Math.exp(' + term + '))' + \
                    (',' if n != size - 1 else '') + '\n'
            fn += '    };\n'
            if l != self.outputLayer:
                fn += '    i = o;\n'
        fn += '}'
        return self._indent(fn, indent)

    def to_c_function(self, fnname='nn_run', indent=0):
        fn = 'void {fnname}(double *i, double *o)'.format(fnname=fnname) + \
            '{\n'
        terms = {}
        oterms = {}
        lterms = []
        for k in range(self.sizes[0]):
            lterms.append('o0_' + str(k))
            terms[lterms[-1]] = 'i[' + str(k) + ']'
        for l in range(1, self.outputLayer + 1):
            size = self.sizes[l]
            for n in range(size):
                term = str(-self.biases[l][n])
                length = len(self.weights[l][n])
                for k in range(length):
                    w = self.weights[l][n][k]
                    term = term + ('-' if w > 0 else '+') + \
                        str(abs(w)) + '*o' + str(l - 1) + '_' + str(k)
                v = '(1/(1+exp(' + term + ')))'
                for k in lterms:
                    v = v.replace(k, terms[k])
                lterms.append('o' + str(l) + '_' + str(n))
                terms[lterms[-1]] = v
                if l == self.outputLayer:
                    oterms['o' + str(l) + '_' + str(n)] = 'o[' + str(n) + ']'
        # for t in lterms:
        #    if not t in oterms:
        #        fn += '    double '+t+'='+terms[t]+';\n'
        #    else:
        #        fn += '    ' + oterms[t]+' = ' + terms[t]+';\n'
        for k, v in oterms.items():
            fn += '    ' + v + ' = ' + terms[k] + ';\n'
        fn += '}\n'
        return self._indent(fn, indent)
