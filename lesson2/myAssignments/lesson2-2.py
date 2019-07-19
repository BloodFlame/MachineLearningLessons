import matplotlib.pyplot as plt

from sklearn.datasets import load_boston
data = load_boston()
X = data['data']
Y = data['target']
# print(X)
# print(Y)

def draw_rm_and_price():
    plt.scatter(X[:,5], Y)

draw_rm_and_price()
plt.show()