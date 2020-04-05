class Node:

    text = ''

    def __init__(self, start=None, end=None, parent=None, depth=0, children=None):
        self.start = start
        self.end = end
        self.link = None
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

    def get_label(self, i=0):
        return self.text[self.start + i:self.end]

    def add_child(self, start, end):
        new_node = Node(start, end, self, self.depth + self.end - self.start)
        self.children.append(new_node)
        return new_node

    def find_child_by_first(self, val):
        for child in self.children:
            if self.text[child.start] == val:
                return child
        return None

    def break_path(self, length):
        new_node = Node(start=self.start + length, end=self.end, parent=self, 
                        depth=self.depth + length, children=self.children)
        self.end = new_node.start
        self.children = [new_node]

    def slow_find(self, suffix):
        child = self.find_child_by_first(suffix[0])
        if child is None:
            return self
        for i in range(child.start + 1, child.end):
            if self.text[i] != suffix[i - child.start]:
                child.break_path(i - child.start)
                return child
        return child.slow_find(suffix[len(child):])

    def fast_find(self, suffix):
        child = self.find_child_by_first(suffix[0])
        if child is None:
            return self
        if len(suffix) > len(child):
            return child.fast_find(suffix[len(child):])
        if len(suffix) == len(child):
            return child
        child.break_path(len(suffix))
        return child


class SuffixTree:

    def __init__(self, text=None, root=None):
        self.root = root
        if text is not None:
            self.mccreight(text)

    def __str__(self, indent=0):
        if self.root is None:
            return 'Empty tree'
        else:
            return self.root.__str__()

    def __repr__(self):
        return "<class SuffixTree>\n" + self.__str__()

    def mccreight(self, text):
        self.text = text
        Node.text = text
        n = len(text)
        self.root = Node(0, 0)
        self.root.add_child(0, n)

        last_head = self.root
        leaf = self.root.children[0]

        for i in range(1, n):
            suffix = text[i:]
            if last_head == self.root:
                head = self.root.slow_find(suffix)
                leaf = head.add_child(i + head.depth + len(head), n)
                last_head = head
            else:
                parent = last_head.parent
                if parent == self.root:
                    if len(last_head) == 1:
                        node = self.root
                    else:
                        node = self.root.fast_find(last_head.get_label(1))
                else:
                    node = parent.link.fast_find(last_head.get_label())
                if len(node.children) == 1:
                    head = node
                else:
                    head = node.slow_find(leaf.get_label())
                leaf = head.add_child(i + head.depth + len(head), n)
                last_head.link = node
                last_head = head

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
            node = node.find_child_by_first(word[node.depth + node.end - node.start])
        return False