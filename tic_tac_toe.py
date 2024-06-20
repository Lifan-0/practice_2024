import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ui_MainWindow(object):
	def setupUi(self, QWidget):
		self.main_layout = QVBoxLayout()

		h_layout = QHBoxLayout()
		self.cntP = QComboBox()
		self.cntP.addItems(['3x3','5x5','7x7'])
		self.cntP.setFixedWidth(50)
		self.btn_cntP = QPushButton('Обновить')
		h_layout.addWidget(QLabel('Поле'))
		h_layout.addWidget(self.cntP)
		h_layout.addWidget(self.btn_cntP)
		h_layout.addStretch(1)
		self.main_layout.addLayout(h_layout)

		self.game_layout = QGridLayout()
		self.main_layout.addLayout(self.game_layout)

		self.result_layout = QVBoxLayout()
		self.result_label = QLabel('')
		self.result_label.setStyleSheet("border: 2px solid black;")
		self.result_layout.addWidget(self.result_label)
		self.main_layout.addLayout(self.result_layout)

		self.main_layout.addStretch(1)
		self.setLayout(self.main_layout)


class MainWindow(QWidget, Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__(None)
		self.setupUi(self)
		#~ self.resize(500, 500)

		self.fill_field()

		self.btn_cntP.clicked.connect(self.fill_field)

		self.setWindowTitle('Крестики-нолики')

	def fill_field(self):
		self.size = int(self.cntP.currentText().split('x')[0])
		self.current_turn = 'o'
		self.turns = [[0 for x in range(self.size)] for x in range(self.size)]
		self.draw, self.winX, self.winO = 0,0,0

		for i in reversed(range(self.game_layout.count())):
			self.game_layout.itemAt(i).widget().setParent(None)

		for i in range(self.size):
			for j in range(self.size):
				btn = QPushButton()
				btn.setFixedWidth(100)
				btn.setFixedHeight(100)
				self.game_layout.addWidget(btn, i, j)
				btn.clicked.connect(lambda checked, arg=[i,j]: self.check_turn(arg))
				btn.setFont(QFont('Arial', 25))

	def check_turn(self, coord):
		if self.sender().text() != '' or (self.draw or self.winX or self.winO) ==1:
			return

		if self.current_turn == 'o':
			self.result_label.setText('Ход O')
			self.sender().setText('x')
			self.current_turn = 'x'
			self.turns[coord[0]][coord[1]] = 1
		elif self.current_turn == 'x':
			self.result_label.setText('Ход X')
			self.sender().setText('o')
			self.current_turn = 'o'
			self.turns[coord[0]][coord[1]] = 2

		self.check_win()

		if self.winX == 1:
			self.result_label.setText('Победили X!')
		elif self.winO == 1:
			self.result_label.setText('Победили O!')
		elif self.draw == 1:
			self.result_label.setText('Ничья!')


	def check_win(self):
		for row in self.turns:
			if row.count(1) == self.size:
				self.winX = 1
				return
			elif row.count(2) == self.size:
				self.winO = 1
				return


		for col in [list(i) for i in zip(*self.turns)]:
			if col.count(1) == self.size:
				self.winX = 1
				return
			elif col.count(2) == self.size:
				self.winO = 1
				return

		width, height = len(self.turns[0]), len(self.turns)
		sz = max(width, height)
		valid_x, valid_y = range(width), range(height)
		center_pos = sorted([x for x in range(1, self.size)])[len([x for x in range(1, self.size)]) // 2]-1
		x, y = (center_pos,center_pos)
		diag1 = [self.turns[i][i-x+y] for i in range(sz) if i-x+y in valid_y]
		diag2 = [self.turns[i][x+y-i] for i in range(sz) if x+y-i in valid_y]

		if diag1.count(1) == self.size or diag2.count(1) == self.size:
			self.winX = 1
			return
		elif diag1.count(2) == self.size or diag2.count(2) == self.size:
			self.winO = 1
			return

		if any(0 in sub for sub in self.turns) == False:
			self.draw = 1


if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.setStyleSheet("QLabel{font:Arial;font-size: 9pt;}")
	window.show()

	sys.exit(app.exec_())