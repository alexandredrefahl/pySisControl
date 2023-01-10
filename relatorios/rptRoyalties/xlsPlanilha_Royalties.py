import xlsxwriter
import os
from datetime import datetime
import bibliotecas.mysqldb
from PyQt5 import QtSql
from locale import atof, setlocale, LC_ALL
setlocale(LC_ALL, 'pt_BR.UTF-8')

class xlsPlanilha_Royalties:

    def __init__(self, codPro, dataINI = "", dataFIM = ""):
        self.Produtos = codPro
        self.dataINI = dataINI
        self.dataFIM = dataFIM
        # Cria a planilha para produção do Relatório
        dir_base = os.path.dirname(os.path.abspath(__file__))
        fileName = "xlsxPlanilha_Royalties-" + datetime.today().strftime('%d-%m-%Y-%H-%M-%S') + '.xlsx'
        self.arquivo = os.path.join(dir_base,fileName)
        self.db = bibliotecas.mysqldb.conecta_MySql()
        self.row = 0
        self.col = 0

    def define_formatos(self):
        # Formatação do Relatório
        self.fmtTituloGeral = self.workbook.add_format({'bold':True})
        self.fmtTituloGeral.set_font_size(14)
        self.fmtTituloGeral.set_align('center')
        self.fmtTituloGeral.set_align('vcenter')
        # Formatação para os TITULOS das Colunas
        self.fmtTitulo = self.workbook.add_format({'bold': True})
        self.fmtTitulo.set_bg_color('#999999')      # Cinza Escuro
        self.fmtTitulo.set_font_color('#FFFFFF')    # Letra preta
        self.fmtTitulo.set_font_size(10)
        self.fmtTitulo.set_align('center')
        self.fmtTitulo.set_align('vcenter')
        self.fmtTitulo.set_border(1)
        # Formatação Num NFe
        self.fmtID = self.workbook.add_format({'num_format':'0000'})
        self.fmtID.set_font_size(10)
        self.fmtID.set_align('center')
        self.fmtID.set_align('vcenter')
        self.fmtID.set_border(1)
        # Formatação Data
        self.fmtData = self.workbook.add_format({'num_format': 'dd/mm/yyyy'})
        self.fmtData.set_font_size(10)
        self.fmtData.set_align('center')
        self.fmtData.set_align('vcenter')
        self.fmtData.set_border(1)
        # Formatação Cód Clone
        self.fmtClone = self.workbook.add_format({'num_format':'0000'})
        self.fmtClone.set_font_size(10)
        self.fmtClone.set_align('center')
        self.fmtClone.set_align('vcenter')
        self.fmtClone.set_border(1)
        # Formatação Mudas
        self.fmtMudas = self.workbook.add_format({'num_format':'0'})
        self.fmtMudas.set_font_size(10)
        self.fmtMudas.set_align('center')
        self.fmtMudas.set_align('vcenter')
        self.fmtMudas.set_border(1)
        # Formatação Valores
        self.fmtValor = self.workbook.add_format({'num_format': '0.00'})
        self.fmtValor.set_font_size(10)
        self.fmtValor.set_align('right')
        self.fmtValor.set_align('vcenter')
        self.fmtValor.set_border(1)

    def monta_planilha(self):
        # Cria o Workbook e adiciona as WorkSheet
        self.workbook = xlsxwriter.Workbook(self.arquivo)
        self.define_formatos()
        # cria uma aba para cada clone que vai ser resumido
        for cultivar in self.Produtos:
            cod,clone = cultivar.split(".")
            self.ws = self.workbook.add_worksheet(cultivar)
            # Coloca o título daquela planilha
            self.ws.merge_range('A1:H1', 'Merged Range')
            self.ws.write_string('A1',cod + "." + clone + ' de ' + self.dataINI + " até " + self.dataFIM, self.fmtTitulo)
            # Monta a linha de cabecalho da tabela
            self.monta_cabecalho()
            self.preenche_dados(cod,clone)
        # Finaliza a planilha
        self.workbook.close()

    def monta_cabecalho(self):
        self.titulos = ["NFe", "Data", "Cód", "Clone", "Qtde", "Unit", "Total", "Royalties"]
        self.larguras = [9,9,5,5,6,6,6,8]
        col = 0
        lin = 2
        # Coloca os títulos nas colunas
        for tit in self.titulos:
            self.ws.write_string(lin, col, tit, self.fmtTitulo)
            self.ws.set_column(col, col, self.larguras[col])
            col += 1

    def preenche_dados(self,cod,clone):
        query = QtSql.QSqlQuery(self.db)
        # monta a SQL Base
        SQL = "select docs.Documento,docs.Data,docs_itens.CodPro,docs_itens.Clone,docs_itens.quantidade,docs_itens.unitario,docs_itens.total from docs_itens inner join docs on docs_itens.Doc_ID=docs.id where docs_itens.CodPro=" + cod + " and docs_itens.Clone=" + clone + " and (docs.Data between '" + self.dataINI + "' and '" + self.dataFIM + "')"
        is_valid_query = query.prepare(SQL)
        if is_valid_query:
            lin=3
            if query.exec_():
                while query.next():
                    ### Aqui escreve a linha padrão ###
                    varNFe = query.value(0)
                    varData = query.value(1).toPyDate()
                    varCod = query.value(2)
                    varClone = query.value(3)
                    varQtde = query.value(4)
                    varUnit = query.value(5)
                    varTotal = query.value(6)
                    varRoyalt = varTotal * 0.07
                    # Coloca os valores na planilha efetivamente
                    self.ws.write_string(lin, 0, varNFe, self.fmtID)       # Número a NFe
                    self.ws.write_datetime(lin, 1, varData, self.fmtData)  # Data da nota
                    self.ws.write_string(lin, 2, str(varCod), self.fmtID)
                    self.ws.write_string(lin, 3, str(varClone), self.fmtClone)
                    self.ws.write_number(lin, 4, varQtde, self.fmtMudas)
                    self.ws.write_number(lin, 5, varUnit, self.fmtValor)
                    self.ws.write_number(lin, 6, varTotal, self.fmtValor)
                    self.ws.write_number(lin, 7, varRoyalt, self.fmtValor)
                    lin = lin + 1
                # Final totaliza a coluna de Mudas, Valor e Royalties
                self.ws.write_formula('E' + str(lin + 1), '=SUM(E4:E' + str(lin) + ')', self.fmtMudas, '')
                self.ws.write_formula('G' + str(lin + 1), '=SUM(G4:G' + str(lin) + ')', self.fmtValor, '')
                self.ws.write_formula('H' + str(lin + 1), '=SUM(H4:H' + str(lin) + ')', self.fmtValor, '')

if __name__ == '__main__':
    #print('Instanciando objeto')
    cods = ["45.396","45.397","45.398","45.399","45.400","45.401"]
    ODF = xlsPlanilha_Royalties(cods, dataINI="2021-12-06", dataFIM="2022-12-05")
    ODF.monta_planilha()
    if os.name=='posix':
        os.system('xdg-open ' + ODF.arquivo)