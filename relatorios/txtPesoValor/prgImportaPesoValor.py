# -*- coding: utf-8 -*-
# Import PyQt5
import datetime

from PyQt5 import QtWidgets, QtSql
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QFileDialog, QMessageBox
# Imports Locais
from bibliotecas import mysqldb
from relatorios.txtPesoValor.rptPesoValor import *
# Imports do Sistema
import locale

class frmImportaPesoValor(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmImportaPesoValor()
        self.ui.setupUi(self)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.db = mysqldb.conecta_MySql()
        # Define a data atual como data fina
        self.ui.btArquivo.clicked.connect(self.btSelecionaArquivo_clicked)
        self.ui.btImportar.clicked.connect(self.btImportar_clicked)
        self.filenames =""

    def btSelecionaArquivo_clicked(self):
        self.filenames = QFileDialog.getOpenFileNames(self,'Localizar Rastreadores','/mnt/rede/rastreadores','Arquivos XML (*.xml)')
        if self.filenames != ('', ''):
            self.ui.txtArquivo.setText(str(len(self.filenames[0])) + " Arquivos Selecionados")

    def btImportar_clicked(self):
        # Verifica se está tudo preenchido
        if len(self.ui.txtArquivo.text()) < 5:
            QMessageBox.information(self,"Aviso","O Nome do arquivo precisa ser selecionado!",QMessageBox.Ok)
            return 0
        # Se está selecionado JadLog verifica se é arquivo XLS
        if self.ui.rdJadLog.isChecked():
            self.importa_JadLog()

    def importa_JadLog(self):
        import xml.etree.ElementTree as ET
        nRec = 0
        for arquivo in self.filenames[0]:
            tree = ET.parse(arquivo)
            root = tree.getroot()
            # Preparando as variáveis no formato do banco de dados!
            varData = root[0][0][0][7].text[:10]
            varValor = locale.atof(root[0][0][5][0].text.replace(".",","))
            varPeso = locale.atof(root[0][0][7][0][2][2].text.replace(".",","))
            varPesoB = varPeso
            varPesoL = varPeso
            varRastreador = root[0][0][1][1].text[23:37]
            #varSite ="https://www.reunidascargas.com.br/painel/rastreamento/"
            varID = locale.atoi(root[0][0][7][1][0][0].text[25:34])
            print(varData, " | ", str(varValor), " | ", str(varPeso), " | ", varRastreador, " | ", str(varID))
            # Prepara a SQL para fazer a inclusão!
            sql_Rastreadores = QtSql.QSqlQuery()
            sql_Rastreadores.prepare(
                "UPDATE docs SET valFrete=:valfrete, PesoBruto=:valpesobruto, PesoLiquido=:valpesoliq WHERE id=:id")
            # Prepara os parametros para incluir o frete
            #sql_Rastreadores.bindValue(":rastreador", varRastreador)
            #sql_Rastreadores.bindValue(":datafrete", varData)
            sql_Rastreadores.bindValue(":valpesobruto", varPesoB)
            sql_Rastreadores.bindValue(":valpesoliq", varPesoL)
            sql_Rastreadores.bindValue(":valfrete", varValor)
            sql_Rastreadores.bindValue(":id", varID)
            # Faz a inclusão propriamente dita
            try:
                sql_Rastreadores.exec()
                nRec = nRec + 1
                QMessageBox.information(self, "Confirmação",
                                        "Rastreador incluido com sucesso: " + varRastreador + " da NFe: " + str(varID), QMessageBox.Ok)
                print(sql_Rastreadores.lastError().text())
                print(sql_Rastreadores.lastQuery())
            except QSqlError as e:
                QMessageBox.critical(self,"Erro na inclusão",sql_Rastreadores.lastError().text(),QMessageBox.Ok)
                print(sql_Rastreadores.lastError().text())
                return 0
        self.ui.lblStatus.setText("Foram processados " + str(len(self.filenames[0])) + " arquivos e incluídos " + str(nRec))


