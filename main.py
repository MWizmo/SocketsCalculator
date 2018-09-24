import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont,QPalette,QColor


class CalculatorWindow(QMainWindow):
    def __init__(self,address):
        super().__init__()
        self._socket=socket.socket()
        self.address=address
        self._socket.connect((self.address, 9000))
        self.initUI()

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
        appearance = self.palette()
        appearance.setColor(QPalette.Normal, QPalette.Window,QColor(200,250,200))
        self.setPalette(appearance)
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
        try:
            self._socket.send(expression.encode('utf-8'))
            data = self._socket.recv(1024).decode('utf-8')
            self.output.setText(data)
            self.output.show()
        except:
            self.statusBar().showMessage('Потеряно соединение с сервером')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ConnectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.quit_btn = QPushButton('Завершить работу', self)
        self.quit_btn.setGeometry(75, 300, 150, 50)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.lbl1=QLabel(self)
        self.lbl1.setText('Введите адрес сервера')
        self.lbl1.setGeometry(20,20,300,20)
        self.lbl1.setFont(QFont("Times", 12, QFont.Decorative))

        self.lbl2 = QLabel(self)
        self.lbl2.setText('Или выберите адрес из списка')
        self.lbl2.setGeometry(40, 120, 300, 20)
        self.lbl2.setFont(QFont("Times", 12, QFont.Decorative))

        self.combo = QComboBox(self)
        self.combo.addItems(["localhost", "192.18.0.1","18.217.88.63"])
        self.combo.setFont(QFont("Times", 12, QFont.Decorative))
        self.combo.setGeometry(90,150,120,30)

        self.input = QLineEdit(self)
        self.input.setGeometry(10, 50, 280, 50)
        self.input.setFont(QFont("Times", 14, QFont.Decorative))

        self.enter_btn = QPushButton('Подключиться', self)
        self.enter_btn.setGeometry(100, 200, 100, 50)
        self.enter_btn.clicked.connect(self.getAddress)

        self.resize(300, 400)
        appearance = self.palette()
        appearance.setColor(QPalette.Normal, QPalette.Window,
                            QColor(200,200,200))
        self.setPalette(appearance)
        self.center()
        self.setWindowTitle('Connect')
        self.show()

    def getAddress(self):
        address=''
        if(self.input.text()=='' or self.input.text()==None):
            address=self.combo.currentText()
        else:
            address=self.input.text()
        try:
            self.calc_window=CalculatorWindow(address=address)
            self.calc_window.show()
            self.hide()
        except:
            self.statusBar().showMessage('Сервер недоступен')


    def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())


sock=socket.socket()
#sock.connect(('18.217.88.63', 9000))
#sock.connect(('localhost', 9000))
#TimeoutError: [WinError 10060] Попытка установить соединение была безуспешной, т.к. от другого компьютера за требуемое время не получен нужный отклик, или было разорвано уже установленное соединение из-за неверного отклика уже подключенного компьютера
app = QApplication(sys.argv)
connector=ConnectWindow()
sys.exit(app.exec_())
