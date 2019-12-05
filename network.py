import numpy as np
import random

class Network:
    def __init__(self, input_size):
        # setup value
        self.output = 0

        # setup size
        self.input_size = input_size
        self.hidden_sizes = [10, 8]
        self.output_size = 1
        self.sizes = [self.input_size]

        for i in self.hidden_sizes:
            self.sizes.append(i)
        self.sizes.append(self.output_size)

        self.W = [np.random.randn(self.sizes[i], self.sizes[i + 1]) for i in range(0, len(self.sizes) - 1)]
        self.fitness = 0

    def forward(self, inputs):
        a = inputs

        for i in range(0, len(self.sizes) - 1):
          z = np.dot(a, self.W[i])
          a = np.tanh(z)

        self.output = a

        return a

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def relu(self, z):
        return z * (z > 0)

    def get_decision(self):
        if self.output > 0:
            return False
        else:
            return True