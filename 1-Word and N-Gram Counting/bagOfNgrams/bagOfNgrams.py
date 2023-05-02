# from nltk import ngrams
# from collections import Counter

# def bag_of_ngrams(text, n):
#     # 将文本分成n元组
#     n_grams = ngrams(text.split(), n)
#     # 统计n元组的出现次数
#     n_grams_freq = Counter(n_grams)
#     # 返回n元组的词袋
#     return dict(n_grams_freq)

# # 示例用法
# text = "This is a sample text for testing bag of n-grams in Python"
# n = 2
# bag = bag_of_ngrams(text, n)
# print(bag)

# import itertools
# from collections import Counter

# class BagOfNgrams:
#     def __init__(self, *args, **kwargs):
#         self.ngrams = Counter()

#         if len(args) == 1:
#             if isinstance(args[0], list):
#                 documents = args[0]
#                 self._compute_ngrams(documents, 2)
#             elif isinstance(args[0], tuple):
#                 unique_ngrams, counts = args[0]
#                 self._initialize_from_ngrams(unique_ngrams, counts)
#         elif len(args) == 0:
#             pass
#         else:
#             raise ValueError("Invalid arguments")

#         if 'NgramLengths' in kwargs:
#             lengths = kwargs['NgramLengths']
#             if isinstance(args[0], list):
#                 documents = args[0]
#                 self._compute_ngrams(documents, lengths)

#     def _compute_ngrams(self, documents, n):
#         for doc in documents:
#             words = doc.split()
#             for ngram in zip(*[words[i:] for i in range(n)]):
#                 self.ngrams[ngram] += 1

#     def _initialize_from_ngrams(self, unique_ngrams, counts):
#         for ngram, count in zip(unique_ngrams, counts):
#             if "<missing>" not in ngram:
#                 self.ngrams[ngram] = count

# # Example usage:
# # Creating an empty n-gram model
# bag = BagOfNgrams()
# print(bag)
# # Creating a bigram model from documents
# documents = ["this is a test", "this is another test"]
# bag = BagOfNgrams(documents)
# print(bag)

# # Creating an n-gram model with specified lengths
# bag = BagOfNgrams(documents, NgramLengths=3)
# print(bag)

# # Creating an n-gram model from unique n-grams and counts
# unique_ngrams = [("this", "is"), ("is", "a"), ("a", "test"), ("<missing>", "value")]
# counts = [2, 1, 2, 1]
# bag = BagOfNgrams((unique_ngrams, counts))
# print(bag)

import itertools
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

class bagOfNgrams:
    def __init__(self, *args, **kwargs):
        self.ngrams = Counter()
        self.vectorizer = None

        if len(args) == 1:
            if isinstance(args[0], list):
                documents = args[0]
                self._compute_ngrams(documents, 2)
            elif isinstance(args[0], tuple):
                unique_ngrams, counts = args[0]
                self._initialize_from_ngrams(unique_ngrams, counts)
        elif len(args) == 0:
            pass
        else:
            raise ValueError("Invalid arguments")

        if 'NgramLengths' in kwargs:
            lengths = kwargs['NgramLengths']
            if isinstance(args[0], list):
                documents = args[0]
                self._compute_ngrams(documents, lengths)

    def _compute_ngrams(self, documents, n):
        self.vectorizer = CountVectorizer(ngram_range=(n, n), analyzer='word', token_pattern=r'\b\w+\b')
        X = self.vectorizer.fit_transform(documents)
        ngram_names = self.vectorizer.get_feature_names_out()
        ngram_counts = X.sum(axis=0).A1
        self.ngrams = Counter(dict(zip(ngram_names, ngram_counts)))

    def _initialize_from_ngrams(self, unique_ngrams, counts):
        for ngram, count in zip(unique_ngrams, counts):
            if "<missing>" not in ngram:
                self.ngrams[ngram] = count

    def get_ngrams(self):
        return self.ngrams

# Example usage:
# Creating an empty n-gram model
bag = bagOfNgrams()

# Creating a bigram model from documents
documents = ["this is a test", "this is another test"]
bag = bagOfNgrams(documents)

# Creating an n-gram model with specified lengths
bag = bagOfNgrams(documents, NgramLengths=3)

# Creating an n-gram model from unique n-grams and counts
unique_ngrams = [("this", "is"), ("is", "a"), ("a", "test"), ("<missing>", "value")]
counts = [2, 1, 2, 1]
bag = bagOfNgrams((unique_ngrams, counts))

# Get the n-grams and their counts
ngrams = bag.get_ngrams()
print(ngrams)

""" test """
from nltk.tokenize import word_tokenize

# Load the text from the file
with open('sonnetsPreprocessed.txt', 'r') as f:
    text = f.read()

# Split the text into documents at newline characters
documents = text.split('\n')
bag = bagOfNgrams(documents)
print(bag)
# # Tokenize the documents
# tokenized_documents = [word_tokenize(doc) for doc in documents]

# # Print the first 10 tokenized documents
# print(tokenized_documents[:10])


""" test """
from sklearn.feature_extraction.text import CountVectorizer

# Load the text from the file
with open('sonnetsPreprocessed.txt', 'r') as f:
    text = f.read()

# Split the text into documents at newline characters
documents = text.split('\n')

# Create a bag-of-n-grams model
vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b')
bag_of_ngrams = vectorizer.fit_transform(documents)

# Print the bag-of-n-grams model properties
print("Counts:", bag_of_ngrams.toarray())
print("Vocabulary:", vectorizer.get_feature_names())
print("Ngrams:", vectorizer.get_feature_names())
print("NgramLengths:", vectorizer.ngram_range)
print("NumNgrams:", len(vectorizer.get_feature_names()))
print("NumDocuments:", len(documents))
