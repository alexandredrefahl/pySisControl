import locale
import requests

from PyQt5 import QtWidgets
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery


def MessageBox(Mensagem, Titulo, Informacoes):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(Mensagem)
    msg.setInformativeText(Informacoes)
    msg.setWindowTitle(Titulo)
    retval = msg.exec_()
    # msg.setDetailedText(Detalhes)

def DLookUp(tabela,condicao):
    query = QSqlQuery()
    try :
        query.exec("SELECT * FROM " + tabela + " WHERE " + condicao)
        return query
    except:
        print("Erro ao tentar resgatar dados no banco de dados")
        return -1

def calculaSEDEX(cepOri="",cepDest="",Dimensoes=[],peso=0):
    url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
    print("Peso: ", str(peso))
    varAltura = Dimensoes[0]
    varLargura = Dimensoes[1]
    varComprimento = Dimensoes[2]
    parametros = {'sCepOrigem' : cepOri,
                  'sCepDestino' : cepDest,
                  'nVlPeso' : peso,
                  'nCdFormato' : 1,
                  'nVlComprimento' : varComprimento,
                  'nVlAltura' : varAltura,
                  'nVlLargura' : varLargura,
                  'sCdMaoPropria' : 'N',
                  'nVlValorDeclarado' : 0,
                  'sCdAvisoRecebimento' : 'N',
                  'nCdServico' : 40010,
                  'nVlDiametro' : 0,
                  'StrRetorno' : 'xml'}
    r = requests.get(url, params=parametros)
    if r.status_code == 200:
        from xml.etree.ElementTree import XML, fromstring
        myxml = fromstring(r.text)
        preco = locale.atof(myxml[0][1].text)
        print(f'O valor do SEDEX é de {preco}')
        prazo = locale.atoi(myxml[0][2].text)
        print(f'O prazo de entrega é de {prazo} dias')
        return preco,prazo
    return 0,0
def getPastaPrincipal():
    from pathlib import Path
    ROOT_DIR = Path(__file__).parent.parent
    return ROOT_DIR
