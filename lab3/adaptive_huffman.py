# pseudocode: https://en.wikipedia.org/wiki/Adaptive_Huffman_coding


from bitarray import bitarray

class Node:

    def __init__(self, left=None, right=None, parent=None, letter='##', count=0, index=0):
        self.left = left
        self.right = right
        self.parent = parent
        self.letter = letter
        self.count = count 
        self.index = index

    def __str__(self, indent=0, print_whole=True):
        res = indent * ' ' + f'({self.letter}, {self.count})\n'
        if print_whole:
            if self.left is not None:
                res += '(0)' + self.left.__str__(indent + 1)
            if self.right is not None:
                res += '(1)' + self.right.__str__(indent + 1)
        return res

    def __repr__(self):
        return '<class Node>' + self.__str__(print_whole=False)

    def is_leaf(self):
        return self.left is None and self.right is None

    def code(self):
        result = bitarray()
        node = self
        while node.parent is not None:
            if node == node.parent.left:
                result = bitarray('0') + result
            else:
                result = bitarray('1') + result
            node = node.parent
        return result

    def swap_nodes(self, other, index_arr):
        """
        Swaps nodes ant their indices in index_arr.
        """
        if self.parent == other.parent:
            if self == self.parent.left:
                self.parent.left = other
                self.parent.right = self
            else:
                self.parent.left = self
                self.parent.right = other
        else:
            if self == self.parent.left:
                self.parent.left = other
            else:
                self.parent.right = other
            if other == other.parent.left:
                other.parent.left = self
            else:
                other.parent.right = self
            self.parent, other.parent = other.parent, self.parent

        self.index, other.index = other.index, self.index
        index_arr[self.index], index_arr[other.index] = index_arr[other.index], index_arr[self.index]

        parent = self.parent        # Recalculating counts of parents, their parents etc.
        while parent is not None:
            parent.count = parent.left.count + parent.right.count
            parent = parent.parent
        parent = other.parent
        while parent is not None:
            parent.count = parent.left.count + parent.right.count
            parent = parent.parent

    def is_sibling_zero_node(self):
        if self.parent.left is None or self.parent.right is None:
            return False
        if self.parent.left.letter == '##':
            return True
        if self.parent.right.letter == '##':
            return True
        return False


class AdaptiveHuffman:

    def __init__(self):
        self.root = Node()
        self.index_arr = [self.root]
        self.nodes = {self.root.letter : self.root}

    def swap_with_leader(self, node, leader=None):
        """
        Swaps node with its block leader.
        """
        if leader is None:
            leader = self.find_block_leader(node)
        if node != leader:
            node.swap_nodes(leader, self.index_arr)
            if not node.is_leaf() and not leader.is_leaf():
                self.reset_order()

    def find_block_leader(self, node):
        leader = node
        leader_prev = node
        while node.count >= leader.count and leader.index < len(self.index_arr) - 1:
            if ((node.is_leaf() and leader.is_leaf()) or (not node.is_leaf() and leader.is_leaf())) \
                                                                        and not leader == node.parent:
                leader_prev = leader
            leader = self.index_arr[leader.index + 1]
        return leader_prev

    def reset_order(self):
        """
        Rebuilds the index_arr in order to restore proper order of the nodes.
        """
        idx = len(self.index_arr) - 1
        queue = []
        queue.append(self.root)
        while queue:
            node = queue.pop(0)
            self.index_arr[idx] = node
            node.index = idx
            idx -= 1
            if node.right is not None:
                queue.append(node.right)
            if node.left is not None:
                queue.append(node.left)

    def slide(self, node):
        """
        Finds the proper node to swap with.
        """
        leader = node
        leader_prev = node
        if not node.is_leaf():
            while node.count + 1 >= leader.count and leader.index < len(self.index_arr) - 1:
                if leader.is_leaf():
                    leader_prev = leader
                leader = self.index_arr[leader.index + 1]
        else:
            while node.count >= leader.count and leader.index < len(self.index_arr) - 1:
                if not leader.is_leaf():
                    leader_prev = leader
                leader = self.index_arr[leader.index + 1]

        self.swap_with_leader(node, leader=leader_prev)


    def slide_and_increment(self, node):
        prev_node = node.parent
        self.slide(node)
        node.count += 1
        if not node.is_leaf():
            return prev_node
        else:
            return node.parent



def encode(dir_from, dir_to):
    """
    Encodes file dir_from to dir_to.
    Puts a few 0s and 1 at the beginning of the result to
    make the file length multiple of 8.
    """
    h = AdaptiveHuffman()
    array = bitarray()
    with open(dir_from, 'r') as file_from:
        for line in file_from:
            for letter in line:
                leaf_to_increment = None

                if letter in h.nodes:
                    node = h.nodes[letter]
                    array += node.code()

                    h.swap_with_leader(node)
                    if node.is_sibling_zero_node():
                        leaf_to_increment = node
                        node = node.parent

                else:
                    node = h.nodes['##']
                    array += node.code()
                    array.fromstring(letter)

                    node.left = Node(parent=node)
                    h.nodes['##'] = node.left

                    node.right = Node(parent=node, letter=letter)
                    h.nodes[letter] = node.right

                    h.index_arr += [node.left, node.right]
                    h.reset_order()
                    leaf_to_increment = node.right

                while node is not None:
                    node = h.slide_and_increment(node)

                if leaf_to_increment is not None:
                    h.slide_and_increment(leaf_to_increment)


    with open(dir_to, 'wb') as file_to:
        extra_len = 7 - (len(array) - 1) % 8
        if extra_len > 0:
            array = bitarray((extra_len - 1) * '0' + '1') + array
        array.tofile(file_to)


def decode(dir_from, dir_to):
    with open(dir_from, 'rb') as file_from:
        array = bitarray()
        array.fromfile(file_from)

    if len(array) > 8:
        while not array[0]:
            array[:1] = bitarray()
        array[:1] = bitarray()

    h = AdaptiveHuffman()
    with open(dir_to, 'w') as file_to:
        node = h.root
        while (True):
            if node.is_leaf() and node.letter == '##':
                letter = array[:8]
                array[:8] = bitarray()
                letter = str(letter.tobytes().decode())
                file_to.write(letter)

                node.left = Node(parent=node)
                h.nodes['##'] = node.left

                node.right = Node(parent=node, letter=letter)
                h.nodes[letter] = node.right

                h.index_arr += [node.left, node.right]
                h.reset_order()
                leaf_to_increment = node.right

                while node is not None:
                    node = h.slide_and_increment(node)
                h.slide_and_increment(leaf_to_increment)

                node = h.root
                if not array:
                    break

            elif node.is_leaf():
                leaf_to_increment = None
                node = h.nodes[node.letter]         
                file_to.write(node.letter)

                h.swap_with_leader(node)
                if node.is_sibling_zero_node():
                    leaf_to_increment = node
                    node = node.parent

                while node is not None:
                    node = h.slide_and_increment(node)
                
                if leaf_to_increment is not None:
                    h.slide_and_increment(leaf_to_increment)

                node = h.root
                if not array:
                    break

            else:
                if array[0]:
                    node = node.right
                else:
                    node = node.left
                array = array[1:]