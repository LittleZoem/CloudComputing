# use dp algorithm to calculate edit distance
def get_edit_distance(s1, s2, insertCost, deleteCost, substituteCost):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(deleteCost + dp[i - 1][j], insertCost + dp[i][j - 1], substituteCost + dp[i - 1][j - 1])
    return dp[m][n]


def tokenizedDocument(s):
    res = []
    if isinstance(s, list):
        for documents in s:
            tmp = []
            sentences = documents.split('.')
            for sentence in sentences:
                tmp.append(word for word in sentence.split())
            tmp.append('.')
            res.append(tmp)
    if isinstance(s, str):
        res = s.split()

    return res


def editDistance(str1: str = None, str2: str = None, document1=None, document2=None, **kwargs):
    insert_cost = 1
    delete_cost = 1
    substitute_cost = 1

    # Check the name-value parameter : InsertCost
    if 'InsertCost' in kwargs.keys():
        if isinstance(kwargs.get('InsertCost'), int) and kwargs.get('InsertCost') > 0:
            insert_cost = kwargs.get('InsertCost')
        else:
            raise ValueError("InsertCost must be an integer and larger than 0")

    # Check the name-value parameter : DeleteCost
    if 'DeleteCost' in kwargs.keys():
        if isinstance(kwargs.get('DeleteCost'), int) and kwargs.get('DeleteCost') > 0:
            delete_cost = kwargs.get('DeleteCost')
        else:
            raise ValueError("DeleteCost must be an integer and larger than 0")

    # Check the name-value parameter : SubstituteCost
    if 'SubstituteCost' in kwargs.keys():
        if isinstance(kwargs.get('SubstituteCost'), int) and kwargs.get('SubstituteCost') > 0:
            substitute_cost = kwargs.get('SubstituteCost')
        else:
            raise ValueError("SubstituteCost must be an integer and larger than 0")

    # Check whether entered two strings or two documents
    if str1 is not None and str2 is not None:
        assert document1 is None and document2 is None
        return get_edit_distance(s1=str1, s2=str2, insertCost=insert_cost, deleteCost=delete_cost,
                                 substituteCost=substitute_cost)

    if document1 is not None and document2 is not None:
        assert str1 is None and str2 is None
        return get_edit_distance(s1=document1, s2=document2, insertCost=insert_cost, deleteCost=delete_cost,
                                 substituteCost=substitute_cost)

    raise AttributeError("arguments should be two string or two tokenizedDocuments")


# str1 = "It's time for breakfast."
# doc1 = tokenizedDocument(str1)
# str2 = "It's now time to sleep."
# doc2 = tokenizedDocument(str2)
str1 = "Text analytics"
str2 = "Text analysis"

print(editDistance(str1=str1, str2=str2))
