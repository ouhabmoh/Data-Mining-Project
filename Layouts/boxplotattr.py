import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class BoxPlotAtr(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app
        layoutMain = QVBoxLayout()

        layoutAttr = QHBoxLayout()

        layoutBas = QHBoxLayout()

        layoutMain.addLayout(layoutAttr)
        layoutMain.addLayout(layoutBas)

        self.table = QTableWidget()

        layoutBas.addWidget(self.table)

        self.listwidget = QListWidget()
        #     self.listwidget.clicked.connect(self.clicked)
        self.listwidget = QListWidget()
        self.listwidget2 = QListWidget()
        #     self.listwidget.clicked.connect(self.clicked)
        layoutAttr.addWidget(self.listwidget)
        layoutAttr.addWidget(self.listwidget2)
        self.c = app.get_columns_index()
        self.c2 = dict(filter(
            lambda x: type(app.list[0][x[1]]) == str or (len(set(app.get_attribute_data(x[1]))) < 10) and (
                    type(app.list[0][x[1]]) != str), self.c.items()))
        self.c1 = dict(filter(lambda x: type(app.list[0][x[1]]) != str, self.c.items()))
        for k in self.c1:
            self.listwidget.insertItem(self.c1[k], k)
        for k in self.c2:
            self.listwidget2.insertItem(self.c2[k], k)
        self.button = QPushButton('plot')
        self.button.clicked.connect(self.plot)
        layoutMain.addWidget(self.button)

        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # adding tool bar to the layout
        layoutV = QVBoxLayout()
        layoutV.addWidget(self.toolbar)
        layoutV.addWidget(self.canvas)

        layoutBas.addLayout(layoutV)

        self.setLayout(layoutMain)

    def plot(self):

        self.figure.clear()
        attributeT1 = self.listwidget.currentItem().text()
        attr1index = self.c[attributeT1]
        attributeT2 = self.listwidget2.currentItem().text()
        attr2index = self.c[attributeT2]

        dataset, labels = self.app.get_attribute_data_by(attr1index, attr2index)
        a = self.app
        func = [a.moy, a.median, a.mode, a.type_mode, a.sigma, a.resume, a.IQR, a.outliers, a.midrange, a.sym,
                a.ettendue]
        self.table.setRowCount(len(func))
        self.table.setColumnCount(len(labels))
        self.table.setHorizontalHeaderLabels(labels)
        self.table.setVerticalHeaderLabels([x.__name__ for x in func])
        # returns pandas array object
        for row in range(len(func)):

            for col_index in range(len(labels)):
                x = func[row](dataset[col_index])
                if isinstance(x, (float, int)):
                    x = '{0:0,.0f}'.format(x)
                tableItem = QTableWidgetItem(str(x))
                self.table.setItem(row, col_index, tableItem)

        self.table.setColumnWidth(2, 300)

        # mode = self.app.mode(dataset[0])
        # self.labels[0].setText("mode {}".format(mode))
        #
        # self.labels[1].setText("mode type {}".format(self.app.type_mode(mode)))
        # if (type(dataset[0][0]) is not str):
        #     self.labels[2].setText("moyenne : {}".format(self.app.moy(dataset[0])))
        #
        #     self.labels[3].setText("mediane {}".format(self.app.median(dataset[0])))
        #
        #     self.labels[4].setText("sigma {}".format(self.app.sigma(dataset[0])))
        #
        #     self.labels[5].setText("resume {}".format(self.app.resume(dataset[0])))
        #
        #     self.labels[6].setText("iqr {}".format(self.app.IQR(dataset[0])))
        #
        #     self.labels[7].setText("outliers {}".format(self.app.outliers(dataset[0])))
        #
        #     self.labels[8].setText("midrange {}".format(self.app.midrange(dataset[0])))
        #     self.labels[9].setText("symetrie {}".format(self.app.sym(dataset[0])))
        #     self.labels[10].setText("etendue {}".format(self.app.ettendue(dataset[0])))
        # create an axis
        ax1 = self.figure.add_subplot(111)

        ax1.boxplot(dataset, labels=labels)
        # plot data
        ax1.set_ylabel(attributeT1)

        ax1.set_title('Box Plot {}'.format(attributeT1))
        # refresh canvas
        self.canvas.draw()
