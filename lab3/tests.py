import unittest
import string
import random
import filecmp
import os
from huffman import encode as static_encode, decode as static_decode
from adaptive_huffman import encode as adaptive_encode, decode as adaptive_decode


class Test(unittest.TestCase):

    def test_static(self):
        for file in os.listdir('files/texts'):
            dir = f'files/texts/{file}'
            enc_dir = f'files/encoded/{file}'
            dec_dir = f'files/decoded/{file}'
            static_encode(dir, enc_dir)
            static_decode(enc_dir, dec_dir)
            self.assertTrue(filecmp.cmp(dir, dec_dir))

    def test_adaptive(self):
        for file in os.listdir('files/texts'):
            dir = f'files/texts/{file}'
            if os.path.getsize(dir) <= 10000:
                enc_dir = f'files/encoded/{file}'
                dec_dir = f'files/decoded/{file}'
                adaptive_encode(dir, enc_dir)
                adaptive_decode(enc_dir, dec_dir)
                self.assertTrue(filecmp.cmp(dir, dec_dir))


if __name__ == "__main__":
    unittest.main()