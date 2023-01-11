#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em 18 de março de 2020

@author: alexandre
"""

from PyQt5 import QtCore,  QtSql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import pink, black, red, blue, green, grey, white
from reportlab.lib.units import inch, mm
import os
from datetime import datetime
import bibliotecas.mysqldb

class rptPlanilha_Reservas:

    def __init__(self, dataINI="", dataFIM="", ordem="Data", criterio="Cadastro"):
        self.dataINI = dataINI
        self.dataFIM = dataFIM
        self.Ordem = ordem
        self.Criterio = criterio
        # Cria o canvas para produção do relatório
        self.arquivo = os.path.join(os.path.dirname(__file__),"rptPlanilha_Reservas-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.pdf')
        self.c = canvas.Canvas(self.arquivo)
        self.pagina = 1
        self.db = bibliotecas.mysqldb.conecta_MySql()
        # Define a largura das colunas
        self.colData = 10 * mm
        self.colNome = 26.5 * mm
        self.colCEP = 69 * mm
        self.colFone = 83 * mm
        self.colCidade = 107 * mm
        self.colUF = 129 * mm

    def show_report(self):
        self.c.setPageSize(landscape(A4))
        self.monta_cabecalho()
        self.monta_titulo()
        self.monta_pagina()
        self.monta_rodape()
        self.c.showPage()
        self.c.save()

    def monta_cabecalho(self):
        # Logotipo
        fileLogo = os.path.join(os.path.dirname(__file__), "logo.jpg")
        self.c.drawImage(fileLogo, -5 * mm, 185 * mm, height=51, preserveAspectRatio=True)
        # Duas linhas e título
        self.c.setStrokeColor(black)
        self.c.setLineWidth(2)
        self.c.line(10 * mm, 205 * mm, 287 * mm, 205 * mm)
        self.c.line(10 * mm, 185 * mm, 287 * mm, 185 * mm)
        self.c.setFont("Helvetica-Bold", 16)
        # Informação dos parametros
        self.c.drawCentredString(148.5 * mm, 192.5 * mm, "RELATÓRIO DE RESERVAS", charSpace=2)
        # self.c.drawString(90 * mm, 190 * mm, "RELATÓRIO DE RESERVAS")
        self.c.setFont("Helvetica", 8)
        self.c.drawRightString(287 * mm, 200 * mm, "Período: " + self.dataINI + " até " + self.dataFIM)
        # Informações da emissão do relatório
        self.c.drawRightString(287 * mm, 195 * mm, "Emissão: " + datetime.today().strftime('%d-%m-%Y'))
        self.c.drawRightString(287 * mm, 187 * mm, "Pág: " + str(self.pagina))

    def monta_titulo(self):
        self.c.setStrokeColor(black)
        self.c.setLineWidth(0)
        self.c.line(10 * mm, 176 * mm, 287 * mm, 176 * mm)
        self.c.setFont("Helvetica", 8)
        lin = 177 * mm
        self.c.drawString(self.colData, lin, "Data")  # Data
        self.c.drawString(self.colNome, lin, "Nome")  # Nome
        self.c.drawString(self.colCEP, lin, "CEP")  # CEP
        self.c.drawString(self.colFone, lin, "Fone")
        self.c.drawString(self.colCidade, lin, "Cidade")
        self.c.drawString(self.colUF, lin, "UF")
        self.c.setFont("Helvetica", 5)
        Titulos = ["Ajubá", "Pérola", "Fantástico", "Imperial", "Vitória", "396", "397", "398", "399", "400", "401",
                   "420", "CS-01", "Amélia", "Beaure", "Rubissol"]
        colProd = 159 * mm
        i = 0
        for tit in Titulos:
            self.c.drawRightString(colProd, lin, Titulos[i])  # Produtos
            colProd += 8.55 * mm
            i += 1

    def monta_rodape(self):
        pass

    def monta_pagina(self):
        query = QtSql.QSqlQuery(self.db)
        # monta a SQL Base
        SQL = "SELECT * FROM planilha_reservas"
        # Verifica qual o critério de Data. Se é do cadastro ou do Prazo
        if self.Criterio == 'Cadastro':
            data = 'data'
        elif self.Criterio == 'Prazo':
            data = 'prazo'
        # Acrescenta o limite de datas caso seja informado
        if len(self.dataINI) > 0 and len(self.dataFIM) > 0:
            SQL = SQL + " WHERE " + data + " BETWEEN '" + self.dataINI + "' AND '" + self.dataFIM + "'"
        # Acrescenta o ordenador caso seja informado
        if self.Ordem != "Data":
            if self.Ordem == "Nome":
                SQL = SQL + " ORDER BY Nome"
            if self.Ordem == "Prazo":
                SQL = SQL + " ORDER BY Prazo"
        else:
            SQL += " ORDER BY Data"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            print("Query validada: ", SQL)
            if query.exec_():
                #print("Executando query")
                x = 1
                ct = 1
                lin = 172 * mm
                alt_lin = 3 * mm
                # vetor para totalizar os produtos
                self.totais = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                while query.next():
                    # Relatório zebrado
                    if x % 2 == 0:
                        self.c.setFillColorRGB(0, 0, 0, 0.10)
                        self.c.rect(3 * mm, lin - (1*mm), 285 * mm, alt_lin, stroke=0, fill=1)
                    self.c.setFont("Courier", 6)
                    self.c.setFillColorRGB(0, 0, 0, 0.50)
                    self.c.drawRightString(9.5 * mm, lin,str(query.value(0)))  # ID
                    self.c.setFillColor(black)
                    self.c.setFont("Courier", 7)
                    varData = query.value(1)
                    self.c.drawString(self.colData, lin, varData.toString(QtCore.Qt.ISODate))  # Data
                    self.c.drawString(self.colNome, lin, query.value(2)[:27])  # Nome
                    self.c.drawString(self.colCEP, lin, query.value(7))  # CEP
                    self.c.drawString(self.colFone, lin, query.value(3)[:15])  # Fone
                    self.c.drawString(self.colCidade, lin, query.value(8)[:15])  # Cidade
                    self.c.drawString(self.colUF, lin, query.value(9))  # UF
                    colProd = 159 * mm
                    for col in range(12, 28):
                        #print(ct," | ",col)
                        self.c.drawRightString(colProd, lin,
                                               "-" if query.value(col) == 0 else str(int(query.value(col))))  # Produtos
                        if query.value(col) is not None:
                            self.totais[col-12] = self.totais[col-12] + int(query.value(col))
                        colProd += 8.55 * mm
                    lin -= alt_lin
                    x += 1
                    ct += 1
                    if x > 55:
                        # Fecha a primeira página
                        self.c.showPage()
                        # Atualiza o número da página
                        self.pagina += 1
                        # Reposiciona
                        lin = 172 * mm
                        # Zera contador de linhas
                        x = 1
                        # Cabecalho e titulo nas paginas seguintes
                        self.monta_cabecalho()
                        self.monta_titulo()
                    #            linhas.append((260 * mm) - (x * 6 * mm) - 2)
                # Exibe os totais
                self.c.setFont("Courier-Bold", 7)
                colProd = 159 * mm
                #print(self.totais)
                for col in range(12, 28):
                    self.c.drawRightString(colProd, lin,"-" if self.totais[col-12] == 0 else str(self.totais[col-12]))  # Produtos
                    colProd += 8.55 * mm



if __name__ == '__main__':
    #print('Instanciando objeto')
    RPT = rptPlanilha_Reservas(ordem="Nome",criterio="Cadastro")
    #print("cria relatorio")
    RPT.show_report()
    os.system('xdg-open ' + RPT.arquivo)

    # query = QtSql.QSqlQuery(db)
    # is_valid_query = query.prepare("SELECT * FROM planilha_reservas")
    # is_valid_query = query.prepare("SELECT * FROM credentials WHERE username = ? and password = ?")
    # Query com parametros
    # if is_valid_query:
    #    # query.addBindValue(username)
    #    # query.addBindValue(password)
    #    if query.exec_():
    #        c = canvas.Canvas('rptPlanilha_Reservas.pdf')
    #        c.setPageSize(landscape(A4))
    #        monta_pagina(c)
    #        linhas = [266 * mm]
    #        x = 0
    #        while query.next():
    #            print(query.value(0), " ", query.value(1), " ", query.value(2))
    #            c.setFont("Helvetica", 10)
    #            c.drawString(15 * mm, (261 * mm) - (x * 6 * mm), str(query.value(0)))
    #            c.drawString(55 * mm, (261 * mm) - (x * 6 * mm), query.value(1))
    #            c.drawString(103 * mm, (261 * mm) - (x * 6 * mm), query.value(1))
    #            linhas.append((260 * mm) - (x * 6 * mm) - 2)
    #            c.setStrokeColor(grey)
    #            x += 1
    #        # Monta o grid depois de ter colocado os dados
    #        c.grid([10 * mm, 50 * mm, 100 * mm, 133 * mm], linhas)
    #        c.setStrokeColor(black)
    #        c.showPage()
    #        c.drawString(20 * mm, 280 * mm, "Segunda Pagina")
    #        c.showPage()
    #        c.drawString(20 * mm, 280 * mm, "Terceira Pagina")
    #        c.save()
    #        os.system("xdg-open report.pdf")
    #    else:
    #        print('Failed')
    # else:
    #    print(query.lastError().text())
    # db.close()
