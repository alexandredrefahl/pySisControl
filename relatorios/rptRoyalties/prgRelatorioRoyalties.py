from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QTreeWidgetItemIterator
from PyQt5.QtCore import QDateTime

import locale
import os
# Imports Locais
from relatorios.rptRoyalties.frmRelatorioRoyalties import Ui_dlgRelatorioRoyalties
from relatorios.rptRoyalties.xlsPlanilha_Royalties import *
class frmRelatorioRoyalties(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgRelatorioRoyalties()
        self.ui.setupUi(self)
        self.ui.btRelatorio.clicked.connect(self.btRelatorio_clicked)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Define a data atual como data final
        self.ui.txtDataFIM.setDateTime(QDateTime.currentDateTime())
        self.ui.txtDatINI.setDateTime(QDateTime.currentDateTime())

    def btRelatorio_clicked(self):
        iterator = QTreeWidgetItemIterator(self.ui.treeWidget, QTreeWidgetItemIterator.Checked)
        cods = []
        while iterator.value():
            item = iterator.value()
            print(item.text(0)[:7])
            cods.append(item.text(0)[:7])
            iterator += 1
        ODF = xlsPlanilha_Royalties(cods, dataINI=self.ui.txtDatINI.date().toString('yyyy-MM-dd'), dataFIM=self.ui.txtDataFIM.date().toString('yyyy-MM-dd'))
        ODF.monta_planilha()
        if os.name == 'posix':
            os.system('xdg-open ' + ODF.arquivo)