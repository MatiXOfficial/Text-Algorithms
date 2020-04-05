from text import Text
import time

from trie import Trie
from suffix_tree_slow import SuffixTree as SuffixTreeSlow
from suffix_tree_fast import SuffixTree as SuffixTreeFast

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def find_time(algorithm, text):
    start = time.time()
    algorithm(text)
    end = time.time()
    return end - start

texts = [Text(filename='1997_714.txt'),
         'a' * 1000000,
         'abcde' * 200000]

t = texts[2]

trie_x = [100 * 2 ** i for i in range(12)]
trie_y = [find_time(Trie, t[:x] + '\0') for x in trie_x]

tree_slow_x = [100 * 2 ** i for i in range(8)]
tree_slow_y = [find_time(SuffixTreeSlow, t[:x] + '\0') for x in tree_slow_x]

tree_fast_x = [100 * 2 ** i for i in range(12)]
tree_fast_y = [find_time(SuffixTreeFast, t[:x] + '\0') for x in tree_fast_x]


fig, ax = plt.subplots(2, 2)
ax[0, 0].plot(trie_x, trie_y, label="trie")
ax[0, 1].plot(tree_slow_x, tree_slow_y, label="slow sufix tree", color='C1')
ax[1, 0].plot(tree_fast_x, tree_fast_y, label="fast sufix tree", color='C2')
ax[1, 1].plot(trie_x, trie_y, label="trie")
ax[1, 1].plot(tree_slow_x, tree_slow_y, label="slow sufix tree")
ax[1, 1].plot(tree_fast_x, tree_fast_y, label="fast sufix tree")

ax[0, 0].legend()
ax[0, 1].legend()
ax[1, 0].legend()
ax[1, 1].legend()

plt.show()