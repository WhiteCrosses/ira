import numpy as np
import matplotlib.pyplot as plt
import time

# create initial data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(X)

# create initial data for the second plot
x2 = np.linspace(-5, 5, 100)
y2 = np.sin(x2)



# create the plot
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 4))
cax = ax.imshow(Z, cmap='viridis', extent=[-5, 5, -5, 5])
cbar = fig.colorbar(cax)
ax.set_xlabel('X')
ax.set_ylabel('Y')
cbar.set_label('Z')
ax.set_title('2D Plot Updating Every Second')

# create the second plot
cax2 = ax2.plot(x2, y2)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('2D Plot Updating Every Second (Z2)')



# update the plot every second
while True:
    Z = np.sin(time.time() + Y) * np.sin(X + Y)
    cax.set_data(Z)

    # update the second plot
    y2 = np.sin(x2 + time.time())
    cax2 = ax2.clear()
    cax2 = ax2.plot(x2, y2)

    plt.draw()
    plt.pause(0.1)
