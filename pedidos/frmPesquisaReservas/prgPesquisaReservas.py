from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QColor
import locale
from bibliotecas.mysqldb import *
from pedidos.frmCalculaFrete.prgCalculaFrete import frmCalculaFrete
from pedidos.frmPesquisaReservas.frmPesquisaReservas import Ui_frmPesquisaReservas
from selenium import webdriver
import bibliotecas.mysqldb
import mysql.connector
from mysql.connector import MySQLConnection, Error

class frmPesquisaReservas_Gui(QtWidgets.QDialog):

    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmPesquisaReservas()
        self.ui.setupUi(self)
        # Atribui as ações dos botoes
        self.ui.cmbVariedade.currentIndexChanged.connect(self.on_cmbVariedade_changed)
        self.ui.txtQtde.editingFinished.connect(self.on_txtQtde_changed)
        self.ui.txtValor.editingFinished.connect(self.on_txtValor_changed)
        self.ui.btEmail.clicked.connect(self.btEmail_Click)
        self.ui.btWhats.clicked.connect(self.btWhatsApp_Click)
        self.ui.btExcluir_item.clicked.connect(self.on_btExcluirItem_clicked)
        self.ui.btAdicionar.clicked.connect(self.on_btIncluir_clicked)
        self.ui.btExcluir.clicked.connect(self.on_btExcluir_clicked)
        self.ui.btAltera.clicked.connect(self.btAltera_clicado)
        self.ui.btPesquisar.clicked.connect(self.aplica_filtro)
        self.ui.btWhats.clicked.connect(self.envia_whats)
        self.ui.btOrcamento.clicked.connect(self.btOrcamento_Click)
        self.ui.btConfirma.clicked.connect(self.on_btConfirmada_clicked)
        self.ui.btPrazo.clicked.connect(self.btPrazo_clicado)
        self.ui.btAtendida.clicked.connect(self.on_btAtendida_clicked)
        # Formata os DataGrids
        self.ui.tblReservas.setColumnWidth(0, 50)       # id
        self.ui.tblReservas.setColumnWidth(1, 85)       # Data
        self.ui.tblReservas.setColumnWidth(2, 200)      # Nome
        self.ui.tblReservas.setColumnWidth(3, 125)      # Fone
        self.ui.tblReservas.setColumnWidth(4, 100)      # Email
        self.ui.tblReservas.setColumnWidth(5, 100)      # Cidade
        self.ui.tblReservas.setColumnWidth(6, 40)       # Uf
        self.ui.tblReservas.setColumnWidth(7, 85)       # Prazo
        self.ui.tblReservas.setColumnWidth(8, 35)       # Atendido
        # Conecta o Banco de Dados
        self.model = QtSql.QSqlQueryModel(self)
        self.db = conecta_MySql()
        self.carrega_combo()
        # Define as variáveis Globais desse módulo
        self.corReserva = QColor(24, 106, 59)
        self.corAtendida = QColor(255,195,0)
        # Carrega as reservas na tela
        self.carrega_reservas(0)
        self.clique=0
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.show()

    def aplica_filtro(self):
        self.carrega_reservas(1)

    def envia_whats(self):
        browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
        browser.get('http://www.chatdireto.com/47999640727')
        browser.get('https://mail.google.com/mail/u/0/#search/teodeandrade01%40gmail.com' )

    def carrega_reservas(self, modo):
        # Modo 0 = Traz todos os resultados | Modo 1 = Filtra os Resultados
        # self.model = QtSql.QSqlTableModel(self)
        self.ui.tblReservas.setRowCount(0)

        # Monta a SQL Base
        SQL = "SELECT id,data,nome,fone,Email,cidade,uf,prazo,atendido,confirmada FROM controle.reservas"
        if modo==0:
            #SQL = "SELECT id,data,nome,fone,Email,cidade,uf,prazo,atendido,confirmada FROM controle.reservas"
            pass
        if modo==1:
            if self.ui.rdNome.isChecked():
                SQL = SQL + " WHERE nome LIKE '%" + self.ui.txtPesquisa.text() + "%'"
            if self.ui.rdEmail.isChecked():
                SQL = SQL + " WHERE email LIKE '%" + self.ui.txtPesquisa.text() + "%'"
            if self.ui.rdFone.isChecked():
                SQL = SQL + " WHERE fone LIKE '%" + self.ui.txtPesquisa.text() + "%'"
        # Executa a SQL Pura ou Filtrada
        self.model.setQuery(QtSql.QSqlQuery(SQL))
        #self.model.setTable("reservas")
        #self.model.select()
        print("Selecionadas: " + str(self.model.rowCount()))
        # Se fosse trabalhar com dados puros usaria o tblViewModelBased mas como quero melhor controle da formatacao
        # vou usar a estratégia e povoar à mão mesmo.
        i = 0
        for i in range(self.model.rowCount()):
            # Data Row
            DR = self.model.record(i)
            self.ui.tblReservas.insertRow(self.ui.tblReservas.rowCount())
            r = self.ui.tblReservas.rowCount() - 1
            # Organiza as variáveis antes de fazer a inserção
            #ID
            varId = QTableWidgetItem('{:04}'.format(DR.value("Id")))
            varId.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            #Data
            tmpData = DR.value("Data")
            varData = QTableWidgetItem(tmpData.toString("dd/MM/yyyy"))
            varData.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            # Nome
            varNome = QTableWidgetItem(DR.value("Nome"))
            # Fone
            varFone= QTableWidgetItem(DR.value("Fone"))
            # Email
            varEmail = QTableWidgetItem(DR.value("Email"))
            varCidade = QTableWidgetItem(DR.value("Cidade"))
            varUF = QTableWidgetItem(DR.value("Uf"))
            varUF.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            #varPrazo
            tmpPrazo = DR.value("Prazo")
            varPrazo = QTableWidgetItem(tmpPrazo.toString("dd/MM/yyyy"))
            varPrazo.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            #varAtendido
            varAtendido = QTableWidgetItem(DR.value("Atendido"))
            varAtendido.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            # Insere as linhas no Table view
            self.ui.tblReservas.setItem(r, 0, varId)
            self.ui.tblReservas.setItem(r, 1, varData)
            self.ui.tblReservas.setItem(r, 2, varNome)
            self.ui.tblReservas.setItem(r, 3, varFone)
            self.ui.tblReservas.setItem(r, 4, varEmail)
            self.ui.tblReservas.setItem(r, 5, varCidade)
            self.ui.tblReservas.setItem(r, 6, varUF)
            self.ui.tblReservas.setItem(r, 7, varPrazo)
            self.ui.tblReservas.setItem(r, 8, varAtendido)
            # Se for uma reserva confirmada
            if DR.value("confirmada") == 1 and DR.value("Atendido") == 0:
                # Marca em verde as linhas das reservas confirmadas
                for j in range(0,8):
                    self.ui.tblReservas.item(r,j).setBackground(self.corReserva)
            # Se for uma reserva atendida
            if DR.value("Atendido") == 1:
                self.ui.tblReservas.item(r,8).setBackground(self.corAtendida)
        # Pega somente os selecionados
        self.Selecionados = self.ui.tblReservas.selectionModel()
        # Ao clicar dispara "carrega_itens"
        self.Selecionados.selectionChanged.connect(self.carrega_itens)
        # Limpa o grid de ítens para que não haja confusão com os selecionados
        self.ui.tblItens.setRowCount(0)

    def carrega_itens(self):
        indexRows = self.Selecionados.selectedRows()
        row=0
        if (len(indexRows)<=0):
            return 0
        for indexRow in sorted(indexRows):
            row = indexRow.row()

        #Limpa a tabela dos itens
        self.ui.tblItens.setRowCount(0)
        self.itens = QtSql.QSqlQueryModel(self)
        if (row>=0):
            varID = self.model.record(row).value("id")
        else:
            varID= -1
        # Monta a SQL Base
        SQL = "SELECT id,Mercadoria,Clone,Descricao,Quantidade,Preco FROM controle.reservas_itens WHERE Doc_ID=" + str(varID)
        self.itens.setQuery(QtSql.QSqlQuery(SQL))
        for i in range(0,self.itens.rowCount()):
            # Data Row
            DR = self.itens.record(i)
            self.ui.tblItens.insertRow(self.ui.tblItens.rowCount())
            r = self.ui.tblItens.rowCount() - 1
            # Organiza as variáveis antes de fazer a inserção
            # ID
            varId = QTableWidgetItem('{:04}'.format(DR.value("Id")))
            varId.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            # Mercadoria
            varMerc = QTableWidgetItem('{:03}'.format(DR.value("Mercadoria")))
            varMerc.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            # Clone
            varClone = QTableWidgetItem('{:04}'.format(DR.value("Clone")))
            varClone.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            # Descricao
            varDesc = QTableWidgetItem(DR.value("Descricao"))
            # Quantidade
            varQtde = QTableWidgetItem(QTableWidgetItem(str(DR.value("Quantidade"))))
            varQtde.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            # Valor
            varValor = QTableWidgetItem(locale.format_string('%.2f', DR.value("Preco")))
            varValor.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            # Insere as linhas no Table view
            self.ui.tblItens.setItem(r, 0, varId)
            self.ui.tblItens.setItem(r, 1, varMerc)
            self.ui.tblItens.setItem(r, 2, varClone)
            self.ui.tblItens.setItem(r, 3, varDesc)
            self.ui.tblItens.setItem(r, 4, varQtde)
            self.ui.tblItens.setItem(r, 5, varValor)
            # Formatar o DataGrid
            self.ui.tblItens.setColumnWidth(0, 50)  # id
            self.ui.tblItens.setColumnWidth(1, 50)  # Merc
            self.ui.tblItens.setColumnWidth(2, 50)  # Clone
            self.ui.tblItens.setColumnWidth(3, 468) # Descrição
            self.ui.tblItens.setColumnWidth(4, 80)  # Quantidade
            self.ui.tblItens.setColumnWidth(5, 80)  # Valor

    def carrega_combo(self):
        self.ComboModel = QtSql.QSqlTableModel(self)
        self.ComboModel.setTable("selecao_clones")
        self.ComboModel.select()
        self.ui.cmbVariedade.setModel(self.ComboModel)
        self.ui.cmbVariedade.setModelColumn(self.ComboModel.fieldIndex("Descricao"))

    def btEmail_Click(self):
        pass

    def btWhatsApp_Click(self):
        pass

    def btOrcamento_Click(self):
        frmOrcamento = frmCalculaFrete()
        # Tem que "subir" 3 níveis de Parent para Chegar na MDI window.
        subWindow = self.parent().parent().parent().addSubWindow(frmOrcamento)
        subWindow.resize(frmOrcamento.size())
        subWindow.showNormal()
        print("Orçamento Click")

    def on_cmbVariedade_changed(self):
        DR = self.ComboModel.record(self.ui.cmbVariedade.currentIndex())
        varPreco = locale.format_string('%.2f', DR.field(4).value())
        self.ui.txtValor.setText(varPreco)
        if self.ui.txtQtde.text() == "":
            valItem=0
        else:
            valItem=int(self.ui.txtQtde.text())
        varTotal = locale.format_string('%.2f',(valItem* DR.field(4).value()))
        self.ui.txtTotalItem.setText(varTotal)

    def on_txtQtde_changed(self):
        self.on_cmbVariedade_changed()

    def on_txtValor_changed(self):
        self.total_do_item()

    def total_do_item(self):
        valor = locale.atof(self.ui.txtValor.text())
        qtde = int(self.ui.txtQtde.text())
        total = valor * qtde
        self.ui.txtTotalItem.setText(locale.format_string('%.2f',total))

    def on_btIncluir_clicked(self):
        # Pega o Datarow do modelo que contém as informações do ítem
        DR = self.ComboModel.record(self.ui.cmbVariedade.currentIndex())
        # Prepara as variáveis de inserção
        varQtde = int(self.ui.txtQtde.text())
        varDescricao = DR.field(3).value()
        varMerc = DR.field(1).value()
        varClone = DR.field(2).value()
        varValor = locale.atof(self.ui.txtValor.text())
        varForma = "Muda Aclimatizada"
        # Pega o ID da reserva que vai ser modificada
        SelRow = self.ui.tblReservas.selectedIndexes()
        row=SelRow[0].row()
        idParent = self.ui.tblReservas.item(row, 0).text()
        print("ID da Reserva: " + idParent )
        # Monta a SQL de Inclusão
        SQL = "INSERT INTO reservas_itens (`Doc_ID`,`Mercadoria`,`Clone`,`Descricao`,`Quantidade`,`Preco`,`Forma`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        # Parametros da inclusão
        args = (idParent,varMerc,varClone,varDescricao,varQtde,varValor,varForma)
        try:
            # define a connection string
            conn = mysql.connector.connect(host=bibliotecas.mysqldb.curHost, user=bibliotecas.mysqldb.user,
                                           passwd=bibliotecas.mysqldb.pasw, database=bibliotecas.mysqldb.database)
            # define um "cursor" operador das transações
            cursor = conn.cursor()
            # executa
            cursor.execute(SQL, args)
            conn.commit()
        except Error as error:
            print(error)
        finally:
            #cursor.close()
            #conn.close()
            print("Item incluido com sucesso")
        # Atualiza Itens na view
        self.carrega_itens()
        self.ui.txtQtde.setText("")

    def on_btExcluirItem_clicked(self):
        if len(self.ui.tblItens.selectionModel().selectedRows()) == 0:
            return False
        # Pega os dados da linha clicada identifica o campo
        SelRows = self.ui.tblItens.selectedIndexes()
        row = SelRows[0].row()
        idItem = self.ui.tblItens.item(row,0).text()
        print("Id do Item: " + idItem)
        vConf = QMessageBox.question(self,"Confirmação", "Você confirma a exclusão deste ítem?", QMessageBox.Yes | QMessageBox.No)
        if vConf == QMessageBox.Yes:
            SQL = "DELETE FROM reservas_itens WHERE id = " + idItem
            #args = (idItem)
            try:
                # define a connection string
                conn = mysql.connector.connect(host=bibliotecas.mysqldb.curHost, user=bibliotecas.mysqldb.user,
                                               passwd=bibliotecas.mysqldb.pasw, database=bibliotecas.mysqldb.database)
                # define um "cursor" operador das transações
                cursor = conn.cursor()
                # executa
                cursor.execute(SQL)
                # Efetiva no Banco de Dados
                conn.commit()
            except Error as error:
                print(error)
            finally:
                print(cursor.rowcount, " registro(s) excluido(s)")
                cursor.close()
                conn.close()

        # Atualiza Itens na view
        self.carrega_itens()

    def on_btExcluir_clicked(self):
        if len(self.ui.tblReservas.selectionModel().selectedRows()) <= 0:
            return False
        # Pega o ID da reserva selecionada no TableView
        SelRow = self.ui.tblReservas.selectedIndexes()
        row = SelRow[0].row()
        idReserva = self.ui.tblReservas.item(row, 0).text()

        vConf = QMessageBox.question(self,"Confirmação", "Você confirma a exclusão desta reserva e TODOS os seus itens?", QMessageBox.Yes | QMessageBox.No)
        if vConf == QMessageBox.Yes:
            SQLReserva= "DELETE FROM reservas WHERE id=" + idReserva
            #args1 = (idReserva)
            SQLItens = "DELETE FROM reservas_itens WHERE Doc_id=" + idReserva
            #args2 = (idReserva)
            try:
                # define a connection string
                conn = mysql.connector.connect(host=bibliotecas.mysqldb.curHost, user=bibliotecas.mysqldb.user,
                                               passwd=bibliotecas.mysqldb.pasw, database=bibliotecas.mysqldb.database)
                # define um "cursor" operador das transações
                cursor = conn.cursor()
                # executa
                cursor.execute(SQLItens)
                conn.commit()
                cursor.execute(SQLReserva)
                conn.commit()
            except Error as error:
                print(error)
            finally:
                cursor.close()
                conn.close()
                QMessageBox.information(self,"Confirmação","A Reserva " + idReserva + " e TODOS os seus itens foi Excluída!",QMessageBox.Ok)
                self.carrega_reservas(1)
            # Atualiza Itens na view

    def btAltera_clicado(self):
        if self.ui.btAltera.text() == "Alterar":
            # Se não tiver nada selecionado então já sai da rotina
            if len(self.ui.tblItens.selectionModel().selectedRows()) <= 0:
                return False
            # Pega o ID do ítem que será alterado
            SelRow = self.ui.tblItens.selectedIndexes()
            if len(SelRow) <= 0:
                return False
            row = SelRow[0].row()
            self.idItem = self.ui.tblItens.item(row, 0).text()
            # Prepara para a próxima etapa que é de salvar
            self.ui.btAltera.setText("Salvar")
            #self.ui.tblItens.setEnabled(False)
            # Pega os dados da linha selecionada na tabela de ítens
            self.ui.txtQtde.setText(self.ui.tblItens.item(row, 4).text())
            # Localiza o item no combo, de acordo com o ítem da reserva
            idx = self.ui.cmbVariedade.findText(self.ui.tblItens.item(row, 3).text(), QtCore.Qt.MatchFixedString)
            if idx >= 0:
                self.ui.cmbVariedade.setCurrentIndex(idx)
            # Define o valor conforme foi ajustado com o cliente
            self.ui.txtValor.setText(self.ui.tblItens.item(row, 5).text())
            # Desabilita a tabela para não poder mudar nada
            return False
        elif self.ui.btAltera.text() == "Salvar":
            print('Texto do botão:', self.ui.btAltera.text())
            print('Texto é Salvar')
            #selrow = self.ui.tblItens.selectedIndexes()
            #row = selrow[0].row()
            #print(row)
            #if len(selrow) <= 0:
            #    return False
            #idItem = self.ui.tblItens.item(row, 0).text()
            self.ui.btAltera.setText("Alterar")
            self.ui.tblItens.setEnabled(True)
            DR = self.ComboModel.record(self.ui.cmbVariedade.currentIndex())
            # Monta a Query para alteração
            qryAlteraItem = QtSql.QSqlQuery()
            qryAlteraItem.prepare("UPDATE reservas_itens SET quantidade=:qtde, preco=:preco, mercadoria=:merc, clone=:clone, descricao=:descricao WHERE id=:idItem")
            qryAlteraItem.bindValue(':idItem',self.idItem)
            qryAlteraItem.bindValue(':qtde',int(self.ui.txtQtde.text()))
            qryAlteraItem.bindValue(':preco', locale.atof(self.ui.txtValor.text()))
            qryAlteraItem.bindValue(':merc',DR.field(1).value())
            qryAlteraItem.bindValue(':clone',DR.field(2).value())
            qryAlteraItem.bindValue(':descricao',DR.field(3).value())
            try:
                print('Passou aqui')
                qryAlteraItem.exec()
            except Error as error:
                QMessageBox.critical(self,"Erro","Erro ao alterar o item " + str(self.idItem) + "\n" + qryAlteraItem.lastError().text() + "\n")
                print(error)
            finally:
                self.carrega_itens()
                self.ui.btAltera.setText("Alterar")
                #self.ui.tblItens.setEnabled(True)
                QMessageBox.information(self,"Confirmação","Item " + str(self.idItem) + " atualizado com sucesso!")

    def on_btConfirmada_clicked(self):
        if len(self.ui.tblReservas.selectionModel().selectedRows()) <=0:
            return False
        SelRow = self.ui.tblReservas.selectedIndexes()
        row = SelRow[0].row()
        idReserva = self.ui.tblReservas.item(row, 0).text()
        a = QMessageBox.question(self,"Confirmação","A Reserva " + str(idReserva) + " será marcada como confirmada?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if a == QMessageBox.Yes:
            SQL = "UPDATE reservas SET confirmada=1 WHERE id=" + str(idReserva)
            try:
                qryConfirmada = QtSql.QSqlQuery()
                qryConfirmada.exec_(SQL)
                print("Linhas afetadas: " + str(qryConfirmada.numRowsAffected()))
                print("Erro:" + qryConfirmada.lastError().text())
            except Error as error:
                print(error)
            finally:
                #cursor.close()
                #conn.close()
                for j in range(0, 8):
                    self.ui.tblReservas.item(row, j).setBackground(self.corReserva)
                QMessageBox.information(self,"Confirmação","A Reserva " + str(idReserva) + " foi confirmada com sucesso!",QMessageBox.Ok)

    def btPrazo_clicado(self):
        if len(self.ui.tblReservas.selectionModel().selectedRows()) <=0:
            return False
        # Pega a informação de data
        texto, okPressed = QInputDialog.getText(self,"Definição de Prazo","Prazo de Entrega (9999-12-31):",QLineEdit.Normal,"")
        # Verifica se foi informada a data
        if okPressed and texto != "":
            SelRow = self.ui.tblReservas.selectedIndexes()
            row = SelRow[0].row()
            idReserva = self.ui.tblReservas.item(row, 0).text()
            varData = texto
            SQL = "UPDATE reservas SET prazo='" + varData + "' WHERE id=" + str(idReserva)
            try:
                qryPrazo = QtSql.QSqlQuery()
                qryPrazo.exec_(SQL)
                print("Linhas afetadas: " + str(qryPrazo.numRowsAffected()))
                print("Erro:" + qryPrazo.lastError().text())
                # define a connection string
                #conn = mysql.connector.connect(host=bibliotecas.mysqldb.curHost, user=bibliotecas.mysqldb.user,
                #                               passwd=bibliotecas.mysqldb.pasw, database=bibliotecas.mysqldb.database)
                # define um "cursor" operador das transações
                #cursor = conn.cursor()
                # executa
                #cursor.execute(SQL)
                #conn.commit()
            except Error as error:
                print(error)
            finally:
                #cursor.close()
                #conn.close()
                QMessageBox.information(self,"Confirmação","O Prazo da reserva " + str(idReserva) + " foi alterado para " + texto)
                # Recarrega as reservas com o valor correto do prazo já
                #if len(self.ui.txtPesquisa.text()) > 1:
                #    self.carrega_reservas(1)
                #else:
                #    self.carrega_reservas(0)
            print(texto)

    def on_btAtendida_clicked(self):
        if len(self.ui.tblReservas.selectionModel().selectedRows()) <= 0:
            return False
        # Pega o ID da reserva selecionada no TableView
        SelRow = self.ui.tblReservas.selectedIndexes()
        row = SelRow[0].row()
        print("btAtendida Row :" + str(row))
        idReserva = self.ui.tblReservas.item(row, 0).text()
        print("btAtendida idReserva: "+str(idReserva))
        # Envia um Messagebox de confirmação
        vConf = QMessageBox.question(self,"Confirmação", "Você a liquidação (Atendimento) desta reserva e TODOS os seus itens?", QMessageBox.Yes | QMessageBox.No)
        if vConf == QMessageBox.Yes:
            SQLReserva= "UPDATE Reservas SET Atendido=1 WHERE id=" + idReserva
            try:
                qryAtendido = QtSql.QSqlQuery()
                qryAtendido.exec_(SQLReserva)
                print("Linhas afetadas: " + str(qryAtendido.numRowsAffected()))
                print("Erro:" + qryAtendido.lastError().text())
            except Error as error:
                print(error)
            finally:
                #cursor.close()
                #conn.close()
                QMessageBox.information(self,"Confirmação","A Reserva " + idReserva + " e TODOS os seus itens foram marcados como atendidos!",QMessageBox.Ok)
                self.carrega_reservas(1)
            # Atualiza Itens na view

