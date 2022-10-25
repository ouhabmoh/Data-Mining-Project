import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Scatter(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app

        layout = QVBoxLayout()
        self.listwidget = QListWidget()
        self.listwidget2 = QListWidget()
        #     self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)
        layout.addWidget(self.listwidget2)
        self.c = app.get_columns_index()
        self.c = dict(filter(lambda x: type(app.list[0][x[1]]) != str, self.c.items()))
        for k in self.c:
            self.listwidget.insertItem(self.c[k], k)
            self.listwidget2.insertItem(self.c[k], k)
        self.button = QPushButton('plot')
        self.button.clicked.connect(self.plot)
        layout.addWidget(self.button)
        self.label = QLabel()
        layout.addWidget(self.label)
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

        attributeT2 = self.listwidget2.currentItem().text()
        attribute2 = self.app.get_attribute_data(self.c[attributeT2])

        for x1, x2 in zip(attribute, attribute2):
            if (self.app.isNan(x1) or self.app.isNan(x2)):
                attribute.remove(x1)
                attribute2.remove(x2)
        self.label.setText("person = {}".format(self.app.person(attribute, attribute2)))
        # create an axis
        ax1 = self.figure.add_subplot()

        ax1.scatter(attribute, attribute2, c='blue')
        ax1.set_xlabel(attributeT)
        ax1.set_ylabel(attributeT2)

        ax1.set_title('Scatter Plot {} {}'.format(attributeT, attributeT2))
        # plot data

        # refresh canvas
        self.canvas.draw()