#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:04:36 2020

@author: alexandre
"""

from PyQt5 import QtCore, QtWidgets, QtSql
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import locale
import datetime
from bibliotecas import mysqldb
from mysql.connector import Error
from pedidos.frmReservas.frmReservas import Ui_frmReservas

class frmReservas_Gui(QtWidgets.QDialog):

    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmReservas()
        self.ui.setupUi(self)

        self.MY_SQL_ADDRESS = mysqldb.getHost()
        self.MY_SQL_USER = mysqldb.getUser()
        self.MY_SQL_PASS = mysqldb.getPasw()
        self.MY_SQL_DATABASE = mysqldb.getDatabase()

        #Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Vincula os botões às suas funções de ação
        self.ui.txtCEP.editingFinished.connect(self.txtCEP_editingFinished)
        self.ui.btIncluir.clicked.connect(self.btIncluir_Clicked)
        self.ui.btAcrescentar.clicked.connect(self.btAcrescentar_Clicked)
        self.ui.txtData.dateChanged.connect(self.txtData_dateChanged)
        self.ui.tblItens.mudancaContagemLinhas.connect(self.tblItens_mudancaContagemLinhas)

        # Personaliza interface
        self.ui.tblItens.setColumnWidth(0, 60)
        self.ui.tblItens.setColumnWidth(1, 60)
        self.ui.tblItens.setColumnWidth(2, 330)
        self.ui.tblItens.setColumnWidth(3, 70)
        self.ui.tblItens.setColumnWidth(4, 70)
        self.ui.tblItens.setAlternatingRowColors(1)
        # Coloca data atual nas caixas de Data
        self.ui.txtData.setDateTime(QtCore.QDateTime.currentDateTime())
        # Conecta o Mysql e carrega os dados no combo
        #self.db = bibliotecas.mysql.conecta_MySql()
        self.db = mysqldb.conecta_MySql()
        self.carrega_combo()
        # Finaliza o setUp e mostra a interface
        self.show()

    def carrega_combo(self):
        self.model = QtSql.QSqlTableModel(self)
        # self.model.setQuery('SELECT * FROM selecao_clones')
        self.model.setTable("selecao_clones")
        self.model.select()
        self.ui.cmbVariedade.setModel(self.model)
        self.ui.cmbVariedade.setModelColumn(self.model.fieldIndex("Descricao"))

    def currentIndexChanged(self, index):
        print("Selecionado ID: ", self.model.index(self.ui.cmbVariedade.currentIndex(), 0).data(0))

    def tblItens_mudancaContagemLinhas(self):
        pass

    def btAcrescentar_Clicked(self):
        # Busca a linha no model que contém os dados da linha
        DR = self.model.record(self.ui.cmbVariedade.currentIndex())
        # Insere uma linha em branco no TableView
        self.ui.tblItens.insertRow(self.ui.tblItens.rowCount())
        r = self.ui.tblItens.rowCount() - 1
        # Organiza as variáveis antes de fazer a inserção
        varMerc = QTableWidgetItem('{:03}'.format(DR.field(1).value()))
        print("Merc: ", DR.field(1).value())
        varMerc.setTextAlignment(QtCore.Qt.AlignCenter)
        varClone = QTableWidgetItem('{:04}'.format(DR.field(2).value()))
        print("Clone: ", DR.field(2).value())
        varClone.setTextAlignment(QtCore.Qt.AlignCenter)
        varDescricao = QTableWidgetItem(DR.field(3).value())
        varQtde = QTableWidgetItem(self.ui.txtQtde.text())
        varQtde.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        varPreco = QTableWidgetItem(locale.format_string('%.2f', DR.field(4).value()))
        varPreco.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Insere as linhas no Table view
        self.ui.tblItens.setItem(r, 0, varMerc)
        self.ui.tblItens.setItem(r, 1, varClone)
        self.ui.tblItens.setItem(r, 2, varDescricao)
        self.ui.tblItens.setItem(r, 3, varQtde)
        self.ui.tblItens.setItem(r, 4, varPreco)
        self.ui.txtQtde.setText("")
        self.ui.txtQtde.setFocus()

    def btIncluir_Clicked(self):
        varData = self.ui.txtData.date().toString("yyyy-MM-dd")
        varCliente = self.ui.txtNome.text()
        varCEP = self.ui.txtCEP.text()
        varCidade = self.ui.txtCidade.text()
        varUF = self.ui.txtUF.text()
        varFone = self.ui.txtFone.text()
        varEmail = self.ui.txtEmail.text()
        varPrazo =self.ui.txtPrazo.date().toString("yyyy-MM-dd")
        varObs=self.ui.txtObs.toPlainText()
        varAtendida = 0
        varConfirmada = 1

        # primeiro faz a inclusão da reserva
        sql_Reserva = QtSql.QSqlQuery()
        sql_Reserva.prepare("INSERT INTO reservas SET Data=:data,Nome=:nome,CEP=:cep,Fone=:fone,Cidade=:cidade,UF=:uf,Email=:email,Observacoes=:obs,Atendido=:atendido,Prazo=:prazo,Confirmada=:confirmada")
        # Faz a associação dos valores
        sql_Reserva.bindValue(":data", varData)
        sql_Reserva.bindValue(":nome", varCliente)
        sql_Reserva.bindValue(":cep", varCEP)
        sql_Reserva.bindValue(":fone", varFone)
        sql_Reserva.bindValue(":cidade", varCidade)
        sql_Reserva.bindValue(":uf", varUF)
        sql_Reserva.bindValue(":email", varEmail)
        sql_Reserva.bindValue(":obs", varObs)
        sql_Reserva.bindValue(":atendido", varAtendida)
        sql_Reserva.bindValue(":prazo", varPrazo)
        sql_Reserva.bindValue(":uf", varUF)
        sql_Reserva.bindValue(":confirmada", varConfirmada)

        # Faz a validação dos campos
        varValida, varMsg = self.valida_campos()

        # Verifica se os campos foram preenchidos da forma correta
        if not varValida:
            QtWidgets.QMessageBox.critical(self, "Erro Validação", "Erro ao verificar as informações preenchidas" + "\n" + varMsg, QtWidgets.QMessageBox.Ok)
            return
        try:
            sql_Reserva.exec()
            print(sql_Reserva.lastError().text())
            print(sql_Reserva.lastQuery())
            print("Inserido: " + str(sql_Reserva.lastInsertId()))
            id_reserva = sql_Reserva.lastInsertId()
        except Error as e:
            QMessageBox.critical(self, "Erro",
                                 "Erro ao incluir a reserva\n" + e.msg + "\n" + sql_Reserva.lastError().text(),
                                 QMessageBox.Ok)
            return
        # Percorre os ítens da tabela para fazer a inclusão
        numLinhas = self.ui.tblItens.rowCount()
        for row in range(0, numLinhas):
            sql_Item = QtSql.QSqlQuery()
            sql_Item.prepare("INSERT INTO reservas_itens SET Doc_ID=:docid,Mercadoria=:mercadoria,Clone=:clone,Descricao=:descricao,Quantidade=:qtde,Preco=:preco,Forma=:forma")
            # Prepara as variaveis no formato para inclusao
            varMerc = self.ui.tblItens.item(row, 0).text()
            varClone = self.ui.tblItens.item(row, 1).text()
            varDesc = self.ui.tblItens.item(row, 2).text()
            varItemQtde = self.ui.tblItens.item(row, 3).text()
            varValor = locale.atof(self.ui.tblItens.item(row, 4).text())
            varForma = "Muda Aclimatizada"

            # Faz a associação dos valores
            sql_Item.bindValue(":docid", id_reserva)
            sql_Item.bindValue(":mercadoria", varMerc)
            sql_Item.bindValue(":clone", varClone)
            sql_Item.bindValue(":descricao", varDesc)
            sql_Item.bindValue(":qtde", varItemQtde)
            sql_Item.bindValue(":preco", varValor)
            sql_Item.bindValue(":forma", varForma)
            try:
                sql_Item.exec()
                print(sql_Item.lastError().text())
                print(sql_Item.lastQuery())
                print("Inserido: " + str(sql_Item.lastInsertId()))
                sql_Item = None
            except Error as e:
                print("Erro ao se conectar ao MySQL: ", e)
                QMessageBox.critical(self,"Erro MySQL","Erro ao incluir item da reserva no Banco de Dados" + "\n" + e.msg,QMessageBox.Ok)
                return
        # Informa que foi bem sucedida a inclusão do pedido
        QMessageBox.information(self,"Confirmação","Reserva " + str(id_reserva) +  " incluída com sucesso!",QMessageBox.Ok)
        # Limpa os campos para uma nova inclusão
        self.limpa_campos()

    def Calcula_Prazo(self):
        # varData = datetime.datetime.strptime(,"%d/%m/%Y")
        varData = self.ui.txtData.date().toPyDate()
        varPrazo = varData + datetime.timedelta(days=150)
        self.ui.txtPrazo.setDate(varPrazo)

    def limpa_campos(self):
        # self.ui.txtData.setDateTime(date.today())
        self.ui.txtNome.setText("")
        self.ui.txtCEP.setText("")
        self.ui.txtCidade.setText("")
        self.ui.txtUF.setText("")
        self.ui.txtFone.setText("")
        self.ui.txtEmail.setText("")
        # self.ui.txtPrazo.setDateTime(date.today())
        self.ui.txtQtde.setText("")
        self.ui.tblItens.setRowCount(0)
        self.ui.cmbVariedade.setCurrentIndex(0)
        self.ui.txtObs.setText("")
        # Coloca o foco no primeiro controle
        self.ui.txtData.setFocus()

    def valida_campos(self):
        valida = True
        msg = ""
        if len(self.ui.txtNome.text()) == 0:
            valida = False
            msg = msg + "Nome não foi preenchido\n"
        if len(self.ui.txtFone.text()) == 0 and len(self.ui.txtEmail.text()) == 0:
            valida = False
            msg += "Nenhuma informação de contato foi registrada (e-mail/Telefone)\n"
        if self.ui.tblItens.rowCount() == 0:
            valida = False
            msg += "Não foi registrado nenhum ítem de interesse.\n"
        return valida, msg

    def txtCEP_editingFinished(self):
        if len(self.ui.txtCEP.text()) == 8:
            cidade, uf = self.busca_endereco(self.ui.txtCEP.text())
        else:
            cidade = ''
            uf = ''
        self.ui.txtCidade.setText(cidade)
        self.ui.txtUF.setText(uf)

    def txtData_dateChanged(self):
        self.Calcula_Prazo()

    def busca_endereco(self, cep):
        import requests
        try:
            headers = {"Accept": "application/json"}
            r = requests.get("https://viacep.com.br/ws/" + cep +"/json/", headers=headers)
        except requests.exceptions.HTTPError as err:
            print(err)
            QtWidgets.QMessageBox.critical(self, "Erro CEP", "Erro de conexão com o provedor", QtWidgets.QMessageBox.Ok)
            return '', ''
        except requests.exceptions.Timeout as err:
            print(err)
            QtWidgets.QMessageBox.critical(self, "Erro CEP", "Erro: tempo limite esgotado", QtWidgets.QMessageBox.Ok)
            return '', ''
        # Se conseguiu pegar o JSON com as informações
        import json
        endereco = r.json()
        if "erro" in endereco:
            QtWidgets.QMessageBox.critical(self, "Erro CEP", "CEP Inválido ou não encontrado", QtWidgets.QMessageBox.Ok)
            return '',''
        return endereco['localidade'], endereco['uf']

    def Mensagem_Erro(self, mensagem, erro):
        msg = QtWidgets.QMessageBox
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setInformativeText(erro)
        msg.setWindowTitle("Erro")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
