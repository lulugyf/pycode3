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

class Main(QtWidgets.QMainWindow,
           ui.UISetup,
           actions.TreeActions,
           actions.TableActions,
           actions.FormatActions,
           actions.ToolActions):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.filename = ""
        self.basedir = ""
        self.changesSaved = True
        self.initUI()

    def initUI(self):
        text = QtWidgets.QTextEdit(self)
        self.text = text

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        text.setTabStopWidth(33)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()
        self.addRecentToFileMenu(fs.FS.getRecentDirs())


        tree = QtWidgets.QTreeView(self)

        # tree.setHeaderHidden(True)
        tree.doubleClicked.connect(self.noteOpen)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.customContextMenuRequested.connect(self.contextTree)
        tree.setRootIsDecorated(True)
        tree.setSortingEnabled(False)
        self.tree = tree


        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        text.setContextMenuPolicy(Qt.CustomContextMenu)
        text.customContextMenuRequested.connect(self.contextNote)
        text.textChanged.connect(self.changed)

        splitter1 = QtWidgets.QSplitter(Qt.Horizontal, self)
        splitter1.addWidget(self.tree)
        splitter1.addWidget(text)
        self.setCentralWidget(splitter1)

        w = self.geometry().width()
        tree_percent = 0.2
        splitter1.setSizes([int(w*tree_percent), int(w*(1-tree_percent))])
        # self.setWindowTitle("sedit Note Writer")
        self.setWindowIcon(QtGui.QIcon("icons/th.jpg"))

        self._openWorkDir()
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

    def noteOpen(self, index):
        data = self.tree.model().getItem(index).itemData
        if data.type == fs.ItemType.DIR:
            return
        if self.filename == data.fpath:
            return
        if not self.changesSaved:
            self.save()
        self.__openNote(data.fpath)

    def __openNote(self, fpath):
        try:
            # print("__openNote, pswd", repr(self.pswd), fpath)
            if self.has_pass == False:
                with open(fpath, "rt") as file:
                    text = file.read()
            else: # q12201
                text = de.decryptFromFile(self.pswd, fpath)
        except:
            return
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

    def _openWorkDir(self, wd=None):
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
        for i in range(2, model.columnCount()):
            tree.setColumnHidden(i, True)

        fs.FS.addRecentDir(wd)

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

        idx_root = model.index(0, 0)
        tree.expand(idx_root)
        self._expand_opened_tree(last_open, tree)

    def _expand_opened_tree(self, last_open, tree):
        # find opened note, expand the tree
        model = tree.model()
        item = model.rootItem.child(0)
        idx_root = model.index(0, 0)
        idx = model.index(0, 0, idx_root)
        print("    --", idx.row(), idx.parent().row(), idx_root.row(), idx_root.parent().row())
        pi = last_open.split(os.path.sep)[:-1]
        for path_seg in pi:
            path_seg = path_seg + "/"
            #print("---path_seg", path_seg)
            for i in range(item.childCount()):
                c = item.child(i)
                if c.itemData.name == path_seg:
                    idx = model.index(i, 0, parent=idx)
                    tree.expand(idx)
                    item = c
                    print("    --", i, c.itemData.name, idx.row(), idx.column())
                    break


    def save(self):
        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:
            # Append extension if not there yet
            if not self.filename.endswith(".writer"):
              self.filename += ".writer"

            if self.has_pass == False:
                with open(self.filename,"wt") as file:
                    file.write(self.text.toHtml())
            else: # q12201
                de.encryptToFile(self.text.toHtml(), self.pswd, self.filename)

            self.changesSaved = True
            self._title()

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
