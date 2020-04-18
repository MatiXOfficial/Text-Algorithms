import random
import string

alphabet = string.ascii_letters + string.digits

sizes = [1000, 10000, 100000, 1000000]
dirs = ['texts/text1kB_random', 'texts/text10kB_random', 'texts/text100kB_random', 'texts/text1MB_random']

for size, dir in zip(sizes, dirs):
    with open(dir, 'w') as file:
        for _ in range(size):
            file.write(random.choice(alphabet))