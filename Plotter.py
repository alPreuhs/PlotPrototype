import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import seaborn as sns
import os
import sys
import readWrite

from PyQt5 import QtCore, QtGui, QtWidgets
from open_plot_file import Ui_Dialog


class Plotter(Ui_Dialog):

    def __init__(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.__init__(self)
        self.setupUi(self.Dialog)
        self.connect_buttons()
        self.plot_data = plt.plot
        self.path = ''
        self.show_bt.setDisabled(True)

    def connect_buttons(self):
        self.cancel_bt.clicked.connect(self.on_cancel_bt_clicked)
        self.open_plot_bt.clicked.connect(self.on_open_plot_button_clicked)
        self.show_bt.clicked.connect(self.on_show_plot_button_clicked)

    def on_cancel_bt_clicked(self):
        sys.exit()

    def on_open_plot_button_clicked(self):
        self.plot_file = QtWidgets.QFileDialog.getOpenFileName(None, "Open Plot File", '.', ("*.plot"))

        self.path = os.path.abspath(self.plot_file[0])
        self.file_edit.setText(self.path)  # os.path.basename(r"" + self.path + ""))

        if (os.path.splitext(self.path)[1] == '.plot'):
            self.show_bt.setEnabled(True)
        else:
            self.show_bt.setDisabled(True)

    def on_show_plot_button_clicked(self):
        self.plot_data = readWrite.read_plot_data(self.path)
        plt.plot(self.plot_data[1, :], self.plot_data[0, :])
        plt.show()


class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = Window()
    prog = Plotter(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
