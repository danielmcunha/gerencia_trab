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
    print(data_set)

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


"""

  Analisa interfaces de rede

"""
def analyze_interfaces():
    while True:
        # Fazendo uma requisicao bulk com dois contadores in/out das interfaces de uma vez (repetindo conforme a quantidade de interfaces), isso vai retornar numInterfaces*2 objetos
        countBulk = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces)
        global elapsed_time
        update_in_data_set(0, countBulk[0].value)
        time.sleep(1)
        elapsed_time += 1

"""

    Main

"""

elapsed_time = 0
t = threading.Thread(target=analyze_interfaces)
t.start()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig, plot_chart, interval = 1000)
plt.show()
