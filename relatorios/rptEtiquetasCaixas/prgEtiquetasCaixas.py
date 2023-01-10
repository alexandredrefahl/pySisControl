# Imports PyQt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import *
# Imports Locais
from relatorios.rptEtiquetasCaixas.frmEtiquetasCaixas import Ui_frmLabelEncomendas
from bibliotecas import mysqldb
from relatorios.rptEtiquetasCaixas.rptEtiquetas_Caixas import *
from relatorios.rptEtiquetasCaixas.rptDanfeSimples import *
# Imports do sistema
import locale
import os


class frmEtiquetasCaixas(QtWidgets.QDialog):
    # Construtor da Classe
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmLabelEncomendas()
        self.ui.setupUi(self)

        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.db = mysqldb.conecta_MySql()
        # Carrega os faturamentos
        self.mdlDocs = QSqlQueryModel()
        self.carrega_faturamentos()
        # Conecta os botões
        self.ui.btImprime.clicked.connect(self.btImprime_Clicked)
        self.ui.btExporta.clicked.connect(self.btExportar_Clicked)
        self.ui.btDanfe.clicked.connect(self.btDanfe_Clicked)

    def carrega_faturamentos(self):
        # Monta a SQL Base

        self.mdlDocs.setQuery("SELECT id,cliente,endereco,num,bairro,cidade,estado,cep,pais,pesoBruto,Documento,Obs,complemento,cnpj_cpf,contato,email,fone FROM Docs ORDER BY id")
        self.mdlDocs.setHeaderData(0,QtCore.Qt.Horizontal,"NFe")
        self.mdlDocs.setHeaderData(1, QtCore.Qt.Horizontal, "Cliente")
        self.mdlDocs.setHeaderData(2, QtCore.Qt.Horizontal, "Endereço")
        self.ui.tblDocs.setModel(self.mdlDocs)
        # Redimensiona as colunas para organizar
        Larg = self.ui.tblDocs.geometry().width()
        self.ui.tblDocs.setColumnWidth(0, 90)
        self.ui.tblDocs.setColumnWidth(1, 450)
        self.ui.tblDocs.setColumnWidth(10, 90)
        # Oculta as colunas do modelo que são só para consulta mas não precisam aparecer
        self.ui.tblDocs.setColumnHidden(2,True)
        self.ui.tblDocs.setColumnHidden(3,True)
        self.ui.tblDocs.setColumnHidden(4, True)
        self.ui.tblDocs.setColumnHidden(5, True)
        self.ui.tblDocs.setColumnHidden(6, True)
        self.ui.tblDocs.setColumnHidden(7, True)
        self.ui.tblDocs.setColumnHidden(8, True)
        self.ui.tblDocs.setColumnHidden(9, True)
        self.ui.tblDocs.setColumnHidden(10,True)
        # Pega somente os selecionados
        self.Selecionados = self.ui.tblDocs.selectionModel()
        # Ao clicar dispara "carrega_itens"
        self.Selecionados.selectionChanged.connect(self.tblDocs_SelectionChanged)

    def tblDocs_SelectionChanged(self):
        indexRows = self.Selecionados.selectedRows()
        row = 0
        self.ui.lblStatus.setText(str(len(indexRows)) + " Documentos selecionados")

    def btImprime_Clicked(self):
        # Pega as linhas selecionadas
        self.ui.lblStatus.setText("Selecionando NFes a serem impressas")
        indexRows = self.Selecionados.selectedRows()
        Rows = []
        row = 0
        # Verifica se tem alguma linha selecionada
        if (len(indexRows) <= 0):
            return 0
        # Limpa o buffer de impressão
        self.Limpa_Lista_Volumes()
        # Percorre as selecionadas para pegar os IDs
        for indexRow in sorted(indexRows):
            row = indexRow.row()
            Rows.append(row)
        #else:
        #    varID = -1
        # Insere os volumes no Banco de Dados para poder chamar a função de imprimir
        self.ui.lblStatus.setText("Inserindo Etiquetas no Banco de Dados")
        num = self.Insere_Volumes(Rows)
        self.ui.lblStatus.setText("Preparando impressão das etiquetas")
        # se forem inseridas etiquetas
        if num > 0:
            self.ui.lblStatus.setText(str(num) + " Etiquetas enviadas para impressão")
            self.Gera_Etiquetas()

    def Limpa_Lista_Volumes(self):
        try:
            clearQuery = QSqlQuery()
            clearQuery.exec("DELETE FROM encomendas_prn")
            print(clearQuery.lastError())
            print(clearQuery.numRowsAffected())
            self.ui.lblStatus.setText("Limpando Banco de Dados")
        except QSqlError as e:
            print(clearQuery.lastError())
            QMessageBox(self,"Erro","Erro ao limpar a lista de Etiquetas\n" + str(clearQuery.lastError()))
            return 0

    def Insere_Volumes(self,Rows):
        #Percorre todos os DOCs que precisam ser inseridos
        ct=0
        for row in Rows:
            DocID = self.mdlDocs.record(row).value("id")
            # Recupera os volumes desta NFe para então fazer a inserção
            Volumes = QSqlQuery("SELECT * FROM docs_volumes WHERE DOC_ID="+str(DocID))
            Volumes.exec()
            while Volumes.next():
                sql_Volumes = QtSql.QSqlQuery()
                sql_Volumes.prepare("INSERT INTO encomendas_prn SET Nome=:nome, Endereco=:endereco, Cidade=:cidade, Estado=:estado, CEP=:cep, Pais=:pais, Peso=:peso, num_volume=:num_volume, Volumes=:volumes, Documento=:documento, Obs=:obs, L=:larg, A=:alt, P=:prof")
                # Prepara as variáveis no formato para inclusão
                #SQL = "SELECT id,cliente,endereco,num,bairro,cidade,estado,cep,pais,pesoBruto,Documento FROM Docs ORDER BY id"
                varNome = self.mdlDocs.record(row).value("cliente")
                varEndereco = self.mdlDocs.record(row).value("endereco") + ", " + str(self.mdlDocs.record(row).value("num"))
                varCidade = self.mdlDocs.record(row).value("cidade")
                varEstado = self.mdlDocs.record(row).value("estado")
                varCep = self.mdlDocs.record(row).value("cep")
                varPais = self.mdlDocs.record(row).value("pais")
                varPeso = Volumes.value(6)
                varNumVolume = Volumes.value(2)
                varVolumes = Volumes.size()
                print("Record Count: " + str(Volumes.size()))
                varDoc = self.mdlDocs.record(row).value("Documento")
                varObs = self.mdlDocs.record(row).value("Obs")
                varL = Volumes.value(3)
                varA = Volumes.value(4)
                varP = Volumes.value(5)
                # Faz a associação das variáveis com os parametros
                sql_Volumes.bindValue(":nome", varNome)
                sql_Volumes.bindValue(":endereco", varEndereco)
                sql_Volumes.bindValue(":cidade", varCidade)
                sql_Volumes.bindValue(":estado", varEstado )
                sql_Volumes.bindValue(":cep", varCep)
                sql_Volumes.bindValue(":pais", varPais )
                sql_Volumes.bindValue(":peso", varPeso )
                sql_Volumes.bindValue(":num_volume", varNumVolume)
                sql_Volumes.bindValue(":volumes", varVolumes )
                sql_Volumes.bindValue(":documento", varDoc )
                sql_Volumes.bindValue(":obs", varObs)
                sql_Volumes.bindValue(":larg", varL)
                sql_Volumes.bindValue(":alt", varA)
                sql_Volumes.bindValue(":prof", varP)
                try:
                    sql_Volumes.exec()
                    print(sql_Volumes.lastError().text())
                    print(sql_Volumes.lastQuery())
                    ct+=1
                except QSqlError as e:
                    print(sql_Volumes.lastError())
                    return 0
        return ct

    def Gera_Etiquetas(self):
        # Gera o vetor com as posições de etiquetas selecionadas
        Pos = []
        # Cria o objeto relatório
        RPT = rptEtiquetas_Caixas()
        # Verifica se alguma posição personalizada está marcada
        if self.ui.chkEti1.isChecked() or self.ui.chkEti2.isChecked() or self.ui.chkEti3.isChecked() or self.ui.chkEti4.isChecked():
            if self.ui.chkEti1.isChecked():
                Pos.append(1)
            if self.ui.chkEti2.isChecked():
                Pos.append(2)
            if self.ui.chkEti3.isChecked():
                Pos.append(3)
            if self.ui.chkEti4.isChecked():
                Pos.append(4)
            print("Vetor posicoes")
            print(Pos)
            RPT.monta_pagina_personalizada(Pos)
        else:
            RPT.monta_pagina()
        # Faz uma chamada para o aplicativo padrão do sistema abrir o relatório
        os.system('xdg-open ' + RPT.arquivo)

    def btDanfe_Clicked(self):
        # Pega as linhas selecionadas
        self.ui.lblStatus.setText("Selecionando as DANFES a serem impressas")
        indexRows = self.Selecionados.selectedRows()
        Rows = []
        # Verifica se tem alguma linha selecionada
        if (len(indexRows) <= 0):
            return 0
        # Percorre as selecionadas para pegar os IDs
        for indexRow in sorted(indexRows):
            row = indexRow.row()
            DocID = self.mdlDocs.record(row).value("id")
            Rows.append(DocID)
        listaIDs = ','.join(str(e) for e in Rows)
        print("ListaIDs: ",listaIDs)
        # Com os IDs separados chamamos a função para gerar etiquetas
        # Instancia o objeto
        RPT = rptDanfe_Simples()
        # Monta a página de etiquetas
        RPT.monta_pagina(listaIDs)
        # Abre o arquivo com visualizador padrão do sistema
        os.system('xdg-open ' + RPT.arquivo)

    def btExportar_Clicked(self):
        # Pega as linhas selecionadas
        self.ui.lblStatus.setText("Selecionando NFes a serem Exportadas")
        indexRows = self.Selecionados.selectedRows()
        Rows = []
        row = 0
        # Verifica se tem alguma linha selecionada
        if len(indexRows) <= 0:
            return 0    # Se não tem nenhuma, já sai da função
        # Percorre as selecionadas para pegar os IDs
        for indexRow in sorted(indexRows):
            row = indexRow.row()
            Rows.append(row)
        # Monta as linhas que farão parte do arquivo
        # Percorre todos os DOCs que precisam ser exportados
        ct = 0
        registros = []
        self.ui.lblStatus.setText("Obtendo dados do banco de dados.")
        for row in Rows:
            self.ui.lblStatus.setText("Exportando registro %02d"%ct)
            varFixo = "2"
            varCPF_CNPJ = str(self.mdlDocs.record(row).value("cnpj_cpf"))
            # Limpa formatação do CNPJ/CPF
            varCPF_CNPJ = varCPF_CNPJ.replace("-", "").replace(".", "").replace(",", "").replace("/", "").replace(" ","")
            varNome = str(self.mdlDocs.record(row).value("cliente"))[:50].title()
            varEmail = str(self.mdlDocs.record(row).value("email")).replace(" ","").lower()
            varCuidados = ""
            varContato  = ""
            varCEP = self.mdlDocs.record(row).value("cep")
            # Limpa formataçaõ do CEP
            varCEP = varCEP.replace("-","").replace(".","").replace(",","").replace("/","")
            varLogradouro = str(self.mdlDocs.record(row).value("endereco"))[:50].replace(",","")
            varNumero = str(self.mdlDocs.record(row).value("num"))
            varComplemento = str(self.mdlDocs.record(row).value("complemento"))
            varBairro = str(self.mdlDocs.record(row).value("bairro")).capitalize()
            varCidade = str(self.mdlDocs.record(row).value("cidade")).upper()
            varTelefone = ""
            varCelular = str(self.mdlDocs.record(row).value("fone"))
            varCelular = varCelular.replace("(","").replace(")","").replace("-","").replace(".","").replace(" ","")
            varFax = ""
            # Monta a String que vai ser a linha
            #registros.append(varFixo + varCPF_CNPJ.ljust(14,"A") + varNome.ljust(50,"B") + varEmail.ljust(50,"C") + varCuidados.ljust(50,"D") + varContato.ljust(50,"E") + varCEP.ljust(8,"F") + varLogradouro.ljust(50,"G") + varNumero.ljust(6,"H") + varComplemento.ljust(30,"I") + varBairro.ljust(50,"J") + varCidade.ljust(50,"K") + varTelefone.ljust(18,"L") + varCelular.ljust(12,"M") + varFax.ljust(12,"N") + chr(13))
            registros.append(varFixo + varCPF_CNPJ.ljust(14) + varNome.ljust(50) + varEmail.ljust(50) + varCuidados.ljust(50) + varContato.ljust(50) + varCEP.ljust(8) + varLogradouro.ljust(50) + varNumero.ljust(6) + varComplemento.ljust(30) + varBairro.ljust(50) + varCidade.ljust(50) + varTelefone.ljust(18) + varCelular.ljust(12) + varFax.ljust(12) + chr(13))
            ct += 1

        if os.name == "posix":  # Linux
            arquivo = os.path.join("/mnt/rede/sigepclient/importar", "importar-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + ".csv")
        if os.name == "nt":  # Windows
            arquivo = os.path.join("m:", "sigepclient", "importar", "importar-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + ".csv")

        self.ui.lblStatus.setText("Gravando arquivo...")
        with open(arquivo, 'w',encoding='ISO-8859-1') as f:
            f.write("1SIGEP DESTINATARIO NACIONAL" + "\r")
            for linha in registros:
                f.write(linha)
            f.write("9"+"%06d"%ct+"\r")
            f.close()
        self.ui.lblStatus.setText("Arquivo exportado com sucesso")

