## 设计

### 1. 总体设计

对于选择的文本分析函数类，根据其内部的关联性，可将函数分为5类，每类属于一个函数库，函数库的结构和函数之间的关系如下图：

| 函数库     | 描述                                         | 函数                                                         |
| ---------- | -------------------------------------------- | ------------------------------------------------------------ |
|            |                                              |                                                              |
| bagOfNgram | ngrams模型库，包括ngrams模型及其相关操作函数 | bagOfNgrams、addDocument、<br/>removeDocument、removeEmptyDocuments、<br/>removeNgrams、removeInfrequentNgrams、<br/>encode、topkngrams |
| ......     |                                              |                                                              |
|            |                                              |                                                              |
|            |                                              |                                                              |



### 2. bagOfNgrams函数库

#### 2.1 总体设计

由于平台的函数描述部分无法识别出类的方法参数，所以只好将所有的方法函数独立出来。其结构和总体设计类似于bagOfWords，这里就不再展示。

#### 2.2 bagOfNgrams类设计

这个`bagOfNgram`类的作用是将文本数据转换为n-gram词袋模型，其中每个文档表示为一个向量，每个元素表示一个唯一的n-gram的出现次数。

类的初始化方法`__init__`接受以下参数：

- `*args` : 一个可变参数，用于传递自定义参数

  如果`args`为空，则会创建一个空的 bag-of-n-grams 模型。

  如果`args`不为空，则可以使用以下参数:

  - `bagOfNgrams(documents)` 表示创建一个bag-of-n-grams模型并计算 `documents` 中的二元组
  - ` bagOfNgrams(documents,'NgramLengths',lengths)` 表示创建一个bag-of-n-grams模型并计算`documents`中长度为`lengths`的 n-gram。

类的方法有：

1. `__call__`(self, documents)：将文本转换为词袋模型。
   - 输入：documents，一个字符串列表，表示要转换为n-gram词袋模型的文本数据。
   - 返回：self，一个bagOfNgrams对象，表示转换后的n-gram词袋模型。
2. `__repr__`(self)：输出结果。
   - 返回：一个字符串，表示bagOfNgrams对象的属性和结果。
3. `update`(self)：更新词袋模型，修改了Ngrams后需要调用此方法。

#### 2.3 topkngrams函数设计

`topkngrams`函数的作用是找到给定词袋模型中出现次数最多的前k个n-grams。函数接受以下参数：

- `bag`：一个bagOfNgrams对象，表示输入的词袋模型。
- `k`：一个整数，表示要找到的前k个n-grams。默认值为5。
- `*args`： 一个可变参数，用于传递自定义参数。如果`args`为空，则`lengths`默认为2。如果`args`不为空，则可以使用以下参数：
  - `'NgramLengths'`：只是为了符合matlab设计的标识参数
  - `lengths`：一个整数或整数列表，用于指定要使用的`n-gram`的长度。如果指定了多个长度，则将使用所有指定的长度。

函数的工作流程如下：

1. 根据输入的`lengths`参数，更新bag对象的`vectorizer`属性。
2. 使用更新后的`vectorizer`重新计算词袋模型。
3. 计算每个n-gram在所有文档中的总出现次数。
4. 找到出现次数最多的前k个n-grams及其出现次数。
5. 打印前k个n-grams及其出现次数。

#### 2.4 addDocuments函数设计

`addDocuments`函数的作用是向现有的`bagOfNgrams`对象中添加新的文档，并更新词袋模型。函数接受以下参数：

- `bag`：一个`bagOfNgrams`对象，表示输入的词袋模型。
- `documents`：一个字符串列表，表示要添加到词袋模型中的新文档。

函数的工作流程如下：

1. 将新的文档添加到bag对象的doc属性中。
2. 使用更新后的doc属性重新计算词袋模型。
3. 更新bag对象的flag属性(表示是否为空词袋)，如果doc属性不为空，则将其设置为2，否则设置为0。

函数返回更新后的bag对象。

#### 2.5 removeDocument函数设计

`removeDocument`函数的作用是从现有的`bagOfNgrams`对象中移除指定的文档，并更新词袋模型。函数接受以下参数：

- `bag`：一个`bagOfNgrams`对象，表示输入的词袋模型。
- `documents`：一个字符串列表，表示要从词袋模型中移除的文档。

函数的工作流程如下：

1. 从bag对象的doc属性中移除指定的文档。
2. 使用更新后的doc属性重新计算词袋模型。

函数返回更新后的bag对象。

#### 2.6 removeInfrequentNgrams函数设计

`removeInfrequentNgrams`函数的作用是从现有的`bagOfNgrams`对象中移除出现次数较少的n-grams，并更新词袋模型。函数接受以下参数：

- `bag：`一个bagOfNgrams对象，表示输入的词袋模型。

- `count：`一个整数，表示要移除出现次数不足count次的n-grams。

- `*args`一个可变参数，用于传递自定义参数。如果args为空，则不指定要移除的n-grams的长度。

  如果args不为空，则可以使用以下参数：

  - `'NgramLengths'`：只是为了符合matlab设计的标识参数
  - `lengths`：一个整数，用于指定要移除的n-grams的长度。如果指定了此参数，则只移除指定长度的n-grams。

函数的工作流程如下：

1. 计算每个n-gram在所有文档中的出现次数。
2. 找到出现次数不足count次的n-grams。
3. 创建一个新的Ngrams列表，其中排除了出现次数不足count次的n-grams。
4. 更新counts属性，移除出现次数不足count次的n-grams对应的列。
5. 更新bag对象的Ngrams、counts属性，并重新计算词袋模型。

函数返回更新后的bag对象。

#### 2.7 removeNgrams函数设计

`removeNgrams`函数的作用是从现有的`bagOfNgrams`对象中移除指定的n-grams，并更新词袋模型。函数接受以下参数：

- `bag`：一个bagOfNgrams对象表示输入的词袋模型。
- `ngrams`：一个字符串列表，表示要从词袋模型中移除的n-grams。
- `*args`：一个可变参数，用于传递自定义参数。如果args为空，则使用默认参数。如果args不为空，则可以使用以下参数：
  - `IgnoreCase`：一个布尔值，表示是否忽略大小写。默认为False。
  - `ngram_length`：一个整数，用于指定要移除的n-grams的长度。如果指定了此参数，则只移除指定长度的n-grams。

函数的工作流程如下：

1. 找到要删除的n-grams的索引。
2. 创建一个新的Ngrams列表，其中排除了要删除的n-grams。
3. 更新counts属性，移除要删除的n-grams对应的列。
4. 更新bag对象的Ngrams、counts属性，并重新计算词袋模型。

函数返回更新后的bag对象。

#### 2.8 removeEmptyDocuments函数设计

`removeEmptyDocuments`函数的作用是从输入的文本列表或`bagOfNgram`对象中删除没有单词或n-grams的文档。函数接受一个参数input，可以是一个文本列表或一个`bagOfNgram`对象。函数的工作流程如下：

1. 如果输入是一个文本列表，则删除其中没有单词的文档。
2. 如果输入是一个`bagOfNgram`对象，则删除其中没有单词或n-grams的文档。
3. 如果输入既不是文本列表也不是`bagOfNgram`对象，则引发ValueError异常。

如果输入是一个文本列表，则函数返回一个新的文本列表，其中删除了没有单词的文档。如果输入是一个`bagOfNgram`对象，则函数返回一个新的`bagOfNgram`对象，其中删除了没有单词或n-grams的文档。

#### 2.9 encode函数设计

`encode`函数的作用是将输入的文本数据编码为词袋模型的频率计数矩阵。函数接受两个参数：

- `bag`：一个`bagOfNgram`对象，表示用于编码的词袋模型。
- `input_data`：一个文本列表或文本字符串，表示要编码的文本数据。

函数的工作流程如下：

1. 如果输入是一个文本列表，则将其转换为词袋模型。
2. 如果输入是一个文本字符串，则将其转换为单词列表，然后将其转换为词袋模型。
3. 如果输入既不是文本列表也不是文本字符串，则引发ValueError异常。
4. 计算频率计数矩阵。
5. 返回频率计数矩阵。

#### 2.10 tfidf函数设计

tfidf() 函数的设计是为了计算词频-逆文档频率（TF-IDF）矩阵。TF-IDF 是一种常用的文本特征提取方法，它可以用于文本分类、信息检索、聚类等任务中。

- `bag`：bag 是一个词袋模型对象，它包含了文本数据的词频信息。
- `documents`：documents 是一个可选参数，它是一个文本数据列表，用于计算指定文本数据的 TF-IDF 矩阵。如果 documents 参数未指定，则计算 bag 中所有文档的 TF-IDF 矩阵。

在函数内部，首先创建了一个 TfidfTransformer() 类的对象，用于计算 TF-IDF 矩阵。然后，根据输入参数计算相应的 TF-IDF 矩阵。如果 documents 参数未指定，则直接使用 bag.X 属性中的数据计算 TF-IDF 矩阵；如果 documents 参数已指定，则需要先将文本数据转换为词袋模型，然后再计算 TF-IDF 矩阵。

最后，使用 toarray() 方法将稀疏矩阵转换为密集矩阵，并返回结果。

## 结果

### 1. bagOfNgrams函数库

#### 1.1 bagOfNgrams类测试

<img src="https://gitee.com/learnfair/img/raw/master/20230506190639.png" style="zoom: 50%;" />

其中文件 `sonnetsPreprocessed.txt` 包含莎士比亚十四行诗的预处理版本，是matlab官方的测试用例，可以看到与官方结果相同：

<img src="https://gitee.com/learnfair/img/raw/master/20230507121900.png" style="zoom: 55%;" />

#### 1.2 addDocuments和removeDocument测试

测试代码和结果：

![](https://gitee.com/learnfair/img/raw/master/20230506232352.png)

可以看出得到的bagOfNgrams数据是正确的

#### 1.3 topkngrams测试

测试代码：

<img src="https://gitee.com/learnfair/img/raw/master/20230507122650.png" style="zoom:67%;" />

测试结果：

<img src="https://gitee.com/learnfair/img/raw/master/20230506231518.png" style="zoom: 55%;" />

可以看出与matlab官方结果相同

<img src="https://gitee.com/learnfair/img/raw/master/20230507131040.png" style="zoom: 67%;" />

#### 1.4 removeInfrequentNgrams测试

测试代码和结果：

![](https://gitee.com/learnfair/img/raw/master/20230507133629.png)

![](https://gitee.com/learnfair/img/raw/master/20230507134052.png)

可以看出`removeInfrequentNgrams(bag1,2)`删掉了词频低于2的n-grams，保留了'i', 'like dogs', 'like'这些词频大于2的n-grams

#### 1.5 removeNgrams测试

测试代码和结果：

![](https://gitee.com/learnfair/img/raw/master/20230507135345.png)

如图所示，`removeNgrams(bag1,'like cats')`成功删掉了bag1中的`'like cats'`这一词组

#### 1.6 removeEmptyDocuments测试

测试代码和结果：

![](https://gitee.com/learnfair/img/raw/master/20230507134725.png)

如图所示，`removeEmptyDocuments(documents)`成功的删掉了没有单词的部分

#### 1.7 encode测试

测试代码和结果：

![](https://gitee.com/learnfair/img/raw/master/20230507135944.png)

如图所示，`encode(bag,documents)`成功基于n-gram 模型 `bag` 返回 `documents` 的频率计数矩阵

#### 1.8 tfidf测试

测试代码和结果：

![image-20230507161706618](https://gitee.com/learnfair/img/raw/master/image-20230507161706618.png)

如图所示，`tfidf(bag,documents)`成功基于n-gram 模型 `bag` 返回 `documents` 的TF-IDF 矩阵

## 总结

实验总结-成功实现了....成功通过测试....

优点：......

缺点：......

对实验和平台的反馈和评价

## 小组分工

|  成员  |                             工作                             | 实现函数库  | 实现函数个数 |
| :----: | :----------------------------------------------------------: | :---------: | :----------: |
|  李涛  |                                                              |             |              |
| 吴先强 | 实现Word and N-Gram Counting类中的bagOfNgrams函数组<br/>进行函数测试和相关部分的报告撰写 | bagOfNgrams |      9       |
|  张琦  |                                                              |             |              |
| 赵乐天 |                                                              |             |              |
| 张文浩 |                                                              |             |              |

