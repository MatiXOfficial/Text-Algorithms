import unittest
import string
import random
import filecmp
from huffman import encode as static_encode, decode as static_decode


class Test(unittest.TestCase):

    dirs = ['files/texts/test1', 'files/texts/test2', 'files/texts/test3', 'files/texts/test4', 'files/texts/text1kB', 'files/texts/text10kB', 'files/texts/text100kB', 'files/texts/text1MB']
    encoded_dirs = ['files/encoded/test1', 'files/encoded/test2', 'files/encoded/test3', 'files/encoded/test4', 'files/encoded/text1kB', 'files/encoded/text10kB', 'files/encoded/text100kB', 'files/encoded/text1MB']
    decoded_dirs = ['files/decoded/test1', 'files/decoded/test2', 'files/decoded/test3', 'files/decoded/test4', 'files/decoded/text1kB', 'files/decoded/text10kB', 'files/decoded/text100kB', 'files/decoded/text1MB']

    def test_static(self):
        for dir, enc_dir, dec_dir in zip(self.dirs, self.encoded_dirs, self.decoded_dirs):
            static_encode(dir, enc_dir)
            static_decode(enc_dir, dec_dir)
            self.assertTrue(filecmp.cmp(dir, dec_dir))


if __name__ == "__main__":
    unittest.main()