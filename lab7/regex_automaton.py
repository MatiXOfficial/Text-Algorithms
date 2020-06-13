# Implementation based on the algorithms from the book:
# M. Crochemore, W. Rytter, "Text Algorithms", 157-165.

import string

class Automaton:
    """
    This class represents a normalized automaton.
    """

    def __init__(self, table=None):
        if table is not None:
            self.table = table
        else:
            self.table = []
        self.accepting_state = len(table) - 1

    def __getitem__(self, idx):
        return self.table[idx]

    def __len__(self):
        return len(self.table)

    def __str__(self):
        result = ''
        for i, row in enumerate(self):
            result += f'{i}: {row}\n'
        return result

    def concatenate(self, other):
        """
        Returns a new automaton: self concatenated with other.
        """
        result = [self[i].copy() for i in range(len(self) - 1)]
        for i in range(len(other)):
            result += [[(char, idx + len(self) - 1) for char, idx in other[i]]]  

        return Automaton(result)

    def star(self):
        """
        Returns a new automaton: self* which is self 0 or more times.
        """
        result = [[('empty', 1), ('empty', 1 + len(self))]]

        for i in range(len(self) - 1):
            result += [[(char, idx + 1) for char, idx in self[i]]]

        result += [[('empty', 1), ('empty', 1 + len(self))], []]
        return Automaton(result)

    def plus(self):
        """
        Returns a new automaton: self+ which is self 1 or more times.
        """
        result = [[('empty', 1)]]

        for i in range(len(self) - 1):
            result += [[(char, idx + 1) for char, idx in self[i]]]

        result += [[('empty', 1), ('empty', 1 + len(self))], []]
        return Automaton(result)

    def question_mark(self):
        """
        Returns a new automaton: self? which is self 0 or 1 time.
        """
        result = [[('empty', 1), ('empty', 1 + len(self))]]

        for i in range(len(self) - 1):
            result += [[(char, idx + 1) for char, idx in self[i]]]

        result += [[('empty', 1 + len(self))], []]
        return Automaton(result)

    def test_word(self, x):
        """
        Returns True if the word x belongs to the language of the automaton
        """
        S = self.closure({0})
        for a in x:
            S = self.closure(self.trans(S, a))
        if self.accepting_state in S:
            return True
        else:
            return False
        
    def closure(self, S):
        """
        Returns a set which is a closure of the set S, which is given as an argument.
        Closure of the set S is a set T consisting of those q that
        there exists an empty-path in the automaton from a state of S to q.
        """
        T = S.copy()
        File = S.copy()
        while File:
            p = File.pop()
            if self.table[p]:
                for letter, q in self.table[p]:
                    if letter == 'empty':
                        T.add(q)
                        File.add(q)
        return T

    def trans(self, S, letter):
        """
        Returns a set of those states q for which there exists a 
        non-empty transition in the automaton from a state from S to q. 
        """
        T = set()
        for p in S:
            if self.table[p]:
                l, q = self.table[p][0]
                if (l == letter or l == 'dot' or
                    l == '\\d' and letter.isnumeric() or
                    l == '\\D' and not letter.isnumeric() or
                    l == '\\w' and letter.isalnum() or
                    l == '\\W' and not letter.isalnum() or
                    l == '\\s' and letter.isspace() or
                    l == '\\S' and not letter.isspace() or
                    l == '\\n' and letter == '\n' or
                    l == '\\t' and letter == '\t' or
                    type(l) == set and letter in l):

                    T.add(q)
        return T

    def find(self, text):
        """
        Searches text for regular expressions represented by the automaton.
        Returns a list of indices in text where the suitable expressions end.
        """
        S = self.closure({0})
        result = []
        for i, a in enumerate(text):
            S = self.closure(self.trans(S, a) | {0})
            if self.accepting_state in S:
                result += [i]
        return result
            

class StringIterator:
    """
    Auxiliary class that will keep the current character 
    of the regex while building the automaton. This class also
    contains a few auxiliary methods: expr, term and factor
    that will be useful while building the automaton.
    """

    symbols = set(['*', '+', '?', ')', ']', None])

    def __init__(self, e):
        self.e = e
        self.i = 0
        self.char = e[0]

    def next(self):
        self.i += 1
        if self.i < len(self.e):
            self.char = self.e[self.i]
        else:
            self.char = None 

    def expr(self):
        G = self.term()
        return G

    def term(self):
        G = self.factor()
        while self.char not in self.symbols:
            H = self.factor()
            G = G.concatenate(H)
        return G

    def factor(self):
        if self.char == '(':
            self.next()
            G = self.expr()
        elif self.char == '[':
            S = set()
            self.next()
            while self.char != ']':
                S.add(self.char)
                self.next()
            G = Automaton([[(S, 1)], []])
        elif self.char == '.':
            G = Automaton([[('dot', 1)], []])
        elif self.char == '\\':
            self.next()
            G = Automaton([[(f'\\{self.char}', 1)], []])
        elif self.char not in self.symbols:
            G = Automaton([[(self.char, 1)], []])
        else:
            raise ValueError("invalid expression")
        self.next()

        if self.char == '*':
            G = G.star()
            while self.char == '*':
                self.next()
        elif self.char == '+':
            G = G.plus()
            while self.char == '+':
                self.next()
        elif self.char == '?':
            G = G.question_mark()
            while self.char == '?':
                self.next()

        return G


def build_automaton(regex):
    """
    Returns an automaton build using a regular expression
    given as an argument: regex.
    
    It can consist of:
    1. letters, digits and whitespace charactes,
    2. dot (.) representing any character,
    3. * (0 or more), + (1 or more), ? (0 or 1),
    4. parentheses () (can be nested),
    5. charater classes:
        - characters between [] (e.g. [abc]),
        - \\d - matches any decimal digit,
        - \\D - matches any non-digit character
        - \\s - matches any whitespace character,
        - \\S - matches any non-whitespace character,
        - \\w - matches any alphanumeric character,
        - \\W - matches any non-alphanumeric character;
    """
    if not regex:
        return Automaton([])
    e = StringIterator(regex)
    G = e.term()
    if e.char != None:
        raise ValueError("invalid expression")
    return G

def regex_find(text, regex):
    """
    Builds an automaton based on regex and searches text 
    for regular expressions represented by the automaton.
    Returns a list of indices in text where the suitable expressions end.
    """
    A = build_automaton(regex)
    return A.find(text)

def regex_print_find(text, regex):
    """
    Builds an automaton based on regex and searches text 
    for regular expressions represented by the automaton.
    Prints text with the suitable expressions being marked.
    """
    A = build_automaton(regex)
    indices = A.find(text)
    add = 1
    for i in indices:
        text = text[:(i + add)] + '[<--HERE]' + text[(i + add):]
        add += 9
    print(f'{len(indices)} occurrences of \"{regex}\"')
    print(text)