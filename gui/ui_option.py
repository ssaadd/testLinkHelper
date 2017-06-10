# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_optionDialog(object):
    def setupUi(self, optionDialog):
        optionDialog.setObjectName("optionDialog")
        optionDialog.resize(385, 175)
        optionDialog.setMinimumSize(QtCore.QSize(385, 175))
        optionDialog.setMaximumSize(QtCore.QSize(385, 175))
        self.layoutWidget = QtWidgets.QWidget(optionDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 341, 112))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.server_urlEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.server_urlEdit.setObjectName("server_urlEdit")
        self.gridLayout.addWidget(self.server_urlEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.devkeyEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.devkeyEdit.setObjectName("devkeyEdit")
        self.gridLayout.addWidget(self.devkeyEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.proxyEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.proxyEdit.setObjectName("proxyEdit")
        self.gridLayout.addWidget(self.proxyEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.login_nameEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.login_nameEdit.setObjectName("login_nameEdit")
        self.gridLayout.addWidget(self.login_nameEdit, 3, 1, 1, 1)
        self.widget = QtWidgets.QWidget(optionDialog)
        self.widget.setGeometry(QtCore.QRect(190, 140, 167, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.acceptButton = QtWidgets.QPushButton(self.widget)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout.addWidget(self.acceptButton)
        self.cancelButton = QtWidgets.QPushButton(self.widget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)

        self.retranslateUi(optionDialog)
        QtCore.QMetaObject.connectSlotsByName(optionDialog)

    def retranslateUi(self, optionDialog):
        _translate = QtCore.QCoreApplication.translate
        optionDialog.setWindowTitle(_translate("optionDialog", "Option"))
        self.label_2.setText(_translate("optionDialog", "devKey"))
        self.label.setText(_translate("optionDialog", "Server Url"))
        self.label_3.setText(_translate("optionDialog", "Proxy"))
        self.label_4.setText(_translate("optionDialog", "login name"))
        self.acceptButton.setText(_translate("optionDialog", "OK"))
        self.cancelButton.setText(_translate("optionDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    optionDialog = QtWidgets.QDialog()
    ui = Ui_optionDialog()
    ui.setupUi(optionDialog)
    optionDialog.show()
    sys.exit(app.exec_())

