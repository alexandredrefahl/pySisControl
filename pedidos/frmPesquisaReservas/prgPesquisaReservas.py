from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QInputDialog, QLineEdit, QTreeWidgetItemIterator
from PyQt5.QtGui import QColor
import locale
from bibliotecas.mysqldb import *
from pedidos.frmCalculaFrete.prgCalculaFrete import frmCalculaFrete
from pedidos.frmPesquisaReservas.frmPesquisaReservas import Ui_frmPesquisaReservas
import bibliotecas.mysqldb
import mysql.connector
from mysql.connector import Error

class frmPesquisaReservas_Gui(QtWidgets.QDialog):

    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmPesquisaReservas()
        self.ui.setupUi(self)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
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
        self.ui.btOrcamento.clicked.connect(self.btOrcamento_Click)
        self.ui.btConfirma.clicked.connect(self.on_btConfirmada_clicked)
        self.ui.btPrazo.clicked.connect(self.btPrazo_clicado)
        self.ui.btAtendida.clicked.connect(self.on_btAtendida_clicked)
        self.ui.rdProdutos.toggled.connect(self.rdProdutos_change)
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
        # Desabilita por padrão o painel de variedades
        self.ui.treeWidget.setVisible(False)
        self.ui.grpSelecao.setVisible(False)
        # Conecta o Banco de Dados
        self.model = QtSql.QSqlQueryModel(self)
        self.db = conecta_MySql()
        self.carrega_combo()
        # Define as variáveis Globais desse módulo
        #self.corReserva = QColor(24, 106, 59)
        self.corReserva = QColor(130, 190, 105)
        #self.corAtendida = QColor(255,195,0)
        self.corAtendida = QColor(235, 235, 129)
        # Carrega as reservas na tela
        self.carrega_reservas(0)
        self.clique=0
        self.show()

    def aplica_filtro(self):
        self.carrega_reservas(1)

    def envia_whats(self):
        # Se não tiver nenhuma reserva Selecionada já sai
        if len(self.ui.tblReservas.selectionModel().selectedRows()) == 0:
            return False
        # Pega os dados da linha clicada identifica o campo
        SelRows = self.ui.tblReservas.selectedIndexes()
        row = SelRows[0].row()
        idReserva = self.ui.tblReservas.item(row, 0).text()
        whats = self.ui.tblReservas.item(row, 3).text()
        print("Whats do Cliente " + whats)
        # Se tiver número registrado
        if len(whats) > 0:
            # Arruma o número para o formato do WhatsWeb
            import webbrowser
            import re
            whats = re.sub("[^0-9]", "", whats)
            print("Whats do Cliente já processado: " + whats)
            firefox = webbrowser.Mozilla("/usr/bin/firefox")
            firefox.open("https://web.whatsapp.com/send?phone=55" + whats)
    def rdProdutos_change(self):
        if self.ui.rdProdutos.isChecked():
            self.ui.treeWidget.setVisible(True)
            self.ui.grpSelecao.setVisible(True)
        else:
            self.ui.treeWidget.setVisible(False)
            self.ui.grpSelecao.setVisible(False)
    def carrega_reservas(self, modo):
        # Modo 0 = Traz todos os resultados | Modo 1 = Filtra os Resultados
        # self.model = QtSql.QSqlTableModel(self)
        self.ui.tblReservas.setRowCount(0)

        # Monta a SQL Base
        SQL = "SELECT id,data,nome,fone,Email,cidade,uf,prazo,atendido,confirmada FROM controle.reservas"
        if modo == 0:
            #SQL = "SELECT id,data,nome,fone,Email,cidade,uf,prazo,atendido,confirmada FROM controle.reservas"
            pass
        if modo == 1:
            if self.ui.rdNome.isChecked():
                SQL = SQL + " WHERE nome LIKE '%" + self.ui.txtPesquisa.text() + "%'"
            if self.ui.rdEmail.isChecked():
                SQL = SQL + " WHERE email LIKE '%" + self.ui.txtPesquisa.text() + "%'"
            if self.ui.rdFone.isChecked():
                SQL = SQL + " WHERE fone LIKE '%" + self.ui.txtPesquisa.text() + "%'"
            if self.ui.rdProdutos.isChecked():
                SQL = SQL + " WHERE id IN(" + self.retornaIDSelecao() + ")"
                print(SQL)
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
            if DR.value("Atendido") == 1:
                varAtendido = QTableWidgetItem("X")
            else:
                varAtendido = QTableWidgetItem("")
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
                for j in range(0,9):
                    self.ui.tblReservas.item(r, j).setBackground(self.corReserva)
            # Se for uma reserva atendida
            if DR.value("Atendido") == 1:
                for j in range(0, 9):
                    self.ui.tblReservas.item(r, j).setBackground(self.corAtendida)
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
        # Se não tiver nenhuma reserva Selecionada já sai
        if len(self.ui.tblReservas.selectionModel().selectedRows()) == 0:
            return
        # Pega os dados da linha clicada identifica o campo
        SelRows = self.ui.tblReservas.selectedIndexes()
        row = SelRows[0].row()
        email = self.ui.tblReservas.item(row, 4).text()
        if len(email) > 0:
            from PyQt5.Qt import QApplication
            QApplication.clipboard().setText(email)
            QMessageBox.information(self, "Área de Transferência", "E-mail do cliente copiado para área de transferência \r" + email, QtWidgets.QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Erro", "O Cliente não tem e-mail registrado na reserva", QMessageBox.Ok)
            return


    def btWhatsApp_Click(self):
        self.envia_whats()

    def btOrcamento_Click(self):
        # Se não tiver nenhuma reserva Selecionada já sai
        if len(self.ui.tblReservas.selectionModel().selectedRows()) == 0:
            return
        # Pega os dados da linha clicada identifica o campo
        SelRows = self.ui.tblReservas.selectedIndexes()
        row = SelRows[0].row()
        idReserva = self.ui.tblReservas.item(row, 0).text()
        frmOrcamento = frmCalculaFrete()
        frmOrcamento.idReserva = idReserva
        frmOrcamento.Carrega_Dados_Reserva()
        # Tem que "subir" 3 níveis de Parent para Chegar na MDI window.
        subWindow = self.parent().parent().parent().addSubWindow(frmOrcamento)
        subWindow.resize(frmOrcamento.size())
        subWindow.showNormal()

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
            except Error as error:
                print(error)
            finally:
                QMessageBox.information(self,"Confirmação","O Prazo da reserva " + str(idReserva) + " foi alterado para " + texto)
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
                QMessageBox.information(self,"Confirmação","A Reserva " + idReserva + " e TODOS os seus itens foram marcados como atendidos!",QMessageBox.Ok)
                self.carrega_reservas(1)
            # Atualiza Itens na view

    def retornaIDSelecao(self):
        # Verifica o que está selecionado
        iterator = QTreeWidgetItemIterator(self.ui.treeWidget, QTreeWidgetItemIterator.Checked)
        selFields = []
        while iterator.value():
            item = iterator.value()
            Var, Clone = item.text(0)[:7].split(".")
            # Monta o nome do campo no formato BRS99_999
            selFields.append("BRS" + Var + "_" + "{:03d}".format(int(Clone)))
            iterator += 1
        # Se não houver nada selecionado já sai da função
        if len(selFields) == 0:
            return ""

        clausula = ""

        # A Cláusula vai depender do que está selecionado nos Radio Buttons

        #
        # Clausula SOMENTE
        #
        if self.ui.rdSomente.isChecked():
            # Pega TODOS os campos que estão constando no relatóro
            SQLCampos = "SHOW COLUMNS FROM planilha_reservas"
            try:
                qryCampos = QtSql.QSqlQuery()
                qryCampos.exec_(SQLCampos)
                print("qryCampos: Linhas retornadas: " + str(qryCampos.numRowsAffected()))
            except Error as error:
                print("Erro:" + qryCampos.lastError().text())
                print(error)
                return ""
            allFields = []
            while qryCampos.next():
                if qryCampos.value(0)[:3] == "BRS":
                    allFields.append(qryCampos.value(0))
            # Garante que existe pelo menos um campo selecionado
            for c in selFields:
                if len(clausula) > 0:
                    clausula += " AND " + c + " > 0"
                else:
                    clausula += " " + c + " > 0"
                # Tira o campo Selecionado da lista de TODOS os campos
                allFields.remove(c)
            # Pega TODOS os outros campos e exclui a pesquisa
            for n in allFields:
                clausula += " AND ISNULL(" + n + ")"
        #
        # Clausula PELO MENOS
        #
        elif self.ui.rdPeloMenos.isChecked():
            # Monta a Clausula WHERE que vai ser usada
            for c in selFields:
                if len(clausula) > 0:
                    clausula += " AND " + c + " > 0"
                else:
                    clausula += " " + c + " > 0"

        #
        # Cláusulo NÃO CONTENHA
        #
        elif self.ui.rdNaoContenha.isChecked():
            # Monta a Clausula WHERE que vai ser usada
            for c in selFields:
                if len(clausula) > 0:
                    clausula += " AND ISNULL(" + c + ")"
                else:
                    clausula += " ISNULL(" + c + ")"

        # Com a cláusula montada vamos à execução final para Retornar os IDs
        SQL = "SELECT id FROM planilha_reservas WHERE" + clausula
        print(SQL)  # Só pra Debug
        qryIDs = QtSql.QSqlQuery()
        valid = qryIDs.prepare(SQL)
        if valid:
            try:
                qryIDs.exec_(SQL)
            except Error as error:
                print("Erro:" + qryIDs.lastError().text())
                print(error)
                return ""
            # Monta os IDS que serão retornados para função principal
            ids = ""
            while qryIDs.next():
                if len(ids) == 0:
                    ids += str(qryIDs.value(0))
                else:
                    ids += "," + str(qryIDs.value(0))
            return ids
        else:
            QMessageBox.critical(self, "Erro no critério de seleção", "Pesquisa não tem critério válido", QMessageBox.Ok)
            return ""
