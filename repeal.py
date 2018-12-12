#coding=utf-8

import re

# https://zhuanlan.zhihu.com/p/33925599

# 1. 从原始文件中取出4级分类, 剔重后排序产生序号, 分别保存到文件中
def csv2cls(srcfile, dst_dir="d:/tmp/d"):
    cls = [{} for i in range(4)]  # 4级分类
    with open(srcfile, encoding="utf-8") as f:
        f.readline()
        for ln in f:
            t = ln.strip().split(",")
            for i in range(4):
                cls[i][t[5+i].strip()] = 1
    for x in range(len(cls)):
        keys = cls[x].keys()
        keys1 = sorted(keys)
        with open("%s/cls_%d.txt"%(dst_dir, x), "w", encoding="utf-8") as f:
            for i in range(len(keys1)):
                f.write("%s,%d\n"%(keys1[i], i))

# 从 csv2cls 生成的文件中读取内容, 生成字典, 用于数值化原始字段内容
def __cls2dict(dst_dir="d:/tmp/d"):
    cls = []
    for x in range(4):
        c = {}
        with open("%s/cls_%d.txt"%(dst_dir, x), encoding="utf-8") as f:
            for ln in f:
                d = ln.strip().split(",")
                if len(d) != 2:
                    continue
                c[d[0].strip()] = d[1]
        cls.append(c)
    return cls

# 2. 原始文件中抽取原始申述内容及类别
def raw2content(srcfile, dst_dir="d:/tmp/d"):
    cls = __cls2dict()
    with open("%s/content.txt"%dst_dir, "w", encoding="utf=8") as fo:
        with open(srcfile, encoding="utf-8") as f:
            f.readline()
            for ln in f:
                t = ln.strip().split(",")
                content=t[3]
                c = ",".join([ cls[i][t[5+i].strip()] for i in range(4)])
                fo.write(content)
                fo.write(",%s\n"%c)

# 3. cut word
# def cutwords(contentfile):
#     import jieba
#     with open(contentfile, encoding="utf-8") as f:
#         for ln in f:
#             t = ln.strip().split(",")
#             content = t[0]
#             seg_list = jieba.cut(content, cut_all=False)

def rd():
    # https://chrisalbon.com/machine_learning/trees_and_forests/random_forest_classifier_example/
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    import pandas as pd
    # Set random seed
    np.random.seed(0)

    # Create an object called iris with the iris data
    iris = load_iris()
    # Create a dataframe with the four feature variables
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    # View the top 5 rows
    print(df.head())

    # Add a new column with the species names, this is what we are going to try to predict
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
    train, test = df[df['is_train'] == True], df[df['is_train'] == False]
    # Show the number of observations for the test and training dataframes
    print('Number of observations in the training data:', len(train))
    print('Number of observations in the test data:', len(test))

    # Create a list of the feature column's names
    features = df.columns[:4]

    y = pd.factorize(train['species'])[0]
    clf = RandomForestClassifier(n_jobs=2, random_state=0)
    clf.fit(train[features], y)
    
    clf.predict(test[features])

def loadDataSet(dataset_in="d:/tmp/d/content_cut.txt"):
    features = []
    labels = []
    with open(dataset_in, encoding="utf-8") as f:
        for ln in f:
            t = ln.strip().split(",")
            # features.append(t[0].split(" "))
            features.append(t[0].strip())
            labels.append(int(t[-1]))
    return features, labels

def main():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    from sklearn import metrics
    import pandas as pd
    import pickle

    features, labels = loadDataSet()
    # vocab = createVocabList(features)
    vect = TfidfVectorizer(ngram_range=(1,3),
                           min_df=10  #词出现次数小于10的忽略掉
                           )
    tv = vect.fit(features, labels)
    out = tv.transform(features)
    y = np.array([int(i) for i in labels])

    clf = RandomForestClassifier(n_jobs=4, random_state=0)
    clf.fit(out, y)

    # 尝试保存模型,  实际执行后发现文件有1.5g大小
    # fo = open("d:/tmp/d/clf.pickle", "wb")
    # pickle.dump(clf, fo)
    # fo.close()

    pred = clf.predict(out)

    # y = np.array([1, 1, 2, 2])
    # pred = np.array([0.1, 0.4, 0.35, 0.8])

    # Create confusion matrix
    cfm = pd.crosstab(y, pred, rownames=['Actual Species'], colnames=['Predicted Species'])

    # zip 真实值和预测值
    #a = np.array([y, pred]).T
    count = 0
    for i in range(y.shape[0]):
        if y[i] == pred[i]:
            count += 1
    print("accuracy: %.2f"%(count*100.0 / y.shape[0]))

    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
    roc_auc = metrics.auc(fpr, tpr)
    import matplotlib.pyplot as plt
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')

if __name__ == '__main__':
    srcfile = 'd:/tmp/unicom@repeal@201808.csv'
    contentfile = "d:/tmp/d/content.txt"
    #csv2cls(srcfile)
    #raw2content(srcfile)
    #cutwords(contentfile)
    rd()
