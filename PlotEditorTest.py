import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import seaborn as sns
import os
import sys
import readWrite
import copy

from PyQt5 import QtCore, QtGui, QtWidgets
from ploteditorgui import Ui_PlotEditor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg

linestyles = ['-', '--', ':']
colorcodes = ['#ca0020', '#f4a582', '#92c5de', '#0571b0', '#ca0020', '#f4a582', '#92c5de', '#0571b0']


# TODO reset button
# TODO size adjustment
# TODO font and color
# TODO enable zoom
# TODO more plots in one image


class PlotEditor(Ui_PlotEditor):

    def __init__(self, PlotEditor, plot_data):
        self.PlotEditor = PlotEditor
        self.PlotEditor_copy = PlotEditor
        Ui_PlotEditor.__init__(self)
        self.setupUi(self.PlotEditor)
        self.plot_data = plot_data

        self.counter = 0
        self.connect_buttons()
        self.assign_parameters()
        self.update_plot()

    def connect_buttons(self):
        self.reset_bt.clicked.connect(self.reset)

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

    def get_default_values(self):
        pass

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

        self.assign_parameters()
        self.update_plot()

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
        self.figure_size_fac = self.figure_size_slider.value() / 100
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

        width_pixels, height_pixels, xfak, yfak = self.compute_widht_height_pixels()
        scene = QtGui.QGraphicsScene()
        canvas = FigureCanvas(self.fig)
        canvas.resize(width_pixels, height_pixels)
        scene.addWidget(canvas)

        self.PlotView.setFixedSize(width_pixels + 2, height_pixels + 2)
        self.PlotView.setSceneRect(0, 0, width_pixels, height_pixels)
        self.PlotView.fitInView(0, 0, width_pixels, height_pixels, True)
        self.PlotView.setScene(scene)

    def compute_widht_height_pixels(self):
        width_inches, height_inches = self.fig.get_size_inches()
        dpi = self.fig.dpi
        width_pixels = width_inches * dpi
        height_pixels = height_inches * dpi
        xfak = 0
        yfak = 0

        if (len(self.ylbl) > 0):
            width_pixels += self.ptToPx(self.xy_font_size, dpi)
            width_pixels += self.ptToPx(self.xy_labelpad, dpi)
            xfak -= self.ptToPx(self.xy_font_size, dpi) + self.ptToPx(self.xy_labelpad, dpi)
        if (len(self.xlbl) > 0):
            height_pixels += self.ptToPx(self.xy_font_size, dpi)
            height_pixels += self.ptToPx(self.xy_labelpad, dpi)
            yfak += self.ptToPx(self.xy_font_size, dpi) + self.ptToPx(self.xy_labelpad, dpi)
        if (len(self.title) > 0):
            height_pixels += self.ptToPx(self.title_font_size, dpi)
            height_pixels += self.ptToPx(self.title_pad, dpi)
            yfak -= (self.ptToPx(self.title_font_size, dpi) + self.ptToPx(self.title_pad, dpi))

        print(width_pixels)
        print(height_pixels)
        return width_pixels, height_pixels, xfak, yfak

    def ptToPx(self, pt, dpi):
        return pt * 4 / 3  # / 72 * dpi
        # 16 pixels == 12 font points


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)


def main():
    app = QtWidgets.QApplication(sys.argv)

    plt.ion()

    plot_data = plt.plot
    path = os.path.abspath('C:/Users/Christopher/OneDrive/Studium/Hiwi/GUI/Plot/PlotPrototype/examples/a.plot')
    plot_data = readWrite.read_plot_data(path)
    plot_editor_window = Window()
    plot_editor = PlotEditor(plot_editor_window, plot_data)
    plot_editor_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
