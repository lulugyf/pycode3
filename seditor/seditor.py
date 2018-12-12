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

from PyQt5 import QtPrintSupport
#PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import (QAbstractItemModel, QFile, QIODevice,
        QItemSelectionModel, QModelIndex, Qt)

from ext import *
import ui
from editabletreemodel import TreeModel

class Main(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.filename = ""
        self.changesSaved = True
        self.initUI()

    def initUI(self):
        self.text = QtWidgets.QTextEdit(self)

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.text.setTabStopWidth(33)

        ui.initToolbar(self)
        ui.initFormatbar(self)
        ui.initMenubar(self)

        splitter1 = QtWidgets.QSplitter(Qt.Horizontal, self)

        #self.tree, self.model = ui.initTreeView(self)
        headers = ("Title", "Description")
        model = TreeModel(headers, open("default.txt").read())
        self.tree = QtWidgets.QTreeView(self)
        self.tree.setModel(model)
        self.tree.setColumnHidden(1, True)
        self.tree.setHeaderHidden(True)

        splitter1.addWidget(self.tree)
        splitter1.addWidget(self.text)

        self.setCentralWidget(splitter1) # self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.context)

        self.text.textChanged.connect(self.changed)

        # w, h = 1030, 800
        # self.setGeometry(100,100,w,h)
        #print(dir(self.geometry()))
        w = self.geometry().width()
        tree_percent = 0.2
        splitter1.setSizes([int(w*tree_percent), int(w*(1-tree_percent))])
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        self.filename = "ab.txt.writer"
        with open(self.filename, "rt") as file:
            self.text.setText(file.read())
            self.changesSaved = True

    def changed(self):
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

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(),1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(),1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()
        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()
        # Get the current cell
        cell = table.cellAt(cursor)
        # Insert a new row at the cell's position
        table.insertRows(cell.row(),1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(),1)


    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):
        state = self.statusbar.isVisible()
        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):
        spawn = Main()
        spawn.show()

    def open(self):
        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")[0]

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

    def save(self):
        # Only open dialog if there is no filename yet
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        if not self.filename:
          self.filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:
            # Append extension if not there yet
            if not self.filename.endswith(".writer"):
              self.filename += ".writer"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename,"wt") as file:
                file.write(self.text.toHtml())

            self.changesSaved = True

    def preview(self):
        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()

    def printHandler(self):
        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):
        cursor = self.text.textCursor()
        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def wordCount(self):
        wc = wordcount.WordCount(self)
        wc.getText()
        wc.show()

    def insertImage(self):
        # Get image file name
        #PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]
        if filename:
            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():
                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                          "Image load error",
                                          "Could not load image file!",
                                          QtWidgets.QMessageBox.Ok,
                                          self)
                popup.show()
            else:
                cursor = self.text.textCursor()
                cursor.insertImage(image,filename)

    def fontColorChanged(self):
        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()
        # Set it as the new text color
        self.text.setTextColor(color)

    def highlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self.text.setTextBackgroundColor(color)

    def bold(self):
        if self.text.fontWeight() == QtGui.QFont.Bold:
            self.text.setFontWeight(QtGui.QFont.Normal)
        else:
            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):
        state = self.text.fontItalic()
        self.text.setFontItalic(not state)

    def underline(self):
        state = self.text.fontUnderline()
        self.text.setFontUnderline(not state)

    def strike(self):
        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):
        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):
        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):
        # Grab the cursor
        cursor = self.text.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:
            cursor.insertText("\t")

    def handleDedent(self,cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):
        cursor = self.text.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)
        else:
            self.handleDedent(cursor)


    def bulletList(self):
        cursor = self.text.textCursor()
        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):
        cursor = self.text.textCursor()
        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def insertTreeChild(self):
        index = self.tree.selectionModel().currentIndex()
        model = self.tree.model()
        if model.columnCount(index) == 0:
            if not model.insertColumn(0, index):
                return
        if not model.insertRow(0, index):
            return
        for column in range(model.columnCount(index)):
            child = model.index(0, column, index)
            model.setData(child, "[No data]", Qt.EditRole)
            if model.headerData(column, Qt.Horizontal) is None:
                model.setHeaderData(column, Qt.Horizontal, "[No header]",
                        Qt.EditRole)
        self.tree.selectionModel().setCurrentIndex(model.index(0, 0, index),
                QItemSelectionModel.ClearAndSelect)
    def insertTreeRow(self):
        index = self.tree.selectionModel().currentIndex()
        model = self.tree.model()
        if not model.insertRow(index.row()+1, index.parent()):
            return
        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row()+1, column, index.parent())
            model.setData(child, "[No data]", Qt.EditRole)
    def removeTreeRow(self):
        index = self.tree.selectionModel().currentIndex()
        model = self.tree.model()
        model.removeRow(index.row(), index.parent())

    def saveTree(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Input you name:",
                "User name:", QtWidgets.QLineEdit.Normal, "hello")
        if ok and text != '':
            print("input---", text)
        model = self.tree.model()
        def ii(it, indent, fo):
            print("%s%s\t%s" % (indent, it.data(0), it.data(1)), file=fo)
            if it.childCount() > 0:
                for ic in it:
                    ii(ic, indent+"  ", fo)
        root = model.rootItem
        fo = open("default.txt", "w", encoding="UTF-8")
        for it in root: ii(it, "", fo)
        fo.close()


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
