import locale
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from skpy import Skype

from bibliotecas.mysqldb import *
from bibliotecas.biblioteca import calculaSEDEX
from pedidos.frmCalculaFrete.frmNewCalculaFrete import *
from pedidos.frmCalculaFrete.libJadLog import *


class frmCalculaFrete(QDialog):
    # Define variáveis globais que vão ser usadas em toda a Classe
    total = 0
    peso = 0
    volume = 0
    mudas = 0
    TamCaixa = ""

    # Só define o id para carregar o orçamento e Executa tudo o outro inicializador
    def __init__(self,IdReserva):
        self.idReserva = IdReserva
        self.__init__()
        self.Carrega_Dados_Reserva(IdReserva)

    # Inicializador Padrão sem parâmetros
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Vincula os botões às suas funções de ação
        self.ui.btAcrescentar.clicked.connect(self.incluir_item)
        self.ui.btLimpar.clicked.connect(self.Limpa_Campos)
        self.ui.btFrete.clicked.connect(self.Calculo_Frete)
        self.ui.btSendSkype.clicked.connect(self.Envia_Cotacao_Skype)
        self.ui.btCopyMail.clicked.connect(self.copia_email)
        self.ui.btCopyWhats.clicked.connect(self.Copia_Whats)
        self.ui.txtCEP.editingFinished.connect(self.txtCEP_editingFinished)
        self.ui.txtValFrete.editingFinished.connect(self.txtValFrete_editingFinished)
        self.ui.tblOrcamento.cellChanged.connect(self.tblOrcamento_CellChanged)
        self.ui.tblOrcamento.mudancaContagemLinhas.connect(self.tblOrcamento_mudancaContagemLinhas)

        # inicializa as informações.
        self.db = conecta_MySql()
        self.carrega_combo()
        # Finaliza o setUp e mostra a interface
        # Personaliza interface
        # self.ui.tblOrcamento.setColumnCount(6)
        self.ui.tblOrcamento.setColumnWidth(0, 55)
        self.ui.tblOrcamento.setColumnWidth(1, 55)
        self.ui.tblOrcamento.setColumnWidth(2, 190)
        self.ui.tblOrcamento.setColumnWidth(3, 70)
        self.ui.tblOrcamento.setColumnWidth(4, 70)
        self.ui.tblOrcamento.setColumnWidth(5, 70)
        self.ui.tblOrcamento.setAlternatingRowColors(1)
        self.show()

    def carrega_combo(self):
        self.model = QtSql.QSqlTableModel(self)
        # self.model.setQuery('SELECT * FROM selecao_clones')
        self.model.setTable("selecao_clones")
        self.model.select()
        print("passou aqui")
        print("Linhas:", str(self.model.rowCount()))
        self.ui.cmbVariedade.setModel(self.model)
        self.ui.cmbVariedade.setModelColumn(self.model.fieldIndex("Descricao"))

    def Limpa_Campos(self):
        self.ui.txtCEP.setText("")
        self.ui.txtQtde.setText("")
        self.ui.txtAlt.setText("")
        self.ui.txtLarg.setText("")
        self.ui.txtProf.setText("")
        self.ui.txtPeso.setText("0,000")
        self.ui.txtValFrete.setText("0,00")
        self.ui.lblNumMudas.setText("0")
        self.ui.lblPrazo.setText("0")
        self.ui.lblTotalMerc.setText("0,00")
        self.ui.lblTotal.setText("0,00")
        self.ui.tblOrcamento.setRowCount(0)
        self.ui.lblCidade.setText("...")
        self.ui.lblEstado.setText("...")
        # Limpa também os acumuladores
        self.total = 0
        self.peso = 0
        self.mudas = 0
        self.TamCaixa = ""
        # Retorna às cores originais
        self.ui.lblTotal.setStyleSheet('color: black')
        self.ui.lblPrazo.setStyleSheet('color: black')
        self.ui.txtQtde.setFocus()

    def incluir_item(self):
        qtde = int(self.ui.txtQtde.text())
        # Busca a linha no model que contém os dados da linha
        # DR = self.model.index.index(self.cmbVariedade.currentIndex(), 0).data
        DR = self.model.record(self.ui.cmbVariedade.currentIndex())
        # Insere uma linha em branco no TableView
        self.ui.tblOrcamento.insertRow(self.ui.tblOrcamento.rowCount())
        r = self.ui.tblOrcamento.rowCount() - 1
        # Organiza as variáveis antes de fazer a inserção
        # Mercadoria
        varMerc = QTableWidgetItem('{:03}'.format(DR.field(1).value()))
        varMerc.setTextAlignment(QtCore.Qt.AlignCenter)
        # Clone
        varClone = QTableWidgetItem('{:04}'.format(DR.field(2).value()))
        varClone.setTextAlignment(QtCore.Qt.AlignCenter)
        # Descrição
        varDescricao = QTableWidgetItem(DR.field(3).value())
        # Quantidade
        varQtde = QTableWidgetItem(self.ui.txtQtde.text())
        varQtde.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Preço
        varPreco = QTableWidgetItem(locale.format_string('%.2f', DR.field(4).value()))
        varPreco.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Total do Item
        varTotItem = QTableWidgetItem(locale.format_string('%.2f', (int(self.ui.txtQtde.text()) * DR.field(4).value())))
        varTotItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Insere as linhas no Table view
        self.ui.tblOrcamento.setItem(r, 0, varMerc)
        self.ui.tblOrcamento.setItem(r, 1, varClone)
        self.ui.tblOrcamento.setItem(r, 2, varDescricao)
        self.ui.tblOrcamento.setItem(r, 3, varQtde)
        self.ui.tblOrcamento.setItem(r, 4, varPreco)
        self.ui.tblOrcamento.setItem(r, 5, varTotItem)
        # Atualiza a Variável Peso
        self.peso += (DR.field(5).value() * qtde)
        print(self.peso)
        # Faz a recontagem dos ítens e atualiza os totais
        self.atualiza_totais()
        self.atualiza_Caixa()
        self.ui.txtQtde.setText("")
        self.ui.txtQtde.setFocus()

    def atualiza_totais(self):
        numRows = self.ui.tblOrcamento.rowCount()
        varMudas = 0
        varTotal = 0
        for row in range(0, numRows):
            varMudas += int(self.ui.tblOrcamento.item(row, 3).text())
            varTotal += locale.atof(self.ui.tblOrcamento.item(row, 5).text())
        self.ui.lblNumMudas.setText(str(varMudas))
        self.mudas = varMudas
        self.ui.lblTotalMerc.setText(locale.format_string('%.2f', varTotal))
        self.total = varTotal
        # Total Geral Com Frete
        varFrete = locale.atof(self.ui.txtValFrete.text())
        varTotalGeral = varTotal + varFrete
        self.ui.lblTotal.setText(locale.format_string('%.2f', varTotalGeral))
        self.atualiza_Peso()
        self.ui.txtPeso.setText(locale.format_string('%.3f', self.peso))

    def atualiza_Caixa(self):
        varMudas = self.mudas
        # Define o Tamanho da Caixa e coloca nos campos
        varDimensoes = self.tamanho_caixa(varMudas)
        varDim = varDimensoes.split(" ")
        self.ui.txtAlt.setText(str(varDim[0]))
        self.ui.txtLarg.setText(str(varDim[1]))
        self.ui.txtProf.setText(str(varDim[2]))

    def atualiza_Peso(self):
        numRows = self.ui.tblOrcamento.rowCount()
        varPeso = 0
        for row in range(0, numRows):
            # Monta a SQL Base
            sql = "SELECT mercadoria,clone,peso FROM selecao_clones WHERE mercadoria=" + self.ui.tblOrcamento.item(row, 0).text() + " AND Clone=" + self.ui.tblOrcamento.item(row, 1).text()
            # Cria um Query Model para pegar os dados do produto
            Mercadoria = QtSql.QSqlQueryModel(self)
            Mercadoria.setQuery(QtSql.QSqlQuery(sql))
            # Pega o único Record que se espera encontrar
            DR = Mercadoria.record(0)
            varPeso += int(self.ui.tblOrcamento.item(row, 3).text()) * DR.value("peso")
            self.peso = varPeso
            # Limpar a memória
            Mercadoria = None
            DR = None

    def copia_email(self):
        # Para cada item monta uma linha
        numRows = self.ui.tblOrcamento.rowCount()
        mensagem = ""
        for row in range(0, numRows):
            varQtde = int(self.ui.tblOrcamento.item(row, 3).text())
            varVariedade = self.ui.tblOrcamento.item(row, 2).text()
            varPreco = self.ui.tblOrcamento.item(row, 4).text()
            varTotItem = self.ui.tblOrcamento.item(row, 5).text()
            # monta a linha que será acrescentada na caixa de texto
            novaLinha = f"{varQtde:03d}" + " mds " + varVariedade.ljust(30,".") + " " + varPreco + " .. " + varTotItem.rjust(7) + "\n"
            # Acrescenta a nova linha
            mensagem += novaLinha
        # Acrescenta o Frete
        if self.ui.rdJadLog.isChecked():
            varTrans = "JadLog"
        else:
            varTrans = "SEDEX"
        linFrete = f"Frete via {varTrans} ".ljust(47,".") + self.ui.txtValFrete.text().rjust(7) + "\n"
        mensagem += linFrete
        # Acrescenta o total
        linTotal = "TOTAL ".ljust(47,".") + self.ui.lblTotal.text().rjust(7)
        mensagem += linTotal
        from PyQt5.Qt import QApplication
        QApplication.clipboard().setText(mensagem)
        QtWidgets.QMessageBox.information(self, "Área de Transferência", "Orçamento copiado para área de transferência", QtWidgets.QMessageBox.Ok)

    def Copia_Whats(self):
        # Para cada item monta uma linha
        numRows = self.ui.tblOrcamento.rowCount()
        mensagem = ""
        for row in range(0, numRows):
            varQtde = int(self.ui.tblOrcamento.item(row, 3).text())
            pos = self.ui.tblOrcamento.item(row, 2).text().find(".")
            varVariedade = self.ui.tblOrcamento.item(row, 2).text()[pos+2:]
            varPreco = self.ui.tblOrcamento.item(row, 4).text()
            varTotItem = self.ui.tblOrcamento.item(row, 5).text()
            # monta a linha que será acrescentada na caixa de texto
            novaLinha = f"{varQtde:03d} " + varVariedade.ljust(14,".") + " " + varPreco + " ." + varTotItem.rjust(7) + "\n"
            # Acrescenta a nova linha
            mensagem += novaLinha
        # Acrescenta o Frete
        if self.ui.rdJadLog.isChecked():
            varTrans = "JadLog"
        else:
            varTrans = "SEDEX"
        linFrete = f"Frete via {varTrans} ".ljust(25, ".") + self.ui.txtValFrete.text().rjust(7) + "\n"
        mensagem += linFrete
        # Acrescenta o total
        linTotal = "TOTAL ".ljust(25, ".") + self.ui.lblTotal.text().rjust(7)
        mensagem += linTotal
        # Formata o texto para Whats
        mensagem = "```" + mensagem + "```"
        from PyQt5.Qt import QApplication
        QApplication.clipboard().setText(mensagem)
        QtWidgets.QMessageBox.information(self, "Área de Transferência", "Orçamento copiado para área de transferência",QtWidgets.QMessageBox.Ok)

    def Calculo_Frete(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # Converte para número
        varValor = locale.atof(self.ui.lblTotal.text())
        # Pega o Peso
        varPeso = locale.atof(self.ui.txtPeso.text())
        # Pega o CEP Digitado
        varCEP = self.ui.txtCEP.text().replace("-", "").replace(".", "")
        # Extrai as dimensões com base no texto de entrada
        varLarg = int(self.ui.txtLarg.text())
        varProf = int(self.ui.txtProf.text())
        varAltu = int(self.ui.txtAlt.text())
        # Verifica se vai ser usado o peso calculado ou peso cubado
        peso_considerado = calcula_peso_real(varLarg, varAltu, varProf, 0, float(varPeso))
        if self.ui.rdJadLog.isChecked():
            # Calcula preço e Prazo pela função
            Preco, Prazo = calcula_frete(varCEP, peso_considerado, varValor)
            # Acréscimo de taxa Administrativa
            Preco += 4.5
            # Calcula Taxa Reguro
            seguro = aliquota_seguro(varCEP)
            val_seguro = varValor * (seguro / 100)
            # Calcula o valor final com os acréscimos
            valor_final = Preco + val_seguro
            # Compensa a alíquota o Simples
            valor_final = (valor_final / 0.955)
        if self.ui.rdSEDEX.isChecked():
            varDim = [varLarg, varAltu, varProf]
            Preco, Prazo = calculaSEDEX(cepOri="89203001", cepDest=varCEP,Dimensoes = varDim, peso = varPeso)
            valor_final = (Preco / 0.955)
        self.ui.txtValFrete.setText(locale.format_string('%.2f', valor_final))
        self.atualiza_totais()
        # Se o prazo for maior que 7 dias
        if Prazo > 7:
            self.ui.lblPrazo.setStyleSheet('color: red')
        self.ui.lblPrazo.setText(f"{Prazo:02d}" + " dias")
        QApplication.restoreOverrideCursor()

    def tamanho_caixa(self, numMudas):
        # Array com os tamanhos das caixas (50, 100, 250, 500, 750, 1000, 1500)
        # Caixa      A0          B0          A1          Elepot1     Elepot2     Caixa 08    Isopor
        TamCaixas = ["17 17 24", "32 15 36", "32 36 25", "34 54 17", "34 54 34", "57 67 67", "70 51 52"]
        if (numMudas <= 50):
            return TamCaixas[0]
        elif (numMudas <= 100):
            return TamCaixas[1]
        elif (numMudas <= 170):
            return TamCaixas[2]
        elif (numMudas <= 350):
            return TamCaixas[3]
        elif (numMudas <= 750):
            return TamCaixas[4]
        elif (numMudas <=1000):
            return TamCaixas[5]
        else:
            return TamCaixas[6]

    def AdicionaTotal(self):
        varTotal = "TOTAL ".ljust(43, ".") + " " + locale.format_string('%.2f', self.total).rjust(7)
        self.ui.txtOrcamento.appendPlainText(varTotal)

    def txtCEP_editingFinished(self):
        if (len(self.ui.txtCEP.text()) == 8):
            cidade, uf = self.busca_endereco(self.ui.txtCEP.text())
        else:
            cidade = ''
            uf = ''
        self.ui.lblCidade.setText(cidade)
        self.ui.lblEstado.setText(uf)

    def txtValFrete_editingFinished(self):
        self.atualiza_totais()
        self.ui.txtValFrete.setText(locale.format_string('%.2f', locale.atof(self.ui.txtValFrete.text())))

    def tblOrcamento_CellChanged(self, row, col):
        try:
            # Se for alterada a quantidade ou o valor
            if self.ui.tblOrcamento.currentItem().column() == 3 or self.ui.tblOrcamento.currentItem().column() == 4:
                cell = self.ui.tblOrcamento.currentItem()
                triggered = cell.text()
                if col == 3:
                    varPreco = locale.atof(self.ui.tblOrcamento.item(row, 4).text())
                    varNewQtde = int(triggered)
                if col == 4:
                    varPreco = locale.atof(triggered)
                    varNewQtde = int(self.ui.tblOrcamento.item(row, 3).text())
                varNewTotal = varPreco * varNewQtde
                varTotItem = QTableWidgetItem(locale.format_string('%.2f', varNewTotal))
                varTotItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                self.ui.tblOrcamento.setItem(row, 5, varTotItem)
                self.atualiza_totais()
                self.atualiza_Caixa()
        except:
            pass

    def tblOrcamento_mudancaContagemLinhas(self):
        self.atualiza_totais()
        self.atualiza_Caixa()

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

    def Envia_Cotacao_Skype(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # Variáveis de acesso
        username = "alexandre.drefahl"
        password = "@arlb0402"
        hora_atual = datetime.now().hour
        saudacao = ""
        if hora_atual < 12:
            saudacao = 'Bom dia!'
        elif 12 <= hora_atual < 18:
            saudacao = 'Boa tarde!'
        else:
            saudacao = 'Boa noite!'
        # Variáveis de saudação
        greetingsAzul = saudacao + " Vanessa\r\r"
        greetingsJadLog = saudacao + " Magali\r\r"
        # Variáveis de parâmetros
        varCEP = self.ui.txtCEP.text().replace("-", "").replace(".", "")
        varVolume = self.ui.txtAlt.text() + " x " + self.ui.txtLarg.text() + " x " + self.ui.txtProf.text()
        varNFe = locale.format_string('%.2f', locale.atof(self.ui.lblTotal.text()))
        varPeso = locale.format_string('%.1f', locale.atof(self.ui.txtPeso.text())) + " kg"
        content = "Podes cotar esse envio? \r \rCEP: {0}\rNFe: {1}\rVolume: {2}\rPeso: {3}\rObrigado!".replace("{0}",
                                                                                                               varCEP).replace(
            "{1}", varNFe).replace("{2}", varVolume).replace("{3}", varPeso)
        # Conecta ao skype
        sk = Skype(username, password)
        if self.ui.chkAzul.isChecked():
            # Cria um chat com Azul
            chAzul = sk.contacts["assistentecomercial01.joi.jttlog"].chat  # cria um chat com a Azul Cargo
            # Envia cotação para Azul Cargo
            chAzul.sendMsg(greetingsAzul + content)
        if self.ui.chkJadLog.isChecked():
            # Cria um chat com JadLog
            chJadLog = sk.contacts["live:comercial_24543"].chat  # cria um chat com JadLog
            # Envia mensagem para JadLog
            chJadLog.sendMsg(greetingsJadLog + content)
        QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(self, "Confirmação", "Cotações Enviadas com sucesso",
                                          QtWidgets.QMessageBox.Ok)

    def Carrega_Dados_Reserva(self,IdReserva):
        print("Carregar dados da reserva " + str(IdReserva))
        DadosReserva = QSqlQueryModel(self)
        DadosReserva.setQuery('SELECT * FROM Reservas WHERE id='+str(IdReserva))
        DadosItens = QSqlQueryModel(self)
        DadosItens.setQuery('SELECT * FROM Reservas_Itens WHERE Doc_ID='+str(IdReserva))
        if DadosReserva.rowCount() == 1:
            print(DadosReserva.record(0).value("Nome"))
        print("Linhas:", str(self.model.rowCount()))