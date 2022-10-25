from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QLabel


class AttributeTendance(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.labels = [QLabel() for i in range(11)]

        layout = QVBoxLayout()
        self.listwidget = QListWidget()
        #     self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)
        self.c = app.get_columns_index()
        for k in self.c:
            self.listwidget.insertItem(self.c[k], k)
        self.button = QPushButton('calculate')
        self.button.clicked.connect(self.clicked)
        layout.addWidget(self.button)
        for label in self.labels:
            layout.addWidget(label)

        self.setLayout(layout)

    def clicked(self):
        for label in self.labels:
            label.setText('')
            label.setWordWrap(True)
        attribute = self.listwidget.currentItem().text()
        attribute = sorted(self.app.get_attribute_data(self.c[attribute]))
        mode = self.app.mode(attribute)
        self.labels[0].setText("mode {}".format(mode))

        self.labels[1].setText("mode type {}".format(self.app.type_mode(attribute)))
        if (type(attribute[0]) is not str):
            self.labels[2].setText("moyenne : {}".format(self.app.moy(attribute)))

            self.labels[3].setText("mediane {}".format(self.app.median(attribute)))

            self.labels[4].setText("sigma {}".format(self.app.sigma(attribute)))

            self.labels[5].setText("resume {}".format(self.app.resume(attribute)))

            self.labels[6].setText("iqr {}".format(self.app.IQR(attribute)))

            self.labels[7].setText("outliers {}".format(self.app.outliers(attribute)))

            self.labels[8].setText("midrange {}".format(self.app.midrange(attribute)))
            self.labels[9].setText("symetrie {}".format(self.app.sym(attribute)))
            self.labels[10].setText("etendue {}".format(self.app.ettendue(attribute)))