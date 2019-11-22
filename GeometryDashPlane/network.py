import numpy as np

class Network:
    def __init__(self):
        # 사이즈 설정
        self.input_size = 2
        self.hidden_sizes = [8, 4]
        self.output_size = 1
        
        # 총 사이즈 배열
        self.sizes = self.input_size
        self.sizes.append(self.hidden_sizes)
        self.sizes.append(self.output_size)
        
        self.W = [[np.random.randn(self.sizes[i], self.sizes[i+1])] for i in range(0,len(self.sizes) - 1)]

        self.fitness = 0

    def forward(self, inputs):
        a = inputs
        for i in range(0,len(self.sizes) - 1):
          z = np.dot(a, self.W[i])
          a = np.tanh(z)
        return a

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def relu(self, z):
        return z * (z > 0)

    def get_decision(self):
        output = self.forward()
        if output < 0: return False
        else: return True
