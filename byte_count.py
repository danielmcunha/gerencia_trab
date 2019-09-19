from Tkinter import *
import ttk
from easysnmp import Session
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import time
import threading

data_set1 = ''
data_set2 = ''
session = {}
numInterfaces = 0
tx_down_set = {}
tx_upld_set = {}
totais = [0,0]
cpu = [0,0]
plotclosed = False

def handle_close(evt):
    global plotclosed
    plotclosed = True

def megabytes(x, pos):
    return str(x/1000000) + ' MB'

def analyze_interfaces():
    countBulk1 = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces);
    bytesIn1 = 0;
    bytesOut1 = 0;
    for i in range(0,len(countBulk1),2):
        bytesIn1 += int(countBulk1[i].value)
        bytesOut1 += int(countBulk1[i+1].value)
    time.sleep(1)
    global plotclosed
    while True:
        if plotclosed:
          break
        countBulk2 = session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, numInterfaces)
        cpu[0] = float(session.get('laLoad.1').value) * 100
        cpu[1] = 100
        bytesIn2 = 0;
        bytesOut2 = 0;
        for i in range(0,len(countBulk2),2):
            bytesIn2 += int(countBulk2[i].value)
            bytesOut2 += int(countBulk2[i+1].value)
        global elapsed_time
        tx_download = bytesIn2 - bytesIn1
        tx_upload = bytesOut2 - bytesOut1
        totais[0] = bytesIn2;
        totais[1] = bytesOut2;
        update_in_data_set(tx_download, tx_upload)
        bytesIn1 = bytesIn2
        bytesOut1 = bytesOut2
        time.sleep(1)

def update_in_data_set(tx_download, tx_upload):
    global data_set1
    global data_set2
    num_points = len(tx_down_set)
    if num_points == 60:
        for i in range(1,num_points-1,1):
            tx_down_set[i] = tx_down_set[i+1]
            tx_upld_set[i] = tx_upld_set[i+1]
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

def plot_chart(i):
    dataArray1 = data_set1.split('\n')
    dataArray2 = data_set2.split('\n')
    xar1 = []
    yar1 = []
    xar2 = []
    yar2 = []
    maxval = 0;
    for eachLine in dataArray1:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            xar1.append(int(x))
            yar1.append(int(y))
            if int(y) > maxval:
                maxval = int(y)
    for eachLine in dataArray2:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            xar2.append(int(x))
            yar2.append(int(y))
            if int(y) > maxval:
                maxval = int(y)
    ax.clear()
    ax.plot(xar1,yar1,color='tab:orange', label='rx. download')
    ax.plot(xar2,yar2,color='tab:blue', label='tx. upload')
    ax.set_title('Taxas de download e upload do host (MB/s)')
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlim(0,60)
    if maxval > 500000:
      ax.set_ylim(0,maxval*2)
    else:
      ax.set_ylim(0,500000)
    ax.legend()

def plot_chart2(i):
    ax2.clear()
    plt.bar([1],totais[0],color='tab:orange')
    plt.bar([2],totais[1],color='tab:blue')
    ax2.set_title('Trafego total no host (MBytes)')
    if totais[0] > 25000000 or totais[1] > 25000000:
      maxtotal = 0;
      if totais[0] > 25000000:
        maxtotal = totais[0]
      if totais[1] > 25000000:
        maxtotal = totais[1]
      ax2.set_ylim(0,maxtotal*1.5)
    else:
      ax2.set_ylim(0,25000000)
    ax2.yaxis.set_major_formatter(formatter)
    plt.xticks([1,2], ('Download','Upload'))

def plot_chart3(i):
    ax3.clear()
    labels = 'Em uso', 'Idle'
    ax3.pie(cpu,labels=labels,autopct='%1.1f%%',shadow=False,startangle=90)
    ax3.set_title('Uso da CPU no host (%)')
    ax3.axis('equal')

class Application:
    def __init__(self, master=None):

        self.fontePadrao = ("Monospace Regular", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer["pady"] = 3
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer["pady"] = 3
        self.terceiroContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["padx"] = 20
        self.quintoContainer["pady"] = 3
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["padx"] = 20
        self.sextoContainer["pady"] = 3
        self.sextoContainer.pack()

        self.setimoContainer = Frame(master)
        self.setimoContainer["padx"] = 20
        self.setimoContainer["pady"] = 3
        self.setimoContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Dados do agente SNMPv3")
        self.titulo["font"] = ("Monospace Regular", "10", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer,text="Usuario", font=self.fontePadrao)
        self.nomeLabel.pack()

        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.pack()

        self.senhaLabel = Label(self.terceiroContainer, text="Senha", font=self.fontePadrao)
        self.senhaLabel.pack()

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.pack()

        self.ipLabel = Label(self.quintoContainer, text="IP do host", font=self.fontePadrao)
        self.ipLabel.pack()

        self.ip = Entry(self.quintoContainer)
        self.ip["width"] = 30
        self.ip["font"] = self.fontePadrao
        self.ip.pack()

        self.hashLabel = Label(self.sextoContainer, text="Hash", font=self.fontePadrao)
        self.hashLabel.pack()

        self.hash = ttk.Combobox(self.sextoContainer, values=["MD5", "SHA"])
        self.hash["width"] = 30
        self.hash["font"] = self.fontePadrao
        self.hash.pack()

        self.encryptionLabel = Label(self.setimoContainer, text="Criptografia", font=self.fontePadrao)
        self.encryptionLabel.pack()

        self.encryption = ttk.Combobox(self.setimoContainer, values=["AES", "DES"])
        self.encryption["width"] = 30
        self.encryption["font"] = self.fontePadrao
        self.encryption.pack()

        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Monitorar"
        self.autenticar["font"] = ("Monospace Regular", "10")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.verificaSenha
        self.autenticar.pack()

        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        ip = self.ip.get()
        hash = self.hash.get()
        encryption = self.encryption.get()
        try:
          global session
          global numInterfaces
          session = Session(hostname=ip, version=3, security_level='auth_with_privacy', security_username=usuario, auth_protocol=hash, auth_password=senha, privacy_protocol=encryption, privacy_password=senha)
          numInterfaces = int(session.get('ifNumber.0').value)
          self.mensagem["text"] = "Autenticado"
          t = threading.Thread(target=analyze_interfaces)
          t.start()
          ani = animation.FuncAnimation(fig, plot_chart, interval = 1000)
          ani2 = animation.FuncAnimation(fig2, plot_chart2, interval = 1000)
          ani3 = animation.FuncAnimation(fig3, plot_chart3, interval = 1000)
          plt.show()
        except:
          print('Ocorreu um erro. Verifique o que aconteceu.')
          self.mensagem["text"] = "Falha durante autenticacao"

fig = plt.figure()
fig.canvas.mpl_connect('close_event', handle_close)
ax = fig.add_subplot(1,1,1)
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
formatter = FuncFormatter(megabytes)
root = Tk()
root.title("Foo Network Manager")
app = Application(root)
root.mainloop()
