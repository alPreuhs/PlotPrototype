import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import seaborn as sns
import os
import sys

from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QRectF, QRect, QDir

import readWrite
import copy

from PyQt5 import QtCore, QtGui, QtWidgets
from ploteditorgui import Ui_PlotEditor
from open_plot_file import Ui_Dialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg

linestyles = ['-', '--', ':']
colorcodes = ['#ca0020', '#f4a582', '#92c5de', '#0571b0', '#ca0020', '#f4a582', '#92c5de', '#0571b0']


# TODO save button
# TODO font and color
# TODO enable zoom
# TODO more plots in one image

class PlotEditor(Ui_PlotEditor):

    def __init__(self, PlotEditor, plot_data):
        self.PlotEditor = PlotEditor
        Ui_PlotEditor.__init__(self)
        self.setupUi(self.PlotEditor)
        self.plot_data = plot_data

        self.counter = 0
        self.connect_buttons()
        self.assign_parameters()
        self.update_plot()

    def connect_buttons(self):
        self.reset_bt.clicked.connect(self.reset)
        self.save_bt.clicked.connect(self.save_scene)

        self.x_label_le.editingFinished.connect(self.update_plot)
        self.y_label_le.editingFinished.connect(self.update_plot)
        self.xy_font_cb.currentFontChanged.connect(self.update_plot)
        self.xy_font_size_cb.currentIndexChanged.connect(self.update_plot)
        self.xy_color_cb.currentIndexChanged.connect(self.update_plot)
        self.xy_kursive_pb.clicked.connect(self.update_plot)
        self.xy_fat_pb.clicked.connect(self.update_plot)
        self.labelpad_sb.valueChanged.connect(self.update_plot)

        self.linestyle_cb.currentIndexChanged.connect(self.update_plot)
        self.linewidth_cb.currentIndexChanged.connect(self.update_plot)
        self.line_color_cb.currentIndexChanged.connect(self.update_plot)

        self.facecolor_cb.currentIndexChanged.connect(self.update_plot)
        self.background_color_cb.currentIndexChanged.connect(self.update_plot)
        self.edgecolor_cb.currentIndexChanged.connect(self.update_plot)
        self.edge_linewidth_cb.currentIndexChanged.connect(self.update_plot)
        self.figure_size_slider.sliderReleased.connect(self.update_plot)

        self.label_le.editingFinished.connect(self.update_plot)
        self.legend_font_sb.currentFontChanged.connect(self.update_plot)
        self.legend_color_cb.currentIndexChanged.connect(self.update_plot)
        self.legend_fat_pb.clicked.connect(self.update_plot)
        self.legend_kursive_pb.clicked.connect(self.update_plot)
        self.legend_font_size_sb.currentIndexChanged.connect(self.update_plot)
        self.legend_pos_cb.currentIndexChanged.connect(self.update_plot)
        self.legend_facecolor_cb.currentIndexChanged.connect(self.update_plot)
        self.legend_edgecolor_cb.currentIndexChanged.connect(self.update_plot)

        self.title_le.editingFinished.connect(self.update_plot)
        self.title_font_cb.currentIndexChanged.connect(self.update_plot)
        self.title_color_cb.currentIndexChanged.connect(self.update_plot)
        self.title_kursive_pb.clicked.connect(self.update_plot)
        self.title_fat_pb.clicked.connect(self.update_plot)
        self.title_font_size_cb.currentIndexChanged.connect(self.update_plot)
        self.horizontal_ali_cb.currentIndexChanged.connect(self.update_plot)
        self.title_pad_sb.valueChanged.connect(self.update_plot)

        self.xy_kursive_pb.setCheckable(True)
        self.xy_fat_pb.setCheckable(True)
        self.title_kursive_pb.setCheckable(True)
        self.title_fat_pb.setCheckable(True)
        self.legend_fat_pb.setCheckable(True)
        self.legend_kursive_pb.setCheckable(True)

    def reset(self):
        self.title_fat_pb.setChecked(False)
        self.legend_fat_pb.setChecked(False)
        self.xy_fat_pb.setChecked(False)
        self.title_kursive_pb.setChecked(False)
        self.legend_kursive_pb.setChecked(False)
        self.xy_kursive_pb.setChecked(False)

        self.x_label_le.clear()
        self.y_label_le.clear()
        self.label_le.clear()
        self.title_le.clear()

        self.title_font_size_cb.setCurrentIndex(0)
        self.legend_font_size_sb.setCurrentIndex(0)
        self.xy_font_size_cb.setCurrentIndex(0)
        self.linewidth_cb.setCurrentIndex(0)
        self.edge_linewidth_cb.setCurrentIndex(0)
        self.title_pad_sb.setValue(0)
        self.labelpad_sb.setValue(0)

        self.xy_color_cb.setCurrentIndex(0)
        self.line_color_cb.setCurrentIndex(0)
        self.facecolor_cb.setCurrentIndex(1)
        self.background_color_cb.setCurrentIndex(1)
        self.edgecolor_cb.setCurrentIndex(1)
        self.legend_color_cb.setCurrentIndex(0)
        self.legend_facecolor_cb.setCurrentIndex(1)
        self.legend_edgecolor_cb.setCurrentIndex(1)
        self.title_color_cb.setCurrentIndex(0)

        self.figure_size_slider.setValue(0)

        self.assign_parameters()
        self.update_plot()

    def save_scene(self):
        # save_plot_window = Window()
        # self.save_file = SavePlot(save_plot_window, self.PlotView)
        # save_plot_window.show()

        filename = QtGui.QFileDialog.getSaveFileName(None, 'Target Directory', QDir.homePath(), "*.png;;*.pgf")

        # Get the size of your graphicsview
        rect = self.PlotView.viewport().rect()
        width, height = rect.size().width(), rect.size().height()
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        targetrect = QRectF(0, 0, width, height)
        sourcerect = QRect(0, 0, width, height)
        # Render the graphicsview onto the pixmap and save it out.
        self.PlotView.render(painter, targetrect, sourcerect)
        path = os.path.abspath(filename[0])

        # TODO: this command causes the program to close due to jumping in main method / why?
        pixmap.save(path)

    def assign_parameters(self):
        # x- and y-labeling
        self.xlbl = self.x_label_le.text()
        self.ylbl = self.y_label_le.text()
        self.xy_font_size = float(self.xy_font_size_cb.currentText())
        self.xy_font = self.xy_font_cb.currentFont()
        self.xy_color = self.xy_color_cb.currentText()
        self.xy_style = 'italic' if (self.xy_kursive_pb.isChecked()) else 'normal'
        self.xy_weight = 'bold' if (self.xy_fat_pb.isChecked()) else 'normal'
        self.xy_labelpad = (self.labelpad_sb.value())

        # title parameters
        self.title = self.title_le.text()
        self.title_font_size = float(self.title_font_size_cb.currentText())
        self.title_font = self.title_font_cb.currentFont()
        self.title_color = self.title_color_cb.currentText()
        self.title_style = 'italic' if (self.title_kursive_pb.isChecked()) else 'normal'
        self.title_weight = 'bold' if (self.title_fat_pb.isChecked()) else 'normal'
        self.title_pad = (self.title_pad_sb.value())
        self.title_horizontal_ali = self.horizontal_ali_cb.currentText()

        # figure colors
        self.facecolor = self.facecolor_cb.currentText()
        self.edgecolor = self.edgecolor_cb.currentText()
        self.background_color = self.background_color_cb.currentText()
        self.edge_linewidth = float(self.edge_linewidth_cb.currentText())

        # line parameters
        self.linestyle = linestyles[self.linestyle_cb.currentIndex()]
        self.linecolor = self.line_color_cb.currentText()
        self.lineswidth = float(self.linewidth_cb.currentText())

        # legend parameters
        self.label = self.label_le.text()
        self.legend_font_size = float(self.legend_font_size_sb.currentText())
        self.legend_font = self.legend_font_sb.currentFont()
        self.legend_color = self.legend_color_cb.currentText()
        self.legend_weight = 'bold' if (self.legend_fat_pb.isChecked()) else 'normal'
        self.legend_style = 'italic' if (self.legend_kursive_pb.isChecked()) else 'normal'
        self.legend_pos = self.legend_pos_cb.currentIndex()
        self.legend_facecolor = self.legend_facecolor_cb.currentText()
        self.legend_edgecolor = self.legend_edgecolor_cb.currentText()

        # set up figure
        self.ref_fig_size = Figure().get_size_inches() if (self.counter == 0) else self.ref_fig_size
        self.max_height = (self.PlotView.maximumHeight() / Figure().dpi) if (self.counter == 0) else self.max_height
        step_size = (self.max_height - self.ref_fig_size[1]) / 9999

        self.figure_size_fac = (self.ref_fig_size[1] + step_size * self.figure_size_slider.value()) / self.ref_fig_size[
            1]
        size_inches = (self.ref_fig_size[0] * self.figure_size_fac,
                       self.ref_fig_size[1] * self.figure_size_fac)
        self.fig = Figure(facecolor=self.facecolor, edgecolor=self.edgecolor,
                          linewidth=self.edge_linewidth, figsize=size_inches)
        self.counter += 1

    def update_plot(self):
        self.assign_parameters()
        ax = self.fig.gca(facecolor=self.background_color)
        ax.clear()
        ax.plot(self.plot_data[1, :],
                self.plot_data[0, :], color=self.linecolor, linestyle=self.linestyle, label=self.label,
                linewidth=self.lineswidth)

        # Set Legend
        if (len(self.label) > 0):
            legend = ax.legend(
                prop={'size': self.legend_font_size, 'family': self.legend_font.family(), 'style': self.legend_style,
                      'weight': self.legend_weight}, facecolor=self.legend_facecolor, edgecolor=self.legend_edgecolor,
                loc=self.legend_pos)
            for text in legend.get_texts():
                text.set_color(self.legend_color)

        # Set title
        ax.set_title(self.title, size=self.title_font_size, family=self.title_font.family(),
                     style=self.title_style, weight=self.title_weight, color=self.title_color,
                     loc=self.title_horizontal_ali, y=1 + (self.title_pad / 100))

        # Set x- and y-labeling
        ax.set_xlabel(self.xlbl, labelpad=self.xy_labelpad, size=self.xy_font_size, family=self.xy_font.family(),
                      style=self.xy_style, weight=self.xy_weight, color=self.xy_color)
        ax.set_ylabel(self.ylbl, labelpad=self.xy_labelpad, size=self.xy_font_size, family=self.xy_font.family(),
                      style=self.xy_style, weight=self.xy_weight, color=self.xy_color)

        scene = QtGui.QGraphicsScene()

        self.fig.tight_layout()
        canvas = FigureCanvas(self.fig)
        scene.addWidget(canvas)

        self.PlotView.setFixedSize(canvas.get_width_height()[0] + 2, canvas.get_width_height()[1] + 2)
        self.PlotView.setSceneRect(0, 0, canvas.get_width_height()[0], canvas.get_width_height()[1])
        self.PlotView.fitInView(0, 0, canvas.get_width_height()[0], canvas.get_width_height()[1])
        self.PlotView.setScene(scene)

        width = self.PlotEditor.minimumWidth() + canvas.get_width_height()[0]
        dialog_width = width if (width > 880) else 880
        self.PlotEditor.resize(dialog_width, self.PlotEditor.geometry().height())


class Plotter(Ui_Dialog):
    def __init__(self, Dialog):
        self.Dialog = Dialog
        Ui_Dialog.__init__(self)
        self.setupUi(self.Dialog)

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


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


def main():
    app = QtWidgets.QApplication(sys.argv)

    plt.ion()
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
