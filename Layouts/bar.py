from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class BarChart2(QWidget):
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
        self.c = dict(filter(
            lambda x: type(app.list[0][x[1]]) == str or (len(set(app.get_attribute_data(x[1]))) < 10) and (
                    type(app.list[0][x[1]]) != str), self.c.items()))

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
        # attribute = list(filter(lambda x: not self.app.isNan(x), attribute))
        atrAttrition = self.app.get_attribute_data(self.c['Attrition'])
        dataset, _ = self.app.get_attribute_data_by(self.c[attributeT], 1)
        freq = []
        label = []
        for d in dataset:
            f = OrderedDict(sorted(self.app.frequency(d).items()))
            freq.append(f.values())
            label = list(f.keys())

        barWidth = 0.25
        # Set position of bar on X axis
        br1 = np.arange(len(freq[0]))
        br = [br1]
        for i in range(len(freq)):
            br2 = [x + barWidth for x in br[i]]
            br.append(br2)

        ax1 = self.figure.add_subplot()
        # Make the plot
        colors = ['g', 'r', 'b']
        for f in range(len(freq)):
            ax1.bar(br[f], freq[f], color=colors[f], width=barWidth,
                    edgecolor='grey', label=label[f])

        # Adding Xticks
        ax1.set_xlabel(attributeT, fontweight='bold', fontsize=15)
        ax1.set_ylabel('Attrition', fontweight='bold', fontsize=15)
        d = self.app.distinct(attribute)
        ax1.set_xticks([r + barWidth for r in range(len(freq[0]))])
        ax1.set_xticklabels(label)

        ax1.legend()
        # create an axis

        # plot data

        # refresh canvas
        self.canvas.draw()