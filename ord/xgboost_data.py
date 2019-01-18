#coding=utf-8
import matplotlib.pyplot as plt

import xgboost as xgb
import os
import operator

os.chdir("/tmp")
# dtrain = xgb.DMatrix('uid_kbytes_cls_lab.80k')
# dtest = xgb.DMatrix('uid_kbytes_cls_lab.20k')
dtrain = xgb.DMatrix('/tmp/feat_label_libsvm_train')
dtest = xgb.DMatrix('/tmp/feat_label_libsvm_test')

params={
    'booster':'gbtree',
    'objective': 'multi:softmax', #多分类问题
    'num_class':32, # 类数，与 multisoftmax 并用
    'gamma':0.05,  # 在树的叶子节点下一个分区的最小损失，越大算法模型越保守 。[0:]
    'max_depth':12, # 构建树的深度 [1:]
    #'lambda':2,  # L2 正则项权重
    'subsample':0.9, # 采样训练数据，设置为0.5，随机选择一般的数据实例 (0:1]
    'colsample_bytree':0.7, # 构建树树时的采样比率 (0:1]
    #'min_child_weight':3, # 节点的最少特征数
    'silent':1 ,
    # 'tree_method': 'gpu_hist',
    'eta': 0.005, # 如同学习率
    'seed':710,
    'nthread':8,# cpu 线程数,根据自己U的个数适当调整
}
plst = list(params.items())
num_rounds = 100
evallist = [(dtest, 'test'), (dtrain, 'train')]

model = xgb.train(plst, dtrain, num_rounds, evallist, early_stopping_rounds=100)
model.save_model("0002.model")

importance = model.get_fscore()
importance = sorted(importance.items(), key=operator.itemgetter(1))
print (importance)
# importance = importance[:30]
xgb.plot_importance(model, max_num_features=30)
plt.show()


# ///////////   usage of the model
import numpy as np
import xgboost as xgb

bst = xgb.Booster({'nthread': 8, 'objective':'multi:softprob'})  # init model
bst.load_model('0002.model')  # load model

dtest = xgb.DMatrix('n')
# ypred = bst.predict_proba(dtest)
ypred_leaf = bst.predict(dtest, pred_leaf=True)
gv = xgb.to_graphviz(bst, num_trees=0)


classifier = xgb.XGBClassifier(objective='binary:softmax', booster='gbtree')
classifier.load_model("0002.model")
xtest = np.array([[2,11,1,1,1,0,5,4,2,2,11,2,1,11,12,6,130,59,0,11,65,59.1,12,0,3518.85,99,1950.03,100,60.33,17,16.51,59,4,59.03,100272]])
ypred = classifier.predict_proba(xtest) # return [[1,0]]