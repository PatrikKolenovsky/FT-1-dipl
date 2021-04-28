import numpy as np

import matplotlib.pyplot as plt

x = np.arange(0, 2 * np.pi, 0.1)  # start,stop,step
y = np.sin(x)

points = []
plt.xlabel('x values from 0 to 2pi')  # string must be enclosed with quotes '  '
plt.ylabel('sin(x)')
plt.title('Plot of sin from 0 to 2pi')
# 1/6 pi a 2/6 pi
plt.plot(points, 'ko', color="red", markersize=5, label="1/6 Pi")
plt.plot(points, 'ko', color="blue", markersize=5, label="2/6 Pi")
plt.plot(x, y, label="Sine")
plt.legend()

plt.show()
