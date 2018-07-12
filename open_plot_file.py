# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_plot_file.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(423, 302)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(423, 302))
        Dialog.setMaximumSize(QtCore.QSize(423, 302))
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(50, 50, 321, 181))
        self.widget.setMinimumSize(QtCore.QSize(321, 181))
        self.widget.setMaximumSize(QtCore.QSize(321, 181))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setVerticalSpacing(24)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.widget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.open_plot_bt = QtWidgets.QPushButton(self.splitter_2)
        self.open_plot_bt.setMinimumSize(QtCore.QSize(147, 32))
        self.open_plot_bt.setMaximumSize(QtCore.QSize(170, 45))
        self.open_plot_bt.setObjectName("open_plot_bt")
        self.file_edit = QtWidgets.QLineEdit(self.splitter_2)
        self.file_edit.setMinimumSize(QtCore.QSize(168, 32))
        self.file_edit.setMaximumSize(QtCore.QSize(170, 45))
        self.file_edit.setObjectName("file_edit")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.show_bt = QtWidgets.QPushButton(self.splitter)
        self.show_bt.setMinimumSize(QtCore.QSize(158, 31))
        self.show_bt.setMaximumSize(QtCore.QSize(170, 45))
        self.show_bt.setObjectName("show_bt")
        self.cancel_bt = QtWidgets.QPushButton(self.splitter)
        self.cancel_bt.setMinimumSize(QtCore.QSize(157, 31))
        self.cancel_bt.setMaximumSize(QtCore.QSize(170, 45))
        self.cancel_bt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cancel_bt.setObjectName("cancel_bt")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_plot_bt.setText(_translate("Dialog", "Open Plot File"))
        self.show_bt.setText(_translate("Dialog", "Show Plot"))
        self.cancel_bt.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

