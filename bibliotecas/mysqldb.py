# Biblioteca para conexão mysql
import subprocess
import platform
from PyQt5 import QtSql

curHost = '10.1.1.254'
host = '10.1.1.254'
remo = '187.59.80.163'
user = 'alexandre'
pasw = '@drf1624'
database = 'controle'
port = 3306

def getHost():
    return curHost

def getUser():
    return user

def getPasw():
    return pasw

def getDatabase():
    return database

def getPort():
    return port

def conecta_MySql() -> object:
    db1 = QtSql.QSqlDatabase().addDatabase('QMYSQL')
    # Seleção automática via Ping de qual endereço vai usar Local ou Remoto
    # Tenta o local primeiro porque quando for remoto ele não vai retornar
    #if ping_ip(host):
    #    db.setHostName(host)
    #    curHost = host
    #elif ping_ip(remo):
    #db.setHostName(remo)
    #curHost = remo
    db1.setHostName(host)
    curHost = host
    db1.setPort(port)
    db1.setDatabaseName(database)
    db1.setUserName(user)
    db1.setPassword(pasw)
    if db1.open():
        print('Servidor MySQL conectado em: ',curHost)
        return db1
    else:
        print("Erro ao conectar ao servidor MySQL: ", db1.lastError().text())

def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
        return False
