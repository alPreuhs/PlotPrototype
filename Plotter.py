import matplotlib as mpl
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

        # self.plot_editor_window = Window()
        # self.plot_editor = PlotEditor(self.plot_editor_window, self.plot_data)

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
        print(self.plot_file[0])
        self.path = os.path.abspath(self.plot_file[0])
        self.file_edit.setText(self.path)  # os.path.basename(r"" + self.path + ""))

        if (os.path.splitext(self.path)[1] == '.plot'):
            self.ok_bt.setEnabled(True)
        else:
            self.ok_bt.setDisabled(True)

    def on_open_plot_ok_clicked(self):
        self.plot_data = readWrite.read_plot_data(self.path)
        plot_editor_window = Window()
        self.plot_editor = PlotEditor(plot_editor_window, self.plot_data)
        plot_editor_window.show()


linestyles = ['-', '--', ':']


class PlotEditor(Ui_PlotEditor):

    def __init__(self, PlotEditor, plot_data):
        self.PlotEditor = PlotEditor
        Ui_PlotEditor.__init__(self)
        self.setupUi(self.PlotEditor)

        self.plot_data = plot_data
        self.init_parameters()
        self.connect_buttons()

    def init_parameters(self):
        self.font_size = float(self.font_size_sb.currentText())
        self.xlbl = self.horizontal_label_le.text()
        self.ylbl = self.vertical_label_le.text()
        self.linestyle = '-'
        self.params = {}

    def connect_buttons(self):
        self.show_plot_bt.clicked.connect(self.on_show_plot_bt_clicked)
        # print(self.font_size_sb.lineEdit())
        self.font_size_sb.lineEdit().returnPressed.connect(self.on_font_size_changed)

    def on_font_size_changed(self):
        try:
            self.font_size = float(self.font_size_sb.currentText())

        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText(self.font_size_sb.currentText() + " is an invalid index.")
            msg.exec_()
            # self.font_size_sb.setCurrentText(self.font_size)

    def set_up_plot(self):
        self.xlbl = self.horizontal_label_le.text()
        self.ylbl = self.vertical_label_le.text()
        self.linestyle = linestyles[self.linestyle_cb.currentIndex()]
        print()

        self.on_font_size_changed()

        # self.font = self.font_sb.currentFont()
        # self.font.setBold(True)
        self.params = {'font.size': self.font_size}
        # 'font.family': "12"}

    def on_show_plot_bt_clicked(self):
        self.set_up_plot()

        plt.rcParams.update(self.params)

        plt.xlabel(self.xlbl)
        plt.ylabel(self.ylbl)

        plt.plot(self.plot_data[1, :], self.plot_data[0, :], linestyle=self.linestyle)
        plt.show()


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # Dialog = Window()
    # prog = Plotter(Dialog)
    # Dialog.show()
    plot_data = plt.plot
    path = os.path.abspath('C:/Users/Christopher/OneDrive/Studium/Hiwi/GUI/Plot/PlotPrototype/examples/a.plot')
    plot_data = readWrite.read_plot_data(path)
    plot_editor_window = Window()
    plot_editor = PlotEditor(plot_editor_window, plot_data)
    plot_editor_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
