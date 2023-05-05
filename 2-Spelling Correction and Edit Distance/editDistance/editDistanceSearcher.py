from editDistance import editDistance


class EditDistanceSearcher:
    def __init__(self, Vocabulary, MaximumDistance, InsertCost=1, DeleteCost=1, SubstituteCost=1):
        self.vocabulary = Vocabulary
        self.maximum_distance = MaximumDistance
        self.insert_cost = InsertCost
        self.delete_cost = DeleteCost
        self.substitute_cost = SubstituteCost

    def search(self, query, edit_distance):
        results = set()
        for index in range(len(self.vocabulary)):
            if abs(len(self.vocabulary[index]) - len(query)) > edit_distance:
                continue
            distance = editDistance(str1=self.vocabulary[index], str2=query, InsertCost=self.insert_cost,
                                    DeleteCost=self.delete_cost, SubstituteCost=self.substitute_cost)
            if distance <= edit_distance:
                results.add((index, distance))
        return sorted(results, key=lambda x: x[1])


def rangesearch(eds: EditDistanceSearcher, words, maxDist):
    idx = []
    d = []
    for word in words:
        if len(eds.search(word, maxDist)) == 0:
            idx.append([])
            d.append([])
        else:
            idx.append(eds.search(word, maxDist)[0])
            d.append(eds.search(word, maxDist)[1])
    return idx, d


def knnsearch(eds: EditDistanceSearcher, words, maxDist, **kwargs):
    k = 1
    include_ties = False
    idx = []
    d = []

    if 'K' in kwargs.keys():
        if isinstance(kwargs.get('K'), int) and kwargs.get('K') > 0:
            k = kwargs.get('K')
        else:
            raise ValueError("K must be an integer and larger than 0")

    if 'IncludeTies' in kwargs.keys():
        if isinstance(kwargs.get('IncludeTies'), bool):
            include_ties = kwargs.get('IncludeTies')
        else:
            raise ValueError("IncludeTies must be a bool variable")

    for word in words:
        if len(eds.search(word, maxDist)) == 0:
            idx.append([])
            d.append([])
        else:
            idx.append(eds.search(word, maxDist)[:k][0])
            d.append(eds.search(word, maxDist)[:k][1])
    return idx, d
