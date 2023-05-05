import codecs
import unicodedata
from enum import Enum, auto
from typing import List


class Granularity(Enum):
    """
    The granularity of the character categories
    """
    major = auto(),
    detailed = auto()


class Unicode:
    @staticmethod
    def nfc(s: str) -> str:
        """
        NFC (Normalization Form C): Canonical Decomposition followed by Canonical Composition.
        :return: NFC
        """
        return unicodedata.normalize('NFC', s)

    @staticmethod
    def nfd(s: str) -> str:
        """
        NFD (Normalization Form D): Canonical Decomposition.
        :return: NFD
        """
        return unicodedata.normalize('NFD', s)

    @staticmethod
    def nfk_c(s: str) -> str:
        """
        NFKC (Normalization Form KC): Compatibility Decomposition, followed by Canonical Composition.
        :return: NFKC
        """
        return unicodedata.normalize('NFKC', s)

    @staticmethod
    def nfk_d(s: str) -> str:
        """
        NFKD (Normalization Form KD): Compatibility Decomposition.
        :return: NFKD
        """
        return unicodedata.normalize('NFKD', s)

    @staticmethod
    def utf_32(s: str) -> List[int]:
        """
        Unicode UTF-32 string representation
        :return: UTF-32
        """
        utf32_array: List[int] = []
        for char in s:
            utf32_array.append(ord(char))

        # 转换为字符串
        return utf32_array

    @staticmethod
    def character_categories(s: str, granularity: Granularity = Granularity.major) -> List[str]:
        """
        returns the major Unicode character categories for the characters in the UTF32 object str.
        :param s: UTF32 object
        :param granularity: major or detailed
        :return: Character Categories
        """

        categories = []

        for char in s:
            char_category = unicodedata.category(char)
            if granularity == Granularity.major:
                char_category = char_category[:1]
            categories.append(char_category)

        return categories

    @staticmethod
    def hex(s: str) -> str:
        """
        converts the UTF-32 representation str32 to hexadecimal values.
        :param s: UTF-32 representation
        :return: hexadecimal values
        """
        if len(s) == 0:
            return ''
        # 将 UTF-32 字符串编码为字节串
        encoded = s.encode('utf-32')

        # 使用 codecs 模块的 encode() 方法将字节串转换为十六进制字符串
        hex_str = codecs.encode(encoded, 'hex').decode('ascii')

        return hex_str

    @staticmethod
    def string(s: str) -> str:
        """
        converts the UTF-32 representation str32 to string.
        :param s: UTF-32 representation
        :return: string
        """
        return str(s)
