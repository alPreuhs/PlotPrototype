import readWrite
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import seaborn as sns
import os



use_tex = False

if use_tex:
    params = {  'text.usetex': True,
                'pgf.texsystem': 'pdflatex',
                'font.family': 'ptm',
                'text.latex.unicode': True,
                'pgf.rcfonts': False,
                'grid.color':'#ffffff',
                'figure.figsize': (4*1.5,(3.8/2)*1.6),
                'font.size': 20,
                'axes.facecolor':'#f0f0f0',
                'text.color':'black',
                'axes.labelcolor':'black',
                'figure.subplot.left': 0.12,
                'figure.subplot.right': 1,
                'figure.subplot.bottom': 0.15,
                'figure.subplot.top': 0.98,
                'figure.dpi': 200.0,
                'lines.linewidth': 2}
else:
    params = { 'pgf.rcfonts': False,
              'grid.color': '#ffffff',
             # 'figure.figsize': (6.5, 3.8),
               'figure.figsize': (8, 3.8),
              'font.size': 20,
              'axes.facecolor': '#f0f0f0',
              'text.color': 'black',
              'axes.labelcolor': 'black',
              'figure.subplot.left': 0.12,
              'figure.subplot.right': 1,
              'figure.subplot.bottom': 0.15,
              'figure.subplot.top': 0.98,
              'figure.dpi': 200.0,
              'lines.linewidth': 2}

# Set the font properties (can use more variables for more fonts)
#font_path = r'C:\Windows\Fonts\comic.ttf'

font_path = r'C:\Windows\Fonts\calibri.ttf'
font_prop_axlb = font_manager.FontProperties(fname=font_path, size=18)
font_prop_lglb = font_manager.FontProperties(fname=font_path, size=10)

plt.rcParams.update(params)

a = plt.rcParams
print(plt.rcParams)

linestyles = ['-','--',':','-','-','--',':','-']
colorcodes = ['#ca0020','#f4a582','#92c5de','#0571b0','#ca0020','#f4a582','#92c5de','#0571b0']


##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
# start here with your file
count = 0
file_extensions = ['a','b', 'c']
for file_extension in file_extensions:

    ##plt.figure()

    fn = 'examples//{}.plot'.format(file_extension)

    ##write the filename WITHOUT extensions:
    fn_plt_WITHOUT_extension = 'examples//{}'.format(file_extension)
    plot_data = readWrite.read_plot_data(fn)

    plot_legend = True
    col = colorcodes[count]
    lns = linestyles[count]
    if count is 0:
        lgd = 'Simulated Motion'
    elif count is 1:
        lgd = 'Estimated Motion Compensation'
    else:
        lgd = 'Residual Motion After Compensation'


    xlbl = r'Projection Index'
    ylbl = 'Translation $t_z$ in mm'

    plt.plot(plot_data[1, :], plot_data[0, :], color=col, linestyle=lns, label = lgd)

    if use_tex:
        if plot_legend:
            plt.legend(loc=0)
        plt.xlabel(xlbl)
        plt.ylabel(ylbl)

    else:
        if plot_legend:
            plt.legend(loc=0, prop=font_prop_lglb)
        plt.xlabel(xlbl, fontproperties=font_prop_axlb)
        plt.ylabel(ylbl, fontproperties=font_prop_axlb)

    # plt.gca().set_ylim(ymax=80, ymin=0)
    if not use_tex:

        for label in (plt.gca().get_xticklabels() + plt.gca().get_yticklabels()):
            label.set_fontproperties(font_prop_axlb)
            label.set_fontsize(8)  # Size here overrides font_prop
        fn_plt = fn_plt_WITHOUT_extension + '.png'
        plt.savefig(fn_plt, orientation='portrait', transparent=False, frameon=False)
    else:
        fn_plt = fn_plt_WITHOUT_extension + '.pgf'
        plt.savefig(fn_plt)
        fn_plt = fn_plt_WITHOUT_extension + '.pdf'
        plt.savefig(fn_plt)


    count += 1