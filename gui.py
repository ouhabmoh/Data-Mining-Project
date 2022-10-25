import sys
from math import sqrt, ceil

import pandas as pd  # pip install pandas
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFileDialog


from Layouts.attr import AttributeTendance
from Layouts.attr2 import AttributeStat
from Layouts.attributebasicinfo import AttributeBasicInfo
from Layouts.attributeinfo2 import AttributeInfo2
from Layouts.bar import BarChart2
from Layouts.barchart import BarChart
from Layouts.boxplot import BoxPlot
from Layouts.boxplotattr import BoxPlotAtr
from Layouts.boxplothist import BoxPlotHistogram
from Layouts.dataBasicInfo import DatasetBasicInfo
from Layouts.hist import Histograme
from Layouts.matcorr import Matrice
from Layouts.scatter import Scatter


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.n_atr = None
        self.list = None
        self.data = None
        self.n_data = None
        self.window_width, self.window_height = 1400, 1000
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('Load Excel (or CSV) data to QTableWidget')

        layout = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QVBoxLayout()
        layout5 = QHBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)
        #        self.loadExcelData(excel_file_path, worksheet_name)
        self.button = QPushButton('&Load Data')
        self.button.clicked.connect(self.loadExcelData)
        layout2.addWidget(self.button)
        self.setLayout(layout)

        self.basic_infoB = QPushButton('&Basic Info')
        self.basic_infoB.clicked.connect(self.showDataBsicInfo)
        layout3.addWidget(self.basic_infoB)
        self.attr_info = QPushButton("Attribute Info")
        self.attr_info.clicked.connect(self.showAttributeInfo)
        layout3.addWidget(self.attr_info)
        self.attr_info2 = QPushButton("Attribute Info2")
        self.attr_info2.clicked.connect(self.showAttributeInfo2)
        layout3.addWidget(self.attr_info2)
        self.tendance = QPushButton('Tendance Centrale Et Symmetrie')
        self.tendance.clicked.connect(self.showAttributeStat)
        layout3.addWidget(self.tendance)
        self.tendance2 = QPushButton('Tendance Centrale Et Symmetrie 2')
        self.tendance2.clicked.connect(self.showAttributeStat2)
        layout3.addWidget(self.tendance2)
        self.boxplot = QPushButton('Box Plot')
        self.boxplot.clicked.connect(self.showBoxPlot)
        layout4.addWidget(self.boxplot)
        self.boxplot2 = QPushButton('Box Plot By Attrition')
        self.boxplot2.clicked.connect(self.showBoxPlot2)
        layout4.addWidget(self.boxplot2)

        self.boxhistogram = QPushButton('BoxPlot Histogram')
        self.boxhistogram.clicked.connect(self.showBoxPlotHist)
        layout4.addWidget(self.boxhistogram)

        self.histogram = QPushButton('Histogram')
        self.histogram.clicked.connect(self.showHistogram)
        layout4.addWidget(self.histogram)

        self.bar = QPushButton('Bar Chart')
        self.bar.clicked.connect(self.showBarChart)
        layout4.addWidget(self.bar)

        self.bar2 = QPushButton('Bar Chart2')
        self.bar2.clicked.connect(self.showBarChart2)
        layout4.addWidget(self.bar2)

        self.scatter = QPushButton('Scatter Plot')
        self.scatter.clicked.connect(self.showScatter)
        layout4.addWidget(self.scatter)

        self.corr = QPushButton('Matrice de Correlation')
        self.corr.clicked.connect(self.showMatrice)
        layout4.addWidget(self.corr)

        self.deleteB = QPushButton('Delete')
        self.deleteB.clicked.connect(self.delete)
        layout2.addWidget(self.deleteB)

        # self.addB = QPushButton('ADD')
        # self.addB.clicked.connect(self.add)
        # layout2.addWidget(self.addB)

        button_save = QPushButton('&Save Data')
        button_save.clicked.connect(self.savefile)
        layout2.addWidget(button_save)

        layout.addLayout(layout5)
        layout5.addLayout(layout2)
        layout5.addLayout(layout3)
        layout5.addLayout(layout4)
        self.setLayout(layout)

    def delete(self):
        row = self.table.currentRow()
        self.list.pop(row)
        self.table.removeRow(row)





    def showMatrice(self):
        self.w7 = Matrice(self)
        self.w7.showMaximized()

    def showScatter(self):
        self.w6 = Scatter(self)
        self.w6.showMaximized()

    def showBarChart(self):
        self.w6 = BarChart(self)
        self.w6.showMaximized()

    def showBarChart2(self):
        self.w6 = BarChart2(self)
        self.w6.showMaximized()

    def showHistogram(self):
        self.w5 = Histograme(self)
        self.w5.showMaximized()

    def showBoxPlot(self):
        self.w4 = BoxPlot(self)
        self.w4.showMaximized()

    def showBoxPlotHist(self):
        self.w4 = BoxPlotHistogram(self)
        self.w4.showMaximized()

    def showBoxPlot2(self):
        self.w4 = BoxPlotAtr(self)
        self.w4.showMaximized()

    def showAttributeStat(self):
        self.w3 = AttributeTendance(self)
        self.w3.showMaximized()

    def showAttributeStat2(self):
        self.w3 = AttributeStat(self)
        self.w3.showMaximized()

    def showAttributeInfo(self):
        self.w2 = AttributeBasicInfo(self)
        self.w2.show()

    def showAttributeInfo2(self):
        self.w2 = AttributeInfo2(self)
        self.w2.show()

    def showDataBsicInfo(self):
        self.w = DatasetBasicInfo(self)
        self.w.show()

    def loadExcelData(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', ".xlsx(*.xlsx)")
        if filename is None:
            return
        df = pd.read_excel(filename, worksheet_name)
        self.data = df
        self.list = df.values.tolist()
        if df.size == 0:
            return

        df.fillna('', inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if (value is None):
                    value = ''
                # if isinstance(value, (float, int)):
                #     value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)

        self.table.setColumnWidth(2, 300)

    def savefile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
        if (filename == None):
            return
        columnHeaders = []

        # create column header list
        for j in range(self.table.model().columnCount()):
            columnHeaders.append(self.table.horizontalHeaderItem(j).text())

        df = pd.DataFrame(columns=columnHeaders)

        # create dataframe object recordset
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                df.at[row, columnHeaders[col]] = self.table.item(row, col).text()

        df.to_excel(filename, index=False, sheet_name=worksheet_name)

    def get_columns_index(self):
        col = {}

        for c in range(len(self.data.columns)):
            col[self.data.columns[c]] = c
        return col

    def basic_info(self):
        self.n_atr = len(self.data.columns)
        print("number of attributes {}".format(self.n_atr))
        self.n_data = len(self.data)

        print("number of instances {}".format(self.n_data))
        return len(self.data.columns), self.n_data

    def get_attribute_data(self, index):
        attr = [x[index] for x in self.list]

        return attr

    def get_attribute_data_attrition(self, index):
        attr1 = [x[index] for x in self.list if (x[1] == 'Yes')]
        attr2 = [x[index] for x in self.list if (x[1] == 'No')]
        return attr1, attr2

    def get_attribute_data_by(self, index1, index2):
        distinct = self.distinct(self.get_attribute_data(index2))
        data = []
        for i in distinct:
            d = [y[index1] for y in self.list if (y[index2] == i)]
            l = list(filter(lambda x: not self.isNan(x), d))
            data.append(sorted(l))

        return data, [str(x) for x in distinct]

    def distinct(self, attribute):
        return list(filter(lambda x: not self.isNan(x), list(set(attribute))))

    def distinct_count(self, attribute):
        return len(self.distinct(attribute))

    def attr_type(self, attrinute):
        return type(attrinute[0])

    def null_values(self, attribute):
        return len([x for x in attribute if (x is None or self.isNan(x))])

    def isNan(self, num):
        return num != num

    def attribute_basic_info(self, attribute):
        print("distinc values :")
        print(self.distinct(attribute))
        print("number of distinct values")
        print(len(self.distinct(attribute)))
        print("attribute type")
        print(self.attr_type(attribute))
        print("number of null values")
        print(self.null_values(attribute))
        print(self.table.horizontalHeaderItem(0).text())
        print(self.table.horizontalHeader().length())

    def stat(self, attr):
        attr = sorted(attr)

        print("moy")
        print(self.moy(attr))
        print("med")
        print(self.median(attr))
        print("mode")
        print(self.mode(attr))
        print("freq")
        print(self.frequency(attr))
        print("mode type")
        print(self.type_mode(self.mode(attr)))
        print("sigma")
        attr = [float(x) for x in attr]
        print(self.sigma(attr))
        print("resume")
        print(self.resume(attr))

        print("iqr")
        print(self.IQR(attr))
        print("outliers")
        print(self.outliers(attr))
        print("midrange")
        print(self.midrange(attr))
        print("etendue")
        print(self.ettendue(attr))
        print(self.sym(attr))

    def moy(self, attr):
        n = len(attr)
        s = 0
        for i in range(n):
            s += float(attr[i])

        return s / n

    def median(self, attr):

        n = len(attr)
        if (n % 2 == 0):
            return (float(attr[n // 2]) + float(attr[(n // 2) + 1])) / 2
        else:
            return attr[n // 2 + 1]

    def mode(self, attr):
        a2 = list(attr)

        most = max(list(map(a2.count, a2)))
        mode = list(set(filter(lambda x: a2.count(x) == most, a2)))

        if (len(mode) == len(attr)):
            return []
        return mode

    def type_mode(self, attr):
        l = len(self.mode(attr))
        if (l == 0):
            return 'pas de mode'
        elif (l == 1):
            return 'unimodal'
        elif (l == 2):
            return 'bimodal'
        elif (l == 3):
            return 'trimodal'

        return 'pi-modal'

    def frequency(self, attr):
        f = {}
        for i in attr:
            if i in f.keys():
                f[i] += 1
            else:
                f[i] = 0

        return f

    def sigma(self, attr):
        moy = self.moy(attr)
        n = len(attr)
        s = 0
        for i in attr:
            s += float((i - moy)) * float((i - moy))

        return sqrt(s / n)

    def Q1(self, attr):
        q1 = ceil(len(attr) / 4)
        return attr[q1]

    def Q3(self, attr):
        q3 = ceil(3 * len(attr) / 4)
        return attr[q3]

    def max(self, attr):
        return max(attr)

    def min(self, attr):
        return min(attr)

    def resume(self, attr):
        return min(attr), self.Q1(attr), self.median(attr), self.Q3(attr), max(attr)

    def midrange(self, attr):
        return (min(attr) + max(attr)) / 2

    def ettendue(self, attr):
        return max(attr) - min(attr)

    def IQR(self, attr):
        return self.Q3(attr) - self.Q1(attr)

    def outliers(self, attr):
        q1 = self.Q1(attr)
        q3 = self.Q3(attr)
        iqr = self.IQR(attr)
        lower = q1 - 1.5 * iqr
        higher = q3 + 1.5 * iqr

        return list(filter(lambda x: (x < lower or x > higher), attr))

    def sym(self, attr):
        moy = self.moy(attr)
        med = self.median(attr)
        mode = self.mode(attr)

        if (abs(moy - med) <= 0.3):
            for m in mode:
                if (abs(moy - m) <= 0.3 and abs(med - m) <= 0.3):
                    return "symmetric"

            return "none"

        else:
            if (moy < med):
                for m in mode:
                    if (med > m):
                        return "none"
                return "negatively skewed data"
            if (moy > med):
                for m in mode:
                    if (med < m):
                        return "none"

                return "positively skewed data"

        return "none"

    def person(self, attr1, attr2):
        p = [x1 * x2 for x1, x2 in zip(attr1, attr2)]
        p = sum(p)
        n = len(attr1)
        p = p - (n * self.moy(attr1) * self.moy(attr2))
        p = p / ((n - 1) * self.sigma(attr1) * self.sigma(attr2))
        return p


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    excel_file_path = 'i.xlsx'
    worksheet_name = 'HR Employee Attrition'

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')

    myApp = MyApp()
    myApp.showMaximized()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
