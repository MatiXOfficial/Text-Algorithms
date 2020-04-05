from trie import Trie
from suffix_tree_slow import SuffixTree as SuffixTreeSlow
from suffix_tree_fast import SuffixTree as SuffixTreeFast

class Text:

    def __init__(self, string=None, filename=None):
        if string is not None and filename is None:
            self.text = string
        elif filename is not None and string is None:
            with open(filename, 'r', errors='ignore') as file:
                self.text = file.read()
        else:
            raise ValueError("Either string or filename necessary!")
        if self.text[-1] in self.text[:-1]:
            self.text += '\0'
        self.trie = None
        self.suffix_tree_slow = None
        self.suffix_tree_fast = None

    def __len__(self):
        return len(self.text)

    def __getitem__(self, i):
        return self.text[i]

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<class Text> ' + self.text

    def factor_in(self, word, mode='trie', end=None):
        if mode == 'trie':
            if self.trie is None:
                if end is None:
                    self.trie = Trie(self.text)
                else:
                    self.trie = Trie(self.text[:end] + '\0')
            return self.trie.factor_in(word)
        elif mode == 'tree_slow':
            if self.suffix_tree_slow is None:
                if end is None:
                    self.suffix_tree_slow = SuffixTreeSlow(self.text)
                else:
                    self.suffix_tree_slow = SuffixTreeSlow(self.text[:end] + '\0')
            return self.suffix_tree_slow.factor_in(word)
        elif mode == 'tree_fast':
            if self.suffix_tree_fast is None:
                if end is None:
                    self.suffix_tree_fast = SuffixTreeFast(self.text)
                else:
                    self.suffix_tree_fast = SuffixTreeFast(self.text[:end] + '\0')
            return self.suffix_tree_fast.factor_in(word)
        else:
            raise ValueError('Wrong mode!')