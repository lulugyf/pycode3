#coding=utf-8

import re
import sys
import traceback

def __getprice(f1, f2):
    '从名称和注释内容中找出价格'
    f = f1 + " " + f2
    g = re.findall(r'([\d\.]+)元', f)
    if g is not None and len(g) > 0:
        # print(repr(g))
        return g[0]  #从观察的情况, 第一个带"元"的是价格
    return "-1"

def __getcontent(ct):
    # print(ct)
    '从套餐内容中分开语音和流量, 返回分钟数 流量数'
    if ct.endswith('分钟'):
        g = re.findall(r'([\d]+)', ct)
        return g[0], "0"
    else:
        g = re.findall(r'([\d]+)', ct)
        return "0", g[0]

def extractFeature(fpath):
    f = open(fpath, encoding="UTF-8")
    # OFFER_ID	OFFER_NAME	套餐id	套餐子记账id	STATID	总量	赠送类型	超套费用	OFFER_COMMENTS
    cidx = 5
    header = f.readline()
    if header.find('STATID') < 0:
        cidx = 4
    for line in f:
        d = line.strip().split('\t')
        id, name, comments, content = d[0], d[1], d[-1], d[cidx]
        try:
            price = __getprice(name, comments)
            voice, flow = __getcontent(content)
            print(id, price, voice, flow)
        except:
            print(line)
            traceback.print_stack()
            break


def checkid(fpath1='pcounts', fpath2='prod_feature.txt'):
    '检查文件1中的代码列,  在文件2中存在的, 代码列都是第一列'
    with open(fpath2, encoding='utf-8') as f:
        prod = {}
        for line in f:
            d = line.strip().split()
            prod[d[0]] = ' '.join(d[1:])
    with open(fpath1, encoding='utf-8') as f:
        for line in f:
            d = line.strip().split()
            pid = d[0]
            if pid not in prod:
                continue
            count = int(d[1])
            if count < 100:
                continue
            print(pid, count, prod[pid])  # 打印字段: 产品id  订购记录数 价格 语音分钟 流量kb

def downParts(fpath):
    '从hdfs下载spark输出的文件, 以 part-0??? 格式的系列文件, 下载的时候直接聚合到一个文件中'
    from pywebhdfs.webhdfs import PyWebHdfsClient
    hdfs = PyWebHdfsClient(host='iasp76', port='12003', user_name='mci')
    flist = hdfs.list_dir(fpath)
    x = flist['FileStatuses']['FileStatus']
    _SUCCESS = False
    for f in x:
        if f['pathSuffix'] == '_SUCCESS':
            _SUCCESS = True
            break
    if not _SUCCESS:
        print("not complete yet!")
        return
    fnames = [f['pathSuffix'] for f in x if f['pathSuffix'].startswith('part-')]
    fnames1 = sorted(fnames)
    foutname = fpath[fpath.rfind('/')+1:]
    l = len(fnames1)
    with open(foutname, "wb") as fo:
        for fname in fnames1:
            fpath1 = fpath + "/" + fname
            fo.write(hdfs.read_file(fpath1))
            print(" progress: ", fname, l)


def filter_cols():
    '取列序号, 要剔除 1, 3 类别的数据'
    f = open("filter.txt", encoding="utf-8")
    f.readline()
    cols = []
    cols1 = []
    i = 0
    for line in f:
        d = line.strip().split("\t")
        if len(d) < 5:
            print("col count invalid", line)
            continue
        if d[4] != '1' and d[4] != '3':
            cols.append("f(%d)"%(int(d[0])-1) )
            cols1.append("%d\t%s\n"%(i, line.strip())) # 剔除列后新的序号与列的对应
            i += 1
    f.close()
    # print(",".join(cols))
    with open("cols_rest.txt", "w", encoding="utf-8") as f:
        for line in cols1:
            f.write(line)

def filter_cols1(fname="cols_rest.txt", tp="2", col=5):
    '打印指定标识列的行'
    with open(fname, encoding="utf-8") as f:
        for line in f:
            d = line.strip().split("\t")
            if len(d) < col+1: continue
            if d[col] == tp:
                print(line.strip())

import operator
def xx():
    dd = [('f49', 1), ('f86', 1), ('f236', 1), ('f209', 1), ('f267', 1), ('f75', 1), ('f83', 2), ('f156', 2), ('f107', 2), ('f81', 3), ('f163', 3), ('f89', 4), ('f192', 5), ('f261', 5), ('f178', 5), ('f268', 5), ('f78', 5), ('f160', 6), ('f76', 6), ('f84', 6), ('f249', 6), ('f92', 7), ('f223', 7), ('f245', 7), ('f63', 7), ('f250', 7), ('f80', 8), ('f74', 8), ('f51', 9), ('f101', 9), ('f7', 9), ('f135', 10), ('f225', 11), ('f219', 11), ('f46', 11), ('f179', 12), ('f183', 12), ('f185', 12), ('f248', 12), ('f27', 12), ('f176', 13), ('f165', 14), ('f73', 14), ('f39', 17), ('f96', 17), ('f105', 17), ('f24', 18), ('f151', 18), ('f254', 18), ('f172', 18), ('f91', 20), ('f104', 20), ('f265', 20), ('f186', 21), ('f93', 21), ('f45', 21), ('f97', 21), ('f171', 21), ('f251', 22), ('f153', 22), ('f168', 25), ('f106', 26), ('f149', 26), ('f123', 27), ('f65', 27), ('f152', 27), ('f112', 27), ('f217', 30), ('f161', 31), ('f182', 32), ('f116', 32), ('f121', 32), ('f164', 32), ('f134', 34), ('f240', 35), ('f162', 35), ('f100', 37), ('f150', 38), ('f99', 39), ('f234', 41), ('f48', 41), ('f175', 42), ('f173', 42), ('f196', 45), ('f207', 46), ('f90', 48), ('f260', 48), ('f167', 49), ('f177', 49), ('f169', 50), ('f174', 51), ('f159', 51), ('f241', 51), ('f259', 54), ('f146', 54), ('f266', 56), ('f9', 58), ('f119', 58), ('f4', 62), ('f98', 62), ('f271', 62), ('f170', 64), ('f12', 64), ('f187', 71), ('f120', 71), ('f148', 74), ('f72', 74), ('f264', 74), ('f127', 74), ('f140', 75), ('f64', 80), ('f52', 80), ('f253', 84), ('f263', 85), ('f103', 86), ('f212', 86), ('f197', 87), ('f215', 87), ('f126', 89), ('f68', 89), ('f59', 92), ('f60', 94), ('f235', 98), ('f67', 102), ('f230', 103), ('f184', 104), ('f243', 104), ('f210', 104), ('f206', 105), ('f238', 106), ('f231', 109), ('f108', 109), ('f258', 110), ('f141', 113), ('f166', 115), ('f195', 115), ('f53', 115), ('f137', 119), ('f229', 119), ('f47', 119), ('f58', 122), ('f237', 123), ('f28', 126), ('f66', 128), ('f55', 128), ('f110', 130), ('f122', 134), ('f199', 136), ('f269', 137), ('f273', 138), ('f71', 138), ('f143', 148), ('f262', 149), ('f220', 151), ('f128', 154), ('f233', 154), ('f56', 156), ('f142', 157), ('f227', 157), ('f226', 158), ('f255', 159), ('f256', 161), ('f109', 166), ('f30', 169), ('f54', 170), ('f118', 177), ('f69', 177), ('f138', 179), ('f193', 180), ('f222', 192), ('f29', 195), ('f115', 195), ('f218', 196), ('f113', 197), ('f221', 197), ('f42', 198), ('f1', 207), ('f232', 208), ('f94', 209), ('f40', 210), ('f270', 221), ('f136', 222), ('f95', 223), ('f203', 227), ('f35', 229), ('f8', 231), ('f57', 236), ('f11', 239), ('f31', 248), ('f33', 249), ('f247', 252), ('f62', 264), ('f32', 272), ('f155', 278), ('f154', 281), ('f158', 282), ('f70', 285), ('f205', 301), ('f144', 303), ('f130', 307), ('f125', 316), ('f18', 328), ('f157', 329), ('f139', 334), ('f13', 338), ('f228', 340), ('f23', 343), ('f41', 351), ('f36', 352), ('f189', 355), ('f22', 368), ('f201', 369), ('f204', 410), ('f61', 412), ('f19', 413), ('f147', 418), ('f272', 453), ('f44', 495), ('f129', 501), ('f111', 506), ('f244', 520), ('f43', 533), ('f202', 546), ('f242', 555), ('f114', 600), ('f257', 615), ('f34', 656), ('f198', 660), ('f145', 666), ('f21', 705), ('f200', 709), ('f10', 841), ('f38', 864), ('f37', 879), ('f17', 900), ('f208', 976), ('f246', 1014), ('f16', 1138), ('f211', 1159), ('f117', 1220), ('f20', 1236), ('f15', 1247), ('f50', 1312), ('f26', 1440), ('f14', 1694), ('f25', 2068), ('f216', 2779)]
    d1 = [int(d[0][1:]) for d in dd]
    # t = sorted(d1, key=operator.itemgetter(0))
    t = sorted(d1)
    print(t[-2:])
import os
import sys
if __name__ == '__main__':
    'main entry'
    os.chdir('d:/tmp/iasp')
    # filter_cols()
    # filter_cols1(fname="cols_rest.txt", tp="2", col=5)  # 这些列的值是非数字化的
    xx()

    # s = '10005	如意通-包月套餐211号新疆通78元月租送1000分钟本地通话	GP0105	GP0105E	1000分钟	vc-语音赠送	按标批资费收取	如意通-包月套餐211号新疆通78元月租送1000分钟本地通话'
    # d = s.split('\t')
    # id, name, comments, content = d[0], d[1], d[-1], d[5]
    # price = __getprice(name, comments)
    # voice, flow = __getcontent(content)
    # sys.stdout = open('pid.txt', 'w')
    # for i in range(3):
    #     extractFeature(r'd:\tmp\iasp\o%d.txt'%i)
    # checkid()
    # sys.stdout.close()

    # if len(sys.argv) > 1:
    #     downParts(sys.argv[1])
    # else:
    #     downParts('/data/uid_price_cls')
