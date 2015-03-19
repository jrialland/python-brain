python-brain
============

This is a lightweight [neural network](http://en.wikipedia.org/wiki/Artificial_neural_network) library for Python.

Its implementation is deeply inspired by ![harthur/brain](https://github.com/harthur/brain).

## Simple example : reinvent XOR

Here's an example of using it to approximate the XOR function using a neural network (which is completely useless :) ):

```python
from brain import NeuralNetwork

net = NeuralNetwork()

#train the network with the real behavior of the XOR function
net.train([
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1]),
    ([1, 1], [0])
])

#present parameters to the trained nn
output = net.run([1, 0])

print output[0]  #prints [0.987]
```

## Training
Use the `NeuralNetwork.train` method to train the network with an array of training data. The network has to be trained with all the data in bulk in one call to `train()`. The more training patterns, the longer it will probably take to train, but the better the network will be at classifiying new patterns.

#### Data format
Each training data should be a 2-tuple containing the `input` and `output` vectors as arrays.

#### Constructor Options
`NeuralNetwork.__init__` takes the following optional arguments:

```python
net = NeuralNetwork(
  hiddenLayers= [4],
  learningRate= 0.6 # global learning rate, useful when training using streams
)
```

#### hiddenLayers
Specify the number of hidden layers in the network and the size of each layer. For example, if you want two hidden layers - the first with 3 nodes and the second with 4 nodes, you'd give:

```
hiddenLayers = [3, 4]
```

By default `brain` uses one hidden layer with size proportionate to the size of the input array.


#### Options
`NeuralNetwork.train` may take options as extra arguments:

```javascript
net.train(data,
  errorThresh = 0.005,  # error threshold to reach
  iterations = 20000,   # maximum training iterations
  logLevel = logging.DEBUG # logging level
  log= False,           # logging.log() progress periodically
  logPeriod= 10,       # number of iterations between logging
  learningRate= 0.3    # learning rate
)
```

The network will train until the training error has gone below the threshold (default `0.005`) or the max number of iterations (default `20000`) has been reached, whichever comes first.

By default training won't let you know how its doing until the end, but set `log` to `true` to get periodic updates on the current training error of the network. The training error should decrease every time.

The learning rate is a parameter that influences how quickly the network trains. It's a number from `0` to `1`. If the learning rate is close to `0` it will take longer to train. If the learning rate is closer to `1` it will train faster but it's in danger of training to a local minimum and performing badly on new data. The default learning rate is `0.3`.


#### Output
The output of `train()` is a 2-tuple of information about how the training went:

```python
error, iterations = net.train(data)
print error # 0.0039139985510105032, training error
print iterations # 406, training iterations

```

#### Failing
If the network failed to train, the error will be above the error threshold. This could happen because the training data is too noisy (most likely), the network doesn't have enough hidden layers or nodes to handle the complexity of the data, or it hasn't trained for enough iterations.

If the training error is still something huge like `0.4` after 20000 iterations, it's a good sign that the network can't make sense of the data you're giving it.

#### standalone python function generation

the `to_function()` method allow you to generate the code of a python method, in case you want to use the behavior of the neural network without embedding the whole library in your project.

In this case you have off course to train the network first, and then export the code :

```python
data = ...
net.train(data)

with file('network.py', 'w') as py:
    py.write(net.to_function('compute_xor'))
```

will generate a network.py script that contains this function : 

```
def compute_xor(i):
    _ = [[], [[-1.3119472186677905, -1.2384811465229646], [-3.4230557744462367, -3.4484088435033957], [-5.9067190819809525, -5.954567420970833], [-0.8994263270628542, -1.0289344868371122]], [[2.1467495993089245, 6.54855247054587, -8.31269196871394, 0.6158671463050152]]]
    o = [i]
    for l in range(1, 3):
        o.append([])
        for n in range([2, 4, 1][l]):
            sum = [[], [1.136422369063891, 4.972469523292342, 2.205335929913742, -0.6381812202917794], [-3.654432844073631]][l][n]
            for k in range(len(_[l][n])):
                sum += _[l][n][k] * i[k]
            o[-1].append(1 / (1 + math.exp(-sum)))
        i = o[l]
    return o[-1]
```

This function uses the neural network that was trained, without any dependency to the python-brain library itself, which allows you to include such generated code in your project.
