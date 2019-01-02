# -*- coding: utf-8 -*-

import sys
import os
os.putenv('QT_PLUGIN_PATH', 'D:\dev\Anaconda3\Library\plugins')
# set QT_PLUGIN_PATH=D:\dev\Anaconda3\Library\plugins

#  http://zetcode.com/gui/pyqt5/    学习

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

codepath = os.path.dirname(__file__)
sys.path.insert(0, codepath)
import ui
import actions
import fs
from ext import de
from treemodel import TreeModel
import traceback

class Main(QtWidgets.QMainWindow,
           ui.UISetup,
           actions.TreeActions,
           actions.TableActions,
           actions.FormatActions,
           actions.ToolActions,
           actions.WorkspaceAction):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.filename = ""
        self.basedir = ""
        self.changesSaved = True
        self.initUI()

    def initUI(self):
        try:
            self.initTreeAndContentView()

            self.initToolbar()
            self.initFormatbar()
            self.initMenubar()
            self.addRecentToFileMenu(fs.FS.getRecentDirs())

            # self.setWindowTitle("sedit Note Writer")
            self.setWindowIcon(QtGui.QIcon("icons/th.jpg"))

            self._openWorkDir()
        except:
            traceback.print_exc()
        #self._title()

    def _title(self, changeSave=True):
        editFile = self.fs.rpath(self.filename)
        t = ""
        if not changeSave:
            t = "*"
        self.setWindowTitle("SEditor [%s] [%s] %s" % (self.basedir, editFile, t) )

    def changed(self):
        if self.changesSaved:
            self._title(False)
        self.changesSaved = False

    def _beforeClose(self):
        '''do something before close'''
        # save the window geometry
        g = self.geometry()
        self.fs.setConf("window_geometry", "%d,%d,%d,%d" % (g.x(), g.y(), g.width(), g.height()))
        self.fs.saveConf()

    def contextNote(self, pos):
        '''show context menu of note'''
        # Grab the cursor
        cursor = self.text.textCursor()
        # Grab the current table, if there is one
        table = cursor.currentTable()

        if table:
            try:
                ui.showTableContextMenu(table, pos, cursor, self)
            except Exception as e:
                print(e)
        else:
            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())
            self.text.contextMenuEvent(event)

    def treeSelChg(self, sel, desel):
        '''tree item selection changed, save the last selection'''
        try:
            first = desel.first()
            if first is None:
                return
            idxs = first.indexes()
            if len(idxs) > 0:
                self.last_sel = idxs[0]
        except Exception as e:
            print("treeSelChg failed")
            import traceback
            traceback.print_exc()

    def noteOpen(self, index):
        '''event-handler: 双击tree节点打开文档'''
        data = self.tree.model().getItem(index).itemData
        if data.type == fs.ItemType.DIR:
            return
        if self.filename == data.fpath:
            return
        if not self.changesSaved:
            # Done 切换note的时候, 应该提示是否保存, 可选择不另外打开
            if self._confirm("Original note had been changed!", "Do you want save it first?"):
                self.save()
            else:
                if hasattr(self, "last_sel"):
                    # 恢复上次的选择
                    idx = self.last_sel
                    self.tree.selectionModel().select(idx, QtCore.QItemSelectionModel.ClearAndSelect)
                return
        self.__openNote(data.fpath)

    def __openNote(self, fpath):
        '''实际执行打开文档'''
        text = fs.readTextFile(fpath, self.has_pass, self.pswd)
        self.filename = fpath
        self.fs.setConf("last_open", self.fs.rpath(self.filename))
        self.text.setText(text)
        self.changesSaved = True
        self._title()
        # 恢复光标位置
        # curpos = self.fs.getConf("cursor_%s"%self.filename)
        # if curpos != '':
        #     cursor = self.text.textCursor()
        #     cursor.setPosition(int(curpos))
        #     self.text.setTextCursor(cursor)


    def _openWorkDir(self, wd=None, reopen=False):
        '''打开工作目录'''
        if wd is None:
            wd = fs.FS.getRecentDirs()[-1]
        if wd == self.basedir:
            return
        print("--openWorkDir:"+wd)
        tree = self.tree
        self.basedir = wd #
        self.fs = fs.FS(self.basedir)
        model = TreeModel(None, self.fs.loadDir())
        tree.setModel(model)
        for i in range(1, model.columnCount()):
            tree.setColumnHidden(i, True)  # 隐藏其它列

        fs.FS.addRecentDir(wd)

        if not reopen:
            has_pass = self.fs.getConf("has_pass")
            if has_pass == "True":
                self.pswd = de.inputPassword(self)
                self.has_pass = True
            else:
                self.pswd = ""
                self.has_pass = False

        last_open = self.fs.getConf("last_open")
        if last_open != "":
            self.__openNote(self.fs.apath(last_open))
        win_geo = self.fs.getConf("window_geometry")
        if win_geo != "":
            v = [int(i) for i in win_geo.split(",")]
            self.win_geo = QtCore.QRect(v[0], v[1], v[2], v[3])

        self.last_sel = self._expand_opened_tree(last_open, tree)
        if not hasattr(self, 'selchangedevent'):
            self.tree.selectionModel().selectionChanged.connect(self.treeSelChg) #这个放在上个语句前, 有打不开的情况
            self.selchangedevent = True

    def _expand_opened_tree(self, last_open, tree):
        ''' find opened note, expand the tree '''
        import treemodel
        # 组合需要逐级展开的 tree-path
        segs = last_open.split(os.path.sep)
        segs.insert(0, self.basedir.split(os.path.sep)[-1])
        nsegs = [i+"/" for i in segs[:-1]]
        nsegs.append(segs[-1][:-7]) #添加文件名并去掉 .writer
        return treemodel.expand(tree, nsegs)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()

    if hasattr(main, 'win_geo'):
        main.setGeometry(main.win_geo) # restore window pos
    else:
        availableSize = QtWidgets.QApplication.desktop().availableGeometry(main).size()
        main.resize(availableSize * 3 / 4)
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
