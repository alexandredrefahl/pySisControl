from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRegExp, QSortFilterProxyModel
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from pedidos.frmPedido.dlgSelecaoClientes import Ui_dlgSelClientes
from bibliotecas.mysqldb import *


class dlgSelecaoClientes(QtWidgets.QDialog):

    Concluido = QtCore.pyqtSignal(str, int)

    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgSelClientes()
        self.ui.setupUi(self)
        # Inicializa as variáveis globais
        self.mdlClientes = None
        self.filterProxyModel = None
        self.tabela = ""
        self.SQL = "SELECT MAX(id), cliente FROM pedidos GROUP BY cliente ORDER BY cliente"
        # Prepara o Line Edit
        icon = QtGui.QIcon("search_ico.png")
        self.ui.txtPesquisa.addAction(icon, QLineEdit.LeadingPosition)
        # Conectar os slots
        self.ui.btConfirmar.clicked.connect(self.on_Concluido)
        self.ui.btCancelar.clicked.connect(self.close)
        self.ui.rdPedidos.toggled.connect(self.on_RadioChangeEvent)
        self.ui.rdFaturamentos.toggled.connect(self.on_RadioChangeEvent)
        self.ui.rdCadastro.toggled.connect(self.on_RadioChangeEvent)
        self.show()
        # Carrega o modelo dos clientes
        self.Carrega_Clientes()
        # Conecta a função depois para dar tempo de carregar o Model
        self.ui.txtPesquisa.textChanged.connect(self.filtrar)

    def Carrega_Clientes(self):
        SQL = QtSql.QSqlQuery(self.SQL)
        SQL.exec_()
        self.mdlClientes = QSqlQueryModel()
        self.mdlClientes.setQuery(SQL)
        # Arruma os Cabecalhos
        self.mdlClientes.setHeaderData(0, QtCore.Qt.Horizontal, "ID#")
        self.mdlClientes.setHeaderData(1, QtCore.Qt.Horizontal, "Cliente")
        self.ui.tblClientes.setModel(self.mdlClientes)
        self.ui.tblClientes.setColumnWidth(0, 50)  # id
        tamanho = self.ui.tblClientes.width() - 50 - 35
        print("Carrega_Cliente > Tamanho: " + str(tamanho))
        self.ui.tblClientes.setColumnWidth(1, tamanho)  # Nome

    @QtCore.pyqtSlot()
    def filtrar(self):
        # Cria um filter proxy model
        self.filterProxyModel = QSortFilterProxyModel(self)
        # Define o model original como source para o filtro
        self.filterProxyModel.setSourceModel(self.mdlClientes)
        # Define o padrão Regex baseado no texto do lineEdit
        pattern = QRegExp("^.*" + self.ui.txtPesquisa.text() + ".*$")
        pattern.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # Define a coluna onde vai ser procurada a expresão
        self.filterProxyModel.setFilterKeyColumn(1)
        # aplica o filtro no modelo
        self.filterProxyModel.setFilterRegExp(pattern)
        # Define o sourceModel da tabela como sendo o model filtrado
        self.ui.tblClientes.setModel(self.filterProxyModel)
        # Arruma o tamanho das colunas
        self.ui.tblClientes.setColumnWidth(0, 50)  # id
        tamanho = self.ui.tblClientes.width() - 50 - 35
        print("Filtroe > Tamanho: " + str(tamanho))
        self.ui.tblClientes.setColumnWidth(1, tamanho)  # Nome

    @QtCore.pyqtSlot()
    def on_Concluido(self):
        # Pega o Id Selecionado Independente da Tabela
        Sel = self.ui.tblClientes.selectionModel().selectedRows()
        if len(Sel) <= 0:
            QMessageBox.critical(self, "Erro", "Não há nenhum cliente selecionado!", QMessageBox.Ok)
            return
        row = Sel[0].row()
        Cli_id = self.ui.tblClientes.model().data(self.ui.tblClientes.model().index(row, 0))
        # Depois verifica qual tabela usar
        if self.ui.rdPedidos.isChecked():
            self.tabela = "pedidos"
        if self.ui.rdCadastro.isChecked():
            self.tabela = "clientes"
        if self.ui.rdFaturamentos.isChecked():
            self.tabela = "docs"
        # Retorna a informação
        self.Concluido.emit(self.tabela, Cli_id)
        self.close()

    @QtCore.pyqtSlot()
    def on_RadioChangeEvent(self):
        if self.ui.rdPedidos.isChecked():
            self.SQL = "SELECT MAX(id), cliente FROM pedidos GROUP BY cliente ORDER BY cliente"
        if self.ui.rdCadastro.isChecked():
            self.SQL = "SELECT id, Nome FROM clientes ORDER BY Nome"
        if self.ui.rdFaturamentos.isChecked():
            self.SQL = "SELECT MAX(id),cliente FROM docs GROUP BY cliente ORDER BY cliente"
        self.Carrega_Clientes()
