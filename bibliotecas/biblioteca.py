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