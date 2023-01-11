
DEVICE = "/dev/ttyUSB0"
STX = chr(2)
CR = chr(13)
LF = chr(10)

class Etiquetas(object):
    def __init__(self):
        self.device = open(DEVICE, "w")

    def send_raw(self, dado):
        self.device.write(dado + CR)
        self.device.flush()

    def abre_etiqueta(self):
        self.send_raw(STX+'n')
        self.send_raw(STX +'M0500')
        self.send_raw(STX+'O0220')
        self.send_raw(STX+'V0')
        self.send_raw(STX+'f220')
        self.send_raw(STX+'D')
        self.send_raw(STX+'L')
        self.send_raw(STX+'D11')
        self.send_raw(STX+'A2')
        self.send_raw('1922A1200310010BRS - 396')
        self.send_raw('1922A1200310181BRS - 396')
        self.send_raw('Q0001')
        self.send_raw('E')

    def close(self):
        self.device.close()

if __name__ == "__main__":
    print('Testando Etiquetas')
    Ser = Etiquetas()
    print('Enviando comando para impressora')
    Ser.abre_etiqueta()
    print('Fechando impressora...')
    Ser.close()