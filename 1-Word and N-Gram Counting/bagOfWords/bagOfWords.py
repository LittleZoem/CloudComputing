import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

class bagOfWords:
    def __init__(self, documents=None, words=None, counts=None):
        self.Wordlist = []
        self.data_wrd = [[], []]
        self.data_doc = [[], []]
        self.data_cnt = [[], []]
        self.NumWords = 0
        self.NumDocuments = 0
        # self.Vocabulary = []  

        if documents is not None and counts is None and words is None:
            self.addDocument(documents)
        elif documents is None and counts is not None and words is not None:
            if type(words) == list:
                words = np.array(words)
            if type(words) == np.ndarray and words.dtype.kind == 'U':
                self.Wordlist = list(words)
                if len(self.Wordlist) != len(list(np.unique(self.Wordlist))):
                    raise ValueError('Non-repeating string expected.')
            else:
                raise TypeError('ValidUniqueWordsExpected')

            if type(counts) == list:
                counts = np.array(counts)
            if type(counts) == np.ndarray and len(counts.shape) == 2 and \
                    counts.dtype.kind in ['i', 'u'] and counts.min() >= 0:
                if counts.shape[1] != len(self.Wordlist):
                    raise ValueError('SizeMismatch')
                doc, word = np.nonzero(counts)
                cnt = counts[doc, word]
                self.data_wrd = [word.tolist(), []]
                self.data_doc = [doc.tolist(), []]
                self.data_cnt = [cnt.tolist(), []]
                self.NumDocuments = counts.shape[0]
                self.NumWords = counts.shape[1]
            else:
                raise TypeError('ValidCountsExpected')


    def addDocument(self, documents):   #待测
        if not self.check_input(documents):
            raise TypeError('ValidDocumentExpected')

        if not documents or type(documents[0]) == str:
            documents = [documents]
        for doc in documents:
            doc_idx = self.NumDocuments
            self.NumDocuments += 1
            data_wrd = []
            data_cnt = []
            for word in doc:
                if word not in self.Wordlist:
                    self.Wordlist.append(word)
                    self.NumWords += 1
                word_idx = self.Wordlist.index(word)
                if word_idx not in data_wrd:
                    data_wrd.append(word_idx)
                    data_cnt.append(1)
                else:
                    data_cnt[data_wrd.index(word_idx)] += 1

            data_doc = [doc_idx] * len(data_wrd)
            self.data_doc[0].extend(data_doc)
            self.data_wrd[0].extend(data_wrd)
            self.data_cnt[0].extend(data_cnt)


    @property
    def Counts(self):
        count = np.zeros((self.NumDocuments, self.NumWords), dtype=np.int32)
        for doc_idx, wrd_idx, cnt in zip(self.data_doc[0], self.data_wrd[0], self.data_cnt[0]):
            count[doc_idx][wrd_idx] = cnt
        return count

    def __call__(self):
        print("bagOfWords with properties:\n")
        print("     Vocabulary: ", self.Wordlist)
        print("       NumWords: ", self.NumWords)
        print("   NumDocuments: ", self.NumDocuments)


    def encode(self, words, **kwargs):
        documents_in = kwargs.get('DocumentsIn', 'rows').lower()
        if not self.check_input(words):
            raise TypeError('ValidinputExpected')
        
        if documents_in not in ['rows', 'columns']:
            raise ValueError("DocumentsIn must be 'rows' or 'columns'.")
        
        if type(words[0]) == str:
            words = [words]

        encode_vec = []
        for line in words:
            vec = np.zeros(len(self.Wordlist), dtype=np.int32)
            docFreqs = Counter(line)
            for i, word in enumerate(self.Wordlist):
                if word in docFreqs:
                    vec[i] = docFreqs[word]
            encode_vec.append(vec)

        encode_vec = np.array(encode_vec)
        if documents_in == 'columns':
            encode_vec = encode_vec.T
        return encode_vec


    def check_input(self, input):
        if isinstance(input, list):
            if all(isinstance(item, str) for item in input):
                return True
            elif all(isinstance(row, list) and all(isinstance(item, str) for item in row) for row in input):
                return True
        return False
        
    def removeEmptyDocuments(self):
        if self.NumDocuments == 0:
            return -1

        docs = np.array(np.concatenate(self.data_doc), dtype=np.int32)
        # if len(docs) == 0:
        #     idx = list(range(self.NumDocuments))
        #     self = bagOfWords()
        #     return idx
        keep = np.ones(self.NumDocuments, dtype=bool)
        unidoc = np.unique(docs)
        for doc in unidoc:
            keep[doc] = False
        idx = np.nonzero(keep)
        idx = idx[0].tolist()
        newidx = np.cumsum(~keep)
        self.data_doc = [(newidx[docs]-1).tolist(), []]
        self.NumDocuments = newidx[-1]

        return idx

    def removeDocument(self, idx):
        assert isinstance(idx, list) and len(idx) > 0, \
            "idx should be a non-empty list"
        assert (all(isinstance(elem, int) for elem in idx) or all(isinstance(elem, bool) for elem in idx)), \
            "idx should be a list of int or bool type"

        idx = np.array(idx)
        if idx.dtype == bool:
            if len(idx) > self.NumDocuments:
                raise ValueError("Invalid logical index")
            idx = np.where(idx)[0]
            if len(idx) == 0:
                return

        if np.any(idx >= self.NumDocuments) or np.any(idx < 0):
            raise ValueError("Invalid numeric index")

        keep = np.ones(self.NumDocuments, dtype=bool)
        keep[idx] = False

        data_doc = np.array(np.concatenate(self.data_doc), dtype=np.int32)
        data_wrd = np.array(np.concatenate(self.data_wrd), dtype=np.int32)
        data_cnt = np.array(np.concatenate(self.data_cnt), dtype=np.int32)

        removeEntries = np.isin(data_doc, idx)
        data_doc = data_doc[~removeEntries]
        data_wrd = data_wrd[~removeEntries]
        data_cnt = data_cnt[~removeEntries]

        newidx = np.cumsum(keep)
        data_doc = newidx[data_doc] - 1
        self.NumDocuments = newidx[-1]

        self.data_doc = [data_doc.tolist(), []]
        self.data_wrd = [data_wrd.tolist(), []]
        self.data_cnt = [data_cnt.tolist(), []]

        self.removeInfrequentWords(0)

    def removeInfrequentWords(self, count, ignore_case=False):
        wordCnt = self.Counts
        wordCnt = np.sum(wordCnt, axis=0)
        if not ignore_case:
            infWord = np.where(wordCnt <= count)[0].tolist()
        else:
            wordlist = self.Wordlist
            lowWord = np.char.lower(wordlist)
            lowCnt = np.zeros_like(lowWord, dtype=int)
            for i, word in enumerate(lowWord):
                lowCnt[i] = np.sum(wordCnt[lowWord == word])
            infWord = np.where(lowCnt <= count)[0].tolist()
        
        return self.removeWords(infWord)

    def topkwords(self, k=5, **kwargs):
        ignore_case = kwargs.get('IgnoreCase', False)
        word = np.array(np.concatenate(self.data_wrd), dtype=np.int32)
        cnt = np.array(np.concatenate(self.data_cnt), dtype=np.int32)
        wordlist = self.Wordlist

        _, wrdIdx = np.unique(word, return_inverse=True)
        wrdCnt = np.array(np.bincount(wrdIdx, weights=cnt), dtype = np.int32)
        uniWord = np.unique(word)
        if ignore_case == False:
            wdic = dict(zip(uniWord, wrdCnt))
            sorted_wdict = dict(sorted(wdic.items(), key=lambda item: item[1], reverse=True))
            k = min(k, len(uniWord))
            top_wdic = dict(list(sorted_wdict.items())[:k])
            top_wdic = {wordlist[x] : v for x, v in top_wdic.items()}
            return top_wdic
        else:
            name = np.array([wordlist[i].lower() for i in uniWord])
            _, nameIdx = np.unique(name, return_inverse=True)
            nameCnt = np.array(np.bincount(nameIdx, weights=wrdCnt), dtype = np.int32)
            uniName = np.unique(name)
            ndic = dict(zip(uniName, nameCnt))
            sorted_ndict = dict(sorted(ndic.items(), key=lambda item: item[1], reverse=True))
            k = min(k, len(uniName))
            top_ndic = dict(list(sorted_ndict.items())[:k])
            return top_ndic

    def removeWords(self, words, ignore_case=False):
        words = np.array(words)
        if words.dtype == bool:
            if len(words) != len(self.Wordlist):
                raise ValueError('ValidIndicesExpected')
            if ignore_case:
                raise ValueError('IgnoreCaseStringsOnly')
            idx = np.nonzero(words)[0].tolist()
        elif np.issubdtype(words.dtype, np.unicode_):
            wordlist = np.array(self.Wordlist)
            if ignore_case:
                idx = np.isin(np.char.lower(wordlist), np.char.lower(words))
                idx = np.nonzero(idx)[0].tolist()
            else:
                idx = np.isin(wordlist, words)
                idx = np.nonzero(idx)[0].tolist()
        elif words.dtype == int:
            if np.any(words >= len(self.Wordlist)) or np.any(words < 0):
                raise ValueError('ValidIndicesExpected')
            if ignore_case:
                raise ValueError('IgnoreCaseStringsOnly')
            idx = np.unique(words)
        else:
            raise ValueError('NamedStringIdxExpected')

        data_doc = np.array(np.concatenate(self.data_doc), dtype=np.int32)
        data_wrd = np.array(np.concatenate(self.data_wrd), dtype=np.int32)
        data_cnt = np.array(np.concatenate(self.data_cnt), dtype=np.int32)

        removeEntries = np.isin(data_wrd, idx)
        data_doc = data_doc[~removeEntries]
        data_wrd = data_wrd[~removeEntries]
        data_cnt = data_cnt[~removeEntries]

        keep = np.ones(self.NumWords, dtype=bool)
        keep[idx] = False
        self.Wordlist = np.array(self.Wordlist)[keep].tolist()
        newidx = np.cumsum(keep)
        self.NumWords = newidx[-1]

        data_wrd = newidx[data_wrd] - 1

        self.data_doc = [data_doc.tolist(), []]
        self.data_wrd = [data_wrd.tolist(), []]
        self.data_cnt = [data_cnt.tolist(), []]

    def wordcloud(self, **kwargs):
        wordCnt = self.Counts
        wordCnt = np.sum(wordCnt, axis=0).tolist()

        wordcloud = WordCloud(width=800, height=800, background_color='white', colormap='viridis')
        wordcloud.generate_from_frequencies(frequencies=dict(zip(self.Wordlist, wordCnt)))

        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def tfidf(self, words=None, **kwargs):
        if words is None:
            tf = self.Counts
        else:
            tf = self.encode(words)

        tf_weight = kwargs.get('TFWeight', 'raw').lower()[0]
        if tf_weight == 'b':
            tf = tf.astype(bool)
        elif tf_weight == 'l':
            tf[tf != 0] = 1 + np.log(tf[tf != 0])

        idf_weight = kwargs.get('IDFWeight', 'normal').lower()[0]
        nt = np.sum(tf > 0, axis=0).ravel()
        if idf_weight == 'u':
            idf = 1
        elif idf_weight == 'n':
            idf = np.log(self.NumDocuments / nt)
        elif idf_weight == 's':
            idf = np.log(1 + self.NumDocuments / nt)
        elif idf_weight == 'm':
            nt_per_doc = nt * (tf > 0)
            idf = np.log(1 + np.max(nt_per_doc, axis=0) / nt)
        elif idf_weight == 'p':
            idf = np.log((self.NumDocuments - nt) / nt)
        elif idf_weight == 't':
            idf = np.log((self.NumDocuments - nt + 0.5) / (nt + 0.5))
            avg_idf = np.mean(idf)
            too_common = nt > self.NumDocuments / 2
            idf[too_common] = kwargs.get('IDFCorrection', 0.25) * avg_idf
        elif idf_weight == 'c':
            idf = np.log((self.NumDocuments - nt + 0.5) / (nt + 0.5))

        # t = tf.multiply(idf)
        t = tf * idf

        if kwargs.get('Normalized', False):
            normfac = np.sqrt(np.sum(tf.power(2), axis=1)).ravel()
            normfac[normfac == 0] = np.finfo(float).eps
            t = t / normfac[:, None]

        if kwargs.get('DocumentsIn', 'rows').lower() == 'columns':
            t = t.T

        return np.around(t, decimals=4)



word = ["iji", "uuu", "popp", "yty"]
count = [[1, 3, 1, 0], [1, 0, 0, 1], [0, 1, 2, 1]]
doc = [["我", "你", "hao"],["it's", "me", "hi", "me", "the", "prob"],[],["ifo"]]
# doc = [["hi", "oh", "UI", "yay"], ["oh", "yay", "hi", "pop", "Pop", "hi"], ["Hi", "Oh", "yay","Oh"],["hi", "oh", "pOP","OH"]]
# print(type(count))
# count = np.array(count)
# bg = bagOfWords(words=word, counts=count)
# doc = [["a", "new", "sentence", "sentence"], ["A", "second", "new", "Sentence"]]
bg = bagOfWords(words=word, counts=count)
print("=0===========", bg())
wds = [["我", "me", "the"], ["Ni", "hao", "prob", "hao"]]
print(bg.Wordlist)
print(bg.data_wrd)
print(bg.data_doc)
print(bg.data_cnt)
print(bg.NumDocuments)
print(bg.NumWords)
print(bg.Counts)
print("------------------------------------------")
# print(bg.removeEmptyDocuments())
# print(bg.Wordlist)
# print(bg.data_wrd)
# print(bg.data_doc)
# print(bg.data_cnt)
# print(bg.NumDocuments)
# print(bg.NumWords)
# print(bg.Counts)
# print(bg.encode(wds, DocumentsIn='columns'))
# print(bg.Wordlist[0], bg.Wordlist[3])
# print(bg.topkwords(2, IgnoreCase=True))
# print(bg.removeWords("me"))
# print(bg.removeInfrequentWords(2))
# print(bg.removeWords([2,3]))
# print(bg.removeDocument([1,2]))
# print(bg.Wordlist)
# print(bg.data_wrd)
# print(bg.data_doc)
# print(bg.data_cnt)
# print(bg.NumDocuments)
# print(bg.NumWords)
# print(bg.Counts)
# print(bg.wordcloud())
print(bg.tfidf(DocumentsIn='columns'))