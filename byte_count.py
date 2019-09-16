from easysnmp import Session
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading


data_set1 = ''
data_set2 = ''
tx_down_set = {}
tx_upld_set = {}
total_down = 0;
total_upld = 0;

session = Session(hostname='192.168.43.161', version=3, security_level='auth_with_privacy', security_username='MD5DESUser', auth_protocol='MD5', auth_password='senhasenhasenha', privacy_protocol='DES', privacy_password='senhasenhasenha')
numInterfaces = int(session.get('ifNumber.0').value)

"""

    Plota grafico

"""
def plot_chart(i):
    dataArray1 = data_set1.split('\n')
    dataArray2 = data_set2.split('\n')
    xar1 = []
    yar1 = []
    xar2 = []
    yar2 = []    
    for eachLine in dataArray1:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            xar1.append(int(x))
            yar1.append(int(y))
    for eachLine in dataArray2:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            xar2.append(int(x))
            yar2.append(int(y))
    ax.clear()
    ax.plot(xar2,yar2,color='tab:blue', label='tx. upload')
    ax.plot(xar1,yar1,color='tab:orange', label='rx. download')
    ax.set_title('Taxas de download e upload do host (bytes/s)')
    ax.set_xlim(0,60)
    ax.legend()

"""

    Atualiza data_set do grafico

"""
def update_in_data_set(tx_download, tx_upload):
    global data_set1
    global data_set2
    num_points = len(tx_down_set)
    if num_points == 60:
        for i in range(1,num_points-1,1):
            tx_down_set[i] = tx_down_set[i+1]
            tx_upld_set[i] = tx_upld_set[i+1]
            total_down_set[i] = total_down_set[i+1];
            total_upld_set[i] = total_upld_set[i+1];
        tx_down_set[len(tx_down_set)-1] = tx_download
        tx_upld_set[len(tx_upld_set)-1] = tx_upload
    else:
        tx_down_set[len(tx_down_set)+1] = tx_download
        tx_upld_set[len(tx_upld_set)+1] = tx_upload
    data_set1 = ''
    data_set2 = ''
    for i in range(1,num_points,1):
        data_set1 += str(i) + ',' + str(tx_down_set[i]) + '\n'
        data_set2 += str(i) + ',' + str(tx_upld_set[i]) + '\n'


"""

  Analisa interfaces de rede

"""
def analyze_interfaces():
    countBulk1 = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces);
    bytesIn1 = 0;
    bytesOut1 = 0;
    for i in range(0,len(countBulk1),2):
        bytesIn1 += int(countBulk1[i].value)
        bytesOut1 += int(countBulk1[i+1].value)
    time.sleep(1)
    while True:
        countBulk2 = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces)
        bytesIn2 = 0;
        bytesOut2 = 0;
        for i in range(0,len(countBulk2),2):
            bytesIn2 += int(countBulk2[i].value)
            bytesOut2 += int(countBulk2[i+1].value)
        global elapsed_time
        tx_download = bytesIn2 - bytesIn1
        tx_upload = bytesOut2 - bytesOut1
        total_down = bytesIn2;
        total_upld = bytesOut2;
        update_in_data_set(tx_download, tx_upload)
        bytesIn1 = bytesIn2
        bytesOut1 = bytesOut2
        time.sleep(1)

"""

    Main

"""

t = threading.Thread(target=analyze_interfaces)
t.start()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig, plot_chart, interval = 1000)
plt.show()

