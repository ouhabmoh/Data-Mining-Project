import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Matrice(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app

        layout = QVBoxLayout()

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

        self.figure.clear()
        df = self.app.data
        f = self.figure
        ax1 = self.figure.add_subplot()
        ax1.matshow(df.corr())
        ax1.set_xticks(range(df.select_dtypes(['number']).shape[1]))
        ax1.set_xticklabels(df.select_dtypes(['number']).columns, rotation=90)

        ax1.set_yticks(range(df.select_dtypes(['number']).shape[1]))
        ax1.set_yticklabels(df.select_dtypes(['number']).columns)
        # cb = ax1.colorbar()
        # cb.ax.tick_params(labelsize=14)
        ax1.set_title('Correlation Matrix', fontsize=16);
        #
        #
        # ax1.matshow(df.corr())
        # ax1.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14,
        #            rotation=45)
        # ax1.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
        # cb = plt.colorbar()
        # cb.ax.tick_params(labelsize=14)
        # plt.title('Correlation Matrix', fontsize=16);
        # ax1.matshow(self.app.data.corr())

        # plot data

        # refresh canvas
        self.canvas.draw()