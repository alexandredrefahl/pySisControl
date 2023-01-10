from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

class ModTableWidget(QtWidgets.QTableWidget):
    mudancaContagemLinhas = pyqtSignal()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            row = self.currentRow()
            self.removeRow(row)
            self.mudancaContagemLinhas.emit()
        else:
            super().keyPressEvent(event)