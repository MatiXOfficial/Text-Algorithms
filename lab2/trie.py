class Node:

    def __init__(self, value=None, parent=None, depth=0, children=None):
        self.value = value
        self.link = None
        if children is None:
            self.children = []
        else:
            self.children = children
        self.parent = parent
        self.depth = depth

    def __str__(self, indent=0):
        res = indent * ' ' + str(indent) + ':' + str(self.value)
        for child in self.children:
            res += '\n' + child.__str__(indent + 1)
        return res

    def __repr__(self):
        return "<class Node>\n" + self.__str__()

    def add_child(self, new_value):
        new_node = Node(new_value, self, self.depth + 1)
        self.children.append(new_node)
        return new_node

    def find_child(self, val):
        for child in self.children:
            if child.value == val:
                return child
        return None

    def up_link_down(self):
        values = []
        sibling = self
        while sibling is not None and sibling.link is None:
            values.append(sibling.value)
            sibling = sibling.parent
        if sibling is None:
            return None, None
        node = sibling.link
        while values:
            current_value = values.pop()
            new_node = node.find_child(current_value)
            if new_node is not None:
                node = new_node
                sibling = sibling.find_child(current_value)
                sibling.link = node
            else:
                break
        return node, sibling

    def graft(self, suffix, sibling=None):
        current_node = self
        for val in suffix:
            current_node = current_node.add_child(val)
            if sibling is not None:
                sibling = sibling.find_child(val)
                sibling.link = current_node
        return current_node


class Trie:

    def __init__(self, text=None, root=None):
        self.root = root
        if text is not None:
            self.left_to_right(text)

    def __str__(self, indent=0):
        if self.root is None:
            return 'Empty trie'
        else:
            return self.root.__str__()

    def __repr__(self):
        return "<class Trie>\n" + self.__str__()

    def left_to_right(self, text):
        self.root = Node('root')
        leaf = self.root.graft(text)
        self.root.children[0].link = self.root
        for i in range(1, len(text)):
            head, sibling = leaf.up_link_down()
            if head is None:
                sibling = self.root.find_child(text[i-1])
                sibling.link = self.root
                head, sibling = leaf.up_link_down()
            leaf = head.graft(text[i+head.depth:], sibling)

    def factor_in(self, word):
        node = self.root
        for val in word:
            node = node.find_child(val)
            if node is None:
                return False
        return True