import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

class Window(QMainWindow):
    def __init__(self,_socket):
        super().__init__()
        self.initUI()
        self._socket=_socket

    def initUI(self):
        self.quit_btn = QPushButton('Завершить работу', self)
        self.quit_btn.setGeometry(225, 330, 150, 50)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.input = QLineEdit(self)
        self.input.setGeometry(100,100,300,50)
        self.input.setFont(QFont("Times", 16, QFont.Decorative))

        self.enter_btn = QPushButton('Enter', self)
        self.enter_btn.setGeometry(100, 160, 80, 50)
        self.enter_btn.clicked.connect(self.getExpression)
        self.enter_btn.setShortcut('Enter')

        self.delete_btn = QPushButton('<', self)
        self.delete_btn.setGeometry(410, 100, 50, 50)
        self.delete_btn.clicked.connect(self.delete)

        self.clear_btn=QPushButton('Clear',self)
        self.clear_btn.setGeometry(320,160,80,50)
        self.clear_btn.clicked.connect(self.clear)

        self.output=QTextBrowser(self)
        self.output.setFont(QFont("Times", 14, QFont.Decorative))
        self.output.setGeometry(100, 230, 300, 40)
        self.output.hide()

        self.resize(600, 400)
        self.center()
        self.setWindowTitle('SimpleCalculator')
        self.show()

    def clear(self):
        self.input.setText('')
        self.output.setText('')
        self.output.hide()

    def delete(self):
        self.input.setText(self.input.text()[:len(self.input.text())-1])

    def getExpression(self):
        expression=self.input.text()
        self.clear()
        self._socket.send(expression.encode('utf-8'))
        data = self._socket.recv(1024).decode('utf-8')
        self.output.setText(data)
        self.output.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

sock = socket.socket()
#sock.connect(('18.188.112.122', 9000))
sock.connect(('localhost', 9000))
app = QApplication(sys.argv)
window=Window(sock)
sys.exit(app.exec_())
