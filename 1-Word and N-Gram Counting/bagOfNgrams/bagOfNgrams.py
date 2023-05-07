import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from collections import OrderedDict
class bagOfNgram:
    def __init__(self, *args):
        self.ngramLengths = [2]
        self.counts = []
        self.Ngrams = set()
        self.doc = []
        self.Vocabulary = []
        self.X = None
        self.flag = args[0] if args else 0
        # 如果args为空，则使用默认参数
        if len(args) <= 1:
            pass
        elif args[1] == 'NgramLengths':
            self.ngramLengths = args[2]
            if not isinstance(self.ngramLengths, list):
                self.ngramLengths = [self.ngramLengths]

        self.vectorizer = CountVectorizer(ngram_range=(min(self.ngramLengths), max(self.ngramLengths)),token_pattern=r'\b\w+\b')
        if self.flag:
            self(args[0])
        else:
            pass

    def __call__(self, documents):
        # 将文本转换为词袋模型
        self.doc = documents
        # 对self.doc分词
        words = [i.split() for i in self.doc]
        # 将Python中文本中的唯一单词存储在一个列表中,使用OrderedDict方法可以使其按照原始文本中单词的顺序排列，
        # 使用set是一个无序的集合，因此唯一单词列表的顺序可能与原始文本中单词的顺序不同。
        # self.Vocabulary = list(set([j for i in words for j in i]))
        self.Vocabulary = list(OrderedDict.fromkeys([j for i in words for j in i]))
        self.X = self.vectorizer.fit_transform(self.doc)

        # 将结果转换为MATLAB的bag对象格式
        self.Ngrams = list(set(self.vectorizer.get_feature_names()))
        self.counts = self.X.toarray().tolist()

        # 返回bag对象
        return self

    def __repr__(self):
        # 输出结果
        if self.flag :
            NgramLengths = str(self.ngramLengths)[1:-1] if len(self.ngramLengths) == 1 else str(self.ngramLengths)
            output = "bagOfNgrams with properties:\n\n"
            output += "        Counts: [" + str(len(self.counts)-1) + "x" + str(len(self.Ngrams)) + " double]\n"
            # output += "    Vocabulary: " + str(self.Vocabulary) + "\n"
            output += "    Vocabulary: [" + "1" + "x" + str(len(self.Vocabulary))+  " string]\n"
            # output += "    Vocabulary: " + str([i.split() for i in self.doc])[1:-1] + "\n"
            output += "        Ngrams: [" + str(len(self.Ngrams)) + "x" + str(max(self.ngramLengths)) + " string]\n"
            output += "  NgramLengths: " + NgramLengths + "\n"
            output += "     NumNgrams: " + str(len(self.Ngrams)) + "\n"
            output += "  NumDocuments: " + str(len(self.counts)-1) + "\n"
            return output
        else:
            return "Empty bagOfNgrams!"

    def update(self):
        # 更新词袋模型，修改了Ngrams后需要调用此方法
        words = [i.split() for i in self.Ngrams]
        self.Vocabulary = list(OrderedDict.fromkeys([j for i in words for j in i]))


def topkngrams(bag, k=5, *args):
    length = [2]
    if len(args) == 0:
            pass
    elif args[0] == 'NgramLengths':
        length = args[1]
        if not isinstance(length, list):
                length = [length]
    bag.vectorizer = CountVectorizer(ngram_range=(min(length), max(length)), token_pattern=r'\b\w+\b')
    bag_of_ngrams = bag.vectorizer.fit_transform(bag.doc)

    # Find the top n bigrams
    sum_ngrams = np.sum(bag_of_ngrams.toarray(), axis=0)

    top_n_indices = sum_ngrams.argsort()[-k:][::-1]
    top_n_bigrams = np.array(bag.vectorizer.get_feature_names())[top_n_indices]
    top_n_counts = sum_ngrams[top_n_indices]

    # Print the top 10 bigrams and their counts
    for bigram, count in zip(top_n_bigrams, top_n_counts):
        print(f"{bigram}: {count}")


def addDocuments(bag, documents):
    bag.doc = bag.doc + documents
    bag(bag.doc)
    bag.flag = 2 if bag.doc else 0
    return bag


def removeDocument(bag,documents):
    bag.doc = [i for i in bag.doc if i not in documents]
    bag(bag.doc)
    return bag


# count为出现次数，'NgramLengths'后面的参数(记为args[1])表示n-gram的长度
# 函数功能是删除总共出现次数小于等于count的,长度为args[1]的n-gram，返回修改后的bagOfNgrams
def removeInfrequentNgrams(bag, count, *args):
    # 获取每个 n-gram 在所有文档中的出现次数
    infrequentNgrams = []
    ngramCounts = np.sum(bag.counts, axis=0)
    if args and args[0] == 'NgramLengths':
        # 找到出现次数不足 count 次的 n-gram且长度为args[1]
        infrequentNgrams = [bag.Ngrams[i] for i in range(len(ngramCounts)) if ngramCounts[i] <= count and len(bag.Ngrams[i].split()) == args[1]]
    else:
        # 找到出现次数不足 count 次的 n-gram
        infrequentNgrams = [bag.Ngrams[i] for i in range(len(ngramCounts)) if ngramCounts[i] <= count]
    # 创建一个新的 Ngrams 列表，其中排除了 infrequentNgrams 中的 n-gram
    newNgrams = [ngram for ngram in bag.Ngrams if ngram not in infrequentNgrams]

    # 更新 counts 属性
    newCounts = []
    for cnt in bag.counts:
        newCount = [cnt[i] for i in range(len(ngramCounts)) if ngramCounts[i] > count]
        newCounts.append(newCount)

    # 更新 bag 对象
    bag.Ngrams = newNgrams
    bag.counts = newCounts
    bag.update()
    return bag


def removeNgrams(bag, ngrams, *args):
    ignore_case = False
    ngram_length = None
    for arg in args:
        if arg == 'IgnoreCase':
            ignore_case = True
        elif isinstance(arg, int):
            ngram_length = arg

    # 创建一个用于存储要删除的 n-grams 索引的集合
    ngrams_to_remove = set()

    # 找到要删除的 n-grams 的索引
    for i, ngram in enumerate(bag.Ngrams):
        if ignore_case:
            ngram = ngram.lower()
        if ngram in ngrams and (ngram_length is None or len(ngram.split()) == ngram_length):
            ngrams_to_remove.add(i)

    # 如果要删除的 n-grams 不在 bag.Ngrams 列表中，则引发 ValueError 异常
    if not ngrams_to_remove:
        raise ValueError('要删除的 n-grams 不在给定的 bagOfNgrams 对象中。')

    # 创建一个新的 Ngrams 列表，其中排除了要删除的 n-grams
    newNgrams = [ngram for i, ngram in enumerate(bag.Ngrams) if i not in ngrams_to_remove]

    # 更新 counts 属性
    newCounts = []
    for cnt in bag.counts:
        newCount = np.delete(cnt, list(ngrams_to_remove), axis=0)
        newCounts.append(newCount)

    # 创建一个新的 bagOfNgrams 对象，其中包含排除了要删除的 n-grams 的 Ngrams 和 counts
    bag.Ngrams = newNgrams
    bag.counts = newCounts
    bag.update()

    return bag


def removeEmptyDocuments(input):
    if isinstance(input, list):
        # 如果输入是一个文本列表，则删除其中没有单词的文档
        non_empty_docs = []
        for doc in input:
            if len(doc.split()) > 0:
                non_empty_docs.append(doc)
        return non_empty_docs

    elif isinstance(input, bagOfNgram):
        # 如果输入是一个 bag-of-n-grams 模型，则删除其中没有单词或 n-grams 的文档
        non_empty_docs = []
        non_empty_counts = []
        for i, doc in enumerate(input.counts):
            if len(input.doc[i].split()) > 0 and doc.any():
                non_empty_docs.append(input.doc[i])
                non_empty_counts.append(doc)
        newBag = bagOfNgram(non_empty_docs)
        newBag.counts = non_empty_counts
        newBag.update()
        return newBag

    else:
        # 如果输入既不是文本列表也不是 bag-of-n-grams 模型，则引发 ValueError 异常
        raise ValueError('输入必须是文本列表或bagOfNgrams对象。')


def encode(bag, input_data):
    if isinstance(input_data, list):
        # 如果输入是一个文本列表，则将其转换为词袋模型
        bag(input_data)
    elif isinstance(input_data, str):
        # 如果输入是一个文本字符串，则将其转换为单词列表，然后将其转换为词袋模型
        words = input_data.split()
        bag([' '.join(words)])
    else:
        # 如果输入既不是文本列表也不是文本字符串，则引发 ValueError 异常
        raise ValueError('输入必须是文本列表或文本字符串。')
    X = bag.X.toarray()

    # 返回频率计数矩阵
    return X


def tfidf(bag, documents=None):
    # 计算词频-逆文档频率 (TF-IDF) 矩阵
    if documents is None:
        # 如果 documents 参数未指定，则计算 bag 中所有文档的 TF-IDF 矩阵
        tfidf = TfidfTransformer().fit_transform(bag.X)
    else:
        # 如果 documents 参数已指定，则计算 documents 中文档的 TF-IDF 矩阵
        tfidf = TfidfTransformer().fit_transform(encode(bag,documents))

    # 返回 TF-IDF 矩阵
    return tfidf.toarray()
