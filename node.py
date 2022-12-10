class Node:

    def __init__(self, attribut, condition = None):

        self.attribut = attribut
        self.condition = condition
        self.children = []


    def add_child(self, node):
        self.children.append(node)