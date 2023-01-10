from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlQuery,QSqlQueryModel
from pedidos.frmPedido.dlgSelecaoClientes import Ui_dlgSelClientes
from bibliotecas.mysqldb import *

class dlgSelecaoClientes(QtWidgets.QDialog):

    Concluido = QtCore.pyqtSignal(str,int)

    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgSelClientes()
        self.ui.setupUi(self)

        self.ui.btConfirmar.clicked.connect(self.on_Concluido)
        self.ui.btCancelar.clicked.connect(self.close)
        # Carrega o banco de dados
        #self.db1 = conecta_MySql()

        # Carrega o modelo dos clientes
        self.Carrega_Clientes()
        self.show()

    def Carrega_Clientes(self):
        SQL = QtSql.QSqlQuery( "SELECT distinct id, cliente from pedidos order by cliente" )
        SQL.exec_()
        self.mdlClientes_Pedidos = QSqlQueryModel()
        self.mdlClientes_Pedidos.setQuery(SQL)
        # Arruma os Cabecalhos
        self.mdlClientes_Pedidos.setHeaderData(0,QtCore.Qt.Horizontal,"Pedido")
        self.mdlClientes_Pedidos.setHeaderData(1, QtCore.Qt.Horizontal, "Cliente")
        print("Selecionadas: " + str(self.mdlClientes_Pedidos.rowCount()))
        self.ui.tblClientes.setModel(self.mdlClientes_Pedidos)
        header = self.ui.tblClientes.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    def on_Concluido(self):
        # Pega o Id Selecionado Independente da Tabela
        Sel = self.ui.tblClientes.selectionModel().selectedRows()
        row = Sel[0].row()
        Cli_id = self.ui.tblClientes.model().data(self.ui.tblClientes.model().index(row, 0))
        # Depois verifica qual tabela usar
        tabela=""
        if self.ui.rdPedidos.isChecked():
            tabela = "pedidos"
        if self.ui.rdCadastro.isChecked():
            tabela = "clientes"
        if self.ui.rdFaturamentos.isChecked():
            tabela = "docs"
        # Retorna a informação
        self.Concluido.emit(tabela,Cli_id)
        self.close()