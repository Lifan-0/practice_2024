import sys

from PyQt5.QtWidgets import * # * подгрузка всех классов библиотеки
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ui_MainWindow(object): # класс оформления, наследуемый
	def setupUi(self, QWidget): # def - метод
		self.main_layout = QVBoxLayout() # контейнер для виджетов (V - вертикальный)

		h_layout = QHBoxLayout()# h_layout горизн. контейнер
		self.cntP = QLineEdit(self)
		self.cntP.setValidator(QIntValidator(1, 99, self))
		self.cntP.setFixedWidth(100)
		self.btn_cntP = QPushButton('Создать')
		h_layout.addWidget(QLabel('Количество планет'))
		h_layout.addWidget(self.cntP)
		h_layout.addWidget(self.btn_cntP)
		h_layout.addStretch(1)
		self.main_layout.addLayout(h_layout)

		self.planets_layout = QVBoxLayout()# контейнер для планет
		self.main_layout.addLayout(self.planets_layout)

		self.output_layout = QVBoxLayout()
		self.main_layout.addLayout(self.output_layout)

		self.main_layout.addStretch(1)
		self.setLayout(self.main_layout)


class MainWindow(QWidget, Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__(None)
		self.setupUi(self)

		self.btn_cntP.clicked.connect(self.add_planet)

		self.setWindowTitle('Вселенная')

	def add_planet(self):
		if self.cntP.text() == '':
			return

		self.clearLayout(self.planets_layout)

		self.lineEdits = []

		self.planets_layout.addWidget(QLabel('\nДанные планет'))
		h_layout = QHBoxLayout()
		n_l, x_l, y_l, z_l, m_l =QLabel('№'), QLabel('X'), QLabel('Y'), QLabel('Z'), QLabel('Масса')
		n_l.setFixedWidth(15)
		n_l.setAlignment(Qt.AlignCenter)
		x_l.setFixedWidth(50)
		x_l.setAlignment(Qt.AlignCenter)
		y_l.setFixedWidth(50)
		y_l.setAlignment(Qt.AlignCenter)
		z_l.setFixedWidth(50)
		z_l.setAlignment(Qt.AlignCenter)
		m_l.setFixedWidth(50)
		m_l.setAlignment(Qt.AlignCenter)
		h_layout.addWidget(n_l)
		h_layout.addWidget(x_l)
		h_layout.addWidget(y_l)
		h_layout.addWidget(z_l)
		h_layout.addWidget(m_l)
		h_layout.addStretch(1)# оформление заголовков 53-68
		self.planets_layout.addLayout(h_layout)

		for n in range(int(self.cntP.text())):
			h_layout = QHBoxLayout()
			self.num_pl = QLabel(self)
			self.num_pl.setFixedWidth(15)
			self.num_pl.setText('{}'.format(n+1))

			self.cX = QLineEdit(self)
			self.cX.setValidator(QIntValidator(1, 9999, self))
			self.cX.setFixedWidth(50)
			self.cX.textChanged.connect(lambda text, i=n : self.edit_changed(int(text), i, 0))

			self.cY = QLineEdit(self)
			self.cY.setValidator(QIntValidator(1, 9999, self))
			self.cY.setFixedWidth(50)
			self.cY.textChanged.connect(lambda text, i=n : self.edit_changed(int(text), i, 1))

			self.cZ = QLineEdit(self)
			self.cZ.setValidator(QIntValidator(1, 9999, self))
			self.cZ.setFixedWidth(50)
			self.cZ.textChanged.connect(lambda text, i=n : self.edit_changed(int(text), i, 2))

			self.cM = QLineEdit(self)
			self.cM.setValidator(QIntValidator(1, 9999, self))
			self.cM.setFixedWidth(50)
			self.cM.textChanged.connect(lambda text, i=n : self.edit_changed(int(text), i, 3))

			h_layout.addWidget(self.num_pl)
			h_layout.addWidget(self.cX)
			h_layout.addWidget(self.cY)
			h_layout.addWidget(self.cZ)
			h_layout.addWidget(self.cM)
			h_layout.addStretch(1)
			self.planets_layout.addLayout(h_layout)

			self.lineEdits.append([0,0,0,0])

		self.go = QPushButton('Расчет')
		self.planets_layout.addWidget(self.go)
		self.go.clicked.connect(self.calc_values)

	def calc_values(self):
		self.clearLayout(self.output_layout)
		slenght, smass = 0,0
		for i, v in enumerate(self.lineEdits):
			print('№{}, input: {}'.format(i, v))
			slenght += (v[0]**2+v[1]**2+v[2]**2)**(1/2)
			smass += v[3]

		aradius = round(slenght/len(self.lineEdits), 2)
		amass = round(smass/len(self.lineEdits), 2)

		self.output_layout.addWidget(QLabel('\nВывод\n\nСредний радиус: {}\nСредняя масса: {}'.format(aradius, amass)))


	def edit_changed(self, text, i, k):
		self.lineEdits[i][k] = text

	def clearLayout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.setParent(None)
				else:
					self.clearLayout(item.layout())


if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.setStyleSheet("QLabel{font:Arial;font-size: 9pt;}")
	window.show()

	sys.exit(app.exec_())