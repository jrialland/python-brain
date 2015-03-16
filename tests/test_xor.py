import unittest

import brain


class XorTest(unittest.TestCase):

	def test(self):
		net = brain.NeuralNetwork()
		net.train([
		    ([0, 0], [0]),
		    ([0, 1], [1]),
		    ([1, 0], [1]),
		    ([1, 1], [0])
		])
		output = net.run([1, 0])
		self.assertTrue(output[0] > 0.9)