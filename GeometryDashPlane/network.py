import numpy as np
import random

class Network:
    def __init__(self):
        # 사이즈 설정
        self.input_size = 8
        self.hidden_sizes = [8, 4]
        self.output_size = 1
        self.output = 0
        # 총 사이즈 배열
        self.sizes = [self.input_size]
        for i in self.hidden_sizes:
            self.sizes.append(i)
        self.sizes.append(self.output_size)
        print(self.sizes)
        
        self.W = [np.random.randn(self.sizes[i], self.sizes[i+1]) for i in range(0,len(self.sizes) - 1)]
        print(self.W)
        self.fitness = 0

    def forward(self, inputs):
        a = inputs
        for i in range(0,len(self.sizes) - 1):
          z = np.dot(a, self.W[i])
          a = np.tanh(z)
    #      print(z)
    #      print("z")
    #      print(a)
    #      print("a")
        self.output = a
        return a

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def relu(self, z):
        return z * (z > 0)

    def get_decision(self):
        self.fitness += 1
        
        if self.output < 0:
            return False
        else:
            return True
