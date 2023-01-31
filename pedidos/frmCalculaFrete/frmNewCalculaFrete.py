# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmNewCalculaFrete.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pedidos.frmReservas.clsmodTableWidget import ModTableWidget


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 530)
        Dialog.setMinimumSize(QtCore.QSize(620, 530))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(37, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txtCEP = QtWidgets.QLineEdit(Dialog)
        self.txtCEP.setMaximumSize(QtCore.QSize(107, 16777215))
        self.txtCEP.setText("")
        self.txtCEP.setMaxLength(8)
        self.txtCEP.setFrame(True)
        self.txtCEP.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCEP.setObjectName("txtCEP")
        self.horizontalLayout.addWidget(self.txtCEP)
        self.lblCidade = QtWidgets.QLabel(Dialog)
        self.lblCidade.setObjectName("lblCidade")
        self.horizontalLayout.addWidget(self.lblCidade)
        self.lblEstado = QtWidgets.QLabel(Dialog)
        self.lblEstado.setObjectName("lblEstado")
        self.horizontalLayout.addWidget(self.lblEstado)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtQtde = QtWidgets.QLineEdit(Dialog)
        self.txtQtde.setMinimumSize(QtCore.QSize(50, 0))
        self.txtQtde.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txtQtde.setAlignment(QtCore.Qt.AlignCenter)
        self.txtQtde.setObjectName("txtQtde")
        self.horizontalLayout_2.addWidget(self.txtQtde)
        self.cmbVariedade = QtWidgets.QComboBox(Dialog)
        self.cmbVariedade.setMinimumSize(QtCore.QSize(350, 0))
        self.cmbVariedade.setCurrentText("")
        self.cmbVariedade.setObjectName("cmbVariedade")
        self.horizontalLayout_2.addWidget(self.cmbVariedade)
        self.btAcrescentar = QtWidgets.QPushButton(Dialog)
        self.btAcrescentar.setMinimumSize(QtCore.QSize(100, 0))
        self.btAcrescentar.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btAcrescentar.setObjectName("btAcrescentar")
        self.horizontalLayout_2.addWidget(self.btAcrescentar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tblOrcamento = ModTableWidget(Dialog)
        self.tblOrcamento.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblOrcamento.setAutoScrollMargin(18)
        self.tblOrcamento.setColumnCount(6)
        self.tblOrcamento.setObjectName("tblOrcamento")
        self.tblOrcamento.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblOrcamento.setHorizontalHeaderItem(5, item)
        self.tblOrcamento.verticalHeader().setDefaultSectionSize(30)
        self.tblOrcamento.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout.addWidget(self.tblOrcamento)
        self.grpDados = QtWidgets.QGroupBox(Dialog)
        self.grpDados.setMinimumSize(QtCore.QSize(0, 90))
        self.grpDados.setMaximumSize(QtCore.QSize(16777215, 90))
        self.grpDados.setObjectName("grpDados")
        self.txtValFrete = QtWidgets.QLineEdit(self.grpDados)
        self.txtValFrete.setGeometry(QtCore.QRect(520, 30, 71, 25))
        self.txtValFrete.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtValFrete.setObjectName("txtValFrete")
        self.txtLarg = QtWidgets.QLineEdit(self.grpDados)
        self.txtLarg.setGeometry(QtCore.QRect(150, 30, 45, 25))
        self.txtLarg.setAlignment(QtCore.Qt.AlignCenter)
        self.txtLarg.setObjectName("txtLarg")
        self.lblPeso = QtWidgets.QLabel(self.grpDados)
        self.lblPeso.setGeometry(QtCore.QRect(410, 34, 21, 20))
        self.lblPeso.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPeso.setObjectName("lblPeso")
        self.txtAlt = QtWidgets.QLineEdit(self.grpDados)
        self.txtAlt.setGeometry(QtCore.QRect(100, 30, 45, 25))
        self.txtAlt.setAlignment(QtCore.Qt.AlignCenter)
        self.txtAlt.setObjectName("txtAlt")
        self.label_5 = QtWidgets.QLabel(self.grpDados)
        self.label_5.setGeometry(QtCore.QRect(10, 34, 80, 17))
        self.label_5.setObjectName("label_5")
        self.txtPeso = QtWidgets.QLineEdit(self.grpDados)
        self.txtPeso.setGeometry(QtCore.QRect(350, 30, 61, 25))
        self.txtPeso.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtPeso.setObjectName("txtPeso")
        self.label_6 = QtWidgets.QLabel(self.grpDados)
        self.label_6.setGeometry(QtCore.QRect(470, 34, 51, 17))
        self.label_6.setObjectName("label_6")
        self.label_2 = QtWidgets.QLabel(self.grpDados)
        self.label_2.setGeometry(QtCore.QRect(310, 34, 40, 17))
        self.label_2.setObjectName("label_2")
        self.txtProf = QtWidgets.QLineEdit(self.grpDados)
        self.txtProf.setGeometry(QtCore.QRect(200, 30, 45, 25))
        self.txtProf.setAlignment(QtCore.Qt.AlignCenter)
        self.txtProf.setObjectName("txtProf")
        self.rdJadLog = QtWidgets.QRadioButton(self.grpDados)
        self.rdJadLog.setGeometry(QtCore.QRect(11, 61, 65, 20))
        self.rdJadLog.setChecked(True)
        self.rdJadLog.setObjectName("rdJadLog")
        self.rdSEDEX = QtWidgets.QRadioButton(self.grpDados)
        self.rdSEDEX.setGeometry(QtCore.QRect(100, 61, 66, 20))
        self.rdSEDEX.setObjectName("rdSEDEX")
        self.verticalLayout.addWidget(self.grpDados)
        self.grpResumo = QtWidgets.QGroupBox(Dialog)
        self.grpResumo.setMinimumSize(QtCore.QSize(0, 80))
        self.grpResumo.setMaximumSize(QtCore.QSize(16777215, 80))
        self.grpResumo.setObjectName("grpResumo")
        self.lblPrazo = QtWidgets.QLabel(self.grpResumo)
        self.lblPrazo.setGeometry(QtCore.QRect(150, 53, 80, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblPrazo.setFont(font)
        self.lblPrazo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPrazo.setObjectName("lblPrazo")
        self.lblTotal_3 = QtWidgets.QLabel(self.grpResumo)
        self.lblTotal_3.setGeometry(QtCore.QRect(100, 53, 60, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblTotal_3.setFont(font)
        self.lblTotal_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotal_3.setObjectName("lblTotal_3")
        self.lblTotal = QtWidgets.QLabel(self.grpResumo)
        self.lblTotal.setGeometry(QtCore.QRect(500, 53, 90, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblTotal.setFont(font)
        self.lblTotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotal.setObjectName("lblTotal")
        self.lblTotal_2 = QtWidgets.QLabel(self.grpResumo)
        self.lblTotal_2.setGeometry(QtCore.QRect(430, 53, 60, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblTotal_2.setFont(font)
        self.lblTotal_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotal_2.setObjectName("lblTotal_2")
        self.lblNumMudas = QtWidgets.QLabel(self.grpResumo)
        self.lblNumMudas.setGeometry(QtCore.QRect(170, 30, 60, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblNumMudas.setFont(font)
        self.lblNumMudas.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblNumMudas.setObjectName("lblNumMudas")
        self.lblTotal_5 = QtWidgets.QLabel(self.grpResumo)
        self.lblTotal_5.setGeometry(QtCore.QRect(70, 30, 90, 17))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(9)
        font.setBold(True)
        self.lblTotal_5.setFont(font)
        self.lblTotal_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotal_5.setObjectName("lblTotal_5")
        self.lblTotal_4 = QtWidgets.QLabel(self.grpResumo)
        self.lblTotal_4.setGeometry(QtCore.QRect(430, 30, 90, 17))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(9)
        font.setBold(True)
        self.lblTotal_4.setFont(font)
        self.lblTotal_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotal_4.setObjectName("lblTotal_4")
        self.lblTotalMerc = QtWidgets.QLabel(self.grpResumo)
        self.lblTotalMerc.setGeometry(QtCore.QRect(530, 30, 60, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.lblTotalMerc.setFont(font)
        self.lblTotalMerc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblTotalMerc.setObjectName("lblTotalMerc")
        self.verticalLayout.addWidget(self.grpResumo)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chkJadLog = QtWidgets.QCheckBox(Dialog)
        self.chkJadLog.setMinimumSize(QtCore.QSize(75, 0))
        self.chkJadLog.setChecked(True)
        self.chkJadLog.setObjectName("chkJadLog")
        self.horizontalLayout_3.addWidget(self.chkJadLog)
        self.chkAzul = QtWidgets.QCheckBox(Dialog)
        self.chkAzul.setMinimumSize(QtCore.QSize(70, 0))
        self.chkAzul.setObjectName("chkAzul")
        self.horizontalLayout_3.addWidget(self.chkAzul)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btCopyMail = QtWidgets.QPushButton(Dialog)
        self.btCopyMail.setMinimumSize(QtCore.QSize(140, 0))
        self.btCopyMail.setObjectName("btCopyMail")
        self.horizontalLayout_3.addWidget(self.btCopyMail)
        self.btFrete = QtWidgets.QPushButton(Dialog)
        self.btFrete.setMinimumSize(QtCore.QSize(140, 0))
        self.btFrete.setObjectName("btFrete")
        self.horizontalLayout_3.addWidget(self.btFrete)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btSendSkype = QtWidgets.QPushButton(Dialog)
        self.btSendSkype.setObjectName("btSendSkype")
        self.horizontalLayout_5.addWidget(self.btSendSkype)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.btCopyWhats = QtWidgets.QPushButton(Dialog)
        self.btCopyWhats.setMinimumSize(QtCore.QSize(140, 0))
        self.btCopyWhats.setObjectName("btCopyWhats")
        self.horizontalLayout_5.addWidget(self.btCopyWhats)
        self.btLimpar = QtWidgets.QPushButton(Dialog)
        self.btLimpar.setMinimumSize(QtCore.QSize(140, 0))
        self.btLimpar.setObjectName("btLimpar")
        self.horizontalLayout_5.addWidget(self.btLimpar)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.txtCEP, self.txtQtde)
        Dialog.setTabOrder(self.txtQtde, self.cmbVariedade)
        Dialog.setTabOrder(self.cmbVariedade, self.btAcrescentar)
        Dialog.setTabOrder(self.btAcrescentar, self.tblOrcamento)
        Dialog.setTabOrder(self.tblOrcamento, self.txtAlt)
        Dialog.setTabOrder(self.txtAlt, self.txtLarg)
        Dialog.setTabOrder(self.txtLarg, self.txtProf)
        Dialog.setTabOrder(self.txtProf, self.txtPeso)
        Dialog.setTabOrder(self.txtPeso, self.txtValFrete)
        Dialog.setTabOrder(self.txtValFrete, self.rdJadLog)
        Dialog.setTabOrder(self.rdJadLog, self.rdSEDEX)
        Dialog.setTabOrder(self.rdSEDEX, self.btFrete)
        Dialog.setTabOrder(self.btFrete, self.chkJadLog)
        Dialog.setTabOrder(self.chkJadLog, self.chkAzul)
        Dialog.setTabOrder(self.chkAzul, self.btSendSkype)
        Dialog.setTabOrder(self.btSendSkype, self.btCopyMail)
        Dialog.setTabOrder(self.btCopyMail, self.btCopyWhats)
        Dialog.setTabOrder(self.btCopyWhats, self.btLimpar)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Cálculo de Orçamento"))
        self.label.setText(_translate("Dialog", "CEP:"))
        self.txtCEP.setPlaceholderText(_translate("Dialog", "digite o CEP"))
        self.lblCidade.setText(_translate("Dialog", "..."))
        self.lblEstado.setText(_translate("Dialog", "..."))
        self.txtQtde.setPlaceholderText(_translate("Dialog", "Qtde"))
        self.cmbVariedade.setPlaceholderText(_translate("Dialog", "Mercadoria"))
        self.btAcrescentar.setText(_translate("Dialog", "Acrescentar"))
        item = self.tblOrcamento.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Merc"))
        item = self.tblOrcamento.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Clone"))
        item = self.tblOrcamento.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Descrição"))
        item = self.tblOrcamento.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Qtde"))
        item = self.tblOrcamento.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Valor"))
        item = self.tblOrcamento.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Total"))
        self.grpDados.setTitle(_translate("Dialog", "Dados do Frete"))
        self.txtValFrete.setText(_translate("Dialog", "0,00"))
        self.txtValFrete.setPlaceholderText(_translate("Dialog", "Peso"))
        self.txtLarg.setPlaceholderText(_translate("Dialog", "Larg."))
        self.lblPeso.setText(_translate("Dialog", "kg"))
        self.txtAlt.setPlaceholderText(_translate("Dialog", "Alt."))
        self.label_5.setText(_translate("Dialog", "Tam. Caixa:"))
        self.txtPeso.setText(_translate("Dialog", "0,000"))
        self.txtPeso.setPlaceholderText(_translate("Dialog", "Peso"))
        self.label_6.setText(_translate("Dialog", "Frete:"))
        self.label_2.setText(_translate("Dialog", "Peso:"))
        self.txtProf.setPlaceholderText(_translate("Dialog", "Prof."))
        self.rdJadLog.setText(_translate("Dialog", "JadLog"))
        self.rdSEDEX.setText(_translate("Dialog", "SEDEX"))
        self.grpResumo.setTitle(_translate("Dialog", "Resumo"))
        self.lblPrazo.setText(_translate("Dialog", "0"))
        self.lblTotal_3.setText(_translate("Dialog", "Prazo:"))
        self.lblTotal.setText(_translate("Dialog", "0"))
        self.lblTotal_2.setText(_translate("Dialog", "TOTAL:"))
        self.lblNumMudas.setText(_translate("Dialog", "0"))
        self.lblTotal_5.setText(_translate("Dialog", "Nº Mudas:"))
        self.lblTotal_4.setText(_translate("Dialog", "Total mudas:"))
        self.lblTotalMerc.setText(_translate("Dialog", "0"))
        self.chkJadLog.setText(_translate("Dialog", "JadLog"))
        self.chkAzul.setText(_translate("Dialog", "Azul"))
        self.btCopyMail.setToolTip(_translate("Dialog", "<html><head/><body><p>Copia no formato de texto fixo para colar no E-mail</p></body></html>"))
        self.btCopyMail.setText(_translate("Dialog", "Copiar p/ E-Mail"))
        self.btFrete.setToolTip(_translate("Dialog", "<html><head/><body><p>Calcula frete pela JadLog (<span style=\" font-size:8pt; font-weight:600;\">padrão</span>)</p></body></html>"))
        self.btFrete.setText(_translate("Dialog", "Calcular Frete"))
        self.btSendSkype.setToolTip(_translate("Dialog", "<html><head/><body><p>Envia pedido de cotação simultâneo para Azul e JadLog via Skype</p></body></html>"))
        self.btSendSkype.setText(_translate("Dialog", "Enviar Cotação Skype"))
        self.btCopyWhats.setToolTip(_translate("Dialog", "<html><head/><body><p>Copia no formato de texto fixo para colar no WhatsApp Web</p></body></html>"))
        self.btCopyWhats.setText(_translate("Dialog", "Copiar p/ WhatsApp"))
        self.btLimpar.setToolTip(_translate("Dialog", "<html><head/><body><p>Limpa tela e inicia novo orçamento</p></body></html>"))
        self.btLimpar.setText(_translate("Dialog", "Limpar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
