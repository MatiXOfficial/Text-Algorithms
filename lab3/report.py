from matplotlib import pyplot as plt
import string
import random
import time
import os
from huffman import encode as static_encode, decode as static_decode
from adaptive_huffman import encode as adaptive_encode, decode as adaptive_decode


def find_time(algorithm, dir_from, dir_to):
    start = time.time()
    algorithm(dir_from, dir_to)
    end = time.time()
    return end - start


############ Compression ratio #########################

plt.title('Compression ratio')
extra_label = 'natural'
max_size = 1000000

sizes = []
ratios = []
for file in os.listdir('files/texts'):
    dir = f'files/texts/{file}'
    if extra_label in file and os.path.getsize(dir) <= max_size:
        enc_dir = f'files/encoded/{file}'
        static_encode(dir, enc_dir)
        sizes.append(os.path.getsize(dir))
        ratios.append(1 - os.path.getsize(enc_dir) / os.path.getsize(dir))

sizes, ratios = zip(*sorted(zip(sizes, ratios)))
plt.plot(sizes, ratios, label='static huffman')

sizes = []
ratios = []
for file in os.listdir('files/texts'):
    dir = f'files/texts/{file}'
    if extra_label in file and os.path.getsize(dir) <= max_size:
        enc_dir = f'files/encoded/{file}'
        adaptive_encode(dir, enc_dir)
        sizes.append(os.path.getsize(dir))
        ratios.append(1 - os.path.getsize(enc_dir) / os.path.getsize(dir))

sizes, ratios = zip(*sorted(zip(sizes, ratios)))
plt.plot(sizes, ratios, label='adaptive huffman')

plt.ylim(0, 1)
plt.xscale("log")
plt.grid()
plt.legend()
plt.show()


########## Encoding time comparison ######################

# plt.title('Encoding time')
# extra_label = 'natural'
# max_size = 1000000

# sizes = []
# times = []
# for file in os.listdir('files/texts'):
#     dir = f'files/texts/{file}'
#     if extra_label in file and os.path.getsize(dir) <= max_size:
#         enc_dir = f'files/encoded/{file}'
#         sizes.append(os.path.getsize(dir))
#         times.append(find_time(static_encode, dir, enc_dir))

# sizes, times = zip(*sorted(zip(sizes, times)))
# plt.plot(sizes, times, label='static huffman', marker='o')

# sizes = []
# times = []
# for file in os.listdir('files/texts'):
#     dir = f'files/texts/{file}'
#     if extra_label in file and os.path.getsize(dir) <= max_size:
#         enc_dir = f'files/encoded/{file}'
#         sizes.append(os.path.getsize(dir))
#         times.append(find_time(adaptive_encode, dir, enc_dir))

# sizes, times = zip(*sorted(zip(sizes, times)))
# plt.plot(sizes, times, label='adaptive huffman', marker='o')

# plt.grid()
# plt.legend()
# plt.show()

######### Decoding time comparison #######################

# plt.title = 'Decoding time'
# extra_label = 'natural'
# max_size = 10000

# sizes = []
# times = []
# for file in os.listdir('files/texts'):
#     dir = f'files/texts/{file}'
#     if extra_label in file and os.path.getsize(dir) <= max_size:
#         enc_dir = f'files/encoded/{file}'
#         dec_dir = f'files/decoded/{file}'
#         sizes.append(os.path.getsize(dir))
#         static_encode(dir, enc_dir)
#         times.append(find_time(static_decode, enc_dir, dec_dir))

# sizes, times = zip(*sorted(zip(sizes, times)))
# plt.plot(sizes, times, label='static huffman', marker='o')

# sizes = []
# times = []
# for file in os.listdir('files/texts'):
#     dir = f'files/texts/{file}'
#     if extra_label in file and os.path.getsize(dir) <= max_size:
#         enc_dir = f'files/encoded/{file}'
#         dec_dir = f'files/decoded/{file}'
#         sizes.append(os.path.getsize(dir))
#         adaptive_encode(dir, enc_dir)
#         times.append(find_time(adaptive_decode, enc_dir, dec_dir))

# sizes, times = zip(*sorted(zip(sizes, times)))
# plt.plot(sizes, times, label='static huffman', marker='o')

# plt.grid()
# plt.legend()
# plt.show()