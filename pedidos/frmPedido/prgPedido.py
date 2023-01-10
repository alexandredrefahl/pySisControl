# Imports PyQt
import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QFrame, QTableWidget, QPlainTextEdit, QLabel, QGroupBox
from PyQt5.QtCore import QDateTime
from PyQt5.QtSql import *
# Imports Locais
from pedidos.frmPedido.frmPedido import Ui_frmPedido
from pedidos.frmPedido.prgDlgSelecaoClientes import dlgSelecaoClientes
from bibliotecas.mysqldb import *
from bibliotecas.biblioteca import *

# Imports do sistema
import locale
import re
# Imports de Bibliotecas Externas
import pycep_correios


class frmPedido(QtWidgets.QDialog):
    # Construtor da Classe
    def __init__(self):
        super().__init__()

        self.ui = Ui_frmPedido()
        self.ui.setupUi(self)

        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Conecta as funções de callback (na ordem em que aparecem na GUI)
        self.ui.txtCFOP.editingFinished.connect(self.txtCFOP_editingfinished)
        self.ui.btCliente.clicked.connect(self.btCliente_clicked)
        self.ui.txtEstado.editingFinished.connect(self.Carrega_Cidades)
        self.ui.txtCidade.currentIndexChanged.connect(self.Codigo_Cidade)
        self.ui.cmbMercadoria.currentIndexChanged.connect(self.Carrega_Preco)
        self.ui.btAdd.clicked.connect(self.btAdd_Clicked)
        self.ui.btCEP.clicked.connect(self.btCEP_clicked)
        self.ui.txtValFrete.editingFinished.connect(self.txtValFrete_editingFinished)
        self.ui.txtValSeguro.editingFinished.connect(self.txtValSeguro_editingFinished)
        self.ui.txtValDesconto.editingFinished.connect(self.txtValDesconto_editingFinished)
        self.ui.txtPesoB.editingFinished.connect(self.txtPesoB_editingFinished)
        self.ui.btIncluir.clicked.connect(self.btIncluir_clicked)
        self.ui.cmbFormaPag.currentIndexChanged.connect(self.cmbFormaPag_idxChanged)
        self.ui.tblItens.cellChanged.connect(self.tblItens_CellChange)
        self.ui.tblItens.mudancaContagemLinhas.connect(self.tblItens_mudancaContagemLinhas)

        # *** Formata TableView Produtos *** #
        self.ui.tblItens.setColumnWidth(0, 55)  # Mercadoria
        self.ui.tblItens.setColumnWidth(1, 55)  # Clone
        self.ui.tblItens.setColumnWidth(2, self.ui.tblItens.geometry().width() - 346)
        # 346 = soma de todas as outras colunas + 16 da Scrollbar + 10 da Linha inicial
        self.ui.tblItens.setColumnWidth(3, 70)  # Qtde
        self.ui.tblItens.setColumnWidth(4, 70)  # Unitário
        self.ui.tblItens.setColumnWidth(5, 70)  # Total
        self.ui.tblItens.setAlternatingRowColors(1)

        # *** Formata TableView Pagamento *** #
        self.ui.tblParcelas.setColumnWidth(0, 85)  # Vencimento
        self.ui.tblParcelas.setColumnWidth(2, 75)  # Valor
        self.ui.tblParcelas.setColumnWidth(1, self.ui.tblParcelas.geometry().width() - 185)  # Descrição 85+75+25(scrll)
        self.ui.tblParcelas.setAlternatingRowColors(1)

        # Carrega o banco de dados
        self.db = conecta_MySql()

        # Preenche os dados dos Combos
        self.carrega_combo_mercadoria()
        self.carrega_combo_transportadoras()
        self.carrega_combo_formapagamento()

        # Coloca data Atual nas caixas de data
        self.ui.txtData.setDateTime(QDateTime.currentDateTime())
        self.ui.txtDataPrev.setDateTime(QDateTime.currentDateTime())

        # Abre a tela do software
        self.show()

        # Carregar dados nos Combos

    def carrega_combo_mercadoria(self):
        self.mdlProdutos = QtSql.QSqlTableModel(self)
        self.mdlProdutos.setTable("selecao_clones")
        self.mdlProdutos.select()
        self.ui.cmbMercadoria.setModel(self.mdlProdutos)
        self.ui.cmbMercadoria.setModelColumn(self.mdlProdutos.fieldIndex("Descricao"))

    def carrega_combo_transportadoras(self):
        self.mdlTransportadoras = QtSql.QSqlTableModel(self)
        self.mdlTransportadoras.setTable("transportadores")
        self.mdlTransportadoras.select()
        self.ui.cmbTransportadora.setModel(self.mdlTransportadoras)
        self.ui.cmbTransportadora.setModelColumn(self.mdlTransportadoras.fieldIndex("Razao"))

    def carrega_combo_formapagamento(self):
        self.mdlForma = QtSql.QSqlTableModel(self)
        self.mdlForma.setTable("forpag")
        self.mdlForma.select()
        self.ui.cmbFormaPag.setModel(self.mdlForma)
        self.ui.cmbFormaPag.setModelColumn(self.mdlForma.fieldIndex("Descricao"))

    def txtCFOP_editingfinished(self):
        if len(self.ui.txtCFOP.text()) == 4:
            query = QSqlQuery()
            query.exec_("SELECT CFOP,Descricao from cfop WHERE CFOP=" + self.ui.txtCFOP.text())
            print("Registros" + str(query.numRowsAffected()))
            if query.numRowsAffected() > 0:
                query.next()
                # print(query.value(0))
                self.ui.txtNatOp.setText(query.value(1))
                self.ui.txtNatOp.setFocus()
            else:
                QtWidgets.QMessageBox.critical(self, "Registro não Localizado", "CFOP Não Encontrado",
                                               QtWidgets.QMessageBox.Ok)

    def Carrega_Cidades(self):
        # Lista dos estados
        estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE",
                   "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        # Se for um estado Válido
        if (len(self.ui.txtEstado.text()) == 2) and (self.ui.txtEstado.text() in estados):
            sql = "SELECT cod,municipio FROM rais WHERE estado='" + self.ui.txtEstado.text() + "'"
            cidades = QtSql.QSqlQueryModel(self)
            cidades.setQuery(QtSql.QSqlQuery(sql))
            self.ui.txtCidade.setModel(cidades)
            self.ui.txtCidade.setModelColumn(1)

    def Codigo_Cidade(self):
        # Pega o Código no Combo para colocar no label
        idx = self.ui.txtCidade.currentIndex()
        print("Selecionado: " + str(idx))
        # Se tem algo selecionado
        if idx > -1:
            CodCidade = self.ui.txtCidade.model().index(idx, 0)
            Cod = self.ui.txtCidade.model().itemData(CodCidade)
            self.ui.txtCodCidade.setText(str(Cod[0]))
            print(Cod)

    def Carrega_Preco(self):
        # Busca a linha no model que contém os dados da linha
        DR = self.mdlProdutos.record(self.ui.cmbMercadoria.currentIndex())
        self.ui.txtValor.setText(locale.format_string('%.2f', DR.field(4).value()))

    def btCliente_clicked(self):
        # Cria o objeto Diálogo
        self.dlgProcuraCliente = dlgSelecaoClientes()
        # Conecta o Signal de Concluido com a função que vai receber os dados (Slot)
        self.dlgProcuraCliente.Concluido.connect(self.CarregaDados)
        # apresenta o diálogo se seleção
        self.dlgProcuraCliente.showNormal()

    def btCEP_clicked(self):
        if len(self.ui.txtCEP.text()) < 8:
            return
        # from pycep_correios import CEPInvalido
        try:
            cep = self.ui.txtCEP.text().replace("-", "")
            endereco = pycep_correios.consultar_cep(cep)
            print(endereco)
            # preenche os campos do endereço
            self.ui.txtEndereco.setText(endereco['end'])
            self.ui.txtBairro.setText(endereco['bairro'])
            self.ui.txtEstado.setText(endereco['uf'])
            # Atualiza a lista de Cidades no Combo
            self.Carrega_Cidades()
            # Encontrar Valor no Combo
            idx = self.ui.txtCidade.findText(endereco['cidade'].upper(), QtCore.Qt.MatchFixedString)
            print(endereco['cidade'].upper())
            print("Combo Cidade: " + str(idx))
            self.ui.txtCidade.setCurrentIndex(idx)
            self.ui.txtCidade.setCurrentText(endereco['cidade'].upper())
            # print(endereco['end'])
            # print(endereco['bairro'])
            # print(endereco['cidade'])
            # print(endereco['complemento'])
            # print(endereco['complemento2'])
            # print(endereco['uf'])
            # print(endereco['cep'])
        except BaseException as exc:
            QMessageBox.critical(self, "Erro CEP", "CEP Não Localizado\n" + str(exc), QtWidgets.QMessageBox.Ok)

    def btAdd_Clicked(self):
        # Busca a linha no model que contém os dados da linha
        DR = self.mdlProdutos.record(self.ui.cmbMercadoria.currentIndex())
        # Insere uma linha em branco no TableView
        self.ui.tblItens.insertRow(self.ui.tblItens.rowCount())
        r = self.ui.tblItens.rowCount() - 1
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
        varPreco = QTableWidgetItem(locale.format_string('%.2f', locale.atof(self.ui.txtValor.text())))
        varPreco.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Total do Item
        varTotItem = QTableWidgetItem(
            locale.format_string('%.2f', (int(self.ui.txtQtde.text()) * locale.atof(self.ui.txtValor.text()))))
        varTotItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        # Insere as linhas no Table view
        self.ui.tblItens.setItem(r, 0, varMerc)
        self.ui.tblItens.setItem(r, 1, varClone)
        self.ui.tblItens.setItem(r, 2, varDescricao)
        self.ui.tblItens.setItem(r, 3, varQtde)
        self.ui.tblItens.setItem(r, 4, varPreco)
        self.ui.tblItens.setItem(r, 5, varTotItem)
        # Atualiza Valor Total e Total de Mudas
        self.Atualiza_Totais()
        self.ui.txtQtde.setText("")
        self.ui.txtQtde.setFocus()

    def cmbFormaPag_idxChanged(self):
        # Se o combo estiver vazio ou nada selecionado
        if self.ui.cmbFormaPag.currentIndex() <= -1:
            return
        # se houver algo válido selecionado
        # Busca a linha no model que contém os dados da linha
        DR = self.mdlForma.record(self.ui.cmbFormaPag.currentIndex())
        # "limpa" a tabela de parcelas
        self.ui.tblParcelas.setRowCount(0)
        varPorcentagem = str(DR.field(9).value())
        varDias = str(DR.field(8).value())
        percParcelas = varPorcentagem.split(";")
        diasParcelas = varDias.split(";")
        for n in range(0, len(percParcelas)):
            self.ui.tblParcelas.insertRow(self.ui.tblParcelas.rowCount())
            r = self.ui.tblParcelas.rowCount() - 1
            tmpData = self.ui.txtData.date().toPyDate() + datetime.timedelta(days=int(diasParcelas[n]))
            varData = QTableWidgetItem(tmpData.strftime("%d/%m/%Y"))
            varData.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
            varDesc = QTableWidgetItem("Parc. " + str(n + 1) + "/" + str(len(percParcelas)))
            varDesc.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            varVal = QTableWidgetItem(locale.format_string('%.2f', (
                        locale.atof(self.ui.txtTOTALGERAL.text()) * (int(percParcelas[n]) / 100))))
            varVal.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            self.ui.tblParcelas.setItem(r, 0, varData)
            self.ui.tblParcelas.setItem(r, 1, varDesc)
            self.ui.tblParcelas.setItem(r, 2, varVal)

    # Conector do Slot para receber os dados do diálogo
    @QtCore.pyqtSlot(str, int)
    def CarregaDados(self, tabela, CliID):
        # Captar os dados de um pedido antigo
        if tabela == "pedidos":
            # ***** PEDIDOS *****
            # Monta a SQL Base
            SQL = "SELECT * FROM pedidos WHERE id=" + str(CliID)
            # Cria um Query Model para pegar os dados do cliente
            cliente = QtSql.QSqlQueryModel(self)
            cliente.setQuery(QtSql.QSqlQuery(SQL))
            # Pega o único Record que se espera encontrar
            DR = cliente.record(0)
            # Começa a preeencher os campos do Formulário
            self.ui.txtNome.setText(DR.value("cliente"))
            self.ui.txtEndereco.setText(DR.value('endereco'))
            self.ui.txtNum.setText(DR.value('num'))
            self.ui.txtBairro.setText(DR.value('bairro'))
            self.ui.txtComplemento.setText(DR.value('complemento'))
            self.ui.txtCEP.setText(DR.value('CEP'))
            self.ui.txtEstado.setText(DR.value('estado'))
            # Atualiza a lista de Cidades no Combo
            self.Carrega_Cidades()
            # Encontrar Valor no Combo
            idx = self.ui.txtCidade.findText(DR.value('cidade'), QtCore.Qt.MatchFixedString)
            if idx >= 0:
                self.ui.txtCidade.setCurrentIndex(idx)
            self.ui.txtPais.setText(DR.value('pais'))
            self.ui.txtCodCidade.setText(DR.value('codcidade'))
            self.ui.txtCodPais.setText(DR.value('CodPais'))
            self.ui.txtFone.setText(DR.value('fone'))
            self.ui.txtEmail.setText(DR.value('email'))
            # Seleciona o Radio Button Baseado neste valor
            if DR.value('PFPJ') == "F":
                self.ui.rdPF.setChecked(True)
            elif DR.value('PFPJ') == "J":
                self.ui.rdPJ.setChecked(True)
            self.ui.txtCNPJ_CPF.setText(re.sub('\W+', '', DR.value('CNPJ_CPF')))
            self.ui.txtContato.setText(DR.value('contato'))
        elif tabela == "docs":
            # ***** NOTAS FISCAIS *****
            pass
        elif tabela == "clientes":
            pass

    def Atualiza_Totais(self):
        numRows = self.ui.tblItens.rowCount()
        varMudas = 0
        varTotal = 0
        varPeso = 0
        for row in range(0, numRows):
            # Monta a SQL Base
            sql = "SELECT mercadoria,clone,peso FROM selecao_clones WHERE mercadoria=" + self.ui.tblItens.item(row, 0).text() + " AND Clone=" + self.ui.tblItens.item(row, 1).text()
            # Cria um Query Model para pegar os dados do produto
            Mercadoria = QtSql.QSqlQueryModel(self)
            Mercadoria.setQuery(QtSql.QSqlQuery(sql))
            # Pega o único Record que se espera encontrar
            DR = Mercadoria.record(0)
            # Começa a preeencher os campos do Formulário
            varMudas += int(self.ui.tblItens.item(row, 3).text())
            varTotal += locale.atof(self.ui.tblItens.item(row, 5).text())
            varPeso += int(self.ui.tblItens.item(row, 3).text()) * DR.value("peso")
            # Limpar a memória
            Mercadoria = None
            DR = None
        # Atualiza Campos individuais
        self.ui.txtTotMudas.setText(str(varMudas))
        self.ui.txtValMerc.setText(locale.format_string('%.2f', varTotal))
        self.ui.txtPesoB.setText(locale.format_string('%.3f', varPeso))
        # Atualiza Resumo dos Pedidos
        self.ui.txtTotMerc.setText(self.ui.txtValMerc.text())
        self.ui.txtTotFrete.setText(self.ui.txtValFrete.text())
        self.ui.txtTotDesc.setText(self.ui.txtValDesconto.text())
        valMerc = locale.atof(self.ui.txtValMerc.text())
        valFrete = locale.atof(self.ui.txtValFrete.text())
        valDesconto = locale.atof(self.ui.txtValDesconto.text())
        valTOTALGERAL = valMerc + valFrete - valDesconto
        self.ui.txtTOTALGERAL.setText(locale.format_string('%.2f', valTOTALGERAL))
        # Atualiza as parcelas
        self.cmbFormaPag_idxChanged()

    def txtValFrete_editingFinished(self):
        if len(self.ui.txtValFrete.text()) > 0:
            self.ui.txtValFrete.setText(locale.format_string('%.2f', locale.atof(self.ui.txtValFrete.text())))
            self.Atualiza_Totais()

    def txtValSeguro_editingFinished(self):
        if len(self.ui.txtValSeguro.text()) > 0:
            self.ui.txtValSeguro.setText(locale.format_string('%.2f', locale.atof(self.ui.txtValSeguro.text())))
            self.Atualiza_Totais()

    def txtValDesconto_editingFinished(self):
        if len(self.ui.txtValDesconto.text()) > 0:
            self.ui.txtValDesconto.setText(locale.format_string('%.2f', locale.atof(self.ui.txtValDesconto.text())))
            self.Atualiza_Totais()

    def txtPesoB_editingFinished(self):
        if len(self.ui.txtPesoB.text()) > 0:
            self.ui.txtPesoB.setText(locale.format_string('%.3f', locale.atof(self.ui.txtPesoB.text())))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F3:
            print("F3 Presionado")
            self.btCliente_clicked()

    def valida_campos(self):
        validado = True
        erro = ""
        # Campos de preenchimento obrigatório
        if len(self.ui.txtNome.text()) < 2:
            erro += "<li><b>NOME</b> precisa ter comprimento mínimo de 2 caracteres</li></br>"
        if len(self.ui.txtEndereco.text()) < 2:
            erro += "<li><b>ENDEREÇO</b> precisa ter comprimento mínimo de 2 caracteres</li></br>"
        if len(self.ui.txtBairro.text()) < 2:
            erro += "<li><b>BAIRRO</b> precisa ter comprimento mínimo de 2 caracteres</li></br>"
        if len(self.ui.txtCEP.text()) < 8:
            erro += "<li><b>CEP</b> precisa ser preenchido e estar no formato <i>99999-999</i></li></br>"
        if len(self.ui.txtEstado.text()) != 2:
            erro += "<li>Informar a Sigla do <b>ESTADO</b> com 2 letras</li></br>"
        if len(self.ui.txtCidade.currentText()) < 2 or self.ui.txtCidade.currentIndex() < 0:
            erro += "<li>Selecione uma <b>CIDADE</b> na caixa de Seleção</li></br>"
        if self.ui.rdPF.isChecked():
            if len(self.ui.txtCNPJ_CPF.text()) < 11:
                erro += "<li>O <b>CPF</b> Precisa ser informado com 11 dígitos (<i>somente números</i>)</li></br>"
        if self.ui.rdPJ.isChecked():
            if len(self.ui.txtCNPJ_CPF.text()) < 14:
                erro += "<li>O <b>CNPJ</b> Precisa ser informado com 14 dígitos (<i>somente números</i>)</li></br>"
        if self.ui.tblItens.rowCount() == 0:
            erro += "<li>O Pedido precisa ter no mínimo 1 <b>ITEM</b></li></br>"
        if locale.atof(self.ui.txtPesoB.text()) <= 0:
            erro += "<li>É necessário informar ou calcular o <b>PESO</b></li></br>"
        if self.ui.cmbTransportadora.currentIndex() >= 0 and locale.atof(
                self.ui.txtValFrete.text()) == 0 and self.ui.cmbModalidade.currentIndex() == 0:
            erro += "<li>Quando a transportadora é informada, é necessário o <b>VALOR DO FRETE</b>.</li></br>"
        if (locale.atof(self.ui.txtValFrete.text()) > 0) and (self.ui.cmbTransportadora.currentIndex() < 0):
            erro += "<li>Quando um valor de frete é informado é necessário optar por uma <b>TRANSPORTADORA</b></li></br>"
        if self.ui.tblParcelas.rowCount() == 0:
            erro += "<li>É necessário definir o <b>NÚMERO DE PARCELAS</b> nos Dados do Pagamento</li></br>"
        # CFOP por estado e por consumidor
        if self.ui.txtEstado.text() != "SC" and self.ui.txtCFOP.text()[0] != "6":
            erro += "<li><b>CFOP</b> para vendas fora do estado deve <b>iniciar com 6</b></li></br>"
        if self.ui.txtEstado.text() == "SC" and self.ui.txtCFOP.text()[0] != "5":
            erro += "<li><b>CFOP</b> para vendas dentro do estado deve <b>iniciar com 5</b></li></br>"
        if self.ui.cmbIE.currentIndex() >= 0:
            if self.ui.cmbIE.currentText()[0] == "9":  # Selecionado não contribuinte
                cfops = ["6107", "5107", "6949", "5949"]
                if self.ui.txtCFOP.text() not in cfops:
                    erro += "<li>O <b>CFOP</b> não condiz com venda para consumidor final</li></br>"
        if self.ui.cmbIE.currentText()[0] == "1" and len(self.ui.txtIE.text()) <= 0:
            erro += "<li>Quando o cliente é Contribuinte é necessário preencher a <b>INSCRIÇÃO ESTADUAL</b></li></br>"
        # *** Encerradas as checagens define e emite o aviso
        if len(erro) > 0:
            validado = False
            # Foi feito desda forma por conta do texto da mensagem em HTML
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "<p style='font-family:verdana'>Os seguintes erros de preenchimento foram encontrados:</br></br><ul>" + erro + "</ul></p>")
            msg.setWindowTitle("Erro de Validação")
            msg.setTextFormat(QtCore.Qt.RichText)
            msg.exec_()
            # QMessageBox.critical(self, "Erro de validação", "Os seguintes erros de preenchimento foram encontrados:\n\n" + erro, QMessageBox.Ok)
        return validado

    def btIncluir_clicked(self):
        # Se não passou na validação dos campos já retorna
        if not self.valida_campos():
            return
        # Se passou pega no BD a próxima id para fazer a inclusão
        # Prepara as Strings SQL
        sql_Pedido = QtSql.QSqlQuery()
        sql_Pedido.prepare(
            "INSERT INTO pedidos SET Data=:data,Cliente=:cliente,CodCli=:codcli,Endereco=:endereco,Num=:num,Bairro=:bairro,Cidade=:cidade,CodCidade=:codcidade,Estado=:estado,CEP=:cep,Pais=:pais,CodPais=:codpais,Fone=:fone,PFPJ=:pfpj,CNPJ_CPF=:cnpj_cpf,email=:email,Inscricao=:inscricao,Contato=:contato,Data_Digitacao=current_timestamp(),Vendedor=:vendedor,Status=:status,Aprovado=:data,AprovadoPor=:aprovador,Valor=:valor,NMudas=:mudas,NItens=:numitens,Prazo=:prazo,ForPag=:forpag,CFOP=:cfop,NaturezaOP=:natop,ModFrete=:modfrete,ValFrete=:valfrete,ValSeguro=:valseguro,ValDesconto=:valdesconto,Observacoes=:obs,Transportadora=:transportadora,TransportadoraID=:transportadoraid,Complemento=:complemento")
        # Preenche os valores
        sql_Pedido.bindValue(':data', self.ui.txtData.date())
        sql_Pedido.bindValue(':cliente', self.ui.txtNome.text())
        sql_Pedido.bindValue(':codcli', -1)
        sql_Pedido.bindValue(':endereco', self.ui.txtEndereco.text())
        sql_Pedido.bindValue(':num', self.ui.txtNum.text())
        sql_Pedido.bindValue(':bairro', self.ui.txtBairro.text())
        sql_Pedido.bindValue(':cidade', self.ui.txtCidade.currentText())
        sql_Pedido.bindValue(':codcidade', self.ui.txtCodCidade.text())
        sql_Pedido.bindValue(':estado', self.ui.txtEstado.text())
        sql_Pedido.bindValue(':cep', self.ui.txtCEP.text())
        sql_Pedido.bindValue(':complemento', self.ui.txtComplemento.text())
        sql_Pedido.bindValue(':pais', self.ui.txtPais.text())
        sql_Pedido.bindValue(':codpais', self.ui.txtCodPais.text())
        sql_Pedido.bindValue(':fone', self.ui.txtFone.text())
        sql_Pedido.bindValue(':inscricao', self.ui.txtIE.text())
        sql_Pedido.bindValue(':contato', self.ui.txtContato.text())
        if self.ui.rdPF.isChecked():
            sql_Pedido.bindValue(':pfpj', "F")
        if self.ui.rdPJ.isChecked():
            sql_Pedido.bindValue(':pfpj', "J")
        sql_Pedido.bindValue(':cnpj_cpf', self.ui.txtCNPJ_CPF.text())
        sql_Pedido.bindValue(':email', self.ui.txtEmail.text())
        sql_Pedido.bindValue(':vendedor', self.ui.txtVendedor.text())
        sql_Pedido.bindValue(':status', int(self.ui.cmbStatus.currentText()[:2]))
        sql_Pedido.bindValue(':aprovador', self.ui.txtAutorizado.text())
        sql_Pedido.bindValue(':valor', locale.atof(self.ui.txtValMerc.text()))
        sql_Pedido.bindValue(':mudas', int(self.ui.txtTotMudas.text()))
        sql_Pedido.bindValue(':numitems', self.ui.tblItens.rowCount())
        sql_Pedido.bindValue(':prazo', self.ui.txtDataPrev.date())
        # Busca a linha no model que contém os dados da linha
        DR = self.mdlForma.record(self.ui.cmbFormaPag.currentIndex())
        sql_Pedido.bindValue(':forpag', DR.field(0).value())
        sql_Pedido.bindValue(':cfop', self.ui.txtCFOP.text())
        sql_Pedido.bindValue(':natop', self.ui.txtNatOp.text())
        sql_Pedido.bindValue(':modfrete', self.ui.cmbModalidade.currentText()[:1])
        sql_Pedido.bindValue(':valfrete', locale.atof(self.ui.txtValFrete.text()))
        sql_Pedido.bindValue(':valseguro', locale.atof(self.ui.txtValSeguro.text()))
        sql_Pedido.bindValue(':valdesconto', locale.atof(self.ui.txtValDesconto.text()))
        sql_Pedido.bindValue(':obs', self.ui.txtObs.toPlainText())
        DR1 = self.mdlTransportadoras.record(self.ui.cmbTransportadora.currentIndex())
        sql_Pedido.bindValue(':transportadora', DR1.field(1).value())
        sql_Pedido.bindValue(':transportadoraid', DR1.field(0).value())
        # Confirma se o pedido foi incluido com sucesso
        if sql_Pedido.exec():
            # **** INCLUSÃO DOS ITENS ****
            Doc_ID = sql_Pedido.lastInsertId()
            print("Pedido Inserido: " + str(Doc_ID))
            # Percorre os ítens da tabela para fazer a inclusão
            numLinhas = self.ui.tblItens.rowCount()
            print(str(numLinhas) + " itens a incluir")
            # Pega os dados na tabela para preparar os valores para inserção
            for row in range(0, numLinhas):
                # Monta a SQL de inclusão dos ítens
                sql_Itens = QtSql.QSqlQuery()
                sql_Itens.prepare(
                    "INSERT INTO pedidos_itens SET Pedido_id=:doc_id,CodPro=:codpro,Clone=:clone,Descricao=:descricao,NCM=:ncm,Unid='md',Quantidade=:quantidade,Unitario=:unitario,Total=:total,Atendido=0,Status=0,Forma='BD',Tipo='AC',CFOP=:cfop,ICMS=:icms, PIS=:pis, COFINS=:cofins, vICMS=:vicms, vPIS=:vpis, vCOFINS=:vcofins")
                # Prepara as variáveis no formato para inclusão
                varDoc_id = Doc_ID
                varCodPro = self.ui.tblItens.item(row, 0).text()
                varClone = self.ui.tblItens.item(row, 1).text()
                # DR = DLookUp("clones", "mercadoria=" + varCodPro + " AND clone=" + varClone)
                query = QSqlQuery()
                if query.exec("SELECT * FROM clones WHERE " + "mercadoria=" + varCodPro + " AND clone=" + varClone):
                    # Move para o primeiro e único registro
                    query.first()
                    varDescricao = self.ui.tblItens.item(row, 2).text()
                    varNcm = query.value(9)
                    print("NCM: ",varNcm)
                    varQtde = int(self.ui.tblItens.item(row, 3).text())
                    varUnit = locale.atof(self.ui.tblItens.item(row, 4).text())
                    varTotal = locale.atof(self.ui.tblItens.item(row, 5).text())
                    varCFOP = self.ui.txtCFOP.text()
                    varIcms = query.value(11)
                    varPIS = query.value(12)
                    varCofins = query.value(13)
                    varValIcms = locale.atof(self.ui.tblItens.item(row, 5).text()) * query.value(11)
                    varValPIS = locale.atof(self.ui.tblItens.item(row, 5).text()) * query.value(12)
                    varValCofins = locale.atof(self.ui.tblItens.item(row, 5).text()) * query.value(13)
                    # https://doc.qt.io/qt-5/qsqlquery.html#execBatch
                    sql_Itens.bindValue(":doc_id", varDoc_id)
                    sql_Itens.bindValue(":codpro", varCodPro)
                    sql_Itens.bindValue(":clone", varClone)
                    sql_Itens.bindValue(":descricao", varDescricao)
                    sql_Itens.bindValue(":ncm", varNcm)
                    sql_Itens.bindValue(":quantidade", varQtde)
                    sql_Itens.bindValue(":unitario", varUnit)
                    sql_Itens.bindValue(":total", varTotal)
                    sql_Itens.bindValue(":cfop", varCFOP)
                    sql_Itens.bindValue(":icms", varIcms)
                    sql_Itens.bindValue(":pis", varPIS)
                    sql_Itens.bindValue(":cofins", varCofins)
                    sql_Itens.bindValue(":vicms", varValIcms)
                    sql_Itens.bindValue(":vpis", varValPIS)
                    sql_Itens.bindValue(":vcofins", varValCofins)
                    try:
                        sql_Itens.exec()
                        print(sql_Itens.lastError().text())
                        print(sql_Itens.lastQuery())
                        print("Item " + str(row) + " Inserido: " + str(sql_Itens.lastInsertId()))
                        DR = None
                        sql_Itens = None
                    except QSqlError as e:
                        QMessageBox.critical(self,"Erro","Erro ao incluir os ítens do pedido\n" + e.text() + "\n" + sql_Itens.lastError(),QMessageBox.Ok)
                        return
                else:
                    QMessageBox.critical(self,"Erro ao localizar dados da mercadoria\n" + query.lastQuery() + "\n" + query.lastError().text())
                    return
            # **** INCLUSÃO DAS PARCELAS ****
            # Percorre os ítens da tabela para fazer a inclusão
            numParcelas = self.ui.tblParcelas.rowCount()
            numLinhas = numParcelas
            print(str(numParcelas) + " parcelas a incluir")
            # Pega os dados na tabela para preparar os valores para inserção
            for row in range(0, numLinhas):
                # Monta a SQL de inclusão dos ítens
                sql_Parcelas = QtSql.QSqlQuery()
                sql_Parcelas.prepare(
                    "INSERT INTO duplicatas SET Pedido_id=:pedido_id, Vencimento=:vencimento, Valor=:valor, Descricao=:descricao, Lancado=0, formaPag='01'")
                # Prepara as variáveis no formato para inclusão
                varParPedido_id = Doc_ID
                tmpData = datetime.datetime.strptime(self.ui.tblParcelas.item(row,0).text(), "%d/%m/%Y")
                varParVencimento = format(tmpData,"%Y-%m-%d")
                #varParVencimento = self.ui.tblParcelas.item(row,0).text()
                varParDescricao = self.ui.tblParcelas.item(row, 1).text()
                varParValor = locale.atof(self.ui.tblParcelas.item(row,2).text())
                # Vincula as variáveis na SQL
                sql_Parcelas.bindValue(":pedido_id", varParPedido_id)
                sql_Parcelas.bindValue(":vencimento", varParVencimento)
                sql_Parcelas.bindValue(":valor", varParValor)
                sql_Parcelas.bindValue(":descricao", varParDescricao)
                try:
                    # Executa a inclusão
                    sql_Parcelas.exec()
                    print(sql_Parcelas.lastError().text())
                    print(sql_Parcelas.lastQuery())
                    print("Parcela " + str(row) + " Inserido: " + str(sql_Parcelas.lastInsertId()))
                    sql_Parcelas = None
                except QSqlError as e:
                    QMessageBox.critical(self,"Erro","Erro ao incluir as parcelas do pedido\n" + e.text() + "\n" + sql_Parcelas.lastError().text())
                    return
        else:
            QMessageBox.critical(self, "Erro!", "Erro ao inserir dados do Pedido:\n" + sql_Pedido.lastError().text(),
                                 QMessageBox.Ok)
        # Após confirmar tudo certo, envia mensagem
        QMessageBox.information(self,"Concluído!","Pedido incluído com sucesso!\nNúmero: " + str(Doc_ID) + "\n" + str(self.ui.tblItens.rowCount()) + " ítens\n" + str(self.ui.tblParcelas.rowCount()) + " Parcelas")
        # Prepara o formulário para nova inclusão
        self.Limpa_Campos()

    def tblItens_mudancaContagemLinhas(self):
        self.Atualiza_Totais()

    def tblItens_CellChange(self,row, col):
        try:
            # Se for alterada a quantidade ou o valor
            if self.ui.tblItens.currentItem().column() == 3 or self.ui.tblItens.currentItem().column() == 4:
                cell = self.ui.tblItens.currentItem()
                triggered = cell.text()
                if col == 3:    # Quantidade
                    varPreco = locale.atof(self.ui.tblItens.item(row, 4).text())
                    varNewQtde = int(triggered)
                if col == 4:    # Unitário
                    varPreco = locale.atof(triggered)
                    varNewQtde = int(self.ui.tblItens.item(row, 3).text())
                varNewTotal = varPreco * varNewQtde
                varTotItem = QTableWidgetItem(locale.format_string('%.2f', varNewTotal))
                varTotItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                self.ui.tblItens.setItem(row, 5, varTotItem)
                # Atualiza totais depois da alteração
                self.Atualiza_Totais()
        except:
            pass

    def Limpa_Campos(self):
        wid = self.ui.scrollAreaWidgetContents.findChild(QFrame,"frame")
        print("FindWidget: ",wid.objectName())
        Nomes = ["txtValor","txtValMerc","txtPesoB","txtValFrete","txtValSeguro","txtValDesconto","txtTotMerc",
                 "txtTotFrete", "txtTotDesc", "txtTotImpostos", "txtTotDespesas", "txtTOTALGERAL" ]
        for widget in wid.children():
            if isinstance(widget, QLineEdit):
                widget.setText("")
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            if isinstance(widget,QTableWidget):
                widget.setRowCount(0)
            if isinstance(widget,QPlainTextEdit):
                widget.setPlainText("")
            # Todos os Widgets que estão com o nome na lista
            if widget.objectName() in Nomes:
                widget.setText("0,00")
            # Widgets que estão em groupBox Isolados
            if isinstance(widget, QGroupBox):
                for w in widget.children():
                    if w.objectName() in Nomes:
                        w.setText("0,00")
        # Zerar Campos específicos
        self.ui.txtEstado.setText("SC")
        self.ui.txtPais.setText("Brasil")
        self.ui.txtCodCidade.setText("0000000")
        self.ui.rdPF.setChecked(True)
        self.ui.txtData.setDateTime(QDateTime.currentDateTime())
        self.ui.txtDataPrev.setDateTime(QDateTime.currentDateTime())
        self.ui.txtTotMudas.setText("0")
        self.ui.txtQtde.setText("0")
        # devolver o foco para o Primeiro Campo
        self.ui.txtData.setFocus()

