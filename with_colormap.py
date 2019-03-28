import sys
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QListWidget, QCheckBox, QGroupBox,
                             QGridLayout, QLabel)

from PyQt5.QtCore import Qt
#Для вставки виджета Matplotlib в окошко Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#Список возможных палитр цвета
colormapList = ['Accent', 'Blues', 'BrBG', 'BuGn',
                'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 
                'Greys', 'OrRd', 'Oranges', 'PRGn', 
                'Paired', 'Pastel1', 'Pastel2', 'PiYG',
                'PuBu', 'PuBuGn', 'PuBu_r', 'PuOr', 'PuRd', 
                'Purples', 'RdBu', 'RdGy', 'RdPu', 
                'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2',
                'Set3', 'Spectral', 'Wistia', 'YlGn', 
                'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 
                'autumn', 'binary', 'bone','brg', 
                'bwr',  'cividis', 'cool', 'coolwarm', 
                'copper', 'cubehelix', 'flag', 'gist_earth', 
                'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 
                'gist_stern','gist_yarg', 'gnuplot', 'gnuplot2',
                'gray', 'hot', 'hsv', 'inferno', 
                'jet', 'magma', 'nipy_spectral', 'ocean', 
                'pink', 'plasma', 'prism', 'rainbow', 
                'seismic', 'spring', 'summer', 'tab10', 
                'terrain', 'twilight', 'twilight_shifted', 'viridis', 
                'winter',]
#Список виджетов, к которым нужен будет доступ из глобальной функции computeIm()
my_controls = []
#Глобальные переменные для расчета Фрактала
N = 512
Z = np.empty((N, N))
max_iter = 64
xmin, xmax, ymin, ymax = -2.2, .8, -1.5, 1.5
X = np.linspace(xmin, xmax, N)
Y = np.linspace(ymin, ymax, N)
#Итерационная процедура определения, является ли пиксель частью множества 
def iter_count(C, max_iter):
    X = C
    for n in range(max_iter):
        if abs(X) > 2.:
            return n
        X = X**2+C
    return max_iter
#В цикле идет обход всех пискселей изображения    
def computeIm():
    #Считываем габариты окна, для которого нужно рассчитать фрактал
    xmin = float(my_controls[0].text())
    xmax = float(my_controls[1].text())
    ymin = float(my_controls[2].text())
    ymax = float(my_controls[3].text())
    #Создаем массивы по которым будет идти просчет фрагмета фрактала
    X = np.linspace(xmin, xmax, N)
    Y = np.linspace(ymin, ymax, N)
    #Пользователь может варьировать количество итераций
    max_iter = int(my_controls[5].text())
    print('Start calculation')
    for i,y in enumerate(Y):
        for j, x in enumerate(X):
            Z[i,j] = iter_count(complex(x,y), max_iter)
    print('Calculation complete')
#Класс который определяет интерефейс     
class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        #Инициализация виджетов
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        self.button1 = QPushButton('Compute')
        self.button1.clicked.connect(computeIm)
        self.button2 = QPushButton('Default')
        self.button2.clicked.connect(self.setDefault)
        self.text1 = QLineEdit("-2.2")
        self.text2 = QLineEdit(".8")
        self.text3 = QLineEdit("-1.5")
        self.text4 = QLineEdit("1.5")
        self.lblX = QLabel('X')
        self.lblY = QLabel('Y')
        self.lblmin = QLabel('<center>min</center>')
        self.lblmax = QLabel('<center>max</center>')
        self.text5 = QLineEdit("512")
        self.text6 = QLineEdit("64")
        self.chbox1 = QCheckBox("reverse Color Map")
        self.list1 = QListWidget()
        self.list1.addItems(colormapList)
        #Добавление в список тех виджетов, к которым будет нужен глобальный доступ
        my_controls.append(self.text1)
        my_controls.append(self.text2)
        my_controls.append(self.text3)
        my_controls.append(self.text4)
        my_controls.append(self.text5)
        my_controls.append(self.text6)
        #Создание контейнеров для виджетов
        layout1 = QHBoxLayout()
        layout1_1 = QGroupBox('Fractal render window coordinates')
        layout1_2 = QGridLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()
        #Размещение виджетов по контейнерам
        layout2.addWidget(self.button)
        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout1_2.addWidget(self.lblmin,0,1)
        layout1_2.addWidget(self.lblmax,0,2)         
        layout1_2.addWidget(self.lblX,1,0)
        layout1_2.addWidget(self.lblY,2,0)        
        layout1_2.addWidget(self.text1,1,1)
        layout1_2.addWidget(self.text2,1,2)
        layout1_2.addWidget(self.text3,2,1)
        layout1_2.addWidget(self.text4,2,2)
        #layout1_1.setLayout(layout1_2)
        layout2.addLayout(layout1_2)
        layout2.addWidget(self.chbox1)
        layout2.addWidget(self.list1)
        layout3.addWidget(self.text5)
        layout3.addWidget(self.text6)
        layout2.addLayout(layout3)
        layout1.addLayout(layout2)
        layout1.addWidget(self.canvas)
        
        self.setLayout(layout1)
        
      
    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        colorMap = self.list1.currentItem().text()
        if self.chbox1.isChecked():
            print('True')
            colorMap = colorMap+'_r'
        ax.imshow(Z, cmap = colorMap)
        self.canvas.draw()
    
    def setDefault(self):
        self.text1.setText("-2.2")
        self.text2.setText(".8")
        self.text3.setText("-1.5")
        self.text4.setText("1.5")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())		