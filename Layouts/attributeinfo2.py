from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class AttributeInfo2(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app
        layoutMain = QVBoxLayout()
        self.table = QTableWidget()
        layoutMain.addWidget(self.table)
        self.c = app.get_columns_index()
        # self.c = dict(filter(
        #     lambda x: type(app.list[0][x[1]]) == str or (len(set(app.get_attribute_data(x[1]))) < 10) and (
        #             type(app.list[0][x[1]]) != str), self.c.items()))
        a = self.app
        func = [a.distinct_count, a.attr_type, a.null_values, a.distinct]
        self.table.setRowCount(len(self.c.keys()))
        self.table.setColumnCount(len(func))
        self.table.setHorizontalHeaderLabels([x.__name__ for x in func])
        self.table.setVerticalHeaderLabels(self.c.keys())
        # returns pandas array object

        for row in self.c.items():
            for col in range(len(func)):

                atr = self.app.get_attribute_data(row[1])
                x = func[col](atr)
                if isinstance(x, (float, int)):
                    x = '{0:0,.0f}'.format(x)
                tableItem = QTableWidgetItem(str(x))
                self.table.setItem(row[1], col, tableItem)

        self.setLayout(layoutMain)
