from easysnmp import Session
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading


data_set = ''
elapsed_time = 0
session = Session(hostname='192.168.0.10', community='public', version=2)
numInterfaces = int(session.get('ifNumber.0').value)

"""

    Plota grafico

"""
def plot_chart(i):
    dataArray = data_set.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax.clear()
    ax.plot(xar,yar)
    ax.set_xlim(0,20)
    ax.set_ylim(0,20)

"""

    Atualiza data_set do grafico

"""
def update_in_data_set(interface, bytes_in):
	global data_set;
	data_set += str(elapsed_time) + ',' + str(bytes_in) + '\n'
	time.sleep(1)

"""

  Analisa interfaces de rede

"""
def analyze_interfaces():
    # Fazendo uma requisicao bulk com dois contadores in/out das interfaces de uma vez (repetindo conforme a quantidade de interfaces), isso vai retornar numInterfaces*2 objetos
    countBulk = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces)
    
    update_in_data_set(0, countBulk[0].value)

"""

    Main

"""
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig, plot_chart(0), interval = 1000)
plt.show()

while True:
    analyze_interfaces()
    time.sleep(1)
    elapsed_time += 1


    
    



