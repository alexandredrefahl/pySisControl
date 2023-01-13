# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        MainWindow.setFont(font)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.verticalLayout.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 19))
        self.menubar.setObjectName("menubar")
        self.menuArquivo = QtWidgets.QMenu(self.menubar)
        self.menuArquivo.setObjectName("menuArquivo")
        self.menuPedidos = QtWidgets.QMenu(self.menubar)
        self.menuPedidos.setObjectName("menuPedidos")
        self.menuConfigura_es = QtWidgets.QMenu(self.menubar)
        self.menuConfigura_es.setObjectName("menuConfigura_es")
        self.menuProdu_o = QtWidgets.QMenu(self.menubar)
        self.menuProdu_o.setObjectName("menuProdu_o")
        self.menuRelat_rios = QtWidgets.QMenu(self.menubar)
        self.menuRelat_rios.setObjectName("menuRelat_rios")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actIncluir_Pedidos = QtWidgets.QAction(MainWindow)
        self.actIncluir_Pedidos.setObjectName("actIncluir_Pedidos")
        self.actSimular_Frete = QtWidgets.QAction(MainWindow)
        self.actSimular_Frete.setObjectName("actSimular_Frete")
        self.actChecar_Email = QtWidgets.QAction(MainWindow)
        self.actChecar_Email.setObjectName("actChecar_Email")
        self.actionSair = QtWidgets.QAction(MainWindow)
        self.actionSair.setObjectName("actionSair")
        self.actBaixaFrascos = QtWidgets.QAction(MainWindow)
        self.actBaixaFrascos.setObjectName("actBaixaFrascos")
        self.actRptPlanilha_Reservas = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        self.actRptPlanilha_Reservas.setFont(font)
        self.actRptPlanilha_Reservas.setObjectName("actRptPlanilha_Reservas")
        self.actPesquisar_Reservas = QtWidgets.QAction(MainWindow)
        self.actPesquisar_Reservas.setObjectName("actPesquisar_Reservas")
        self.actRptEtiquetas_Caixas = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        self.actRptEtiquetas_Caixas.setFont(font)
        self.actRptEtiquetas_Caixas.setObjectName("actRptEtiquetas_Caixas")
        self.actIncluir_Pedido = QtWidgets.QAction(MainWindow)
        self.actIncluir_Pedido.setObjectName("actIncluir_Pedido")
        self.actRptRastreadores = QtWidgets.QAction(MainWindow)
        self.actRptRastreadores.setObjectName("actRptRastreadores")
        self.actRptPesoValor = QtWidgets.QAction(MainWindow)
        self.actRptPesoValor.setObjectName("actRptPesoValor")
        self.actInventario = QtWidgets.QAction(MainWindow)
        self.actInventario.setObjectName("actInventario")
        self.actRptVendas = QtWidgets.QAction(MainWindow)
        self.actRptVendas.setObjectName("actRptVendas")
        self.actRoyalties = QtWidgets.QAction(MainWindow)
        self.actRoyalties.setObjectName("actRoyalties")
        self.menuArquivo.addAction(self.actionSair)
        self.menuPedidos.addAction(self.actIncluir_Pedido)
        self.menuPedidos.addSeparator()
        self.menuPedidos.addAction(self.actIncluir_Pedidos)
        self.menuPedidos.addAction(self.actPesquisar_Reservas)
        self.menuPedidos.addSeparator()
        self.menuPedidos.addAction(self.actSimular_Frete)
        self.menuPedidos.addAction(self.actChecar_Email)
        self.menuProdu_o.addAction(self.actBaixaFrascos)
        self.menuProdu_o.addAction(self.actInventario)
        self.menuRelat_rios.addAction(self.actRptPlanilha_Reservas)
        self.menuRelat_rios.addAction(self.actRptEtiquetas_Caixas)
        self.menuRelat_rios.addAction(self.actRptRastreadores)
        self.menuRelat_rios.addAction(self.actRptPesoValor)
        self.menuRelat_rios.addAction(self.actRptVendas)
        self.menuRelat_rios.addAction(self.actRoyalties)
        self.menuRelat_rios.addSeparator()
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuProdu_o.menuAction())
        self.menubar.addAction(self.menuPedidos.menuAction())
        self.menubar.addAction(self.menuConfigura_es.menuAction())
        self.menubar.addAction(self.menuRelat_rios.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sis control Linux"))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuPedidos.setTitle(_translate("MainWindow", "Pedidos"))
        self.menuConfigura_es.setTitle(_translate("MainWindow", "Configurações"))
        self.menuProdu_o.setTitle(_translate("MainWindow", "Produção"))
        self.menuRelat_rios.setTitle(_translate("MainWindow", "Relatórios"))
        self.actIncluir_Pedidos.setText(_translate("MainWindow", "Incluir Reservas"))
        self.actSimular_Frete.setText(_translate("MainWindow", "Simular Frete"))
        self.actChecar_Email.setText(_translate("MainWindow", "Checar Email"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))
        self.actBaixaFrascos.setText(_translate("MainWindow", "Baixa de Frascos"))
        self.actRptPlanilha_Reservas.setText(_translate("MainWindow", "Planilha de Reservas"))
        self.actPesquisar_Reservas.setText(_translate("MainWindow", "Gerenciar Reservas"))
        self.actRptEtiquetas_Caixas.setText(_translate("MainWindow", "Etiquetas Caixas"))
        self.actIncluir_Pedido.setText(_translate("MainWindow", "Incluir Pedido"))
        self.actRptRastreadores.setText(_translate("MainWindow", "Importar Rastreadores"))
        self.actRptPesoValor.setText(_translate("MainWindow", "Importa Peso e Valor"))
        self.actInventario.setText(_translate("MainWindow", "Importa dados Inventário"))
        self.actRptVendas.setText(_translate("MainWindow", "Vendas por periodo"))
        self.actRoyalties.setText(_translate("MainWindow", "Royalties por periodo"))
        self.actRoyalties.setToolTip(_translate("MainWindow", "Gera relatório de Royalties pelo período definido"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
