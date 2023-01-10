import xlsxwriter
import os
from datetime import datetime
import bibliotecas.mysqldb
from PyQt5 import QtSql

class xlsPlanilha_Reservas:

    def __init__(self, dataINI="", dataFIM="", ordem="Data", criterio="Cadastro"):
        self.dataINI = dataINI
        self.dataFIM = dataFIM
        self.Ordem = ordem
        self.Criterio = criterio
        # Cria o canvas para produção do relatório
        self.arquivo = os.path.join(os.path.dirname(__file__),"xlsxPlanilha_Reservas-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.xlsx')
        self.db = bibliotecas.mysqldb.conecta_MySql()
        self.row=0
        self.col=0

    def define_formatos(self):
        # Formatação TITULO DO RELATORIO
        self.fmtTituloGeral = self.workbook.add_format({'bold':True})
        self.fmtTituloGeral.set_font_size(14)
        self.fmtTituloGeral.set_align('center')
        self.fmtTituloGeral.set_align('vcenter')
        # Formatação para os TITULOS das Colunas
        self.fmtTitulo = self.workbook.add_format({'bold':True})
        self.fmtTitulo.set_bg_color('#125409')
        self.fmtTitulo.set_font_color('#FFFFFF')
        self.fmtTitulo.set_font_size(8)
        self.fmtTitulo.set_align('center')
        self.fmtTitulo.set_align('vcenter')
        self.fmtTitulo.set_border(1)
        # Formatação DATAS
        self.fmtData = self.workbook.add_format({'num_format':'dd/mm/yyyy'})
        self.fmtData.set_font_size(8)
        self.fmtData.set_align('center')
        self.fmtData.set_align('vcenter')
        self.fmtData.set_border(1)
        # Formatação MUDAS
        self.fmtMudas = self.workbook.add_format({'num_format':'0'})
        self.fmtMudas.set_font_size(8)
        self.fmtMudas.set_align('center')
        self.fmtMudas.set_align('vcenter')
        self.fmtMudas.set_border(1)
        # Formatação ID
        self.fmtID = self.workbook.add_format({'num_format':'0000'})
        self.fmtID.set_font_size(8)
        self.fmtID.set_align('center')
        self.fmtID.set_align('vcenter')
        self.fmtID.set_border(1)
        # Formatação Nome
        self.fmtNome = self.workbook.add_format()
        self.fmtNome.set_font_size(8)
        self.fmtNome.set_align('vcenter')
        self.fmtNome.set_border(1)

    def monta_planilha(self):
        # Create a workbook and add a worksheet.
        self.workbook = xlsxwriter.Workbook(self.arquivo)
        self.ws = self.workbook.add_worksheet()
        self.define_formatos()
        self.monta_cabecalho()
        self.preenche_dados()
        self.workbook.close()

    def monta_cabecalho(self):
        # Define as colunas da tabela
        self.titulos = ['Data', 'NºRes', 'Cliente', '396', '397', '398', '399', '400', '401', '429', '417', '418', '419',
                        '420', 'CS', 'Ame', 'Beau', 'Rub', 'Anbé', 'Cot','Nut', 'Aju', 'Per', 'Fant', 'Imp', 'Vit', 'ASA',
                        'Aca', 'Rub', 'Cat', 'Mds', 'Produção']
        # Define a largura da coluna das quantidades
        w = 3.6
        self.larguras = [8,4.5,28,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,5,5]
        col = 0
        # Coloca os títulos nas colunas
        for tit in self.titulos:
            self.ws.write_string(2,col,tit,self.fmtTitulo)
            self.ws.set_column(col,col, self.larguras[col])
            col+=1
        # Merge cells dos cabecalhos
        self.ws.merge_range('D2:O2', 'Merged Range')
        self.ws.write_string('D2','Mandioca',self.fmtTitulo)
        self.ws.merge_range('P2:U2', 'Merged Range')
        self.ws.write_string('P2', 'Batata-Doce',self.fmtTitulo)
        self.ws.merge_range('V2:Z2', 'Merged Range')
        self.ws.write_string('V2', 'Abacaxi',self.fmtTitulo)
        self.ws.merge_range('AA2:AD2', 'Merged Range')
        self.ws.write_string('AA2', 'Batata-Salsa',self.fmtTitulo)
        # Titulo Geral
        self.ws.merge_range('A1:AF1', 'Merged Range')
        self.ws.write_string('A1', "Lista de Reservas de " + self.dataINI + " até " + self.dataFIM, self.fmtTituloGeral)

    def preenche_dados(self):
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
        print('Is Valid query:',is_valid_query)
        if is_valid_query:
            print("Query validada: ", SQL)
            lin = 3
            if query.exec_():
                while query.next():
                ### Aqui escreve a linha padrão ###
                    print('Data:',query.value(1))
                    varData = query.value(10).toPyDate()
                    self.ws.write_datetime(lin, 0, varData, self.fmtData)       # Prazo de entrega
                    self.ws.write_number(lin, 1, query.value(0), self.fmtID)    # Número da Reserva
                    self.ws.write_string(lin, 2, query.value(2) + ' [' + query.value(3)[-4:] +  ']', self.fmtNome)    # Nome do cliente
                    col = 3
                    # Looping para variedades de MANDIOCA
                    for i in range(17, 29):                                      # Colunas das mandiocas
                        if query.value(i) > 0:
                            self.ws.write_number(lin, col, query.value(i), self.fmtMudas)
                        else:
                            self.ws.write_string(lin, col, '', self.fmtMudas)
                        col = col + 1
                    print(col)
                    # Looping para variedades de BATATA-DOCE
                    #col=14
                    for i in range(29,35):                                      # Colunas Batata-doce
                        if query.value(i) > 0:
                            self.ws.write_number(lin, col, query.value(i), self.fmtMudas)
                        else:
                            self.ws.write_string(lin, col, '', self.fmtMudas)
                        col = col + 1
                    # Looping para variedades de ABACAXI
                    #col = 17
                    # Colunas Abacaxis
                    for i in range(12,17):
                        if query.value(i) > 0:
                            self.ws.write_number(lin, col, query.value(i), self.fmtMudas)
                        else:
                            self.ws.write_string(lin, col, '', self.fmtMudas)
                        col = col + 1
                    #col = 22
                    # Looping para Variedade de BATATA-SALSA
                    # Colunas Batata-Salsa
                    for i in range(36,40):
                        if query.value(i) > 0:
                            self.ws.write_number(lin, col, query.value(i), self.fmtMudas)
                        else:
                            self.ws.write_string(lin, col, '', self.fmtMudas)
                        col = col + 1
                    # FORMULAS FINAIS
                    # O último parâmetro em branco na fórmula força o recálculo (não sei porque, mas funciona)
                    self.ws.write_formula('AE' + str(lin+1), '=SUM(D' + str(lin+1) + ':Z' + str(lin+1) + ')', self.fmtMudas,'')
                    self.ws.write_formula('AF' + str(lin+1), '=A' + str(lin+1) + '-120', self.fmtData,'')
                    lin = lin + 1
                    print(lin)


if __name__ == '__main__':
    #print('Instanciando objeto')
    ODF = xlsPlanilha_Reservas(ordem="Prazo",criterio="Prazo", dataINI="2021-08-01", dataFIM="2022-09-30")
    ODF.monta_planilha()
    if os.name=='posix':
        os.system('xdg-open ' + ODF.arquivo)
   
