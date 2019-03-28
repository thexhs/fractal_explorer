import sys
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

my_controls = []

N = 512
Z = np.empty((N, N))
max_iter = 64
xmin, xmax, ymin, ymax = -2.2, .8, -1.5, 1.5
X = np.linspace(xmin, xmax, N)
Y = np.linspace(ymin, ymax, N)

def iter_count(C, max_iter):
	X = C
	for n in range(max_iter):
		if abs(X) > 2.:
			return n
		X = X**2+C
	return max_iter
	
def computeIm():
    xmin = float(my_controls[0].text())
    xmax = float(my_controls[1].text())
    ymin = float(my_controls[2].text())
    ymax = float(my_controls[3].text())
    X = np.linspace(xmin, xmax, N)
    Y = np.linspace(ymin, ymax, N)	
    print('Start calculation')
    for i,y in enumerate(Y):
        for j, x in enumerate(X):
            Z[i,j] = iter_count(complex(x,y), max_iter)
    print('Calculation complete')
	
class Window(QDialog):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
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
		
		my_controls.append(self.text1)
		my_controls.append(self.text2)
		my_controls.append(self.text3)
		my_controls.append(self.text4)
		
		layout1 = QHBoxLayout()
		layout2 = QVBoxLayout()		
		
		layout2.addWidget(self.button)
		layout2.addWidget(self.button1)
		layout2.addWidget(self.button2)
		layout2.addWidget(self.text1)
		layout2.addWidget(self.text2)
		layout2.addWidget(self.text3)
		layout2.addWidget(self.text4)
		
		layout1.addLayout(layout2)
		layout1.addWidget(self.canvas)

		self.setLayout(layout1)
		
	def plot(self):
		self.figure.clear()
		ax = self.figure.add_subplot(111)
		ax.imshow(Z, cmap = cm.jet)
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