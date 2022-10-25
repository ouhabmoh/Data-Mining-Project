import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class BoxPlot(QWidget):
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
        ax1 = self.figure.add_subplot(111)

        ax1.boxplot(attribute)
        # plot data
        ax1.set_ylabel(attributeT)

        ax1.set_title('Box Plot {}'.format(attributeT))
        # refresh canvas
        self.canvas.draw()

