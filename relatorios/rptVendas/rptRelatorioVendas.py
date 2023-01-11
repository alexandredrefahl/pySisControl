from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime
import locale
import os
# Imports Locais
from relatorios.rptVendas.frmRelatorioVendas import Ui_dlgRelatorioVendas
from relatorios.rptVendas.prgRelatorio_Vendas import rptRelatorio_Vendas
class dlgRelatorioVendas(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgRelatorioVendas()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Define a data atual como data final
        self.ui.txtDataFIM.setDateTime(QDateTime.currentDateTime().addDays(-7))
        self.ui.txtDataINI.setDateTime(QDateTime.currentDateTime())

    def pushButton_clicked(self):
        RPT = rptRelatorio_Vendas(dataINI=self.ui.txtDataINI.date().toString("yyyy-MM-dd"), dataFIM=self.ui.txtDataFIM.date().toString("yyyy-MM-dd"))
        # print("cria relatorio")
        RPT.show_report()
        os.system('xdg-open ' + RPT.arquivo)