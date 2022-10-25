from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class AttributeStat(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.c = app.get_columns_index()

        self.setLayout(layout)
        a = self.app
        func = [a.moy, a.median, a.mode, a.type_mode, a.sigma, a.resume, a.IQR, a.outliers, a.midrange, a.sym,
                a.ettendue]
        labels = a.data.columns
        self.table.setRowCount(len(labels))
        self.table.setColumnCount(len(func))
        self.table.setHorizontalHeaderLabels([x.__name__ for x in func])
        self.table.setVerticalHeaderLabels(labels)
        # returns pandas array object
        for row in range(len(func)):

            for col_index in range(len(labels)):
                attribute = sorted(self.app.get_attribute_data(self.c[labels[col_index]]))
                attribute = list(filter(lambda x: not a.isNan(x), attribute))
                try:
                    x = func[row](attribute)
                except:
                    x = 'None'
                if isinstance(x, (float, int)):
                    x = '{0:0,.0f}'.format(x)
                tableItem = QTableWidgetItem(str(x))
                self.table.setItem(col_index, row, tableItem)

        self.table.setColumnWidth(2, 300)