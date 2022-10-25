from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class DatasetBasicInfo(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        layout = QVBoxLayout()
        nA, nI = app.basic_info()
        self.label = QLabel("number of attributes {}".format(nA))
        layout.addWidget(self.label)
        self.label2 = QLabel("number of Instances {}".format(nI))
        layout.addWidget(self.label2)
        self.setLayout(layout)
