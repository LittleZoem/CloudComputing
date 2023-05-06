import re
from typing import List


def contains_ngrams(documents: List[List[str]], ngrams: List[List[str]], ignore_case: bool = False) -> List[
    bool]:
    if ignore_case:
        documents = [[word.lower() for word in doc] for doc in documents]
        ngrams = [[word.lower() for word in ngram] for ngram in ngrams]
    tf = []
    for doc in documents:
        if any(any(ngram == doc[i:i + len(ngram)] for i in range(len(doc) - len(ngram) + 1)) for ngram in ngrams):
            tf.append(True)
        else:
            tf.append(False)
    return tf


def contains_words(documents: List[List[str]], words: List[str], ignore_case: bool = False) -> List[bool]:
    """
    在 tokenizedDocument 数组中查找包含指定单词的句子，并返回一个逻辑数组指示每个句子是否包含指定单词。
    :param documents: tokenizedDocument 数组，其中每个元素都是一个字符串列表，表示一个句子的单词序列。
    :param words: 要查找的单词列表。
    :param ignore_case: 是否忽略单词的大小写。
    :return: 一个逻辑数组，指示每个句子是否包含指定单词。
    """
    tf = []
    for doc in documents:
        if ignore_case:
            doc = [word.lower() for word in doc]
            words = [word.lower() for word in words]
        if any(word in doc for word in words):
            tf.append(True)
        else:
            tf.append(False)
    return tf


def contains(documents: List[List[str]], words: List[str], ignore_case: bool = False) -> List[bool]:
    """
    在 tokenizedDocument 数组中查找包含指定单词的句子，并返回一个逻辑数组指示每个句子是否包含指定单词。
    :param documents: tokenizedDocument 数组，其中每个元素都是一个字符串列表，表示一个句子的单词序列。
    :param words: 要查找的单词列表。
    :param ignore_case: 是否忽略单词的大小写。
    :return: 一个逻辑数组，指示每个句子是否包含指定单词。
    """
    tf = []
    for doc in documents:
        if ignore_case:
            doc = [word.lower() for word in doc]
            words = [word.lower() for word in words]
        if any(any(word in token for token in doc) for word in words):
            tf.append(True)
        else:
            tf.append(False)
    return tf


def plus(doc1: List[List[str]], doc2: List[List[str]]) -> List[List[str]]:
    if len(doc1) != len(doc2):
        raise Exception('len(doc1) != len(doc2)')
    doc = []
    for i in range(len(doc1)):
        new_list = doc1[i] + doc2[i]
        doc.append(new_list)
    return doc


def docfun(func, *args):
    return func(*args)


def string(documents: List[List[str]]) -> List[str]:
    if len(documents) == 0:
        return []
    elif len(documents) == 1:
        return documents[0]
    else:
        raise Exception('please input a scalar tokenizedDocument object.')


def doc_length(documents: List[List[str]]) -> List[int]:
    return [len(doc) for doc in documents]


def join_words(documents: List[List[str]], delim=None) -> List[str]:
    if delim is None:
        delim = [' ']
    if len(delim) != 1:
        raise Exception('delim must be a string scalar.')
    return [delim[0].join(doc) for doc in documents]


def replace(documents: List[List[str]], olds: List[str], news: List[str]) -> List[List[str]]:
    if len(olds) != len(news):
        raise Exception('len(old) != len(new)')
    new_documents = []
    for doc in documents:
        new_doc = []
        for word in doc:
            new_word = word
            for old in olds:
                if old in word:
                    new_word = word.replace(old, news[olds.index(old)])
            new_doc.append(new_word)
        new_documents.append(new_doc)
    return new_documents


def reregexprep(documents: List[List[str]], expressions: List[str], replaces: List[str]) -> List[List[str]]:
    if len(expressions) != len(replaces):
        raise Exception('len(old) != len(new)')
    new_documents = []
    for doc in documents:
        new_doc = []
        for word in doc:
            new_word = word
            for expression in expressions:
                new_word = re.sub(expression, replaces[expressions.index(expression)], new_word)
            new_doc.append(new_word)
        new_documents.append(new_doc)
    return new_documents


class Documents:
    pass
