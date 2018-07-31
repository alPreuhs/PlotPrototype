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
from copy import deepcopy


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
colorcodes = ['#ca0020', '#f4a582', '#92c5de', '#0571b0', '#ca0020', '#f4a582', '#92c5de', '#0571b0']


# TODO some fonts aren't compatible

class PlotEditor(Ui_PlotEditor):

    def __init__(self, PlotEditor, plot_data):
        self.PlotEditor = PlotEditor
        Ui_PlotEditor.__init__(self)
        self.setupUi(self.PlotEditor)

        self.first = True
        self.plot_data = plot_data
        # self.init_parameters()
        self.connect_buttons()

    def init_parameters(self):
        self.font_size = float(self.font_size_sb.currentText())
        self.font = self.font_sb.currentFont()
        self.legend_font_size = float(self.legend_font_size_sb.currentText())
        self.legend_font = self.legend_font_sb.currentFont()
        self.axes_label_color = self.axes_label_color_cb.currentText()
        self.legend_color = self.legend_color_cb.currentText()
        self.xlbl = self.horizontal_label_le.text()
        self.ylbl = self.vertical_label_le.text()
        self.label = self.label_le.text()
        self.linestyle = '-'
        self.params = {}
        self.style = 'normal'
        self.weight = 'normal'
        self.lineswidth = float(self.linewidth_cb.currentText())
        self.linecolor = self.line_color_cb.currentText()
        self.background_color = self.background_color_cb.currentText()
        self.legend_pos = self.legend_pos_cb.currentIndex()
        self.legend_facecolor = self.legend_facecolor_cb.currentText()
        self.legend_style = 'normal'
        self.legend_weight = 'normal'
        self.kursive_pb.setCheckable(True)
        self.fat_pb.setCheckable(True)
        self.legend_fat_pb.setCheckable(True)
        self.legend_kursive_pb.setCheckable(True)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        if (self.first == True):
            self.ref_fig_size = self.fig.get_size_inches()
        else:
            self.ref_fig_size = self.ref_fig_size

        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.first = False

    def handle_close(self, evt):
        self.show_plot_bt.setVisible(True)
        self.show_plot_bt.setText("Show Plot")

    def show_update_plot(self):
        if plt.get_fignums():
            self.show_plot()
        else:
            self.init_parameters()
            self.show_plot_bt.setText("Update Plot")
            self.show_plot()

    def connect_buttons(self):
        self.show_plot_bt.clicked.connect(self.show_update_plot)
        self.font_size_sb.lineEdit().returnPressed.connect(self.on_font_size_changed)
        self.legend_font_size_sb.lineEdit().returnPressed.connect(self.on_legend_font_size_changed)
        self.linewidth_cb.lineEdit().returnPressed.connect(self.on_line_width_changed)

        self.label_le.textChanged.connect(self.on_label_changed)
        self.horizontal_label_le.textChanged.connect(self.on_xlabel_changed)
        self.vertical_label_le.textChanged.connect(self.on_ylabel_changed)
        self.figure_size_slider.valueChanged.connect(self.on_fig_size_changed)

    def show_plot(self):

        self.ax.clear()

        self.set_up_plot()
        plt.rcParams.update(self.params)

        self.ax.plot(self.plot_data[1, :], self.plot_data[0, :], color=self.linecolor,
                     linestyle=self.linestyle, label=self.label)

        # set axes labels
        plt.xlabel(self.xlbl)
        plt.ylabel(self.ylbl)

        if (len(self.label) > 0):
            plt.legend(
                prop={'size': self.legend_font_size, 'family': self.legend_font.family(), 'style': self.legend_style,
                      'weight': self.legend_weight},
                loc=self.legend_pos)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_up_plot(self):
        self.xlbl = self.horizontal_label_le.text()
        self.ylbl = self.vertical_label_le.text()
        self.label = self.label_le.text()

        self.linestyle = linestyles[self.linestyle_cb.currentIndex()]
        self.axes_label_color = self.axes_label_color_cb.currentText()
        self.linecolor = self.line_color_cb.currentText()
        self.background_color = self.background_color_cb.currentText()
        self.legend_color = self.legend_color_cb.currentText()
        self.legend_facecolor = self.legend_facecolor_cb.currentText()
        self.legend_pos = self.legend_pos_cb.currentIndex()
        self.on_font_size_changed()
        self.on_line_width_changed()
        self.on_legend_font_size_changed()

        self.style = 'italic' if (self.kursive_pb.isChecked()) else 'normal'
        self.weight = 'bold' if (self.fat_pb.isChecked()) else 'normal'
        self.legend_style = 'italic' if (self.legend_kursive_pb.isChecked()) else 'normal'
        self.legend_weight = 'bold' if (self.legend_fat_pb.isChecked()) else 'normal'

        self.fig_size = self.ref_fig_size * (self.figure_size_slider.value() / 500)
        self.fig.set_size_inches(self.fig_size[0], self.fig_size[1])

        self.params = {'font.size': self.font_size,
                       'font.family': self.font.family(),
                       'font.style': self.style,
                       'font.weight': self.weight,
                       'lines.linewidth': self.lineswidth,
                       'axes.facecolor': self.background_color,
                       'axes.labelcolor': self.axes_label_color,
                       'text.color': self.legend_color,
                       'legend.facecolor': self.legend_facecolor}

    def on_font_size_changed(self):
        try:
            self.font_size = float(self.font_size_sb.currentText())
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText(self.font_size_sb.currentText() + " is an invalid index.")
            msg.exec_()

    def on_legend_font_size_changed(self):
        try:
            self.legend_font_size = float(self.legend_font_size_sb.currentText())
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText(self.legend_font_size_sb.currentText() + " is an invalid index.")
            msg.exec_()

    def on_xlabel_changed(self):
        self.xlbl = self.horizontal_label_le.text()
        self.show_plot()

    def on_ylabel_changed(self):
        self.ylbl = self.vertical_label_le.text()
        self.show_plot()

    def on_label_changed(self):
        self.label = self.label_le.text()
        self.show_plot()

    def on_fig_size_changed(self):
        self.fig_size = self.ref_fig_size * (self.figure_size_slider.value() / 500)
        self.show_plot()

    def on_line_width_changed(self):
        try:
            self.lineswidth = float(self.linewidth_cb.currentText())
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText(self.linewidth_cb.currentText() + " is an invalid index.")
            msg.exec_()


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


def main():
    app = QtWidgets.QApplication(sys.argv)

    plt.ion()
    Dialog = Window()
    prog = Plotter(Dialog)
    Dialog.show()

    # plot_data = plt.plot
    # path = os.path.abspath('C:/Users/Christopher/OneDrive/Studium/Hiwi/GUI/Plot/PlotPrototype/examples/a.plot')
    # plot_data = readWrite.read_plot_data(path)
    # plot_editor_window = Window()
    # plot_editor = PlotEditor(plot_editor_window, plot_data)
    # plot_editor_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
