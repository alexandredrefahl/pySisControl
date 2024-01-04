# -*- coding: utf-8 -*-

import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import os
import email
import csv
import datetime
import mysql.connector 
from mysql.connector import MySQLConnection, Error

MY_SQL_HOST = "187.59.80.163"

def download_arquivos():
    # Conecta no servidor
    mail = imaplib.IMAP4_SSL("uscentral30.myserverhosts.com",993)
    # Autentica
    mail.login("comercial@clona-gen.com.br", "mypass")
    # Seleciona a Caixa de Entrada
    mail.select('Inbox')
    # Filtra os emails que tem o Assunto: Interessados
    type, data = mail.search(None, '(SUBJECT "Interessado")')
    mail_ids = data[0]
    id_list = mail_ids.split()
    print("Encontrados " + str(len(id_list)) + " e-mails.")
    i=0
    for num in data[0].split():
        print("-------------------------")
        print("Processando e-mail " + str(num))
        print("-------------------------")
        type, data = mail.fetch(num,'(RFC822)')
        raw_email = data[0][1]
        # raw_email = raw_email.encode('ascii', 'ignore').decode('ascii')
        # converts byte literal to string removing b''
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
                fileName="Reserva_" + str(i) + ".csv"
                filePath = os.path.join('.', fileName)
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    part.set_charset("utf-8")
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                print('Baixado Arquivo "{file}"'.format(file=fileName))
                a = input("Mover e-mail para pasta Arquivados (s/n):")
                if (a == "s"):
                    mail.copy(num,"inbox.interessados")
                # Processa o arquivo baixado
                with open(filePath, encoding='utf-8') as csv_file:
                    print("Abrindo arquivo CSV")
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            #pula o cabecalho do arquivo
                            line_count += 1
                        else:
                            mail_Data=row[0]
                            mail_Nome= row[1].title()
                            mail_Cidade=row[2].title()
                            mail_Email = row[3].lower()
                            mail_Fone = formata_telefone(row[4])
                            mail_Interesse= row[5]
                            print('Data:',mail_Data,'\nNome: ',mail_Nome,'\nCidade:',mail_Cidade,'\nEmail: ',mail_Email,'\nFone: ',mail_Fone,'\nInteresse: ',mail_Interesse)
                            a = input("Registra Reserva no Banco de Dados (s/n):")
                            if (a=="s"):
                                registra_reserva(mail_Data,mail_Nome,mail_Cidade,mail_Email,mail_Fone,mail_Interesse)
                            a = input("Enviar E-mail para Cliente (s/n):")
                            if (a=="s"):
                                envia_email(mail_Nome,mail_Email, mail_Interesse)
                            
                            line_count += 1
        # Mark one or more items for deletion: 
        # mail.store(msg_no, '+FLAGS', '\\Deleted')
        # Expunge the mailbox: 
        # imap.expunge()
        # Substituir string dentro da mensagem
        # s.replace("aa", "123")
        i += 1

    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            #email_subject = msg['subject']
            email_from = msg['from']
            print ('De : ' + email_from + '\n')
            #print ('Subject : ' + email_subject + '\n')
            #print(msg.get_payload(decode=True))         

def registra_reserva(data,nome,cidade,email,fone,interesse):
    query = "INSERT INTO reservas (`Data`,`Nome`,`Fone`,`Email`,`Atendido`) VALUES (%s,%s,%s,%s,0)"
    data_sql=datetime.datetime.strptime(data,"%m/%d/%Y")
    args = (data_sql,nome.title(),fone,email.lower())
 
    try:
        conn = mysql.connector.connect(host=MY_SQL_HOST,user="alexandre",passwd="@drf1624",database="controle")
        
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            id_reserva = cursor.lastrowid
            print('Linha inserida', id_reserva)
            
            # Vamos à inserção dos ítens
            for var in ("396","397","398","399","400","401"):
                if (var in interesse):
                    query = "INSERT INTO reservas_itens (`Doc_ID`,`Mercadoria`,`Clone`,`Descricao`,`Quantidade`,`Preco`,`Forma`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    args = (id_reserva,45,var,"Manihota esculenta cv. BRS-"+var,25,2.00,"Muda Aclimatizada")
                    try:
                        cursor.execute(query, args)
                    except Error as error:
                        print(error)
        else:
            print('Linha não inserida')
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

def envia_email(Nome, Email, Interesse):
    # Extrai o nome arruma as maiusculas e pega somente o primeiro nome
    tratamento = Nome.split(" ")[0].title()
    variedades = ""
    # Trata as variedades de interesse
    for var in ("396","397","398","399","400","401"):
        if (var in Interesse):
            if (len(variedades)==0):
                variedades = var
            else:
                variedades = variedades + ", " + var
    # Carregar texto base do e-mail
    arquivo_html = open("modelo_resposta.html","r")
    texto_email = arquivo_html.read()
    texto_email = texto_email.replace("[Nome]",tratamento)
    texto_email = texto_email.replace("[saudacao]","Bom dia") 
    texto_email = texto_email.replace("[variedades]",variedades)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Mudas de Mandiocas BRS"
    msg['From'] = "comercial@clona-gen.com.br"
    msg['To'] = Email
    msg['Cc'] = "alexandredrefahl@gmail"
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
    server = smtplib.SMTP("uscentral30.myserverhosts.com")
    server.ehlo()
    server.starttls()
    server.login("comercial@clona-gen.com.br", "mypass")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail( "comercial@clona-gen.com.br",[Email,"alexandredrefahl@gmail.com"], msg.as_string())
    print("Email enviado...\r\r")
    server.quit()

def formata_telefone(txtFone):
    # Limpa os caracteres especiais
    for char in txtFone:
        if char in "() -*#/":
            txtFone = txtFone.replace(char,"")
    # Verifica se é celular
    if len(txtFone)==11:
        telFormatado = "({}) {}{}-{}".format(txtFone[0:2],txtFone[2] ,txtFone[3:7], txtFone[7:])
    # Telefone Fixo
    elif len(txtFone)==10:
        telFormatado = "({}) {}-{}".format(txtFone[0:2],txtFone[2:6],txtFone[6:])
    # Ou se o cliente fez muitas anotações, retorna como está
    else:
        telFormatado = txtFone
    return telFormatado

# Função para limpar a tela 
def clear(): 
    # No windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # Para MAC e linux (Nesse caso, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

