class Node:

    text = ''

    def __init__(self, start=None, end=None, parent=None, depth=0, children=None):
        self.start = start
        self.end = end
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.depth = depth

    def __str__(self, indent=0):
        res = indent * ' ' + str(indent) + '-' + str(self.start) + ':' + str(self.end)
        for child in self.children:
            res += '\n' + child.__str__(indent + 1)
        return res

    def __repr__(self):
        return "<class Node>\n" + self.__str__()

    def __len__(self):
        return self.end - self.start

    def add_child(self, start, end):
        new_node = Node(start, end, self, self.depth + len(self))
        self.children.append(new_node)
        return new_node

    def find_child_by_first(self, val):
        for child in self.children:
            if self.text[child.start] == val:
                return child
        return None

    def break_path(self, child, length):
        new_node = Node(child.start + length, child.end, child, child.depth + length, child.children)
        child.end = new_node.start
        child.children = [new_node]

    def slow_find(self, suffix):
        child = self.find_child_by_first(suffix[0])
        if child is None:
            return self
        for i in range(child.start + 1, child.end):
            if self.text[i] != suffix[i - child.start]:
                self.break_path(child, i - child.start)
                return child
        return child.slow_find(suffix[len(child):])


class SuffixTree:

    def __init__(self, text=None, root=None):
        self.root = root
        if text is not None:
            self.build_tree(text)

    def __str__(self, indent=0):
        if self.root is None:
            return 'Empty tree'
        else:
            return self.root.__str__()

    def __repr__(self):
        return "<class SuffixTree>\n" + self.__str__()

    def build_tree(self, text):
        self.text = text
        Node.text = text
        n = len(text)
        self.root = Node(0, 0)
        self.root.add_child(0, n)
        for i in range(1, n):
            suffix = text[i:]
            head = self.root.slow_find(suffix)
            head.add_child(i + head.depth + len(head), n)

    def factor_in(self, word):
        node = self.root.find_child_by_first(word[0])
        while node is not None:
            for i in range(node.start + 1, node.end):
                if node.depth + i - node.start == len(word):
                    return True
                if self.text[i] != word[node.depth + i - node.start]:
                    return False
            if node.depth + node.end - node.start == len(word):
                return True
            node = node.find_child_by_first(word[node.depth + len(node)])
        return False