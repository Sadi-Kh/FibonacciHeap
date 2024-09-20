import math


class Node:
    def __init__(self, key):
        self.key = key
        self.parent = self.child = self.left = self.right = None
        self.degree = 0
        self.marked = False


# P = r + 2m


class FibonacciHeap:

    def __init__(self):
        self.min = None
        self.root_list = None
        self.node_count = 0

    def insert(self, node):
        node.degree = 0
        node.parent = node.child = None
        node.marked = False
        if self.min is None:
            self.insert_root_list(node)
            self.min = node
        else:
            self.insert_root_list(node)
            if node.key < self.min.key:
                self.min = node
        self.node_count += 1

    def find_min(self):
        return self.min

    def union(self, h2):
        new_heap = FibonacciHeap()
        new_heap.root_list, new_heap.min = self.root_list, self.min

        last = h2.root_list.left
        h2.root_list.left = new_heap.root_list.left
        new_heap.root_list.left.right = h2.root_list
        new_heap.root_list.left = last
        new_heap.root_list.left.right = new_heap.root_list

        if h2.min_node.key < new_heap.min_node.key:
            new_heap.min_node = h2.min_node

        new_heap.node_count = self.node_count + h2.node_count
        return new_heap

    def extract_min(self):
        z = self.min
        if z is not None:
            for child in self.iterate(z.child):
                self.insert_root_list(child)
                child.parent = None
        self.remove_from_root_list(z)
        if z == z.right:
            self.min = self.root_list = None
        else:
            self.min = z.right
            self.consolidate()
        self.node_count -= 1
        return z

    def consolidate(self):
        check = [None] * int(math.log(self.node_count) * 2)
        nodes = [h for h in self.iterate(self.root_list)]
        for i in range(0, len(nodes)):
            x = nodes[i]
            d = x.degree
            while check[d] is not None:
                y = check[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                check[d] = None
                d += 1
            check[d] = x

        for node in check:
            if node is not None:
                if node.key < self.min.key:
                    self.min = node

    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.insert_as_child(x, y)
        x.degree += 1
        y.parent = x
        y.marked = False

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            return None
        node.key = new_key
        parent = node.parent
        if parent is not None and node.key < parent.key:
            self.cut(node, parent)
            self.cascading_cut(parent)
        if node.key < self.min.key:
            self.min = node

    def cut(self, node, parent):
        self.remove_from_child_list(parent, node)
        parent.degree -= 1
        self.insert_root_list(node)

    def cascading_cut(self, node):
        parent = node.parent
        if parent is not None:
            if node.marked is False:
                node.marked = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)

    def delete_node(self, node):
        self.decrease_key(node, -math.inf)
        self.extract_min()

    @staticmethod
    def iterate(root):
        node = stop = root
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def insert_root_list(self, node):
        node.marked = False
        node.parent = None
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    @staticmethod
    def insert_as_child(parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    @staticmethod
    def remove_from_child_list(parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left


if __name__ == '__main__':
    h = FibonacciHeap()
