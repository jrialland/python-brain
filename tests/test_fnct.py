import unittest
import brain

class FnctTest(unittest.TestCase):

	def test(self):
		net = brain.NeuralNetwork()
		net.train([
		    ([0, 0], [0]),
		    ([0, 1], [1]),
		    ([1, 0], [1]),
		    ([1, 1], [0])
		])
		print(net.to_function('test_nn'))