# -*- coding: utf-8 -*-

# Imports do Python
from PyQt5.QtWidgets import *

#Imports do Sistema
from main import *
from producao.frmBaixaFrascos.prgBaixaFrascos import *
from producao.frmInventario.prgInventario import *
from pedidos.frmReservas.prgReservas import frmReservas_Gui
from pedidos.frmEmail.prgEmail import *
from pedidos.frmPesquisaReservas.prgPesquisaReservas import *
from pedidos.frmCalculaFrete.prgCalculaFrete import *
from pedidos.frmPedido.prgPedido import *
from relatorios.rptEtiquetasCaixas.prgEtiquetasCaixas import *
from relatorios.rptPlanilhaReservas.rptPlanilha_Reservas import *
from relatorios.rptPlanilhaReservas.prgPlanilhaReservas import *
from relatorios.txtRastreadores.prgImportaRastreadores import *
from relatorios.txtPesoValor.prgImportaPesoValor import *


import sys, os
from datetime import datetime

class frmSisControl(QtWidgets.QMainWindow):
    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Conecta os eventos com as respecticas funções
        self.ui.actIncluir_Pedidos.triggered.connect(self.actInclusaoReserva_triggered)
        self.ui.actBaixaFrascos.triggered.connect(self.actBaixaFrascos_triggered)
        self.ui.actSimular_Frete.triggered.connect(self.actSimularFrete_triggered)
        self.ui.actChecar_Email.triggered.connect(self.actChecarEmail_triggered)
        self.ui.actRptPlanilha_Reservas.triggered.connect(self.actRptPlanilha_Reservas_triggered)
        self.ui.actRptEtiquetas_Caixas.triggered.connect(self.actRptEtiquetas_Caixas_triggered)
        self.ui.actPesquisar_Reservas.triggered.connect(self.actPesquisar_Reservas_triggered)
        self.ui.actIncluir_Pedido.triggered.connect(self.actIncluirPedido_triggered)
        self.ui.actRptRastreadores.triggered.connect(self.actRptRastreadores_triggered)
        self.ui.actRptPesoValor.triggered.connect(self.actRptPesoValor_triggered)
        self.ui.actInventario.triggered.connect(self.actInventario_triggered)

        # Variável de controle para centralizar
        self.is_first_time = True

    def actInclusaoReserva_triggered(self):
        frmReserva = frmReservas_Gui()
        subWindow = self.ui.mdiArea.addSubWindow(frmReserva)
        subWindow.resize(frmReserva.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actIncluirPedido_triggered(self):
        frmPed = frmPedido()
        subWindow = self.ui.mdiArea.addSubWindow(frmPed)
        subWindow.resize(frmPed.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actBaixaFrascos_triggered(self):
        frmBaixa_Frascos = frmBaixaFrascos()
        subWindow = self.ui.mdiArea.addSubWindow(frmBaixa_Frascos)
        subWindow.resize(frmBaixa_Frascos.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actSimularFrete_triggered(self):
        frmSimulaFrete = frmCalculaFrete()
        subWindow = self.ui.mdiArea.addSubWindow(frmSimulaFrete)
        subWindow.resize(frmSimulaFrete.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actChecarEmail_triggered(self):
        frmEmailGui = frmEmail_Gui()
        subWindow = self.ui.mdiArea.addSubWindow(frmEmailGui)
        subWindow.resize(frmEmailGui.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actPesquisar_Reservas_triggered(self):
        frmPesquisaReservasGui = frmPesquisaReservas_Gui()
        subWindow = self.ui.mdiArea.addSubWindow(frmPesquisaReservasGui)
        subWindow.resize(frmPesquisaReservasGui.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actRptPlanilha_Reservas_triggered(self):
        frmPlanilhaReserva_Gui = frmPlanilhaReservasGui()
        subWindow = self.ui.mdiArea.addSubWindow(frmPlanilhaReserva_Gui)
        subWindow.resize(frmPlanilhaReserva_Gui.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actRptEtiquetas_Caixas_triggered(self):
        frmRptEtiquetas = frmEtiquetasCaixas()
        subWindow = self.ui.mdiArea.addSubWindow(frmRptEtiquetas)
        subWindow.resize(frmRptEtiquetas.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actRptRastreadores_triggered(self):
        frmRptRastreadores = frmImportaRastreadores()
        subWindow = self.ui.mdiArea.addSubWindow(frmRptRastreadores)
        subWindow.resize(frmRptRastreadores.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actRptPesoValor_triggered(self):
        frmRptPesoValor = frmImportaPesoValor()
        subWindow = self.ui.mdiArea.addSubWindow(frmRptPesoValor)
        subWindow.resize(frmRptPesoValor.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def actInventario_triggered(self):
        frameInventario = frmInventario()
        subWindow = self.ui.mdiArea.addSubWindow(frameInventario)
        subWindow.resize(frameInventario.size())
        self.center_subwindow(subWindow)
        subWindow.showNormal()

    def showEvent(self, event):
        if self.isVisible() and self.is_first_time:
            for sub in self.ui.mdiArea.subWindowList():
                self.center_subwindow(sub)
            self.is_first_time = False

    def center_subwindow(self, sub):
        center = self.ui.mdiArea.viewport().rect().center()
        geo = sub.geometry()
        geo.moveCenter(center)
        sub.setGeometry(geo)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = frmSisControl()
    w.showMaximized()
    sys.exit(app.exec_())