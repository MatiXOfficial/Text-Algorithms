import unittest
from text import Text


class Tests(unittest.TestCase):

    texts = [Text('bbb$'),
             Text('aabbabd'),
             Text('ababcd'),
             Text('abcbccd'),
             Text(filename='1997_714.txt')]

    def test_trie_factorin(self):
        self.assertTrue(self.texts[0].factor_in('bbb'))
        self.assertFalse(self.texts[0].factor_in('bbbb'))

        self.assertTrue(self.texts[1].factor_in('bbab'))
        self.assertFalse(self.texts[1].factor_in('abbb'))

        self.assertTrue(self.texts[2].factor_in('d'))
        self.assertFalse(self.texts[2].factor_in('e'))

        self.assertTrue(self.texts[3].factor_in('ccd'))
        self.assertFalse(self.texts[3].factor_in('accd'))

        self.assertTrue(self.texts[4].factor_in('Ustawa', end=1000))
        self.assertTrue(self.texts[4].factor_in('fizyczne'))
        self.assertTrue(self.texts[4].factor_in('Ustawa reguluje opodatkowanie'))
        self.assertTrue(self.texts[4].factor_in('20 listopada'))
        self.assertFalse(self.texts[4].factor_in('kruszwil'))
        self.assertFalse(self.texts[4].factor_in('20listopada'))
        self.assertFalse(self.texts[4].factor_in('ziemniaki'))

    def test_factorin_tree_slow(self):
        self.assertTrue(self.texts[0].factor_in('bbb', mode='tree_slow'))
        self.assertFalse(self.texts[0].factor_in('bbbb', mode='tree_slow'))

        self.assertTrue(self.texts[1].factor_in('bbab', mode='tree_slow'))
        self.assertFalse(self.texts[1].factor_in('abbb', mode='tree_slow'))

        self.assertTrue(self.texts[2].factor_in('d', mode='tree_slow'))
        self.assertFalse(self.texts[2].factor_in('e', mode='tree_slow'))

        self.assertTrue(self.texts[3].factor_in('ccd', mode='tree_slow'))
        self.assertFalse(self.texts[3].factor_in('accd', mode='tree_slow'))

        self.assertTrue(self.texts[4].factor_in('Ustawa', mode='tree_slow', end=50000))
        self.assertTrue(self.texts[4].factor_in('fizyczne', mode='tree_slow'))
        self.assertTrue(self.texts[4].factor_in('Ustawa reguluje opodatkowanie', mode='tree_slow'))
        self.assertTrue(self.texts[4].factor_in('20 listopada', mode='tree_slow'))
        self.assertFalse(self.texts[4].factor_in('kruszwil', mode='tree_slow'))
        self.assertFalse(self.texts[4].factor_in('20listopada', mode='tree_slow'))
        self.assertFalse(self.texts[4].factor_in('ziemniaki', mode='tree_slow'))

    def test_factorin_tree_fast(self):
        self.assertTrue(self.texts[0].factor_in('bbb', mode='tree_fast'))
        self.assertFalse(self.texts[0].factor_in('bbbb', mode='tree_fast'))

        self.assertTrue(self.texts[1].factor_in('bbab', mode='tree_fast'))
        self.assertFalse(self.texts[1].factor_in('abbb', mode='tree_fast'))

        self.assertTrue(self.texts[2].factor_in('d', mode='tree_fast'))
        self.assertFalse(self.texts[2].factor_in('e', mode='tree_fast'))

        self.assertTrue(self.texts[3].factor_in('ccd', mode='tree_fast'))
        self.assertFalse(self.texts[3].factor_in('accd', mode='tree_fast'))

        self.assertTrue(self.texts[4].factor_in('Ustawa', mode='tree_fast', end=100000))
        self.assertTrue(self.texts[4].factor_in('gastronomiczna', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('o podatku dochodowym', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('jest prowadzona w formie', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('Zrzeczenia', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('konserw oraz', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('prezerw z ryb', mode='tree_fast'))
        self.assertTrue(self.texts[4].factor_in('zakwalifikowanych przez komisje etnograficzno-artystyczne', mode='tree_fast'))
        self.assertFalse(self.texts[4].factor_in('kruszwil', mode='tree_fast'))
        self.assertFalse(self.texts[4].factor_in('20listopada', mode='tree_fast'))
        self.assertFalse(self.texts[4].factor_in('ziemniaki', mode='tree_fast'))


if __name__ == "__main__":
    unittest.main()