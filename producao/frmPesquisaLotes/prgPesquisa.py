# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmlotes.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QCheckBox
from PyQt5 import uic
from PyQt5.QtSql import QSqlQueryModel, QSqlTableModel, QSqlDatabase

QDialog, UI_frmPesquisa = uic.loadUiType("frmPesquisa.ui")

# Define a Classe
class clsPesquisa(QDialog, UI_frmPesquisa):
    def __init__(self, parent=None):
        super(clsPesquisa, self).__init__(parent)
        self.setupUi(self)

        #Define o banco de dados principal
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName ("10.1.1.254")
        db.setPort (3306)
        db.setDatabaseName("controle")
        db.setUserName("alexandre")
        db.setPassword("@drf1624")
        db.open()

        self.mdLotes = QSqlTableModel(self)
        mdlDados = QSqlQueryModel(self)
        mdlDados.setQuery("SELECT * FROM lotes WHERE ativo=1")
        self.tableView.setModel(mdlDados)
        #num = mdlDados.rowCount()
        #self.lblTotalLotes.setText(num)
        self.formata_datagrid()        

    def formata_datagrid(self):
        # Redimensiona as colunas
        self.tableView.resizeColumnsToContents()
        #oculta algumas colunas que não são interessantes
        self.tableView.setColumnHidden(0,False)
        self.tableView.setColumnHidden(16,True) # Anotações
        self.tableView.setColumnHidden(17,True) # Contaminação
        self.tableView.setColumnHidden(18,True) # Fungo
        self.tableView.setColumnHidden(19,True) # Bactéria
        self.tableView.setColumnHidden(20,True) # Oxidação
        self.tableView.setColumnWidth (0,50)    # id
        self.tableView.setColumnWidth (1,50)    # Mercadoria
        self.tableView.setColumnWidth (2,50)    # Lote
        self.tableView.setColumnWidth (3,50)    # Clone
        