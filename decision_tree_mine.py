import math


from condition import Condition
from node import Node


class DecisionTreeMine:

    def __init__(self, data, attributs, label_index, functions):
        self.data = data
        self.attributs = attributs
        self.label_index = label_index
        self.f = functions

    def generate_tree(self, data, attributs):

        if(self.same_class(data)):
            return Node(self.class_of_data(data))
        if(not attributs):
            return Node(self.majority_class(data))
        attr, cond = self.attribute_selection(data, attributs)
        node = Node(attr, cond)
        self.remove_attribut(data, attributs ,attr)
        divisions = self.divise(data,attr)

        for d in divisions.values():
            if(not d):
                label = self.majority_class(data)
                leaf_node = Node(label)
                node.add_child(leaf_node)

            else:
                node.add_child(self.generate_tree(d, attributs))

        return node



    def remove_attribut(self,data, attributs,attr_index):
        attributs.remove(attr_index)
        # [d.pop(attr_index) for d in data]

    def same_class(self,data):

        labels = [x[self.label_index] for x in data]
        return all(element == labels[0] for element in labels)


    def class_of_data(self,data):
        return [x[self.label_index] for x in data][0]

    def majority_class(self, data):
        label = [x[self.label_index] for x in data]
        return self.f.mode(label)

    def attribute_selection(self, data, attributs):
        ig = []
        for attr in attributs:
            lables = [x[self.label_index] for x in data]

            i = self.information(lables)
            if(self.is_attr_dis(attr)):

                dataj = self.divise(data, attr)
                ld = len(data)
                ia = 0
                for d in dataj.items():
                    lbs = [x[self.label_index] for x in d[1]]
                    id = self.information(lbs)
                    ia += len(d[1])/ld*id

                ig.append((attr,i-ia))
            else:
                a = [x[attr] for x in data]
                ld = len(data)
                inf = []
                for i in range(len(a)-1):
                    ia1 = 0
                    a1 = a[i]
                    a2 = a[i+1]
                    m = (a1+a2)/2
                    ls = self.divise_by_point(data,attr,m)
                    for l in ls:
                        lbs1 = [x[self.label_index] for x in l]
                        id1 = self.information(lbs1)
                        ia1 += len(l) / ld * id1

                    inf.append((m,i-ia1))
                best_split, ia = max(inf, key=lambda item:item[1])
                ig.append((attr,ia,best_split))

        attr_index = max(ig,key=lambda item:item[1])
        if(self.is_attr_dis(attr_index[0])):
            attr_index = attr_index[0]
            attribute = [x[attr_index] for x in data]
            uniques = self.f.distinct(attribute)
            condition = Condition(uniques,0)
            return attr_index,condition
        else:
            condition = Condition(attr_index[2], 1)
            return attr_index[0], condition



    def information(self, attr):
        freq = self.f.frequency(attr)
        l = len(attr)
        proba = [f / l for f in freq.values()]
        return -sum([p * math.log2(p) for p in proba])

    def is_attr_dis(self, att):
        return True

    def divise_by_point(self,data, attr_index, m):
        attr = [x[attr_index] for x in data]
        l1 = [x for x in data if x[attr] <= m]
        l2 = [x for x in data if x[attr] > m]
        return [l1,l2]

    def divise(self, data, attr_index):

        attr = [x[attr_index] for x in data]
        uniques = {l : [] for l in self.f.distinct(attr)}

        for i in data:
            uniques[i[attr_index]].append(i)

        return uniques