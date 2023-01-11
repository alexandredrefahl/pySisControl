from PyQt5 import QtSql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.colors import pink, black, red, blue, green, grey, white
from reportlab.lib.units import inch, mm
import os
from datetime import datetime
import locale
import bibliotecas.mysqldb

class rptRelatorio_Vendas:
    def __init__(self,dataINI="", dataFIM=""):
        # Estabelece os parâmetros
        self.dataINI = dataINI
        self.dataFIM = dataFIM
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Cria o canvas para produção do relatório
        self.arquivo = os.path.join(os.path.dirname(__file__), "rptRelatorioVendas-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.pdf')
        self.c = canvas.Canvas(self.arquivo)
        self.pagina = 1
        self.db = bibliotecas.mysqldb.conecta_MySql()

    def show_report(self):
        self.c.setPageSize(portrait(A4))
        self.monta_cabecalho()
        self.monta_resumo()
        self.monta_detalhamento()
        self.c.showPage()
        self.c.save()

    def monta_cabecalho(self):
        #self.c.setFillColorRGB(0.92, 0.53, 0.20)
        #self.c.rect(0 * mm, 260 * mm , 210 * mm, 36 * mm, stroke=0, fill=1)
        #Logotipo
        fileLogo = os.path.join(os.path.dirname(__file__), "logo.jpg")
        self.c.drawImage(fileLogo, -5 * mm, 270 * mm, height=51, preserveAspectRatio=True)
        self.c.setStrokeColor(white)
        self.c.setFont("Helvetica-Bold", 16)
        # Informação dos parametros
        self.c.drawCentredString(105 * mm, 275 * mm, "RELATÓRIO DE VENDAS", charSpace=2)
        self.c.setFont("Helvetica", 8)
        self.c.drawRightString(205 * mm, 285 * mm, "Período: " + self.dataINI + " até " + self.dataFIM)
        # Informações da emissão do relatório
        self.c.drawRightString(205 * mm, 280 * mm, "Emissão: " + datetime.today().strftime('%d-%m-%Y'))
        self.c.drawRightString(205 * mm, 275 * mm, "Pág: " + str(self.pagina))

    def monta_resumo(self):
        # self.c.setFillColorRGB(0.92, 0.53, 0.20)
        hLine = 3 * mm
        wRect = 40 * mm
        hRect = 40 * mm
        base_rect = 210 * mm
        # Calcula o tamanho da linha baseado na posição do quadrado
        base_line = (base_rect + hRect - hLine) * mm

        # Quadro de Pedidos
        self.c.setStrokeColorRGB(0.9, 0.9, 0.9)   # Verde Aqua
        self.c.rect(10 * mm, base_rect, wRect, hRect, stroke=1, fill=0)
        self.c.setFillColorRGB(0.08, 0.87, 0.76)
        self.c.rect(10 * mm, 247 * mm, wRect, 3 * mm, stroke=0, fill=1)
        # Quadro de Vendas
        self.c.setStrokeColorRGB(0.9, 0.9, 0.9)   # Verde Escuro
        self.c.rect(60 * mm, base_rect, wRect, hRect, stroke=1, fill=0)
        self.c.setFillColorRGB(0.11, 0.53, 0.08)
        self.c.rect(60 * mm, 247 * mm, wRect, 3 * mm, stroke=0, fill=1)
        # Quadro de Quadro de Mudas
        self.c.setStrokeColorRGB(0.9, 0.9, 0.9)  # Amarelo Queimado
        self.c.rect(110 * mm, base_rect, wRect, hRect, stroke=1, fill=0)
        self.c.setFillColorRGB(0.96, 0.80, 0.02)
        self.c.rect(110 * mm, 247 * mm, wRect, hLine, stroke=0, fill=1)
        # Quadro de Frete
        self.c.setStrokeColorRGB(0.9, 0.9, 0.9)  # Azul Escuro
        self.c.rect(160 * mm, base_rect, wRect, hRect, stroke=1, fill=0)
        self.c.setFillColorRGB(0.08, 0.57, 0.88)
        self.c.rect(160 * mm, 247 * mm, wRect, hLine, stroke=0, fill=1)
        # Titulos das caixas
        self.c.setFillColor(black)
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawCentredString(30 * mm, 240 * mm, "PEDIDOS")
        self.c.drawCentredString(80 * mm, 240 * mm, "VENDAS")
        self.c.drawCentredString(130 * mm, 240 * mm, "MUDAS")
        self.c.drawCentredString(180 * mm, 240 * mm, "FRETE")
        self.c.setFillColor(grey)
        self.c.setFont("Helvetica", 8)
        # Pedidos
        self.c.drawString(12 * mm, 233 * mm, "Gerados")
        self.c.drawString(12 * mm, 220 * mm, "Entregues")
        # Vendas
        self.c.drawString(62 * mm, 233 * mm, "Valor no Período")
        self.c.drawString(62 * mm, 220 * mm, "Acumulado do Mês")
        # Mudas
        self.c.drawString(112 * mm, 233 * mm, "Mudas no Período")
        self.c.drawString(112 * mm, 220 * mm, "Acumulado do Mês")
        # Frete
        self.c.drawString(162 * mm, 233 * mm, "Frete do Período")
        self.c.drawString(162 * mm, 220 * mm, "Líquido do Período")
    def monta_detalhamento(self):
        self.c.setFillColor(black)
        self.c.setFont("Helvetica-Bold", 17)
        self.c.drawString(10 * mm, 193 * mm, "RESUMO DE MUDAS VENDIDAS")
        lin = 180 * mm
        hLin = 6 * mm
        # Cabeçalho da tabela
        self.c.setFont("Helvetica", 10)
        self.c.drawString(12 * mm, lin, "Cód")
        self.c.drawString(20 * mm, lin, "Clone")
        self.c.drawString(32 * mm, lin, "Descrição")
        self.c.drawString(120 * mm, lin, "Qtde")
        self.c.drawString(140 * mm, lin, "Acumulado")
        self.c.drawString(160 * mm, lin, "Valor")
        self.c.drawString(180 * mm, lin, "Acumulado")
        self.c.setStrokeColor(black)
        self.c.rect(10 * mm, 178 * mm , 190 * mm, hLin , stroke=1, fill=0)
        # Pega os dados no banco de dados
        query = QtSql.QSqlQuery(self.db)
        # monta a SQL Base
        SQL = "SELECT codpro,clone,(SELECT Nome FROM CLONES WHERE MERCADORIA = docs_itens.CodPro AND clone= docs_itens.Clone), sum(quantidade),sum(total) FROM docs_itens INNER JOIN docs ON docs_itens.Doc_ID=docs.id WHERE docs.data between '" + self.dataINI + "' and '" + self.dataFIM + "' GROUP BY codpro,clone ORDER BY codpro,clone"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            print("Query validada: ", SQL)
            if query.exec_():
                # print("Executando query")
                x = 1
                ct = 1
                lin = 172 * mm
                hLin = 4.5 * mm
                # Variáveis de totalização
                tMudas = 0
                tValor = 0
                while query.next():
                    self.c.setFillColor(black)
                    self.c.drawCentredString(16 * mm, lin, query.value(0))     # Codigo
                    self.c.drawCentredString(26 * mm, lin, "{:04d}".format(query.value(1)))     # Clone
                    self.c.drawString(32 * mm, lin, str(query.value(2)))            # Descrição
                    self.c.drawRightString(138 * mm, lin, str(int(query.value(3))))      # Mudas
                    self.c.drawRightString(178 * mm, lin, locale.currency(query.value(4), symbol=False, grouping=True)) # Valor
                    # Acumulando total

                    tMudas += query.value(3)
                    tValor += query.value(4)
                    # Relatório zebrado
                    if x % 2 == 0:
                        self.c.setFillColorRGB(0, 0, 0, 0.10)
                        self.c.rect(10 * mm, lin - (1 * mm), 190 * mm, hLin, stroke=0, fill=1)
                    x += 1
                    lin -= hLin
                # Coloca os totais na ultima linha
                self.c.setFont("Helvetica-Bold", 10)
                self.c.drawRightString(138 * mm, lin, str(int(tMudas)))  # Mudas
                self.c.drawRightString(178 * mm, lin, locale.currency(tValor, symbol=False,grouping=True))  # Valor
        # Busca quantidade de pedidos
        SQL = "SELECT count(id) from pedidos where data between '" + self.dataINI + "' and '" + self.dataFIM + "'"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            if query.exec_():
                while query.next():
                    varNPedidos = query.value(0)
        # Busca Pedidos Atendidos
        SQL = "SELECT count(id) from pedidos where (data between '" + self.dataINI + "' and '" + self.dataFIM + "') AND NOT isnull(DataEntregue)"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            if query.exec_():
                while query.next():
                    varNAtendidos = query.value(0)
        # Busca os totais
        SQL = "select sum(vFrete), sum(vtotal), sum(vprod) from docs where (data between '" + self.dataINI + "' and '" + self.dataFIM + "')"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            if query.exec_():
                while query.next():
                    varFrete = query.value(0)
                    varTotal = query.value(1)
                    varProdutos = query.value(2)
        # Acumulados do mês
        SQL = "select sum(vFrete), sum(vtotal), sum(vprod) from docs where Year(data) = year('" + self.dataFIM + "') and month(data)=month('" + self.dataFIM + "')"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            if query.exec_():
                while query.next():
                    varAcFrete = query.value(0)
                    varAcTotal = query.value(1)
                    varAcProdutos = query.value(2)
        # Acumulado de mudas
        SQL = "select sum(Quantidade) from docs_itens inner join docs on docs.id = docs_itens.Doc_ID where Year(data) = year('" + self.dataFIM + "') and month(data)=month('" + self.dataFIM + "')"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            if query.exec_():
                while query.next():
                    varAcMudas = query.value(0)
        # Preenche os totais gerais
        self.c.setFillColor(black)
        self.c.setFont("Helvetica-Bold", 17)
        # Pedidos
        self.c.drawString(12 * mm, 227 * mm, str(varNPedidos))
        self.c.drawString(12 * mm, 214 * mm, str(varNAtendidos))
        # Vendas
        self.c.drawString(62 * mm, 227 * mm, locale.currency(varTotal, symbol=True, grouping=True))
        self.c.drawString(62 * mm, 214 * mm, locale.currency(varAcTotal, symbol=True, grouping=True))
        # Mudas
        self.c.drawString(112 * mm, 227 * mm, str(int(tMudas)))
        self.c.drawString(112 * mm, 214 * mm, str(int(varAcMudas)))
        # Mudas
        self.c.drawString(162 * mm, 227 * mm, locale.currency(varFrete, symbol=True, grouping=True))
        self.c.drawString(162 * mm, 214 * mm, locale.currency(varProdutos, symbol=True, grouping=True))


if __name__ == '__main__':
    #print('Instanciando objeto')
    RPT = rptRelatorio_Vendas(dataINI="2023-01-01",dataFIM="2023-01-10")
    #print("cria relatorio")
    RPT.show_report()
    os.system('xdg-open ' + RPT.arquivo)