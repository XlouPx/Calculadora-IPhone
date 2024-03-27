from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from logger import LogManagement

class MeuApp(QMainWindow):
    num1 = 0
    num2 = 0
    numResult = 0
    op = None

    def __init__(self):
        super().__init__()
        loadUi('interface.ui', self)
        self.setAcoes()

    def setAcoes(self):
        self.btn0.clicked.connect(lambda: self.btnClicado('0'))
        self.btn1.clicked.connect(lambda: self.btnClicado('1'))
        self.btn2.clicked.connect(lambda: self.btnClicado('2'))
        self.btn3.clicked.connect(lambda: self.btnClicado('3'))
        self.btn4.clicked.connect(lambda: self.btnClicado('4'))
        self.btn5.clicked.connect(lambda: self.btnClicado('5'))
        self.btn6.clicked.connect(lambda: self.btnClicado('6'))
        self.btn7.clicked.connect(lambda: self.btnClicado('7'))
        self.btn8.clicked.connect(lambda: self.btnClicado('8'))
        self.btn9.clicked.connect(lambda: self.btnClicado('9'))

        self.btnMaismenos.clicked.connect(self.inverterSinal)
        self.btnLimpar.clicked.connect(self.limpar)
        self.btnIgual.clicked.connect(self.mostrarResultado)
        self.btnVirgula.clicked.connect(self.adicionarVirgula)
        
        self.btnPorcento.clicked.connect(lambda: self.definirOperacao('%'))
        self.btnMais.clicked.connect(lambda: self.definirOperacao('+'))
        self.btnDivisao.clicked.connect(lambda: self.definirOperacao('/'))
        self.btnMenos.clicked.connect(lambda: self.definirOperacao('-'))
        self.btnVezes.clicked.connect(lambda: self.definirOperacao('*'))


    def mostrarDisplay(self, value):
        value_str = str(value).replace('.', ',')
        self.entrada.setText(value_str)

    def pegarDisplay(self):
        value = self.entrada.text()
        if value:
            value = value.replace(',', '.')
            try:
                value = int(value)
            except ValueError:
                value = float(value)
        return value

    def btnClicado(self, valor):
        texto_atual = self.pegarDisplay()
        if texto_atual == 0 and valor != '0':
            self.mostrarDisplay(str(valor))
        else:
            self.mostrarDisplay(str(texto_atual) + str(valor))

    def definirOperacao(self, operacao):
        texto_atual = self.pegarDisplay()
        if texto_atual != 0:
            self.op = operacao
            self.mostrarDisplay(f"{texto_atual} {operacao}")
            self.entrada.clear()

    def mostrarResultado(self):
        if self.op:
            self.num2 = self.pegarDisplay()
            if self.op == '+':
                self.numResult = self.somar()
            elif self.op == '-':
                self.numResult = self.subtrair()
            elif self.op == '*':
                self.numResult = self.multiplicar()
            elif self.op == '/':
                self.numResult = self.dividir()
            elif self.op == '%':
                self.numResult = self.calcularPorcentagem()
            self.mostrarDisplay(self.numResult)

    def limpar(self):
        self.num1 = 0
        self.num2 = 0
        self.numResult = 0
        self.op = None
        self.mostrarDisplay(0)

    def adicionarVirgula(self):
        texto_atual = self.pegarDisplay()
        if '.' not in str(texto_atual):
            self.mostrarDisplay(str(texto_atual) + '.')

    def inverterSinal(self):
        texto_atual = self.pegarDisplay()
        texto_atual *= -1
        self.mostrarDisplay(texto_atual)

    def somar(self):
        return self.num1 + self.num2

    def subtrair(self):
        return self.num1 - self.num2

    def multiplicar(self):
        return self.num1 * self.num2

    def dividir(self):
        if self.num2 != 0:
            return self.num1 / self.num2
        else:
            return "Erro"

    def calcularPorcentagem(self):
        porcento = self.pegarDisplay() / 100
        if self.op == '+' or self.op == '-':
            porcento = self.num1 * porcento
        return porcento


if __name__ == '__main__':
    app = QApplication([])
    janela = MeuApp()
    janela.show()
    app.exec_()
