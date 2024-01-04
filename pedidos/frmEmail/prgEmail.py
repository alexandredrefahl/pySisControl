# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import locale, os, email, csv
from datetime import datetime
#import datetime
from bibliotecas.mysqldb import *
from pedidos.frmEmail.frmEmail import *


class frmEmail_Gui(QtWidgets.QDialog):

    # Definição da Classe e dos Widgets
    def __init__(self):
        super().__init__()
        self.ui = Ui_winEmail()
        self.ui.setupUi(self)

        # Define o padrão numérico para a representação
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Carrega o banco de dados
        self.db = conecta_MySql()

        # Preencher cada widget com os valores iniciais
        # Conectar cada widget que pode ter uma ação à função específica (Sinais)
        self.ui.btRegistrar.clicked.connect(self.Registrar)  # Lembre de passar a definição do método não o valor de retono
        self.ui.btEmail.clicked.connect(self.download_arquivos)

        # Define propriedades extra dos Widgets
        self.ui.pbProgresso.setVisible(False)
        # Mostra a interface gráfica
        self.show()

    def download_arquivos(self):
        a = QMessageBox.question(self,"Confirmação","Você gostaria de baixar os e-mails (SIM) ou usar os arquivos já baixados? (NÃO)",QMessageBox.Yes | QMessageBox.No)
        if a == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.ui.pbProgresso.setVisible(True)
            # Conecta no servidor
            mail = imaplib.IMAP4_SSL("uscentral66.myserverhosts.com", 993)
            # Autentica
            mail.login("email@clona-gen.com.br", "mypass")
            # Seleciona a Caixa de Entrada
            mail.select('INBOX.Responder')
            # Filtra os emails que tem o Assunto: Interessados
            type, data = mail.search(None, '(SUBJECT "Interessado")')
            if len(data[0]) == 0:
                QMessageBox.critical(self, "Erro!", "Erro ao resgatar mensagens", QMessageBox.Ok)

            mail_ids = data[0]
            # Lista os ids que foram selecionados
            id_list = mail_ids.split()
            # Atualiza a label de status
            self.ui.lblStatus.setText("Foram encontrados " + str(len(id_list)) + " e-mails.")
            # Atualiza a barra de progresso
            self.ui.pbProgresso.setRange(0, len(id_list) - 1)
            self.ui.pbProgresso.setValue(0)
            print("Encontrados " + str(len(id_list)) + " e-mails.")
            i = 0
            for num in data[0].split():
                self.ui.pbProgresso.setValue(i)
                print("-------------------------")
                print("Processando e-mail " + str(num))
                print("-------------------------")
                # Atualizando Label
                self.ui.lblStatus.setText("Processando e-mail " + str(i) + " de " + str(len(id_list)))
                typ, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('latin-1')
                email_message = email.message_from_string(raw_email_string)
                # Download do Anexo
                for part in email_message.walk():
                    # this part comes from the snipped I don't understand yet...
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    # Pego o nome do anexo
                    fileName = part.get_filename()
                    if bool(fileName):
                        fileName = "Reserva_" + str(i) + ".csv"
                        filePath = os.path.join('.','csv', fileName)
                        if not os.path.isfile(filePath):
                            fp = open(filePath, 'wb')
                            part.set_charset("utf-8")
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                        print('Baixado Arquivo "{file}"'.format(file=fileName))
                        # Se a checkbox estiver ativada arquiva e apaga senão não
                        if self.ui.chkArquivar.isChecked():
                            mail.copy(num, "inbox.interessados")
                            mail.store(num, "+FLAGS", "\\Deleted")
                i += 1
            # No final da operação "limpa" a caixa de mensagem
            mail.expunge()

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('De : ' + email_from + '\n')
                    # print ('Subject : ' + email_subject + '\n')
                    # print(msg.get_payload(decode=True))
            self.ui.pbProgresso.setVisible(0)
            self.ui.lblStatus.setText(str(i) + " e-mails processados")
        else:
            self.preenche_QTableView()
        QApplication.restoreOverrideCursor()

    def registra_contatosBD(self):
        # Processa o arquivo baixado
        print("Caminho:", os.path.join(os.curdir, 'csv'))
        lista_arquivos = self.lista_arquivos_csv(os.path.join(os.curdir, 'csv'), ".csv")
        # Variável para contar os aquivos
        i = 0
        # Estados para verificar se está na lista
        Estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        for arquivo in lista_arquivos:
            # Abre o arquivo CSV
            with open(os.path.join(os.curdir, "csv", arquivo), encoding='utf-8') as csv_file:
                print("Abrindo arquivo CSV")
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                # Para cada linha do arquivo faz o processamento
                for row in csv_reader:
                    if line_count == 0:
                        # pula o cabecalho do arquivo
                        line_count += 1
                    else:
                        # Pré processa as variáveis
                        var_Data = datetime.strptime(row[0], '%m/%d/%Y')
                        db_Data = var_Data.strftime('%Y-%m-%d')
                        db_Nome = row[1].title()
                        db_Fone = self.formata_telefone(row[4])
                        db_Email = row[3].lower()
                        db_Cidade = row[2].title()
                        db_Estado = row[2][-2:].upper()
                        if db_Estado in Estados:
                            db_Cidade = db_Cidade[:-3]
                        else:
                            db_Estado = ""
                        db_Atendido = 0
                        db_Contactado = 0
                        db_Produtos = row[5]
                        db_Assunto = "Mudas de Mandioca"

    def preenche_QTableView(self):
        # formata o datagrid e cria o dataModel
        self.model = QStandardItemModel()
        # Formata o número de colunas
        self.model.setColumnCount(7)
        # Dá nome para as colunas
        headerNames = []
        headerNames.append("Id")
        headerNames.append("Data")
        headerNames.append("Nome")
        headerNames.append("Cidade")
        headerNames.append("e-mail")
        headerNames.append("Fone")
        headerNames.append("Interesse")
        # Atribui o nome ao model
        self.model.setHorizontalHeaderLabels(headerNames)
        # Padrão de seleção por linhas
        self.ui.tblEmails.setSelectionBehavior(self.ui.tblEmails.SelectRows)
        # Habilita a ordenação
        self.ui.tblEmails.setSortingEnabled(True)

        # Processa o arquivo baixado
        print("Caminho:",os.path.join(os.curdir,'csv'))
        lista_arquivos = self.lista_arquivos_csv(os.path.join(os.curdir,'csv'), ".csv")
        # Variável para contar os aquivos
        i = 0
        for arquivo in lista_arquivos:
            # Abre o arquivo CSV
            with open(os.path.join(os.curdir,"csv",arquivo), encoding='utf-8') as csv_file:
                print("Abrindo arquivo CSV")
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                # Para cada linha do arquivo faz o processamento
                for row in csv_reader:
                    if line_count == 0:
                        # pula o cabecalho do arquivo
                        line_count += 1
                    else:
                        # Pré processa as variáveis
                        mail_ID = QStandardItem(f"{i:04d}")
                        var_Data = datetime.strptime(row[0], '%m/%d/%Y')
                        mail_Data = QStandardItem(var_Data.strftime('%Y-%m-%d'))
                        mail_Nome = QStandardItem(row[1].title())
                        mail_Cidade = QStandardItem(row[2].title())
                        mail_Email = QStandardItem(row[3].lower())
                        mail_Fone = QStandardItem(self.formata_telefone(row[4]))
                        mail_Interesse = QStandardItem(row[5])
                        # print('Data:',mail_Data,'\nNome: ',mail_Nome,'\nCidade:',mail_Cidade,'\nEmail: ',mail_Email,'\nFone: ',mail_Fone,'\nInteresse: ',mail_Interesse)

                        # Atribui cada uma das variáveis a uma coluna do model na linha selecionada
                        self.model.setItem(i, 0, mail_ID)
                        self.model.setItem(i, 1, mail_Data)
                        self.model.setItem(i, 2, mail_Nome)
                        self.model.setItem(i, 3, mail_Cidade)
                        self.model.setItem(i, 4, mail_Email)
                        self.model.setItem(i, 5, mail_Fone)
                        self.model.setItem(i, 6, mail_Interesse)
                        i = i + 1
        # Atribui os dados à tabela
        self.ui.tblEmails.setModel(self.model)
        # Não parece estar funcionando
        self.ui.tblEmails.setColumnWidth(0, 45)  # Id
        self.ui.tblEmails.setColumnWidth(1, 90)  # Data
        self.ui.tblEmails.setColumnWidth(2, 250)  # Nome
        self.ui.tblEmails.setColumnWidth(3, 120)  # Cidade
        self.ui.tblEmails.setColumnWidth(4, 250)  # Email
        self.ui.tblEmails.setColumnWidth(5, 150)  # Fone
        self.ui.tblEmails.setColumnWidth(6, 250)  # Interesse
        # Pega somente os selecionados
        self.Selecionados = self.ui.tblEmails.selectionModel()
        # Ao clicar dispara "Info_linha"
        self.Selecionados.selectionChanged.connect(self.info_linha)
        font = QtGui.QFont("Verdana", 8)
        self.ui.tblEmails.setFont(font)
        # Desabilita o botão de Email
        self.ui.btEmail.setEnabled(0)
        self.ui.chkArquivar.setEnabled(0)

    def formata_telefone(self, txtFone):
        # Limpa os caracteres especiais
        for char in txtFone:
            if char in "() -*#/":
                txtFone = txtFone.replace(char, "")
        # Verifica se é celular
        if len(txtFone) == 11:
            telFormatado = "({}) {}{}-{}".format(txtFone[0:2], txtFone[2], txtFone[3:7], txtFone[7:])
        # Telefone Fixo
        elif len(txtFone) == 10:
            telFormatado = "({}) {}-{}".format(txtFone[0:2], txtFone[2:6], txtFone[6:])
        # Ou se o cliente fez muitas anotações, retorna como está
        else:
            telFormatado = txtFone
        return telFormatado

    def lista_arquivos_csv(self, path_to_dir, suffix=".csv"):
        filenames = os.listdir(path_to_dir)
        return [filename for filename in filenames if filename.endswith(suffix)]

    def Registrar(self):
        # Define o cursor como Wait
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # Esta parte é executada quanto o botão é pressionado
        # Pega os dados da linha atual selecionada para fazer a inclusão
        indexRows = self.Selecionados.selectedRows()
        # Percorre cada item selecionado (no caso apenas 1 linha)
        for indexRow in sorted(indexRows):
            row = indexRow.row()
        mail_Data = self.ui.txtData.text()
        mail_Nome = self.ui.txtNome.text()
        mail_Cidade = self.ui.txtCidade.text()[:-3]  # Tirar o final da string que é o Estado
        mail_Email = self.ui.txtEmail.text()
        mail_Fone = self.ui.txtCelular.text()
        mail_Interesse = self.model.item(row, column=6).text()
        mail_UF = self.ui.txtCidade.text()[-2:]

        if self.ui.chkMysql.isChecked():
            contactado = 0
            if self.ui.chkMysql.isChecked():
                contactado = 1
            else:
                contactado = 0
            self.registra_reserva(mail_Data, mail_Nome, mail_Cidade, mail_Email, mail_Fone, mail_Interesse, mail_UF,contactado)
        if self.ui.chkEmail.isChecked():
            self.envia_email(mail_Nome, mail_Email, mail_Interesse,mail_Fone)
        cor_fundo = QColor(251, 236, 93, 127)
        # Tem que pintar célula por célula de cada linha
        for i in range(0, 7):
            self.model.setData(self.model.index(row, i), QBrush(cor_fundo), Qt.BackgroundRole)
        # restaura o cursor de ponteiro
        QApplication.restoreOverrideCursor()

    def info_linha(self, index):
        # Pega os dados da linha clicada e coloca nos campos
        indexRows = self.Selecionados.selectedRows()
        for indexRow in sorted(indexRows):
            row = indexRow.row()
        # Preenche os campos com a linha selecionada
        self.ui.txtCelular.setText(self.model.item(row, column=5).text())
        self.ui.txtEmail.setText(self.model.item(row, column=4).text())
        self.ui.txtNome.setText(self.model.item(row, column=2).text())
        varData = self.model.item(row, column=1).text()
        print(varData)
        # datetime.datetime.strptime(varData,"%d-%m-%y")
        self.ui.txtData.setText(varData)
        self.ui.txtCidade.setText(self.model.item(row, column=3).text())
        # Preenche a lista com as mudas de interesse
        itens = self.model.item(row, column=6).text().split(",")
        # Limpa o list view
        self.ui.lstVariedades.clear()
        for item in itens:
            it = QListWidgetItem(item)
            self.ui.lstVariedades.addItem(it)

    def registra_reserva(self, data, nome, cidade, email, fone, interesse, uf, contactado=0):
        print("Data recebida na função")
        print(data)
        #sql_Reserva = QtSql.QSqlQuery()
        sql_Contato = QtSql.QSqlQuery()
        #sql_Reserva.prepare("INSERT INTO reservas SET `Data`=:data, `Nome`=:nome, `Fone`=:fone, `Email`=:email, `Cidade`=:cidade, `UF`=:uf, `Atendido`=:atendido")
        sql_Contato.prepare("INSERT INTO contatos SET `Data`=:data, `Nome`=:nome, `Fone`=:fone, `Email`=:email, `Cidade`=:cidade, `UF`=:uf, `Atendida`=:atendido, `Contactado`=:contactado, `Produtos`=:produtos, `Assunto`=:assunto")
        # Prepara  as variáveis
        varData = data
        varNome = nome.title()
        varFone = fone
        varEmail = email.lower()
        varCidade = cidade
        varUf = uf.upper()
        varAtendido = 0
        varContactado = contactado
        varProdutos = "Mandioca"
        varAssunto = "Mudas de Mandioca"
        # Preenche os valores
        #sql_Reserva.bindValue(':data', varData)
        #sql_Reserva.bindValue(':nome', varNome)
        #sql_Reserva.bindValue(':fone', varFone)
        #sql_Reserva.bindValue(':email', varEmail)
        #sql_Reserva.bindValue(':cidade', varCidade)
        #sql_Reserva.bindValue(':uf', varUf)
        #sql_Reserva.bindValue(':atendido', 0)
        sql_Contato.bindValue(':data', varData)
        sql_Contato.bindValue(':nome', varNome)
        sql_Contato.bindValue(':fone', varFone)
        sql_Contato.bindValue(':email', varEmail)
        sql_Contato.bindValue(':cidade', varCidade)
        sql_Contato.bindValue(':uf', varUf)
        sql_Contato.bindValue(':atendido', varAtendido)
        sql_Contato.bindValue(':contactado', varContactado)
        sql_Contato.bindValue(':produtos', varProdutos)
        sql_Contato.bindValue(':assunto', varAssunto)
        from PyQt5.QtSql import QSqlError
        try:
            # Confirma se o pedido foi incluido com sucesso
            if sql_Contato.exec():
                # **** INCLUSÃO DOS ITENS ****
                id_reserva = sql_Contato.lastInsertId()
                print("Contato Inserido: " + str(id_reserva))
                # Percorre os ítens da tabela para fazer a inclusão
                numLinhas = self.ui.lstVariedades.count()
                print(str(numLinhas) + " itens a incluir")
                print('Linha inserida', id_reserva)

                # Vamos à inserção dos ítens
                ct = 1
                for varClone in ("396", "397", "398", "399", "400", "401","429"):
                    if (varClone in interesse):
                        sql_Item = QtSql.QSqlQuery()
                        #sql_Item.prepare("INSERT INTO reservas_itens SET `Doc_ID`=:docid,`Mercadoria`=:mercadoria,`Clone`=:clone,`Descricao`=:descricao,`Quantidade`=:qtde,`Preco`=:preco,`Forma`=:forma")
                        sql_Item.prepare("INSERT INTO contatos_itens SET `Doc_ID`=:docid,`Mercadoria`=:mercadoria,`Clone`=:clone,`Descricao`=:descricao,`Quantidade`=:quantidade")
                        # Prepara as variáveis auxiliáres
                        sql_Item.bindValue(':docid', id_reserva)
                        sql_Item.bindValue(':mercadoria', 45)
                        sql_Item.bindValue(':clone', varClone)
                        sql_Item.bindValue(':descricao', "Manihota esculenta cv. BRS-" + varClone)
                        sql_Item.bindValue(':quantidade', 25)
                        #sql_Item.bindValue(':preco', 2.50)
                        #sql_Item.bindValue(':forma', "Muda Aclimatizada")
                        try:
                            if sql_Item.exec():
                                print("Item " + str(ct) + " do contato " + str(id_reserva) + " inserido com sucesso no ID " + str(sql_Item.lastInsertId()))
                            else:
                                print(sql_Item.lastError().text())
                        except QSqlError as err:
                            print("Erro ao inserir item")
                            print(err.text())
                        ct = ct + 1
                    else:
                        print('Linha não inserida')
                QMessageBox.information(self,"Confirmação","Contato " + str(id_reserva)  + " incluída com sucesso!",QMessageBox.Ok)
            else:
                print("Erro ao incluir a reserva")
                print(sql_Contato.executedQuery())
                print(sql_Contato.lastError().text())
        except:
            print(sql_Contato.lastError().text())
            #QMessageBox(self,"Erro","Erro ao incluir o item do contato\n" + sql_Contato.lastError().text(), QMessageBox.Ok)

    def envia_email(self, Nome, Email, Interesse, Fone):
        # Extrai o nome arruma as maiusculas e pega somente o primeiro nome
        tratamento = Nome.split(" ")[0].title()
        variedades = ""
        # Trata as variedades de interesse
        for var in ("396", "397", "398", "399", "400", "401"):
            if (var in Interesse):
                if (len(variedades) == 0):
                    variedades = var
                else:
                    variedades = variedades + ", " + var
        # Carregar texto base do e-mail
        arquivo_html = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "modelo_resposta.html"), "r")
        texto_email = arquivo_html.read()
        texto_email = texto_email.replace("[Nome]", tratamento)
        hora_atual = datetime.now().hour
        if hora_atual < 12:
            varSaudacao = 'Bom dia'
        elif 12 <= hora_atual < 18:
            varSaudacao = 'Boa tarde'
        else:
            varSaudacao = 'Boa noite'
        texto_email = texto_email.replace("[saudacao]", varSaudacao)
        texto_email = texto_email.replace("[variedades]", variedades)
        texto_email = texto_email.replace("[email]", Email)
        texto_email = texto_email.replace("[fone]", Fone)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Mudas de Mandiocas BRS"
        msg['From'] = "email@clona-gen.com.br"
        msg['To'] = Email
        msg['Cc'] = "otheremail@email.com"
        # Create the body of the message (a plain-text and an HTML version).
        text = "Texto Email"
        html = texto_email
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        server = smtplib.SMTP("uscentral66.myserverhosts.com")
        server.ehlo()
        server.starttls()
        server.login("email@clona-gen.com.br", "mypass")
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        server.sendmail("email@clona-gen.com.br", [Email, "otheremail@email.com"], msg.as_string())
        print("Email enviado...\r\r")
        server.quit()
