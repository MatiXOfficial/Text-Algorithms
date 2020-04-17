from bitarray import bitarray

class Node:

    def __init__(self, left=None, right=None, letter='', count=0):
        self.left = left
        self.right = right
        self.letter = letter
        self.count = count

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

    def get_letter_codes(self, current_code=bitarray()):
        letter_codes = {}
        if self.letter:
            letter_codes[self.letter] = current_code
        if self.left is not None:
            letter_codes.update(self.left.get_letter_codes(current_code + bitarray('0')))
        if self.right is not None:
            letter_codes.update(self.right.get_letter_codes(current_code + bitarray('1')))
        return letter_codes

    def get_tree_structure(self):
        """
        Builds a bitarray representing the tree structure ready to be written to a file.
        The idea is to traverse the tree in pre-order.

        When we encounter an internal_node, we add bit '1' to the result and 
        proceed with the pre-order traversal.

        Else, when we encounter a leaf, we add bit '0' and ascii code of the leaf's 
        letter to the result and go back to the proper internal node
        """
        if self.is_leaf():
            result = bitarray('0')
            result.fromstring(self.letter)
        else:
            result = bitarray('1')
            result += self.left.get_tree_structure()
            result += self.right.get_tree_structure()
        return result


class Huffman:
    
    def __init__(self, freq=None, array=None):
        if freq is not None:
            self.freq = freq
            self.root = self._build_huffman_tree()
        else:
            self.root = self._decode_huffman_tree(array)

    def _build_huffman_tree(self):
        leafs = [Node(letter=l, count=c) for (l, c) in self.freq]
        internal_nodes = []
        while len(leafs) + len(internal_nodes) > 1:
            head = leafs[:min(2, len(leafs))]                       # max two leafs with lowest counts
            head += internal_nodes[:min(2, len(internal_nodes))]    # max two internal nodes with lowest counts

            left, right = sorted(head, key=lambda node : node.count)[:2]    # two nodes with lowest counts
            internal_nodes.append(Node(left=left, right=right, count=left.count + right.count))

            if len(leafs) > 0 and left == leafs[0]:
                leafs.pop(0)
            else:
                internal_nodes.pop(0)
            if len(leafs) > 0 and right == leafs[0]:
                leafs.pop(0)
            else:
                internal_nodes.pop(0)

        if internal_nodes:
            return internal_nodes[0]
        else:   # if there is only one letter in the tree
            return Node(left=leafs[0], right=leafs[0], count=leafs[0].count)

    def get_letter_codes(self):
        return self.root.get_letter_codes()

    def get_tree_structure(self):
        return self.root.get_tree_structure()

    def _decode_huffman_tree(self, array):
        root = Node()
        stack = [root]
        array[:1] = bitarray()
        while stack:
            bit = array[0]
            array[:1] = bitarray()
            node = stack.pop()
            if bit:         # internal node
                if node.left is None:
                    node.left = Node()
                    stack.append(node)
                    stack.append(node.left)
                else:
                    node.right = Node()
                    stack.append(node.right)
            else:           # leaf
                if node.left is None:
                    letter = array[:8]
                    array[:8] = bitarray()
                    node.left = Node(letter=letter.tobytes().decode())
                    stack.append(node)
                else:
                    letter = array[:8]
                    array[:8] = bitarray()
                    node.right = Node(letter=letter.tobytes().decode())
        return root

    def decode_to_file(self, array, dir):
        node = self.root
        with open(dir, 'w') as file:
            for bit in array:
                if bit:
                    node = node.right
                else:
                    node = node.left
                if node.is_leaf():
                    file.write(str(node.letter))
                    node = self.root



def encode(dir_from, dir_to):
    """
    Encodes the text in dir_from using static Huffman compression.
    Saves the compressed text with the Huffman tree structure to dir_to.
    """
    freq = count_letters(dir_from)
    huffman_tree = Huffman(freq)
    letter_codes = huffman_tree.get_letter_codes()

    with open(dir_from, 'r') as file_from, open(dir_to, 'wb') as file_to:
        array = bitarray()
        array += huffman_tree.get_tree_structure()
        for line in file_from:
            for letter in line:
                array += letter_codes[letter]
        extra_len = 7 - (len(array) - 1) % 8
        array = bitarray(extra_len * '0') + array # Adds extra 0s at the beginning of array to avoid adding them to the end
        array.tofile(file_to)

def count_letters(dir):
    """
    Returns a list of tuples with letters and their counts.
    """
    freq = {}
    with open(dir, 'r') as file:
        for line in file:
            for letter in line:
                freq[letter] = freq.get(letter, 0) + 1
    freq = list(freq.items())
    freq.sort(key=lambda tup : tup[1])
    return freq
    
def decode(dir_from, dir_to):
    with open(dir_from, 'rb') as file_from:
        array = bitarray()
        array.fromfile(file_from)
        while not array[0]:
            array[:1] = bitarray()
    huffman = Huffman(array=array)
    huffman.decode_to_file(array, dir_to)