from PyQt5 import QtSql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER, portrait
from reportlab.lib.colors import pink, black, red, blue, green, grey, white
from reportlab.lib.units import inch, mm
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime
import locale
#import bibliotecas.mysql
from bibliotecas.mysqldb import conecta_MySql
from bibliotecas.biblioteca import getPastaPrincipal
#import locmysql

class rptEtiquetas_Caixas:
    def __init__(self):
        # Cria o canvas para produção do relatório
        dir_base = os.path.join(getPastaPrincipal(), "spool")
        self.arquivo = os.path.join(dir_base, "rptEtiquetasCaixas-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.pdf')
        self.c = canvas.Canvas(self.arquivo)
        self.pagina = 1
        # Limites das Etiquetas (Papel PIMACO 6288)
        self.Eti_XI = [109 * mm,   1 * mm, 109 * mm,   1 * mm]
        self.Eti_YI = [277.5 * mm, 139.5 * mm, 139.5 * mm, 277.5 * mm]
        self.Eti_XF = [215 * mm, 109 * mm, 215 * mm, 109 * mm]
        self.Eti_YF = [141 * mm,   1 * mm,   1 * mm, 141 * mm]
        self.Dados = conecta_MySql()

    def monta_pagina_personalizada(self, Posicoes):
        self.c.setPageSize(portrait(LETTER))
        ct = 0
        # Recupera as etiquetas selecionadas no Banco de Dados
        query = QtSql.QSqlQuery()
        SQL = "SELECT * FROM encomendas_prn"
        # Executa a Seleção
        query.exec_(SQL)
        print("Registros:" + str(query.size()))
        # Se encontrou algo
        if query.size() <= len(Posicoes):
            ct = 0
            while query.next():
                print('Posicao Enviada ' + str(Posicoes[ct]))
                self.desenha_etiqueta(Posicoes[ct]-1,query.record())
                ct += 1
                if ct > 3 :
                    # Fecha a primeira página
                    self.c.showPage()
                    # Atualiza o número da página
                    self.pagina += 1
                    ct = 0
        else:
            print("O número de etiquetas é diferente do número de posiçoes selecionados")
        self.c.showPage()
        self.c.save()

    def monta_pagina(self):
        self.c.setPageSize(portrait(LETTER))
        ct = 0
        # Recupera as etiquetas selecionadas no Banco de Dados
        query = QtSql.QSqlQuery()
        SQL = "SELECT * FROM encomendas_prn"
        # Executa a Seleção
        query.exec_(SQL)
        # Se encontrou algo
        if query.size() > 0:
            ct = 0
            while query.next():
                print(query.record())
                self.desenha_etiqueta(ct, query.record())
                ct += 1
                if ct > 3 :
                    # Fecha a primeira página
                    self.c.showPage()
                    # Atualiza o número da página
                    self.pagina += 1
                    ct = 0
        else:
            pass
        self.c.showPage()
        self.c.save()

    def desenha_etiqueta(self, Num, Data):
        self.c.setStrokeColor(black)
        self.c.setLineWidth(0.5)
        # Compensa a numeração porque os vetores começam em 0
        num = Num-1
        print("Num recebido (-1): " + str(num))
        # Moldura
        self.c.rect(self.Eti_XI[num],self.Eti_YI[num],self.Eti_XF[num]-self.Eti_XI[num],self.Eti_YF[num]-self.Eti_YI[num], fill=0)
        # Tarjas Pretas
        self.c.rect(self.Eti_XI[num], self.Eti_YI[num]-(5*mm), self.Eti_XF[num] - self.Eti_XI[num],
                    5 * mm, fill=1)
        self.c.rect(self.Eti_XI[num], self.Eti_YI[num] - (34 * mm), self.Eti_XF[num] - self.Eti_XI[num],
                    5 * mm, fill=1)
        # Titulos das Sessões em Branco
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setStrokeColor(white)
        self.c.setFillColor(white)
        self.c.drawCentredString(self.Eti_XI[num]+int((self.Eti_XF[num]-self.Eti_XI[num])/2),self.Eti_YI[num]-(4.3 * mm),"OBJETO")
        self.c.drawCentredString(self.Eti_XI[num]+int((self.Eti_XF[num]-self.Eti_XI[num])/2),self.Eti_YI[num]-(33 * mm),"DESTINO")
        self.c.setFont("Helvetica",8)
        self.c.setFillColor(black)
        self.c.setStrokeColor(black)
        # Linhas de Grade
        lin = self.Eti_YI[num] - (19*mm)
        self.c.line(self.Eti_XI[num],lin,self.Eti_XF[num],lin)
        lin = self.Eti_YI[num] - (75 * mm)
        self.c.line(self.Eti_XI[num], lin, self.Eti_XF[num], lin)
        lin = self.Eti_YI[num] - (101 * mm)
        self.c.line(self.Eti_XI[num], lin, self.Eti_XF[num], lin)
        col = self.Eti_XI[num] + (26.6 * mm)
        y1 = self.Eti_YI[num] - (19*mm)
        y2 = self.Eti_YI[num] - (29*mm)
        self.c.line(col, y1, col, y2)
        col = self.Eti_XI[num] + (53.2 * mm)
        self.c.line(col, y1, col, y2)
        col = self.Eti_XI[num] + (79.8 * mm)
        self.c.line(col, y1, col, y2)
        # Posições
        col1 = self.Eti_XI[num] + (2 * mm)
        col2 = self.Eti_XI[num] + (27.6 * mm)
        col3 = self.Eti_XI[num] + (54.2 * mm)
        col4 = self.Eti_XI[num] + (80.8 * mm)
        lin = self.Eti_YI[num] - (9 * mm)
        self.c.drawString(col1, lin, "NFe:")
        self.c.drawString(self.Eti_XI[num] + (56 * mm), lin, "Volume:")
        lin = self.Eti_YI[num] - (21.5 * mm)
        self.c.drawString(col1,lin , "Largura")
        self.c.drawString(col2, lin, "Comprimento")
        self.c.drawString(col3, lin, "Altura")
        self.c.drawString(col4, lin, "Peso")
        lin = self.Eti_YI[num] - (37.5 * mm)
        self.c.drawString(col1, lin, "Nome:")
        lin = self.Eti_YI[num] - (47.5 * mm)
        self.c.drawString(col1, lin, "Endereço:")
        lin = self.Eti_YI[num] - (57.5 * mm)
        self.c.drawString(col1, lin, "Cidade:")
        self.c.drawString(col3, lin, "Estado:")
        lin = self.Eti_YI[num] - (67.5 * mm)
        self.c.drawString(col1, lin, "País:")
        lin = self.Eti_YI[num] - (78.5 * mm)
        self.c.drawString(col1, lin, "CEP:")
        # Variáveis de Dados
        varCEP = str(Data.field("CEP").value()).replace("-","").replace(".","")
        varNFe = Data.field("Documento").value()
        varVol = str(Data.field("num_volume").value()).zfill(3) + "/" + str(Data.field("Volumes").value()).zfill(3)
        varNome = Data.field("Nome").value().upper()
        varEnder = Data.field("Endereco").value()
        varCidade = Data.field("Cidade").value().upper()
        varUF = Data.field("Estado").value()
        varPais = Data.field("Pais").value()
        varLarg = str(int(Data.field("L").value()*100)) + " cm"
        varComp = str(int(Data.field("P").value()*100)) + " cm"
        varAltura = str(int(Data.field("A").value()*100)) + " cm"
        varPeso = locale.format_string('%.3f',Data.field("Peso").value()) + " kg"
        # Código de Barras
        fonte = os.path.join(os.path.dirname(__file__),"Arial.ttf")
        print(fonte)
        Codigo = barcode.get("Code128",varCEP,writer=ImageWriter())
        options = dict(text_distance=4,font_size=10,font_path=fonte,module_height=11)
        dir_base = os.path.join(getPastaPrincipal(), "tmp")
        arq = Codigo.save(os.path.join(dir_base, str(varCEP)), options)
        CodigoBarras = os.path.join(dir_base, arq)
        self.c.drawImage(CodigoBarras, self.Eti_XI[num] + (18 * mm), self.Eti_YI[num] - (99 * mm),height=(20*mm), width=(65*mm), preserveAspectRatio=False)
        # Campos de Dados
        lin = self.Eti_YI[num] - (16.5 * mm)
        self.c.setFont("Helvetica-Bold",18)
        self.c.drawString(col1,lin,varNFe)
        self.c.drawString(self.Eti_XI[num] + (56 * mm), lin,varVol)
        self.c.setFont("Helvetica",11)
        lin = self.Eti_YI[num] - (26.6 * mm)
        self.c.drawString(col1, lin, varLarg)
        self.c.drawString(col2, lin, varComp)
        self.c.drawString(col3, lin, varAltura)
        self.c.drawString(col4, lin, varPeso)
        self.c.setFont("Helvetica-Bold",12)
        lin = self.Eti_YI[num] - (42.5 * mm)
        self.c.drawString(col1, lin, varNome.upper())
        self.c.setFont("Helvetica",11)
        lin = self.Eti_YI[num] - (52.5 * mm)
        self.c.drawString(col1, lin, varEnder)
        lin = self.Eti_YI[num] - (62.5 * mm)
        self.c.drawString(col1, lin, varCidade.upper())
        self.c.drawString(col3, lin, varUF.upper())
        lin = self.Eti_YI[num] - (72 * mm)
        self.c.drawString(col1, lin, varPais)
        # Dados Clona-Gen
        self.c.setFont("Helvetica-Bold", 10.5)
        self.c.setStrokeColor(black)
        col = self.Eti_XI[num] + (26 * mm)
        lin = self.Eti_YI[num] - (109 * mm)
        fileLogo = os.path.join(os.path.dirname(__file__), "logo.jpg")
        self.c.drawImage(fileLogo, self.Eti_XI[num] - (10 * mm), lin - (14 * mm), height=51, preserveAspectRatio=True)
        self.c.drawString(col, lin, "Clona-Gen Com. de Mds de Plantas Ltda.")
        self.c.setFont("Helvetica", 10.5)
        lin -= (4 * mm)
        self.c.drawString(col, lin, "Rua Ottokar Doerffel, 534")
        lin -= (4 * mm)
        self.c.drawString(col, lin, "89203-001   JOINVILLE-SC")
        lin -= (4 * mm)
        self.c.drawString(col, lin, "Tel: (47) 3439-6607")
        lin -= (4 * mm)
        self.c.drawString(col, lin, "WhatsApp: (47) 99784-4023")
        lin -= (4 * mm)
        self.c.drawString(col, lin, "www.clona-gen.com.br")
        lin -= (4 * mm)
        self.c.drawString(col, lin, "comercial@clona-gen.com.br")

if __name__ == '__main__':
    print('Instanciando objeto')
    RPT = rptEtiquetas_Caixas()
    print("cria relatorio")
    RPT.monta_pagina()
    os.system('xdg-open ' + RPT.arquivo)