from edit_table import EditTable, lcs as lcs_table, diff
from lcs import lcs as fast_lcs

from spacy.tokenizer import Tokenizer
from spacy.lang.pl import Polish

import sys
import random

def delta(a, b):
    if a == b:
        return 0
    else:
        return 1


stdoutold = sys.stdout
sys.stdout = open('results.txt', 'w')

################## edit distance ############
pairs = [('los', 'kloc'),
         ('Łódź', 'Lodz'),
         ('kwintesencja', 'quintessence'),
         ('ATGAATCTTACCGCCTCG', 'ATGAGGCTCTGGCCCCTG')]

# 3.
print("------------ 3. -----------------")
for a, b in pairs:
    EditTable(a, b, delta).print_seq()
    print()


################## lcs ######################
random.seed(1234)
with open("romeo-i-julia-700.txt", "r", errors='ignore') as file:
    original_text = file.read()

tokenizer = Tokenizer(Polish().vocab)
tokens = tokenizer(original_text)

tokens_v1 = [token for token in tokens if random.random() > 0.03]
tokens_v2 = [token for token in tokens if random.random() > 0.03]

# 7.
print("---------------- 7. --------------")
print("tokens number:", len(tokens))
# print(lcs_table(tokens_v1, tokens_v2))
print(fast_lcs(tokens_v1, tokens_v2))


################## diff #####################
dir1 = 'text1.txt'
dir2 = 'text2.txt'
random.seed(1234)

lines = original_text.split('\n')

with open(dir1, 'w') as file1, open(dir2, 'w') as file2:
    for line in lines:
        tokens = tokenizer(line)

        tokens_v1 = [str(token) for token in tokens if random.random() > 0.03]
        file1.write(' '.join(tokens_v1))
        file1.write('\n')

        tokens_v2 = [str(token) for token in tokens if random.random() > 0.03]
        file2.write(' '.join(tokens_v2))
        file2.write('\n')

# 8.
print("\n------------ 8. ----------------")
diff(dir1, dir2)