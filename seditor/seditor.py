# -*- coding: utf-8 -*-

import sys
import os
os.putenv('QT_PLUGIN_PATH', 'D:\dev\Anaconda3\Library\plugins')
# set QT_PLUGIN_PATH=D:\dev\Anaconda3\Library\plugins

#  http://zetcode.com/gui/pyqt5/    学习


#PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
#PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
#PYQT5 QFileDialog, QColorDialog, QDialog


#PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import (QAbstractItemModel, QFile, QIODevice,
        QItemSelectionModel, QModelIndex, Qt)


import ui
import actions
import fs
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

        splitter1 = QtWidgets.QSplitter(Qt.Horizontal, self)

        tree = QtWidgets.QTreeView(self)

        # tree.setHeaderHidden(True)
        tree.doubleClicked.connect(self.noteOpen)
        tree.setContextMenuPolicy(Qt.CustomContextMenu)
        tree.customContextMenuRequested.connect(self.contextTree)
        tree.setRootIsDecorated(True)
        tree.setSortingEnabled(False)
        self.tree = tree

        splitter1.addWidget(self.tree)
        splitter1.addWidget(text)

        self.setCentralWidget(splitter1) # self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        text.setContextMenuPolicy(Qt.CustomContextMenu)
        text.customContextMenuRequested.connect(self.contextNote)
        text.textChanged.connect(self.changed)

        # w, h = 1030, 800
        # self.setGeometry(100,100,w,h)
        w = self.geometry().width()
        tree_percent = 0.2
        splitter1.setSizes([int(w*tree_percent), int(w*(1-tree_percent))])
        # self.setWindowTitle("sedit Note Writer")
        self.setWindowIcon(QtGui.QIcon("icons/th.jpg"))

        self._openWorkDir()
        self._title()

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

        root = model.rootItem
        for row in range(root.childCount()):
            idx = model.index(row, 0)
            tree.expand(idx)
        fs.FS.addRecentDir(wd)

        last_open = self.fs.getConf("last_open")
        if last_open != "":
            self.__openNote(last_open)
        win_geo = self.fs.getConf("window_geometry")
        if win_geo != "":
            v = [int(i) for i in win_geo.split(",")]
            self.win_geo = QtCore.QRect(v[0], v[1], v[2], v[3])

    def _title(self, changeSave=True):
        editFile = self.fs.path(self.filename)
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
        with open(fpath, "rt") as file:
            self.text.setText(file.read())
            self.changesSaved = True
        self.filename = fpath
        self._title()
        self.fs.setConf("last_open", self.filename)


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
