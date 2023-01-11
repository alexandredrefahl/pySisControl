import sys

DEVICE = "/dev/ttyUSB0"
STX = chr(2)
CR  = chr(13)
LF  = chr(10)

class Etiqueta(object):
    def __init__(self, test=False):
        self.lines  = []
        self.test   = test
        if not self.test:
            self.device = open(DEVICE,"w")
        self.write_line(STX+"j")              # Tira a pausa entre as etiquetas
        self.write_line(STX+"L")              # Entra no modo de formatação da etiqueta
        self.write_line("D11")                # Define o tamanho do pixel 1 x 1  no caso
        self.write_line("PC")                 # Padrão de velocidade de impressão = C = 65 mm/s
        self.write_line("H11")                # Temperatura de impressão

    def write_line(self, data):
        """
            Função que envia os dados puros para a impressora
            :data: o que será enviado
            :return: Sem retorno
        """
        if not self.test:
            self.device.write(data+CR)
            self.device.flush()
        sys.stdout.write("[IMP] "+ data+CR+LF)
        sys.stdout.flush()

    def text(self):
        linha = "1911A1800570030MACRO"
        self.write_line(linha)
        linha = "1911A1200340045Meio B5"
        self.write_line(linha)
        linha = "1911A080010000950 ml/L"
        self.write_line(linha)
        linha = "1911A080010008907/07/2020"
        self.write_line(linha)

    def envia_etiqueta_serial(self,Cod_Esq, Des_Esq, Dat_Esq, Mds_Esq, Fra_Esq, Cod_Dir, Des_Dir, Dat_Dir, Mds_Dir, Fra_Dir):
        #Etiqueta 01 (Esq)
        self.write_line("1e4202800370018C{0}&E{1}".format(Cod_Esq[:12], Cod_Esq[12:]))
        self.write_line("1911A0600260050{0}".format(Cod_Esq))
        self.write_line("1911A0600810010Lote")
        self.write_line("1911A0800690010{0}".format(Des_Esq))
        self.write_line("1911A0600100010Data:")
        self.write_line("1911A0800080033{0}".format(Dat_Esq))
        self.write_line("1911A0600100097Mudas:")
        self.write_line("1911A0800080133{0}".format(Mds_Esq))
        self.write_line("1911A0600830121Frasco")
        self.write_line("1911A0800690126{0}".Format(Fra_Esq))

        #Etiqueta 02 (Dir)
        self.write_line("1e4202800370184C{0}&E{1}".format(Cod_Dir[:12], Cod_Dir[12:]))
        self.write_line("1911A0600260216{0}".format(Cod_Dir))
        self.write_line("1911A0600810175Lote")
        self.write_line("1911A0800690175{0}".format(Des_Dir))
        self.write_line("1911A0600100175Data:")
        self.write_line("1911A0800080198{0}".format(Dat_Dir))
        self.write_line("1911A0600100263Mudas:")
        self.write_line("1911A0800080298{0}".format(Mds_Dir))
        self.write_line("1911A0600830286Frasco")
        self.write_line("1911A0800690292{0}".format(Fra_Dir))

    def fechar(self, copies = 1):
        self.write_line("Q%04d" % (int(copies),) )
        self.write_line("E")
        if not self.test:
            self.device.close()


if __name__ == '__main__':
    lbl = Etiqueta()
    #Chama a funcao para imprimir a etiqueta
    Cod_ESQ = str(364771).zfill(13)
    Des_ESQ = str(45).zfill(3) + "." + str(88).zfill(3) + "." + str(396).zfill(4)
    Dat_ESQ = "02/06/20"
    Mds_ESQ = str('10')
    Fra_ESQ = str('20')
    Cod_DIR = str(364771).zfill(13)
    Des_DIR = str(45).zfill(3) + "." + str(88).zfill(3) + "." + str(396).zfill(4)
    Dat_DIR = "02/06/20"
    Mds_DIR = str(10)
    Fra_DIR = str(21)
    lbl.envia_etiqueta_serial(Cod_ESQ, Des_ESQ, Dat_ESQ, Mds_ESQ, Fra_ESQ, Cod_DIR, Des_DIR, Dat_DIR, Mds_DIR, Fra_DIR)
    lbl.fechar()