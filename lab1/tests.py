from string_matching_algorithms import *
import time

def find_speed(string_matching, text_source, pattern):
    start = time.time()
    result = string_matching(text_source, pattern)
    end = time.time()
    return (result, end - start)

def compare_algorithms(title, text_source, pattern):
    print(title, ':', sep='')
    naiv = find_speed(naiv_string_matching, text_source, pattern)
    print("finished naiv")
    fa = find_speed(fa_string_matching, text_source, pattern)
    print("finished fa")
    kmp = find_speed(kmp_string_matching, text_source, pattern)
    print("finished kmp")
    print ("Good results: ", naiv[0] == fa[0] == kmp[0])
    print("naiv:", naiv[1])
    print("fa:", fa[1])
    print("kmp:", kmp[1])

def find_speed_pre(fun, pattern):
    start = time.time()
    fun(pattern)
    end = time.time()
    return end - start

def compare_preprocessing(title, pattern):
    print(title, ':', sep='')
    print("transition table (old):", find_speed_pre(transition_table_old, pattern))
    print("transition table:", find_speed_pre(transition_table, pattern))
    print("prefix function: ", find_speed_pre(prefix_function, pattern))


# compare_algorithms('Ustawa', 'lab1/ustawa.txt', 'art')    # zad. 4

# compare_algorithms('Wikipedia', 'lab1/wikipedia-tail-kruszwil.txt', 'kruszwil')   # zad. 5


with open('lab1/ustawa.txt', 'r', errors='ignore') as file:
    ustawa = file.read()

# compare_algorithms('Ustawa - długi wzorzec', 'lab1/ustawa.txt', 'a' * (len(ustawa) // 10))  # zad. 6


import string
import random

alphabet = string.ascii_letters + string.digits
pattern = ''
for i in range(1000):
    pattern += random.choice(alphabet)

compare_preprocessing('Duża wielkosć alfabetu', pattern) # zad. 7