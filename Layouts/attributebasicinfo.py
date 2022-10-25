from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QLabel


class AttributeBasicInfo(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()
        self.label4 = QLabel()
        self.label3 = QLabel()
        self.app = app
        self.label2 = QLabel()
        self.label = QLabel()

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

        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.label4)

        self.setLayout(layout)

    def clicked(self):
        attribute = self.listwidget.currentItem().text()
        attribute = self.app.get_attribute_data(self.c[attribute])

        self.label.setText("distinc values : {}".format(self.app.distinct(attribute)))
        self.label.setWordWrap(True)
        self.label2.setText("number of distinc values {}".format(len(self.app.distinct(attribute))))
        self.label2.setWordWrap(True)
        self.label3.setText("attribute type {}".format(self.app.attr_type(attribute)))
        self.label3.setWordWrap(True)
        self.label4.setText("number of null values {}".format(self.app.null_values(attribute)))
        self.label4.setWordWrap(True)
