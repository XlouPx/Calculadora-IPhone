from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from logger import LogManagement
from os import path
from decimal import Decimal
import operator

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num1 = ""
        self.num2 = ""
        self.operador = None
        self.log = LogManagement(__file__)

        loadUi(self.localPath('interface.ui'), self)
        self.log.info("Inicialização do programa.")
        self.setAcoes()

    def localPath(self, relativo):
        return f'{path.dirname(path.realpath(__file__))}\\{relativo}'

    def setAcoes(self):
        self.conectarBotoesNumericos()
        self.conectarBotoesOperacao()
        self.conectarBotoesMetodos()

    def conectarBotoesNumericos(self):
        botoes_numericos = [getattr(self, f"btn{i}") for i in range(10)]
        for botao in botoes_numericos:
            botao.clicked.connect(lambda _, num=botao.text(): self.btnClicado(num))

    def conectarBotoesOperacao(self):
        botoes_operacao = [self.btnPorcentagem, self.btnMais, self.btnDivisao, self.btnMenos, self.btnVezes]
        operacoes = [self.porcentagem, operator.add, operator.truediv, operator.sub, operator.mul]
        for botao, operacao in zip(botoes_operacao, operacoes):
            if botao:
                botao.clicked.connect(lambda _, op=operacao, text=botao.text(): self.definirOperacao(op, text))

    def conectarBotoesMetodos(self):
        botoes_metodos = {
            self.btnMaismenos: self.inverterSinal,
            self.btnLimpar: self.limpar,
            self.btnIgual: self.mostrarResultado,
            self.btnVirgula: self.adicionarVirgula
        }
        for botao, metodo in botoes_metodos.items():
            if botao:
                botao.clicked.connect(metodo)

    def btnClicado(self, btn):
        if self.operador is None:
            self.num1 += btn
            self.mostrarDisplay(self.num1)
        else:
            self.num2 += btn
            self.mostrarDisplay(self.num2)

    def mostrarDisplay(self, value):
        value = str(value).replace('.',  ',')
        self.entrada.setText(str(value))

    def pegarDisplay(self):
        value = self.entrada.text().replace(',', '.')
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return 0

    def definirOperacao(self, operacao, operador):
        if self.num1 != "":
            if operador == '%':
                self.porcentagem()
                return
            self.operador = operacao
            self.mostrarDisplay(operador)

    def mostrarResultado(self):
        if self.operador is None or self.num2 == "":
            return
        
        num1 = float(self.num1)
        num2 = float(self.num2)

        if self.operador == operator.truediv and num2 == 0:
            self.log.error("Erro: Divisão por zero")
            return
        
        result = self.operador(num1, num2)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        self.mostrarDisplay(result)
        self.num1 = str(result)
        self.num2 = ""
        self.operador = None
        
    def porcentagem(self):
        if self.num1 != "":
            porcento = float(self.num1) / 100
            self.mostrarDisplay(porcento)
            self.num1 = ""  

    def inverterSinal(self):
        numero = self.pegarDisplay()
        numero *= -1
        self.mostrarDisplay(numero)
        if self.operador is None:
            self.num1 = str(numero)
        else:
            self.num2 = str(numero)

    def adicionarVirgula(self):
        numero = self.pegarDisplay()
        numero_str = str(numero)
        if "." not in numero_str:
            numero_str += "."
            self.mostrarDisplay(numero_str)
            if self.operador is None:
                self.num1 = numero_str
            else:
                self.num2 = numero_str

    def limpar(self):
        self.num1 = ""
        self.num2 = ""
        self.operador = None
        self.mostrarDisplay("")

if __name__ == '__main__':
    app = QApplication([])
    janela = MeuApp()
    janela.show()
    app.exec_()
