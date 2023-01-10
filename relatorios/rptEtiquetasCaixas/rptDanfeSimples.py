from PyQt5 import QtSql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER, portrait
from reportlab.lib.colors import  black
from reportlab.lib.units import  mm
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime
from bibliotecas.mysqldb import conecta_MySql

class rptDanfe_Simples:
    def __init__(self):
        # Cria o canvas para produção do relatório
        self.arquivo = os.path.join(os.path.dirname(__file__),"rptDanfeSimplificado-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.pdf')
        self.c = canvas.Canvas(self.arquivo)
        self.pagina = 1
        #self.dbLabel = bibliotecas.mysql.conecta_MySql()
        # Limites das Etiquetas (Papel PIMACO 6288)
        self.Eti_XI = [109 * mm,   1 * mm, 109 * mm,   1 * mm]
        self.Eti_YI = [277.5 * mm, 139.5 * mm, 139.5 * mm, 277.5 * mm]
        self.Eti_XF = [215 * mm, 109 * mm, 215 * mm, 109 * mm]
        self.Eti_YF = [141 * mm,   1 * mm,   1 * mm, 141 * mm]
        self.Dados = conecta_MySql()

    def monta_pagina(self,IDs):
        self.c.setPageSize(portrait(LETTER))
        ct = 0
        # Recupera as etiquetas selecionadas no Banco de Dados
        query = QtSql.QSqlQuery(self.Dados)
        SQL = "SELECT * FROM docs WHERE id IN(" + IDs + ")"
        # Executa a Seleção
        query.exec_(SQL)
        # Se encontrou algo
        if query.size() > 0:
            ct = 0
            while query.next():
                print(query.record())
                self.desenha_etiqueta(ct,query.record())
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
        # Para Simplificar a nomenclatura das variáveis
        XI = self.Eti_XI[num]
        XF = self.Eti_XF[num]
        YI = self.Eti_YI[num]
        YF = self.Eti_YF[num]
        XC = XI + int((XF - XI) / 2)     # X do centro da etiqueta
        Tam_Tit_Sessao = 7
        # Moldura
        self.c.rect(XI,YI,XF-XI,YF-YI, fill=0)

        # Moldura da Danfe
        self.c.rect(XI + (6 * mm), YI - (9 * mm), XF - XI - (12 * mm),YF - YI + ( 15 * mm) , fill=0)
        # Linha pontilhada no inicio
        self.c.setDash(6, 4)
        self.c.line(XI + (6* mm), YI - (6 * mm), XF - (6 * mm), YI - (6 * mm))
        # Desliga a linha pontilhada
        self.c.setDash(1,0)
        # Desenha as várias linhas de divisória horizontal de acordo com as sessões
        lins = [16,36,44,65,72,85,93,112,117]
        for i in lins:
            self.c.line(XI + (6 * mm), YI - (i * mm), XF - (6 * mm),
                        YI - (i * mm))
        # Titulo Geral
        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawCentredString(XC,YI - (14 * mm), "DANFE Simplificado - Etiqueta")

        # Sessão 01 - Chave de acesso
        varchNFe = str(Data.field("chNFE").value())
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        self.c.drawString(XI +(8*mm),YI - (19 * mm) , "CHAVE DE ACESSO")
        self.c.drawCentredString(XC,YI - (34 * mm),varchNFe)
        Codigo = barcode.get("Code128", Data.field("chNFE").value() , writer=ImageWriter())
        options = {"write_text": False}
        arq = Codigo.save(os.path.join(os.path.dirname(__file__), varchNFe), options)
        CodigoBarras = os.path.join(os.path.dirname(__file__), arq)
        self.c.drawImage(CodigoBarras, XI + (13 * mm), YI - (32 * mm), height=(11 * mm),
                         width=(80 * mm), preserveAspectRatio=False)

        # Sessão 02 - Protocolo der Autorização
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        self.c.drawString(XI +(8*mm),YI - (38.5 * mm) , "PROTOCOLO DE AUTORIZAÇÃO DA NF-E")
        varProt = str(Data.field("procNFe").value())
        varData = Data.field("DataNFe").value()
        varData = varData.toPyDate()
        varData = str(varData)
        varHora = str(Data.field("HoraNFE").value())
        self.c.drawString(XI + (8 * mm), YI - (42.5 * mm), varProt)
        self.c.drawString(XI + (38 * mm), YI - (42.5 * mm), varData + "T" + varHora + "-2")

        # Sessão 03 - Remetente
        lin = YI - (48 * mm)
        alt_lin = 3.1
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(XI + (24 * mm), lin, "CLONA-GEN BIOTECNOLOGIA VEGETAL")
        self.c.setFont("Helvetica", 7.5)
        self.c.drawString(XI + (24 * mm), lin - (alt_lin * 1 * mm), "CNPJ: 07.727.715/0001-90")
        self.c.drawString(XI + (24 * mm), lin - (alt_lin * 2 * mm), "IE:   255097050")
        self.c.drawString(XI + (24 * mm), lin - (alt_lin * 3 * mm), "RUA OTTOKAR DOERFFEL, 534")
        self.c.drawString(XI + (24 * mm), lin - (alt_lin * 4 * mm), "ATIRADORES")
        self.c.drawString(XI + (24 * mm), lin - (alt_lin * 5 * mm), "89203-001      JOINVILLE-SC")
        # Logotipo
        fileLogo = os.path.join(os.path.dirname(__file__), "logo.jpg")
        self.c.drawImage(fileLogo, XI - (9 * mm), YI - (62 * mm), height=40, preserveAspectRatio=True)

        # Sessão 04 Dados da NFe
        varNumNFe = str(Data.field("Documento").value())
        varSerie = str(Data.field("Serie").value())
        varTipo = str(Data.field("Tipo").value())
        varDataNFe = Data.field("Data").value()
        varDataNFe = varDataNFe.toString("dd/MM/yyyy")
        # Número e Série
        self.c.setFont("Helvetica-Bold", 8.5)
        self.c.drawString(XI + (8 * mm), YI - (68 * mm), "Nº " + varNumNFe)
        self.c.setFont("Helvetica-Bold", 6.5)
        self.c.drawString(XI + (8 * mm), YI - (71 * mm), "SÉRIE: " + varSerie)
        # Entrada ou Saida
        self.c.setFont("Helvetica", 5)
        self.c.drawString(XI + (37 * mm), YI - (67.5 * mm), "0 - Entrada")
        self.c.drawString(XI + (37 * mm), YI - (70.5 * mm), "1 - Saída")
        self.c.rect(XI + (51 * mm), YI - (71 * mm), (7 * mm), (5 * mm), fill=0)
        self.c.line(XI + (60 * mm),YI - (65*mm),XI + (60 * mm),YI - (72*mm))
        self.c.setFont("Helvetica-Bold", 9)
        self.c.drawString(XI + (53.5 * mm), YI - (69.5 * mm), varTipo)
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        self.c.drawString(XI + (63 * mm), YI - (68 * mm), "DATA DA EMISSAO")
        self.c.drawString(XI + (63 * mm), YI - (71 * mm), varDataNFe)

        # Sessão 05 DESTINATARIO
        self.c.setFont("Helvetica-Bold", 8.5)
        self.c.drawCentredString(XC,YI - (75 * mm),"DESTINATÁRIO/REMETENTE")
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        self.c.drawString(XI + (8 * mm), YI - (79.5 * mm), "NOME/RAZÃO SOCIAL")
        self.c.drawString(XI + (8 * mm), YI - (87.5 * mm), "CPF/CNPJ")
        self.c.drawString(XI + (45 * mm), YI - (87.5 * mm), "INSCRIÇÃO ESTADUAL")
        self.c.drawString(XI + (89 * mm), YI - (87.5 * mm), "UF")
        self.c.line(XI + (44 * mm), YI - (85 * mm), XI + (44 * mm), YI - (93 * mm))
        self.c.line(XI + (88 * mm), YI - (85 * mm), XI + (88 * mm), YI - (93 * mm))
        varNome = Data.field("Cliente").value()
        varCpfCnpj = str(Data.field("CNPJ_CPF").value())
        varIE = Data.field("Inscricao").value()
        varUF = Data.field("Estado").value()
        self.c.setFont("Helvetica", 8.5)
        self.c.drawString(XI + (8 * mm), YI - (83.5 * mm), varNome.upper())
        varCpfCnpj = str(varCpfCnpj)
        if len(varCpfCnpj) == 11:
            varCpf = '{}.{}.{}-{}'.format(varCpfCnpj[:3], varCpfCnpj[3:6], varCpfCnpj[6:9], varCpfCnpj[9:])
            self.c.drawString(XI + (8 * mm), YI - (91.5 * mm), varCpf)
        elif len(varCpfCnpj) == 14:
            varCNPJ = "{}.{}.{}/{}-{}".format(varCpfCnpj[:2],varCpfCnpj[2:5],varCpfCnpj[5:8],varCpfCnpj[8:12],varCpfCnpj[12:])
            self.c.drawString(XI + (8 * mm), YI - (91.5 * mm), varCNPJ)
        self.c.drawString(XI + (45 * mm), YI - (91.5 * mm), varIE)
        self.c.drawString(XI + (89 * mm), YI - (91.5 * mm), varUF.upper())

        # Sessão 06 ENDEREÇO DESTINO
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        lin = (99.5 * mm)
        alt_lin = 3.5
        if len(Data.field("entregaLgr").value()) > 2:
            # Tem endereço de entrega
            self.c.drawString(XI + (8 * mm),YI - (95.5 * mm),'ENDEREÇO DE ENTREGA')
            varLgr = Data.field("entregaLgr").value()
            varNro = Data.field("entregaNro").value()
            varCpl = Data.field("entregaCpl").value()
            varBairro = Data.field("entregaBairro").value()
            varCEP = Data.field("entregaCEP").value()
            varCEP = varCEP.replace("-", "").replace(".", "")
            varCEP = "{}-{}".format(varCEP[:5], varCEP[5:])
            varCidade = Data.field("entregaxMun").value()
            varUF = Data.field("entregaUF").value()
            varFone = Data.field("entregaFone").value()
            self.c.setFont("Helvetica", 8.5)
            self.c.drawString(XI + (8 * mm), YI - (lin), varLgr + ", " + str(varNro))
            self.c.setFont("Helvetica", Tam_Tit_Sessao)
            self.c.drawString(XI + (8 * mm), YI - (lin + 1 * alt_lin * mm), varCpl)
            self.c.drawString(XI + (45 * mm), YI - (lin + 1 * alt_lin * mm), "Bairro: " + varBairro)
            self.c.drawString(XI + (8 * mm), YI - (lin + 2 * alt_lin * mm), varCEP)
            self.c.drawString(XI + (45 * mm), YI - (lin + 2 * alt_lin * mm), varCidade + " - " + varUF)
            self.c.drawString(XI + (8 * mm), YI - (lin + 3 * alt_lin * mm), "TELEFONE: " + varFone)
        else:
            self.c.drawString(XI + (8 * mm), YI - (95.5 * mm), 'ENDEREÇO')
            varLgr = Data.field("Endereco").value()
            varNro = Data.field("Num").value()
            varCpl = Data.field("Complemento").value()
            varBairro = Data.field("Bairro").value()
            varCEP = Data.field("CEP").value()
            varCEP = varCEP.replace("-","").replace(".","")
            varCEP = "{}-{}".format(varCEP[:5],varCEP[5:])
            varCidade = Data.field("Cidade").value()
            varUF = Data.field("Estado").value()
            varFone = Data.field("Fone").value()
            self.c.setFont("Helvetica", 8.5)
            self.c.drawString(XI + (8 * mm), YI - (lin), varLgr + ", " + str(varNro))
            self.c.setFont("Helvetica", Tam_Tit_Sessao)
            self.c.drawString(XI + (8 * mm), YI - (lin + (1 * alt_lin * mm)), varCpl)
            self.c.drawString(XI + (45 * mm), YI - (lin + (1 * alt_lin * mm)), "Bairro: " + varBairro)
            self.c.drawString(XI + (8 * mm), YI - (lin + (2 * alt_lin * mm)), varCEP)
            self.c.drawString(XI + (45 * mm), YI - (lin + (2 * alt_lin * mm)), varCidade + " - " + varUF)
            self.c.drawString(XI + (8 * mm), YI - (lin + (3 * alt_lin * mm)), "TELEFONE: " + varFone)

        # Sessão 07 VALOR TOTAL
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        self.c.drawString(XI+(8*mm),YI - (115.5 * mm),"VALOR TOTAL:")
        self.c.setFont("Helvetica", 8.5)
        varTOTAL = Data.field("vTotal").value()
        self.c.drawString(XI + (32 * mm), YI - (115.5 * mm), f'{varTOTAL:.2f}'.replace(".",","))

        # Sessão 08 TRANSPORTADORA/VOLUME
        self.c.setFont("Helvetica", Tam_Tit_Sessao)
        varTransporte = Data.field("Transportadora").value()
        varVolumes = Data.field("traNumeracao").value()
        self.c.drawString(XI + (8 * mm), YI - (120.5 * mm), "TRANSPORTADORA: ")
        self.c.drawString(XI + (8 * mm), YI - (125.5 * mm), "VOLUMES: ")
        self.c.setFont("Helvetica", 8.5)
        self.c.drawString(XI + (35 * mm), YI - (120.5 * mm), varTransporte)
        self.c.drawString(XI + (35 * mm), YI - (125.5 * mm), varVolumes)

if __name__ == '__main__':
    print('Instanciando objeto')
    RPT = rptDanfe_Simples()
    print("cria relatorio")
    RPT.monta_pagina("1473")
    os.system('xdg-open ' + RPT.arquivo)