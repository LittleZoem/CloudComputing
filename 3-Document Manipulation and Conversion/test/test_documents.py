import unittest
from documents import doc_length, string, join_words, replace, reregexprep, plus, contains, contains_ngrams, \
    contains_words, docfun


def test_doc_length():
    # 测试用例 1
    assert doc_length([['hello', 'world'], ['how', 'are', 'you']]) == [2, 3]

    # 测试用例 2
    assert doc_length([[], ['only', 'one', 'word']]) == [0, 3]

    # 测试用例 3
    assert doc_length([['a', 'b', 'c'], ['d', 'e'], ['f']]) == [3, 2, 1]


def test_contains_ngrams():
    doc_array = [
        ["The", "Quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
        ["The", "quick", "fox", "jumps", "over", "the", "lazy", "dog"]
    ]

    assert contains_ngrams(doc_array, [["quick", "brown"], ["lazy", "Dog"]], ignore_case=True) == [True, True]


def test_contains_words():
    # 定义文本数据
    str1 = "This is a sample sentence"
    str2 = "Another sentence here"
    str3 = "And here's one more"

    # 将每个句子表示为一个字符串列表
    docArray = [str1.split(), str2.split(), str3.split()]

    # 定义要查找的单词列表
    words = ["here", "is"]

    assert contains_words(docArray, words) == [True, True, False]


def test_contains():
    doc_array = [
        ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
        ["Another", "sentence", "here"],
        ["And", "here's", "one", "more", "sentence"]
    ]

    # 定义要查找的模式
    words = ["an", "sa"]

    assert contains(doc_array, words, ignore_case=True) == [False, True, True]


def test_join_words():
    # 测试用例1：空列表
    assert join_words([]) == []

    # 测试用例2：单个文档
    doc1 = ['this', 'is', 'a', 'test', 'document']
    assert join_words([doc1]) == ['this is a test document']

    # 测试用例3：多个文档
    doc2 = ['another', 'test', 'document']
    doc3 = ['yet', 'another', 'test', 'document']
    assert join_words([doc1, doc2, doc3]) == ['this is a test document', 'another test document',
                                              'yet another test document']

    # 测试用例4：使用自定义分隔符
    doc4 = ['this', 'is', 'a', 'test', 'document']
    assert join_words([doc4], delim=['-']) == ['this-is-a-test-document']


def test_replace():
    # 测试用例1：空列表
    assert replace([], [], []) == []

    # 测试用例2：单个文档，单个替换
    doc1 = ['this', 'is', 'a', 'test', 'document']
    assert replace([doc1], ['test'], ['example']) == [['this', 'is', 'a', 'example', 'document']]

    # 测试用例3：单个文档，多个替换
    doc2 = ['another', 'test', 'document']
    assert replace([doc2], ['another', 'test'], ['this', 'example']) == [
        ['this', 'example', 'document']]

    # 测试用例4：多个文档，多个替换
    doc3 = ['yet', 'another', 'test', 'document']
    assert replace([doc1, doc2, doc3], ['test', 'another'], ['exam', 'this']) == [
        ['this', 'is', 'a', 'exam', 'document'], ['this', 'exam', 'document'], ['yet', 'this', 'exam', 'document']]


def test_reregexprep():
    doc = [["I", "walk"], ["they", "walked"], ["we", "are", "walking"]]
    reg = [r"walk(\w*)", "th.y"]
    rep = [r"ascend\1", "-"]
    assert reregexprep(doc, reg, rep) == [['I', 'ascend'], ['-', 'ascended'], ['we', 'are', 'ascending']]


def test_string():
    # 测试用例1：空列表
    assert string([]) == []

    # 测试用例2：单个文档
    doc1 = ['this', 'is', 'a', 'test', 'document']
    assert string([doc1]) == doc1


def test_docfun():
    doc1 = ['this', 'is', 'a', 'test', 'document']
    assert docfun(string, [doc1]) == doc1


def test_plus():
    # 测试用例 1
    doc1 = [['hello', 'world'], ['how', 'are', 'you']]
    doc2 = [['I', 'am'], ['doing', 'well', 'thanks']]
    assert plus(doc1, doc2) == [['hello', 'world', 'I', 'am'], ['how', 'are', 'you', 'doing', 'well', 'thanks']]
    # 测试用例 2
    doc1 = [['a', 'b', 'c'], ['d', 'e']]
    doc2 = [['f', 'g', 'h'], ['i', 'j']]
    assert plus(doc1, doc2) == [['a', 'b', 'c', 'f', 'g', 'h'], ['d', 'e', 'i', 'j']]

    # 测试用例 3
    doc1 = [[]]
    doc2 = [[]]
    assert plus(doc1, doc2) == [[]]

    # class DocumentTest(unittest.TestCase):
    #     pass
