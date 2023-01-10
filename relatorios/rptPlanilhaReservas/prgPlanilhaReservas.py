# Import PyQt5
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime
# Imports Locais
from relatorios.rptPlanilhaReservas.frmPlanilhaReservas import Ui_frmRptRelatorioReservas
from relatorios.rptPlanilhaReservas.rptPlanilha_Reservas import *
from relatorios.rptPlanilhaReservas.xlsPlanilha_Reservas import *
# Imports do Sistema
import locale

class frmPlanilhaReservasGui(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmRptRelatorioReservas()
        self.ui.setupUi(self)
        self.ui.btGerar.clicked.connect(self.btGerar_Clicked)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Define a data atual como data final
        self.ui.txtDataFIM.setDateTime(QDateTime.currentDateTime())
        self.ui.txtDataINI.setDateTime(QDateTime.currentDateTime().addMonths(-2))

    def btGerar_Clicked(self):
        if self.ui.rdNome.isChecked():
            ordem="Nome"
        if self.ui.rdData.isChecked():
            ordem="Data"
        if self.ui.rdCadastro.isChecked():
            crit="Cadastro"
        if self.ui.rdPrazo.isChecked():
            crit="Prazo"
        varDataINI = self.ui.txtDataINI.date().toString("yyyy-MM-dd")
        varDataFIM = self.ui.txtDataFIM.date().toString("yyyy-MM-dd")
        if self.ui.opPDF.isChecked():
            RPT = rptPlanilha_Reservas(ordem=ordem, criterio=crit, dataINI=varDataINI,dataFIM=varDataFIM)
            RPT.show_report()
            if os.name == 'posix':
                os.system('xdg-open ' + RPT.arquivo)
        if self.ui.opODS.isChecked():
            ODF = xlsPlanilha_Reservas(ordem="Prazo", criterio="Prazo", dataINI=varDataINI, dataFIM=varDataFIM)
            ODF.monta_planilha()
            if os.name == 'posix':
                os.system('xdg-open ' + ODF.arquivo)

