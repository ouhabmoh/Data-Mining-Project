import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class BoxPlotHistogram(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app

        layout = QVBoxLayout()
        self.listwidget = QListWidget()
        #     self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)
        self.c = app.get_columns_index()
        self.c = dict(filter(lambda x: type(app.list[0][x[1]]) != str, self.c.items()))
        for k in self.c:
            self.listwidget.insertItem(self.c[k], k)
        self.button = QPushButton('plot')
        self.button.clicked.connect(self.plot)
        layout.addWidget(self.button)

        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plot(self):
        self.figure.clear()
        attributeT = self.listwidget.currentItem().text()
        attribute = self.app.get_attribute_data(self.c[attributeT])
        attribute = list(filter(lambda x: not self.app.isNan(x), attribute))
        # create an axis

        ax2 = self.figure.add_subplot(211)
        ax1 = self.figure.add_subplot(212)
        ax1.boxplot(attribute, vert=False)
        # plot data
        ax1.set_ylabel(attributeT)
        # ax1.set_title('Box Plot {}'.format(attributeT))

        counts, bins = np.histogram(attribute)
        # create an axis

        # bin = self.app.distinct_count(attribute)
        # freq =  OrderedDict(sorted(self.app.frequency(attribute).items()))

        ax2.set_title('{}'.format(attributeT))
        # ax2.hist(freq.keys(), bin, weights=freq.values())
        ax2.hist(bins[:-1], bins, weights=counts)
        ax2.set_xlabel(attributeT)
        ax2.set_ylabel("Frequency")
        mean = self.app.moy(attribute)
        mode = self.app.mode(attribute)
        median = self.app.median(attribute)
        ax2.axvline(mean, color='b', linestyle='dashed', linewidth=1)
        ax2.axvline(median, color='r', linestyle='dashed', linewidth=1)
        c = ['g', 'y', 'c']
        i = 0
        for m in mode:
            ax2.axvline(m, color=c[i], linestyle='dashed', linewidth=1 + i)
            i += 1
        # ax2.axvline(mode, color='g', linestyle='dashed', linewidth=1)
        # v = max(list(freq.values()))
        # ax2.set_ylim([0, v * 1.3])
        # min_ylim, max_ylim = ax2.get_ylim()
        # ax2.text(mean -3, max_ylim *0.9, 'Mean: {:.2f}'.format(mean))
        # ax2.text(median + 3, max_ylim *0.9, 'Median: {:.2f}'.format(median))
        # for m in mode:
        #     ax2.text(m +3, max_ylim *0.9, 'Mode: {:.2f}'.format(m))

        # refresh canvas

        self.canvas.draw()

