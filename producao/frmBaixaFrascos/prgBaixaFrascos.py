import locale

from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QApplication

from bibliotecas.mysqldb import *
from producao.frmBaixaFrascos.frmBaixaFrascos import Ui_frmBaixaFrascos


class frmBaixaFrascos(QDialog):

    # Construtor da Classe
    def __init__(self):
        # Importa o construtor da Classe pai "QDialog"
        super().__init__()
        self.ui = Ui_frmBaixaFrascos()
        self.ui.setupUi(self)
        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Conecta os Eventos às suas Funções de Tratamento
        self.ui.txtCodigo.editingFinished.connect(self.txtCodigo_editingFinished)
        self.ui.txtCodigo.installEventFilter(self)
        # self.ui.btBaixar.clicked.connect(self.btBaixar_Clicked)

        # Inicializa a lista de Ids
        self.ids = []
        self.ids_lotes=[]

        # Personaliza interface
        self.ui.tblFrascos.setColumnWidth(0, 140)  # ID
        self.ui.tblFrascos.setColumnWidth(1, 75)  # Mercadoria
        self.ui.tblFrascos.setColumnWidth(2, 75)  # Lote
        self.ui.tblFrascos.setColumnWidth(3, 75)  # Clone
        self.ui.tblFrascos.setColumnWidth(4, 70)  # Nº Frasco
        self.ui.tblFrascos.setColumnWidth(5, 60)  # Motivo
        self.ui.tblFrascos.setColumnWidth(6, 70)  # Nº Mudas
        # self.ui.tblFrascos.setAlternatingRowColors(1)
        # Coloca data atual nas caixas de Data
        self.ui.txtData.setDateTime(QtCore.QDateTime.currentDateTime())
        # Conecta o Mysql e carrega os dados no combo
        self.db = conecta_MySql()
        # Carrega os repicadores no combo
        self.carrega_combo()
        # Finaliza o setUp e mostra a interface
        self.show()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and source is self.ui.txtCodigo):
            # print('key press:', (event.key(), event.text()))
            if event.key() == QtCore.Qt.Key_F12:
                print("Pressionado F12")
                # Se foi pressionado F12 Aciona a rotina de baixar os frascos
                self.btBaixar_Clicked()
        return super(QDialog, self).eventFilter(source, event)

    def carrega_combo(self):
        # Monta a query
        Query = QSqlQuery("SELECT id,nome FROM controle.repicador where ativo=1")
        # Enquanto houver resultados
        while Query.next():
            self.ui.cmbOperador.addItem(Query.value(1), Query.value(0))

    def txtCodigo_editingFinished(self):
        if len(self.ui.txtCodigo.text()) == 0:
            return

        if int(self.ui.txtCodigo.text()) in self.ids:
            print("Frasco já está na lista")
            QMessageBox.information(self, "Aviso", "Este Frasco já está na lista!", QMessageBox.Ok)
            self.ui.txtCodigo.setText("")
            self.ui.txtCodigo.setFocus()
            return

        # Define uma cor para cada tipo de baixa
        corFungo = QColor(233, 198, 175, 127)
        corBacteria = QColor(238, 255, 170, 127)
        corOxidacao = QColor(204, 204, 204, 127)
        corPlantio = QColor(170, 255, 170, 127)
        corRepicagem =  QColor(153, 255, 85, 127)
        # prepara a SQL que vai buscar as informações do frasco
        busca = QSqlQuery()
        busca.prepare(
            'SELECT id,variedade,(SELECT lotes.lote from lotes where lotes.id=aux_frascos.lote) as nLote,clone,vidro,nmudas,Lote FROM aux_frascos where id= ? ')
        busca.addBindValue(int(self.ui.txtCodigo.text()))
        busca.exec_()
        if busca.size() > 0:
            # Move para o primeiro registro
            busca.first()
            # Acrescenta uma linha
            self.ui.tblFrascos.insertRow(self.ui.tblFrascos.rowCount())
            # Prepara as células que vão ser incluidas
            varID = QTableWidgetItem('{:013}'.format(busca.value("id")))
            varMerc = QTableWidgetItem('{:02}'.format(busca.value("variedade")))
            varLot = QTableWidgetItem('{:03}'.format(busca.value("nLote")))
            varClone = QTableWidgetItem('{:04}'.format(busca.value("clone")))
            varVidro = QTableWidgetItem('{:03}'.format(busca.value("vidro")))
            varMot = ""
            if self.ui.radioButton.isChecked():
                varMot = "F"
                corLinha = corFungo
            elif self.ui.radioButton_2.isChecked():
                varMot = "B"
                corLinha = corBacteria
            elif self.ui.radioButton_3.isChecked():
                varMot = "O"
                corLinha = corOxidacao
            elif self.ui.radioButton_4.isChecked():
                varMot = "P"
                corLinha = corPlantio
            elif self.ui.radioButton_5.isChecked():
                varMot = "R"
                corLinha = corRepicagem
            print("Motivo: ", varMot)
            varMotivo = QTableWidgetItem(varMot)
            print("Qtde: ", busca.value("nmudas"))
            varNMudas = QTableWidgetItem(str(busca.value("nmudas")))
            lin = self.ui.tblFrascos.rowCount() - 1
            # Faz a inclusão dos ítens
            self.ui.tblFrascos.setItem(lin, 0, varID)
            self.ui.tblFrascos.setItem(lin, 1, varMerc)
            self.ui.tblFrascos.setItem(lin, 2, varLot)
            self.ui.tblFrascos.setItem(lin, 3, varClone)
            self.ui.tblFrascos.setItem(lin, 4, varVidro)
            self.ui.tblFrascos.setItem(lin, 5, varMotivo)
            self.ui.tblFrascos.setItem(lin, 6, varNMudas)
            print(lin)
            for i in range(0, self.ui.tblFrascos.columnCount()):
                self.ui.tblFrascos.item(lin, i).setBackground(corLinha)
            # Atualiza o número de frascos
            self.ui.lblNFrascos.setText(str(self.ui.tblFrascos.rowCount()))
            # Atualiza a lista de Ids
            self.ids.append(busca.value("id"))
            # Evitar lotes repetidos e um trabalho excessivo do servidor
            if busca.value("Lote") not in self.ids_lotes:
                self.ids_lotes.append(busca.value("Lote"))
                print("Lote Analisado: ",busca.value("Lote"))
            self.ui.txtCodigo.setText("")
            self.ui.txtCodigo.setFocus()

    def txtCodigo_returnPressed(self):
        print("Foi pressionado Enter")

    def btBaixar_Clicked(self):
        # Primeiro verifica se tem linhas a serem baixadas
        if self.ui.tblFrascos.rowCount() == 0:
            # Se não tiver nenhum frasco na tabela retorna sem fazer nada
            return

        # Muda para Wait Cursor
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # Percorre os ítens da tabela para fazer a baixa
        numLinhas = self.ui.tblFrascos.rowCount()
        # Para fazer a porcentagem correta
        self.ui.pbBaixa.setMaximum(numLinhas)
        baixas = []
        for row in range(0, numLinhas):
            varID = int(self.ui.tblFrascos.item(row, 0).text())
            varMot = self.ui.tblFrascos.item(row, 5).text()
            varOp = self.ui.cmbOperador.itemData(self.ui.cmbOperador.currentIndex())
            # Por procedimento baixar frasco por frasco
            sql = QSqlQuery()
            sql.prepare("UPDATE aux_frascos SET bxExclusao = CURRENT_TIMESTAMP(), bxOperador= :op, bxMotivo = :mot WHERE id = :id")
            sql.bindValue(":op", varOp)
            sql.bindValue(":mot", varMot)
            sql.bindValue(":id", varID)
            sql.exec()
            nRows = sql.numRowsAffected()
            self.ui.lblMsg.setText("Atualizando Frasco:"+ str(varID))
            self.ui.lblMsg.repaint()
            print(nRows, " Frascos atualizados (",varID,")")
            self.ui.pbBaixa.setValue(row)
            self.ui.pbBaixa.repaint()
        # Transforma a variável List em Lista separada por vírgula
        varIDs = ','.join(map(str, self.ids_lotes))
        print("Lista IDs Lotes: ",varIDs)
        # Recalcula estoque dos lotes afetados (Deixa tudo o trabalho para o servidor)
        for curID in self.ids_lotes:
            sql_Lotes = QSqlQuery()
            sql_Lotes.prepare('CALL atualiza_estoque_lote(:idLote)')
            sql_Lotes.bindValue(":idLote", curID)
            self.ui.lblMsg.setText("Atualizando Estoque do Lote:" + str(curID))
            self.ui.lblMsg.repaint()
            try:
                sql_Lotes.exec()
                print("Estoque atualizado: ",curID, " Rows Affected: ",sql_Lotes.numRowsAffected())
            except:
                print("Ocorreu um erro ao recalcular o estoque dos lotes")
                print("Erro: ",sql_Lotes.lastError())
                # Volta o cursor ao normal
                QApplication.restoreOverrideCursor()
        # Limpa a tabela de frascos
        self.ui.tblFrascos.setRowCount(0)
        self.ui.pbBaixa.setValue(0)
        self.ui.lblNFrascos.setText("0")
        self.ui.lblMsg.setText("...")
        self.ids = []
        # Volta o cursor ao normal
        QApplication.restoreOverrideCursor()

