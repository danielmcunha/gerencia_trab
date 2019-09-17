import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading


pullData = ''

def atualiza_dados():
	for i in range(10):
		global pullData;
		pullData += str(i) + ',' + str(i*2) + '\n'
		time.sleep(1)

t = threading.Thread(target=atualiza_dados)
t.start()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def animate(i):
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax.clear()
    ax.plot(xar,yar)
    ax.set_xlim(0,20)
    ax.set_ylim(0,20)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
money = [1.5e5, 2.5e6, 5.5e6, 2.0e7]


def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x * 1e-6)


formatter = FuncFormatter(millions)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
plt.bar(x, money)
plt.xticks(x, ('Bill', 'Fred', 'Mary', 'Sue'))
plt.show()
