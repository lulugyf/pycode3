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
        tree.doubleClicked.connect(self.itemOpen)
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
        text.customContextMenuRequested.connect(self.context)
        text.textChanged.connect(self.changed)

        # w, h = 1030, 800
        # self.setGeometry(100,100,w,h)
        w = self.geometry().width()
        tree_percent = 0.2
        splitter1.setSizes([int(w*tree_percent), int(w*(1-tree_percent))])
        # self.setWindowTitle("sedit Note Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

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
        # w = tree.geometry().width()
        # print("--w", w)
        # tree.setColumnWidth(0, int(w*0.8))

        root = model.rootItem
        for row in range(root.childCount()):
            idx = model.index(row, 0)
            tree.expand(idx)
        fs.FS.addRecentDir(wd)


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

    def closeEvent(self,event):
        if self.changesSaved:
            event.accept()
        else:
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("The document has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QtWidgets.QMessageBox.Save   |
                                      QtWidgets.QMessageBox.Cancel |
                                      QtWidgets.QMessageBox.Discard)
            
            popup.setDefaultButton(QtWidgets.QMessageBox.Save)
            answer = popup.exec_()
            if answer == QtWidgets.QMessageBox.Save:
                self.save()
            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

    def context(self, pos):
        # Grab the cursor
        cursor = self.text.textCursor()
        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:
            try:
                ui.showTableContextMenu(table, pos, cursor, self)
            except Exception as e:
                print(e)
        else:
            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())
            self.text.contextMenuEvent(event)
    def contextTree(self, pos):
        '''tree context menu request'''
        tree = self.tree
        index = tree.indexAt(pos)
        # index = self.tree.selectionModel().currentIndex()
        if not index.isValid():
            return
        model = self.tree.model()
        data = model.getItem(index).itemData

        menu = QtWidgets.QMenu(self)
        if data.type == fs.ItemType.FILE:
            delNoteAction = QtWidgets.QAction("Delete Note", self)
            delNoteAction.triggered.connect(lambda: self.delNote(model, index, data))
            menu.addAction(delNoteAction)
        elif data.type == fs.ItemType.DIR:
            addNoteAction = QtWidgets.QAction("Add Note", self)
            addNoteAction.triggered.connect(lambda: self.addNote(model, index, data.fpath))
            menu.addAction(addNoteAction)
            addFolderAction = QtWidgets.QAction("Add Folder", self)
            addFolderAction.triggered.connect(lambda: self.addFolder(model, index, data))
            menu.addAction(addFolderAction)
            delFolderAction = QtWidgets.QAction("Delete Folder", self)
            delFolderAction.triggered.connect(lambda: self.delFolder(model, index, data))
            menu.addAction(delFolderAction)
        menu.move(self.tree.mapToGlobal(pos))
        menu.show()

    def itemOpen(self, index):
        data = self.tree.model().getItem(index).itemData
        if data.type == fs.ItemType.DIR:
            return
        if self.filename == data.fpath:
            return
        if not self.changesSaved:
            self.save()
        # print("--double click on ", repr(data))

        self.filename = data.fpath
        with open(self.filename, "rt") as file:
            self.text.setText(file.read())
            self.changesSaved = True
        self._title()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()

    availableSize = QtWidgets.QApplication.desktop().availableGeometry(main).size()
    main.resize(availableSize * 3 / 4)
    # main.setColumnWidth(0, tree.width() / 3)
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
