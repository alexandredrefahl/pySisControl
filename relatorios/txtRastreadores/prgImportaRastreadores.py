# -*- coding: utf-8 -*-
# Import PyQt5
import datetime

from PyQt5 import QtWidgets, QtSql
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QFileDialog, QMessageBox
# Imports Locais
from bibliotecas import mysqldb
from relatorios.txtRastreadores.rptRastreadores import Ui_frmImportaRastreador
# Imports do Sistema
import locale

class frmImportaRastreadores(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmImportaRastreador()
        self.ui.setupUi(self)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.db = mysqldb.conecta_MySql()
        # Define a data atual como data fina
        self.ui.btArquivo.clicked.connect(self.btSelecionaArquivo_clicked)
        self.ui.btImportar.clicked.connect(self.btImportar_clicked)
        self.filenames =""

    def btSelecionaArquivo_clicked(self):
        if self.ui.rdReunidas.isChecked():
            self.filenames = QFileDialog.getOpenFileNames(self,'Localizar Rastreadores','/mnt/rede/rastreadores','Arquivos XML (*.xml)')
            if self.filenames != ('', ''):
                self.ui.txtArquivo.setText(str(len(self.filenames[0])) + " Arquivos Selecionados")
        else:
            filename = QFileDialog.getOpenFileName(self, 'Localizar Rastreador', '/mnt/rede/rastreadores','All Files (*.*)')
            if isinstance(filename,tuple):
                self.ui.txtArquivo.setText(filename[0])

    def btImportar_clicked(self):
        # Verifica se está tudo preenchido
        if len(self.ui.txtArquivo.text()) < 5:
            QMessageBox.information(self,"Aviso","O Nome do arquivo precisa ser selecionado!",QMessageBox.Ok)
            return 0
        # Se está selecionado JadLog verifica se é arquivo XLS
        if self.ui.rdJadLog.isChecked():
            self.importa_JadLog()
        if self.ui.rdCorreios.isChecked():
            self.importa_correios()
        if self.ui.rdReunidas.isChecked():
            self.importa_reunidas()

    def importa_JadLog(self):
        print(self.ui.txtArquivo.text()[-4::])
        if not (self.ui.txtArquivo.text()[-4::] == ".xls" or self.ui.txtArquivo.text()[-4::] == "xlsx"):
            QMessageBox.critical(self, "Aviso", "O tipo do arquivo precisa ser XLS ou XLSX", QMessageBox.Ok)
            return 0
        else:
            from xlrd import open_workbook
            wb = open_workbook(self.ui.txtArquivo.text())
            sheet = wb.sheet_by_name("Consulta")
            nLinhas = sheet.nrows
            nRec = 0
            for cur_row in range(2, nLinhas):
                varRastreador = sheet.cell(cur_row, 0)  # Codigo
                varNFE = sheet.cell(cur_row, 1)  # Nota Fiscal
                varData = sheet.cell(cur_row, 11)  # Data da Emissão
                self.ui.lblStatus.setText("Localizando NFe " + varNFE.value)
                query = QSqlQuery()
                query.exec("SELECT * FROM docs WHERE id=" + str(varNFE.value))
                query.first()
                # Se o rastreador ainda não tiver sido registrado
                print("Rastreador BD: " + str(query.value("Rastreador")) + " da NFe: " + str(varNFE.value))
                if len(str(query.value("Rastreador"))) <= 0:
                    nRec = nRec + 1
                    sql_Rastreadores = QtSql.QSqlQuery()
                    sql_Rastreadores.prepare(
                        "UPDATE docs SET Rastreador=:rastreador, dataFrete=:datafrete, siteRastreador=:site WHERE id=:id")
                    txtRastreador = varRastreador.value
                    txtId = varNFE.value
                    txtDataFrete = datetime.datetime.strptime(varData.value, "%d/%m/%Y")
                    txtDataFreteSQL = txtDataFrete.strftime("%Y-%m-%d")
                    txtSite = "https://www.jadlog.com.br/siteDpd/tracking.jad?cte=" + txtRastreador + "&lang=pt_br"
                    # Prepara os parametros para incluir o frete
                    sql_Rastreadores.bindValue(":rastreador", txtRastreador)
                    sql_Rastreadores.bindValue(":datafrete", txtDataFreteSQL)
                    sql_Rastreadores.bindValue(":site", txtSite)
                    sql_Rastreadores.bindValue(":id", txtId)
                    # Faz a inclusão propriamente dita
                    try:
                        sql_Rastreadores.exec()
                        QMessageBox.information(self, "Confirmação",
                                                "Rastreador incluido com sucesso: " + txtRastreador, QMessageBox.Ok)
                        print(sql_Rastreadores.lastError().text())
                        print(sql_Rastreadores.lastQuery())
                    except QSqlError as e:
                        print(sql_Rastreadores.lastError().text())
                        return 0
            self.ui.lblStatus.setText("Foram processados " + str(nLinhas - 2) + " registros e incluídos " + str(nRec))

    def importa_correios(self):
        if not (self.ui.txtArquivo.text()[-4::] == ".xls" or self.ui.txtArquivo.text()[-4::] == "xlsx"):
            QMessageBox.critical(self, "Aviso", "O tipo do arquivo precisa ser XLS ou XLSX", QMessageBox.Ok)
            return 0
        else:
            from xlrd import open_workbook
            wb = open_workbook(self.ui.txtArquivo.text())
            sheet = wb.sheet_by_name("Planilha1")
            nLinhas = sheet.nrows
            nRec = 0
            for cur_row in range(2, nLinhas-2):
                varRastreador = sheet.cell(cur_row, 7)  # Rastreador
                varNFe = sheet.cell(cur_row, 11)  # NFe
                varValor = sheet.cell(cur_row, 17)  # Valor
                varPeso = sheet.cell(cur_row, 4)  # Peso
                varData = sheet.cell(cur_row, 0)  # Emissão
                self.ui.lblStatus.setText("Localizando NFe " + str(int(varNFe.value)))
                query = QSqlQuery()
                query.exec("SELECT id,rastreador FROM docs WHERE id=" + str(int(varNFe.value)))
                query.first()
                # Se o rastreador ainda não tiver sido registrado
                print("Rastreador BD: " + str(query.value("Rastreador")) + " da NFe: " + str(int(varNFe.value)))
                if len(str(query.value("Rastreador"))) <= 0:
                    nRec = nRec + 1
                    # Prepara a SQL para fazer a inclusão!
                    sql_Rastreadores = QtSql.QSqlQuery()
                    sql_Rastreadores.prepare(
                        "UPDATE docs SET Rastreador=:rastreador, dataFrete=:datafrete, siteRastreador=:site, valFrete=:valfrete WHERE id=:id")
                    # Preparando as variáveis no formato do banco de dados!
                    txtRastreador = varRastreador.value
                    txtId = str(int(varNFe.value))
                    txtDataFrete = datetime.datetime.strptime(varData.value, "%d/%m/%Y")
                    txtDataFreteSQL = txtDataFrete.strftime("%Y-%m-%d")
                    txtSite = "https://www.websro.com.br/detalhes.php?P_COD_UNI=" + txtRastreador
                    txtValor = varValor.value
                    print('############')
                    print("Registro nº: " + str(nRec))
                    print(txtRastreador)
                    print(txtId)
                    print(txtDataFreteSQL)
                    print(txtValor)
                    print(txtSite)
                    print('------------')
                    # Prepara os parametros para incluir o frete
                    sql_Rastreadores.bindValue(":rastreador", txtRastreador)
                    sql_Rastreadores.bindValue(":datafrete", txtDataFreteSQL)
                    sql_Rastreadores.bindValue(":site", txtSite)
                    sql_Rastreadores.bindValue(":valfrete", txtValor )
                    sql_Rastreadores.bindValue(":id", txtId)
                    # Faz a inclusão propriamente dita
                    try:
                        sql_Rastreadores.exec()
                        QMessageBox.information(self, "Confirmação",
                                                "Rastreador incluido com sucesso: " + txtRastreador, QMessageBox.Ok)
                        print(sql_Rastreadores.lastError().text())
                        print(sql_Rastreadores.lastQuery())
                    except QSqlError as e:
                        print(sql_Rastreadores.lastError().text())
                        return 0
            self.ui.lblStatus.setText("Foram processados " + str(nLinhas - 2) + " registros e incluídos " + str(nRec))

    def importa_reunidas(self):
        import xml.etree.ElementTree as ET
        nRec = 0
        for arquivo in self.filenames[0]:
            tree = ET.parse(arquivo)
            root = tree.getroot()
            # Preparando as variáveis no formato do banco de dados!
            varData = root[0][0][0][7].text[:10]
            varValor = locale.atof(root[0][0][7][0].text.replace(".",","))
            varPeso = locale.atof(root[0][0][9][0][5][2].text.replace(".",","))
            varRastreador = root[0][0][0][6].text
            varSite ="https://www.reunidascargas.com.br/painel/rastreamento/"
            varID = locale.atoi(root[0][0][9][1][0][0].text[25:34])
            print(varData, " | ", str(varValor), " | ", str(varPeso), " | ", varRastreador, " | ", str(varID))
            # Prepara a SQL para fazer a inclusão!
            sql_Rastreadores = QtSql.QSqlQuery()
            sql_Rastreadores.prepare(
                "UPDATE docs SET Rastreador=:rastreador, dataFrete=:datafrete, siteRastreador=:site, valFrete=:valfrete WHERE id=:id")
            # Prepara os parametros para incluir o frete
            sql_Rastreadores.bindValue(":rastreador", varRastreador)
            sql_Rastreadores.bindValue(":datafrete", varData)
            sql_Rastreadores.bindValue(":site", varSite)
            sql_Rastreadores.bindValue(":valfrete", varValor)
            sql_Rastreadores.bindValue(":id", varID)
            # Faz a inclusão propriamente dita
            try:
                sql_Rastreadores.exec()
                nRec = nRec + 1
                QMessageBox.information(self, "Confirmação",
                                        "Rastreador incluido com sucesso: " + varRastreador, QMessageBox.Ok)
                print(sql_Rastreadores.lastError().text())
                print(sql_Rastreadores.lastQuery())
            except QSqlError as e:
                print(sql_Rastreadores.lastError().text())
                return 0
        self.ui.lblStatus.setText("Foram processados " + str(len(self.filenames[0])) + " arquivos e incluídos " + str(nRec))


