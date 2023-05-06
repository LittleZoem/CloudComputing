# 云计算

---



## 介绍

​	小组组队形式共同完成在天演平台开发和部署` Matlab` 函数库，从划分好的Toolbox 中选择主题，个人负责`Document Manipulation and Conversion`相关函数实现，使用 Python 语言的相关函数，在天演平台完成函数的开发部署并撰写小组实验报告。

---



## 选题背景

​	在科学研究和工程开发中，文档处理和转换是非常常见的任务。`Matlab`是一种流行的科学计算软件，它提供了许多`Document Manipulation and Conversion`(文档处理和转换)函数，例如`docfun、containsWords、containsNgrams、contains、plus、replace、regexprep、doclength、doc2cell、joinWords、string`等。这些函数可以帮助用户快速、方便地处理和转换文档数据，提高工作效率和准确性。然而，对于那些不熟悉`Matlab`的用户或者需要在python环境下使用的用户来说，使用这些函数可能会遇到一定的困难。因此，我们可以使用Python在天演平台开发部署来实现这些函数，以便更多的用户基于天演平台可以方便地使用它们。

---



## 设计

实现函数清单如下：

| [docfun](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.docfun.html) | Apply function to words in documents                        |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| [containsWords](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.containswords.html) | Check if word is member of documents                        |
| [containsNgrams](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.containsngrams.html) | Check if n-gram is member of documents                      |
| [contains](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.contains.html) | Check if pattern is substring in documents                  |
| [plus](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.plus.html) | Append documents                                            |
| [replace](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.replace.html) | Replace substrings in documents                             |
| [regexprep](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.regexprep.html) | Replace text in words of documents using regular expression |
| [doclength](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.doclength.html) | Length of documents in document array                       |
| [joinWords](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.joinwords.html) | Convert documents to string by joining words                |
| [string](https://ww2.mathworks.cn/help/textanalytics/ref/tokenizeddocument.string.html) | Convert scalar document to string vector                    |

设计思路如下：

​	`Document Manipulation and Conversion`中的相关函数主要是基于`tokenizedDocument`进行操作，`tokenizedDocument`是`Matlab`中的一个类，用于表示已经被分词的文档,类中存在许多属性和方法，但是在`python`中没有对应的数据类型，在保留其数据类型意义的同时，为了方便操作，将`tokenizedDocument array`简化为`python`中的`List[List[str]]`数据类型表示多文档分词后的结果。

​	`Document Manipulation and Conversion`函数中大多数函数实现较为简单，不需要引入额外的库，只需引入`typing`库做函数类型检查即可，只有在函数`regexprep`中由于需引入正则表达式而使用了内置库`re`,`docfun、containsWords、containsNgrams、plus、doclength、joinWords、string`这些函数实现设计都只是借助于简化后的数据结构`List[List[str]]`就可以较为简单地实现，详见平台或附件中的代码和描述，此处不再赘述。

​	在实现函数时，也可能会遇到一些困难，例如`matlab`和`python`对同一相似概念的实现略有不同，例如`matlab`和`python`中的正则表达式，二者虽然语法和用法存在一些差异，但是大体相同，在实现`matlab`中的`regexprep`函数时需要使用正则来匹配文档中的`word`,为了便于实现，使用`python`中的正则表达式规则来实现函数，使用`python`内置库中的`re.sub`来实现正则匹配和替换，此节末会对此函数详细介绍。

​	对于部分函数如`contains`以及`replace`，在实现过程中会需要使用`matlab`中的`Pattern`来进行匹配，但是在`Python`当中`Pattern`表达的意思和`matlab`差异较大，主要运用于正则表达式相关操作中，`Python`也没有类似的`matlab`中的`Pattern`实现，正则表达式是比较相近的，但是关于正则表达式地匹配会在`regexprep`实现，故这两个函数只实现了`substring`匹配。

#### regexprep

**函数实现**

```python
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
```

​	实现Matlab中的regexprep函数。它接受三个参数：documents、expressions和replaces，分别表示待处理的文档列表、正则表达式列表和替换字符串列表。函数的返回值是一个新的文档列表，其中每个文档都被替换了符合正则表达式的字符串。

函数的实现过程如下：

1. 首先，函数检查`expressions`和`replaces`列表的长度是否相等，如果不相等，则抛出一个异常。
2. 然后，函数遍历`documents`列表中的每个文档，并对每个文档中的每个单词进行处理。
3. 对于每个单词，函数遍历`expressions`列表中的每个正则表达式，并使用`Python`中的`re.sub()`函数将符合正则表达式的字符串替换为对应的替换字符串。
4. 将处理后的单词添加到新的文档中。
5. 将处理后的文档添加到新的文档列表中。
6. 最后，函数返回新的文档列表。

为了实现`Matlab`中的`regexprep`函数而编写的，它使用`Python`中的`re`库来实现正则表达式的匹配和替换操作。

**测试**

```python
def test_reregexprep():
    doc = [["I", "walk"], ["they", "walked"], ["we", "are", "walking"]]
    reg = [r"walk(\w*)", "th.y"]
    rep = [r"ascend\1", "-"]
    assert reregexprep(doc, reg, rep) == [['I', 'ascend'], ['-', 'ascended'], ['we', 'are', 'ascending']]
```

<img src="resource\image-20230506120241339.png" alt="image-20230506120241339" width="700;" />

测试`test_reregexprep`在本地`python`测试后再再天演平台进行测试，本测试是采用多个正则表达式进行测试，测试均通过。

**函数描述：**

该函数的详情描述在天演平台已经填写，此处搬来描述，其余不再赘述。

<img src="resource\image-20230506115715101.png" alt="image-20230506115715101" width="700;" />

<img src="resource\image-20230506115829256.png" alt="image-20230506115829256" width="700;;" />



---



## 结果

<img src="resource\image-20230506125128463.png" alt="image-20230506125128463" width="700;"   />

​	在天演平台上根据`matlab`原函数初步成功开发、测试、部署了`Document Manipulation and Conversion`中的相关函数`docfun、containsWords、containsNgrams、plus、doclength、joinWords、string`.

---



## 结论

​	本项目主要实现`Matlab`中的`Document Manipulation and Conversion`函数，以便在天演平台上进行文本处理和转换。这些函数可以对文档进行各种操作，例如检查单词是否在文档中出现、替换文档中的字符串、将文档转换为字符串等等。这些函数的实现使用`Python`语言，最后成功在天演平台上进行测试和部署.

---



## 小组成员分工

赵乐天主要负责`matlab`中`Document Manipulation and Conversion`相关函数的`python`实现、测试、部署以及报告编写

