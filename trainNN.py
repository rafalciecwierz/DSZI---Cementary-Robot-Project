import numpy as np
from numpy import genfromtxt

X = np.array((), dtype=float)
y = np.array((), dtype=float)

dane = genfromtxt('decisiontreeTrainingSetMedium.csv', delimiter=';', dtype=float)

dane = np.delete(dane, (0), axis=0)

#For predictions purpoes only
xPredicted = np.array(([1, 1, 2, 2]), dtype=float)
xPredicted = xPredicted / np.amax(xPredicted, axis=0)


X = dane
y = dane
X = np.delete(X, (4), axis=1)
y = np.delete(y, (0,1,2,3), axis=1)

# scale units
X = X / np.amax(X, axis=0)
y = y/40

class Neural_Network(object):
  def __init__(self):
    #parameters
    self.inputSize = 4
    self.outputSize = 1
    self.hiddenSize = 3

    #weights
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize) # (3x4) weight matrix from input to hidden layer
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer

  def forward(self, X):
    #forward propagation through our network
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x4 weights
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
    o = self.sigmoid(self.z3) # final activation function
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def predict(self):
      print ("Predicted data based on trained weights: ")
      print ("Input (scaled): \n" + str(xPredicted))
      print("Output: \n" + str(self.forward(xPredicted)))


  def backward(self, X, y, o):
    # backward propgate through the network
    self.o_error = y - o # error in output - margines błędu warstwy wyjściowej (o), przyjmując różnicę przewidywanego wyjścia i rzeczywistego wyniku (y)
    self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error
    #Zastosowanie pochodnej naszej sigmoidalnej funkcji aktywacji do błędu warstwy wyjściowej.
    #Wynik ten nazywamy sumą wyjściową delty.

    self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
    #Suma wyjściowej delta błędu warstwy wyjściowej. Dowiadujemy się, jak bardzo nasza warstwa z2 (ukryta) przyczyniła się do błędu wyjściowego,
    # wykonując produkt dot z naszą drugą macierzą wagową. Możemy nazwać to błędem z2.

    self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error
    #Oblicz sumę wyjściową delta dla warstwy z2, stosując pochodną naszej sigmoidalnej funkcji aktywacji (podobnie jak krok 2).

    self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
    self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights
    #Dostosuj wagi dla pierwszej warstwy, wykonując iloczyn skalarny warstwy wejściowej z ukrytą sumą wyjściową delta (z2).
    #  W przypadku drugiej warstwy należy wykonać iloczyn kropki warstwy ukrytej (z2) i sumy wyjściowej delta wyjściowego (o).


  def train (self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)

  def saveWeights(self):
      np.savetxt("w1.txt", self.W1, fmt="%s")
      np.savetxt("w2.txt", self.W2, fmt="%s")


NN = Neural_Network()
for i in range(1000): # trains the NN 1,000 times
  print("Input: \n" + str(X))
  print("Actual Output: \n" + str(y))
  print("Predicted Output: \n" + str(NN.forward(X)))
  print("Loss: \n" + str(np.mean(np.square(y - NN.forward(X))))) # mean sum squared loss
  print("\n")
  NN.train(X, y)

def getPriorityN(tomb):
    return int(NN.forward([tomb])*1000)

NN.saveWeights()
NN.predict()
print(getPriorityN(xPredicted))


