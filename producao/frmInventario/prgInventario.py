# -*- coding: utf-8 -*-
# Import PyQt5
import datetime
import os.path

from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlQuery, QSqlError
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
# Imports Locais
from bibliotecas import mysqldb
from producao.frmInventario.frmInventario import Ui_dlgInventario

# Imports do Sistema
import locale
import xlrd

class frmInventario(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgInventario()
        self.ui.setupUi(self)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.db = mysqldb.conecta_MySql()
        # Definições de UI
        self.ui.pbProgresso.setVisible(False)
        # Vincula as ações com os botões
        self.ui.btSelect.clicked.connect(self.seleciona_Arquivo)
        self.ui.btInventario.clicked.connect(self.executa_Inventario)

    def seleciona_Arquivo(self):
        filename = QFileDialog.getOpenFileName(self, 'Localizar Inventário', '.','Arquivo XLS (*.xls)')
        if isinstance(filename, tuple):
            self.ui.txtArquivo.setText(filename[0])

    def baixa_todos_frascos(self):
        sql_baixa = QSqlQuery()
        sql = "UPDATE aux_frascos SET bxExclusao=:dataExclusao,bxMotivo='I',aux_frascos.bxOperador=1 WHERE ISNULL(bxExclusao)"
        sql_baixa.prepare(sql)
        varData = '2022-05-13'
        sql_baixa.bindValue(':dataExclusao',varData)
        try:
            sql_baixa.exec_()
            print(sql_baixa.lastError().text())
            print(sql_baixa.lastQuery())
            return True
        except QSqlError as e:
            QMessageBox(self,"Erro na SQL","Erro na Cláusula SQL de baixa dos Frascos:\n" + sql_baixa.lastError().text())
            return False

    def habilita_escaneados(self,Codigos):
        SQL = "UPDATE aux_frascos SET bxExclusao = NULL,bxMotivo = NULL, bxOperador = NULL WHERE id IN(:ids)"
        sql_habilita = QSqlQuery()
        sql_habilita.prepare(SQL)
        sql_habilita.bindValue(":ids",Codigos)
        try:
            sql_habilita.exec_()
            print(sql_habilita.lastError().text())
            print(sql_habilita.lastQuery())
            return True
        except QSqlError as e:
            QMessageBox(self,"Erro na SQL","Erro na Cláusula SQL de baixa dos Frascos:\n" + sql_habilita.lastError().text())
            return False

    def recalcula_estoque(self,Codigos):
        # Recalcula o estoque de todos os lotes selecionados
        #Primeiramente seleciona os codigos do LOTES correspondentes aos Frascos
        SQL = "SELECT DISTINCT Lote FROM aux_frascos WHERE id IN(" + Codigos + ")"
        sql_lotes = QSqlQuery()
        #sql_lotes.prepare(SQL)
        #sql_lotes.bindValue(":IDS",Codigos)
        try:
            sql_lotes.exec(SQL)
            print("Num Registros: " + str(sql_lotes.size()))
            print(sql_lotes.lastError().text())
            print("Ultima Query: " + sql_lotes.executedQuery())
        except QSqlError as e:
            QMessageBox(self, "Erro na SQL", "Erro na Cláusula SQL de baixa dos Frascos:\n" + sql_lotes.lastError().text())
            return False
        # Se executou a Query com sucesso, segue processando os lotes.
        num_de_lotes = sql_lotes.size()
        self.ui.pbProgresso.setVisible(True)
        self.ui.pbProgresso.setMaximum(num_de_lotes)
        ct = 1
        while sql_lotes.next():
            # Pega o ID do primeiro lote selecionado
            curID = sql_lotes.value(0)
            # Checagem redundante
            if curID == None:
                break
            # Recalcular o estoque para cada um dos lotes
            sql_Lote = QSqlQuery()
            sql_Lote.prepare('CALL atualiza_estoque_lote(:idLote)')
            sql_Lote.bindValue(":idLote", curID)
            self.ui.lblMsg.setText("Atualizando Estoque do Lote:" + str(curID) + " (" + str(ct) + "/" + str(num_de_lotes) + ")")
            self.ui.pbProgresso.setValue(ct)
            try:
                sql_Lote.exec()
                self.ui.lblMsg.setText("Estoque do lote " + str(curID) + " atualizado!")
                print("Estoque atualizado: ", curID)
                print(sql_Lote.lastError().text())
                ct = ct + 1
            except QSqlError as e:
                QMessageBox(self,"Erro","Erro ao atualizar o estoque do lote: " + str(curID) + "\n" + sql_Lote.lastError().text())
                # Mensagens de Debug
                print("Ocorreu um erro ao recalcular o estoque dos lotes")
                print("Erro: ", sql_Lote.lastError())
                # Volta o cursor ao normal
                QApplication.restoreOverrideCursor()
                return False
        return True

    def carrega_codigos_excel(self):
        if self.ui.txtArquivo.text() == "":
            QMessageBox(self,"Erro","É necessário definir o nome do arquivo (XLS)")
            return ""
        else:
            arqNome = self.ui.txtArquivo.text()
            self.ui.pbProgresso.setVisible(True)
            try:
                # abre a planilha para pegar os códigos no arquivo
                workbook = xlrd.open_workbook(arqNome)
                worksheet = workbook.sheet_by_name('inventario')
            except xlrd.XLRDError as e:
                QMessageBox(self,"Erro de Leitura","Erro ao ler o arquivo Excel\n")
                self.ui.pbProgresso.setVisible(False)
                return 0
            self.ui.pbProgresso.setMaximum(worksheet.nrows)
            ct = 1
            ids_coletados = ""
            # percorre as linhas da tabela para pegar os códigos
            num_Linhas = worksheet.nrows
            for row in range(num_Linhas):
                id_frasco = str(int(worksheet.cell(row, 0).value))
                if id_frasco != "" and id_frasco != None:
                    ids_coletados = ids_coletados + id_frasco + ","
                    self.ui.pbProgresso.setValue(ct)
                    self.ui.lblMsg.setText("Processando linha " + str(ct) + " de " + str(num_Linhas))
                    ct = ct + 1
            self.ui.lblMsg.setText(str(num_Linhas) + "Registros processados com sucesso!")
            self.ui.pbProgresso.setVisible(False)
            return ids_coletados

    def executa_Backup(self):
        pass

    def executa_Inventario(self):
        # Pega os códigos
        codigos = self.carrega_codigos_excel()
        f = open(os.path.join(".","tmp","codigos.txt"), "w")
        f.write(codigos[:-1])
        f.close()
        print(codigos[:-1])
        # Faz o Backup
        # Limpa todos os códigos
        #self.baixa_todos_frascos()
        # Reativa os códigos Escaneados
        #self.habilita_escaneados(codigos[:-1]) # esse -1 tira a última virgula
        # Atualiza o estoque dos lotes
        result = self.recalcula_estoque(codigos[:-1])
        # Conclui o inventário
        if result:
            QMessageBox(self,"Sucesso!","TODOS os lotes processados! \n Inventário concluído com sucesso!!!")
        else:
            QMessageBox(self,"Erro","Algum problema ao processar o estoque dos lotes do inventário.")






