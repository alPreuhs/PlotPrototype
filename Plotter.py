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
from ploteditorgui import Ui_PlotEditor


class Plotter(Ui_Dialog):
    def __init__(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.__init__(self)
        self.setupUi(self.Dialog)

        self.plot_editor_window = Window()
        self.plot_editor = PlotEditor(self.plot_editor_window)
        # Ui_PlotEditor.__init__(self)
        # self.setupUi(self.PlotEditor)

        self.connect_buttons()
        self.plot_data = plt.plot
        self.path = ''
        self.ok_bt.setDisabled(True)

    def connect_buttons(self):
        self.cancel_bt.clicked.connect(self.on_cancel_bt_clicked)
        self.open_plot_bt.clicked.connect(self.on_open_plot_button_clicked)
        self.ok_bt.clicked.connect(self.on_open_plot_ok_clicked)

    def on_cancel_bt_clicked(self):
        sys.exit()

    def on_open_plot_button_clicked(self):
        self.plot_file = QtWidgets.QFileDialog.getOpenFileName(None, "Open Plot File", '.', ("*.plot"))

        self.path = os.path.abspath(self.plot_file[0])
        self.file_edit.setText(self.path)  # os.path.basename(r"" + self.path + ""))

        if (os.path.splitext(self.path)[1] == '.plot'):
            self.ok_bt.setEnabled(True)
        else:
            self.ok_bt.setDisabled(True)

    def on_open_plot_ok_clicked(self):
        self.plot_data = readWrite.read_plot_data(self.path)

        self.plot_editor = PlotEditor(self.plot_editor_window)
        self.plot_editor.plot_data = self.plot_data
        self.plot_editor_window.show()


class PlotEditor(Ui_PlotEditor):
    def __init__(self, PlotEditor):
        self.PlotEditor = PlotEditor
        Ui_PlotEditor.__init__(self)
        self.setupUi(self.PlotEditor)

        self.plot_data = plt.plot
        self.connect_buttons()

    def connect_buttons(self):
        self.show_plot_bt.clicked.connect(self.on_show_plot_bt_clicked)

    def update_plot(self):
        pass

    def on_show_plot_bt_clicked(self):
        plt.plot(self.plot_data[1, :], self.plot_data[0, :])
        plt.show()


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


def main():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = Window()
    prog = Plotter(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
