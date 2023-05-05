import unittest

from unicode import Unicode, Granularity


class UnicodeTest(unittest.TestCase):
    def test_nfc(self):
        # empty string
        self.assertEqual('', Unicode.nfc(''))

        # ascii string
        for actual, expected in [('a', 'a'), ('G', 'G')]:
            self.assertEqual(Unicode.nfc(actual), expected)

        # unicode string
        for actual, expected in [('é', 'é'), ('café', 'café'), ('cafe\u0301', 'café')]:
            self.assertEqual(Unicode.nfc(actual), expected)

        # special characters
        for actual, expected in [('\u212B', 'Å'), ('Ω', 'Ω'), ('ℵ', 'ℵ')]:
            self.assertEqual(Unicode.nfc(actual), expected)

        # edge case
        for actual, expected in [('\u1E9B\u0323', 'ẛ̣'), ('\uFEFF', '\uFEFF'), ('\u2060', '\u2060')]:
            self.assertEqual(Unicode.nfc(actual), expected)

    def test_nfd(self):
        # empty string
        self.assertEqual('', Unicode.nfd(''))

        # ascii string
        for actual, expected in [('a', 'a'), ('G', 'G')]:
            self.assertEqual(Unicode.nfd(actual), expected)

        # unicode string
        for actual, expected in [('é', 'é'), ('café', 'café'), ('cafe\u0301', 'café')]:
            self.assertEqual(Unicode.nfd(actual), expected)

        # special characters
        for actual, expected in [('\u212B', 'Å'), ('Ω', 'Ω'), ('ℵ', 'ℵ')]:
            self.assertEqual(Unicode.nfd(actual), expected)

        # edge case
        for actual, expected in [('\u1E9B\u0323', 'ẛ̣'), ('\uFEFF', '\uFEFF'), ('\u2060', '\u2060')]:
            self.assertEqual(Unicode.nfd(actual), expected)

    def test_nfk_c(self):
        # empty string
        self.assertEqual('', Unicode.nfk_c(''))

        # ascii string
        for actual, expected in [('a', 'a'), ('G', 'G')]:
            self.assertEqual(Unicode.nfk_c(actual), expected)

        # unicode string
        for actual, expected in [('é', 'é'), ('café', 'café'), ('cafe\u0301', 'café'), ('Å', 'Å'), ('æ', 'æ'),
                                 ('ﬃ', 'ffi')]:
            self.assertEqual(Unicode.nfk_c(actual), expected)

        # special characters
        for actual, expected in [('\u212B', 'Å'), ('Ω', 'Ω'), ('ℵ', 'א')]:
            self.assertEqual(Unicode.nfk_c(actual), expected)

        # edge case
        for actual, expected in [('\u1E9B\u0323', 'ṩ'), ('\uFEFF', '\uFEFF'), ('\u2060', '\u2060')]:
            self.assertEqual(Unicode.nfk_c(actual), expected)

    def test_nfk_d(self):
        # empty string
        self.assertEqual('', Unicode.nfk_d(''))

        # ascii string
        for actual, expected in [('a', 'a'), ('G', 'G')]:
            self.assertEqual(Unicode.nfk_d(actual), expected)

        # unicode string
        for actual, expected in [('é', 'é'), ('café', 'café'), ('cafe\u0301', 'café'), ('Å', 'Å'), ('æ', 'æ'),
                                    ('ﬃ', 'ffi')]:
                self.assertEqual(Unicode.nfk_d(actual), expected)

        # special characters
        for actual, expected in [('\u212B', 'Å'), ('Ω', 'Ω'), ('ℵ', 'א')]:
            self.assertEqual(Unicode.nfk_d(actual), expected)

        # edge case
        for actual, expected in [('\u1E9B\u0323', 'ṩ'), ('\uFEFF', '\uFEFF'), ('\u2060', '\u2060')]:
            self.assertEqual(Unicode.nfk_d(actual), expected)
    def test_utf_32(self):
        # empty string
        self.assertEqual([], Unicode.utf_32(''))

        # ascii string
        ascii_str = 'Hello'
        expected_hex = [72, 101, 108, 108, 111]
        self.assertEqual(Unicode.utf_32(ascii_str), expected_hex)

    def test_character_categories(self):
        self.assertEqual('Ll', Unicode.character_categories('é'))
        self.assertEqual('Ll', Unicode.character_categories('é', Granularity.major))
        self.assertEqual('Ll', Unicode.character_categories('é', Granularity.detailed))

    def test_hex(self):
        # empty string
        self.assertEqual('', Unicode.hex(''))

        # ascii string
        ascii_str = 'Hello'
        expected_hex = 'fffe000048000000650000006c0000006c0000006f000000'
        self.assertEqual(Unicode.hex(ascii_str), expected_hex)

        # unicode string
        unicode_str = '\u0048\u0065\u006C\u006C\u006F\u0020\u0077\u006F\u0072\u006C\u0064'  # 'Hello world' 的 UTF-32 编码
        expected_hex = 'fffe000048000000650000006c0000006c0000006f00000020000000770000006f000000720000006c00000064000000'
        self.assertEqual(Unicode.hex(unicode_str), expected_hex)

        # special characters
        special_chars = '\uFEFF\u2060'  # 零宽度非断空格和零宽度非换行空格的 UTF-32 编码
        expected_hex = 'fffe0000fffe000060200000'
        self.assertEqual(Unicode.hex(special_chars), expected_hex)

        # edge case
        edge_cases = '\U0001F600'  # '😀' 的 UTF-32 编码
        expected_hex = 'fffe000000f60100'
        self.assertEqual(Unicode.hex(edge_cases), expected_hex)

    def test_string(self):
        # empty string
        self.assertEqual('', Unicode.string(''))
        self.assertEqual('é', Unicode.string('\u00e9'))
