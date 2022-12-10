from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class Tree(QWidget):

    def __init__(self, root, columns):
        super().__init__()

        self.root = root
        self.columns = columns
        self.label = QLabel()
        canvas = QPixmap(1200, 900)
        canvas.fill(QtCore.Qt.white)
        self.label.setPixmap(canvas)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.painter = QPainter(self.label.pixmap())
        self.painter.setPen(QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine))
        self.draw_tree(self.root,200,150, 0)


    def draw_tree(self, node, x, y, l):
        if(not node):
            return

        self.draw_node(node, x,y)
        children = node.children

        l+=1
        x1 = x -100

        for i in range(len(children)):
            newX = x1+100*i
            newY = y+100
            if(l==1):
                newX += i * l * 200
            #
            self.draw_tree(children[i],newX, newY, l)
            self.painter.drawLine(x+40, y+30, newX+40, newY)
            self.painter.drawText(newX,y+80,node.condition.vals[i])




        #
    def draw_node(self, node, x,y):

        rectangle = QRect(x, y, 80, 30)
        if (isinstance(node.attribut, int)):
            text = self.columns[node.attribut]
            self.painter.drawRect(rectangle)
        else:
            text = node.attribut
            self.painter.drawEllipse(rectangle)

        self.painter.drawText(rectangle, QtCore.Qt.AlignCenter, str(text))
