# -*- coding: utf-8 -*-

# 文件处理工具

from treemodel import TreeItem
import os
from enum import Enum
import time
import shutil
import pathlib

class ItemType(Enum):
    DIR = 1
    FILE = 2

class FSItem:
    _names_ = ('name', 'mtime', 'fpath', 'type')
    def __init__(self, name, mtime, fpath, type):
        self.__attr = [name, mtime, fpath, type]
    def __len__(self):
        return len(self.__attr)
    def __getitem__(self, item):
        return self.__attr[item]
    def __getattr__(self, item):
        return self.__attr[FSItem._names_.index(item)]

class FS:
    def __init__(self, basedir):
        self.basedir = basedir

    def loadDir(self):
        basedir = self.basedir
        os.chdir(basedir)
        if not os.path.isdir(basedir):
            print("basedir must be a directory:", basedir)
            return None
        basename = os.path.basename(basedir)
        rootItem = TreeItem(['Name', "Date", "Path", ItemType.DIR])
        baseItem = rootItem.appendChild(FSItem("[D]"+basename, '', basedir, ItemType.DIR))
        def children(path, parent):
            for n in os.listdir(path):
                if n.startswith("."): continue
                fpath = path + os.path.sep + n
                if os.path.isdir(fpath):
                    c = parent.appendChild(FSItem("[D]"+n, '', fpath, ItemType.DIR))
                    children(fpath, c)
                elif n.endswith(".writer"):
                    n = n[:-7]
                    mtime = time.strftime("%Y%m%d %H:%M", time.localtime(os.path.getmtime(fpath) ))
                    parent.appendChild(FSItem(n, mtime, fpath, ItemType.FILE))
        children(basedir, baseItem)
        return rootItem

    def imagePath(self, imageFile, noteFile):
        '''copy the image file into content folder
        return the copied path and content path in html
        '''
        content_dir = os.path.dirname(noteFile) + os.path.sep + ".attr-" + os.path.basename(noteFile)[:-7]
        if not os.path.exists(content_dir):
            os.mkdir(content_dir)
        fpath = content_dir + os.path.sep + os.path.basename(imageFile)
        if not fpath.startswith(self.basedir):
            print("invalid path!!!", fpath, self.basedir)
            return None, None
        shutil.copy(imageFile, fpath)
        cpath = fpath[len(self.basedir):].replace("\\", "/")
        if cpath[0] == '/':
            cpath = cpath[1:]
        return fpath, cpath
    def tempImagePath(self, noteFile, imageType="jpg"):
        '''产生一个临时的图片文件路径'''
        content_dir = os.path.dirname(noteFile) + os.path.sep + ".attr-" + os.path.basename(noteFile)[:-7]
        if not os.path.exists(content_dir):
            os.mkdir(content_dir)
        fpath = content_dir + os.path.sep + str(time.time()) + "." + imageType
        if not fpath.startswith(self.basedir):
            print("invalid path!!!", fpath, self.basedir)
            return None, None
        cpath = fpath[len(self.basedir):].replace("\\", "/")
        if cpath[0] == '/':
            cpath = cpath[1:]
        return fpath, cpath

    def path(self, fpath):
        '''返回文件的相对路径'''
        if not fpath.startswith(self.basedir):
            print("invalid path--!", fpath, self.basedir)
            return '-'
        cpath = fpath[len(self.basedir):]
        if cpath[0] == os.path.sep:
            cpath = cpath[1:]
        return cpath

    @staticmethod
    def getRecentDirs():
        userHome = str(pathlib.Path.home())
        recentFile = userHome + os.path.sep + ".seditor.recent"
        if not os.path.exists(recentFile):
            newPath = userHome + os.path.sep + "mywd"
            if not os.path.exists(newPath):
                os.mkdir(newPath)
            recents = [newPath,]
        else:
            with open(recentFile, encoding="UTF-8") as f:
                lines = f.readlines()
                if len(lines) > 10:
                    lines = lines[-10:]
            recents = [s.strip() for s in lines]
        return recents
    @staticmethod
    def addRecentDir(path):
        userHome = str(pathlib.Path.home())
        recentFile = userHome + os.path.sep + ".seditor.recent"
        recents = FS.getRecentDirs()
        if path == recents[-1]:
            return
        recents.append(path)
        if len(recents) > 10:
            recents = recents[-10:]
        with open(recentFile, "w", encoding="UTF-8") as f:
            f.write("\n".join(recents) )


if __name__ == '__main__':
    fpath = r"d:\tmp\notes"
    print(os.path.basename(fpath))
    mtime = time.strftime("%Y%m%d %H:%M", time.localtime(os.path.getmtime(fpath)))
    print(mtime)

    # _names_ = ('name', 'mtime', 'fpath', 'type')
    # print(_names_.index('fpath'))
    h = pathlib.Path.home()
    print(dir(h))