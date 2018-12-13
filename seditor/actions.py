# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtPrintSupport
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
import os, time, shutil

from ext import *
import fs

import traceback
import types
from functools import wraps

def MyPyQtSlot(*args):
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @QtCore.pyqtSlot(*args)
    def slotdecorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args)
            except:
                print("Uncaught Exception in slot")
                traceback.print_exc()
        return wrapper
    return slotdecorator

class TreeActions(object):
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
                QtCore.QItemSelectionModel.ClearAndSelect)

    def insertTreeRow(self):
        print("----insertTreeRow")
        try:
            index = self.tree.selectionModel().currentIndex()
            model = self.tree.model()
            if not model.insertRow(index.row()+1, index.parent()):
                return
            for column in range(model.columnCount(index.parent())):
                child = model.index(index.row()+1, column, index.parent())
                model.setData(child, "[No data]", Qt.EditRole)
        except Exception as e:
            print("error", e)
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

    def addNote(self, model, index, data):
        text, ok = QtWidgets.QInputDialog.getText(self, "Input note name:",
                 "Note name:", QtWidgets.QLineEdit.Normal, "[new note]")
        if not ok:
            return
        fpath = data.fpath + os.path.sep + text + ".writer"
        if os.path.exists(fpath):
            QMessageBox.information(self, "Warning", "Note exists")
            return
        fo = open(fpath, "w", encoding="UTF-8")
        fo.write("<html><body></body></html>")
        fo.close()
        # print("--addNote", text, data, fpath)
        position = model.appendRow(fs.FSItem(text, time.strftime("%Y%m%d %H:%M"), fpath, fs.ItemType.FILE), index)
        self.tree.selectionModel().setCurrentIndex(model.index(position, 0, index),
                QtCore.QItemSelectionModel.ClearAndSelect)
    def delNote(self, model, index, data):
        reply = QMessageBox.question(self, "Warning",
                                     "Do you really want to Delete the note?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply != QMessageBox.Yes:
            return
        os.remove(data.fpath)
        model.removeRow(index.row(), index.parent())
    def addFolder(self, model, index, data):
        text, ok = QtWidgets.QInputDialog.getText(self, "Input folder name:",
                 "Folder name:", QtWidgets.QLineEdit.Normal, "[new folder]")
        if not ok:
            return
        fpath = data.fpath + os.path.sep + text
        try:
            os.mkdir(fpath)
        except Exception as e:
            QMessageBox.information(self, "Warning", "Folder exists")
            return
        position = model.appendRow(fs.FSItem("[D]"+text, '', fpath, fs.ItemType.DIR), index)
        self.tree.selectionModel().setCurrentIndex(model.index(position, 0, index),
                                                   QtCore.QItemSelectionModel.ClearAndSelect)
    def delFolder(self, model, index, data):
        item = model.getItem(index)
        if item.childCount() > 0:
            QMessageBox.information(self, "Warning", "Folder not empty!")
            return
        reply = QMessageBox.question(self, "Warning",
                                     "Do you really want to Delete this folder?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply != QMessageBox.Yes:
            return
        os.rmdir(data.fpath)
        model.removeRow(index.row(), index.parent())

class TableActions:
    '''表格变更的操作方法'''
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

class FormatActions:
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

class ToolActions:
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
        '''new window'''
        # spawn = Main()
        # spawn.show()
        index = self.tree.selectionModel().currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Warning", "Select a folder first!")
            return
        model = self.tree.model()
        data = model.getItem(index).itemData
        if data.type != fs.ItemType.DIR:
            QMessageBox.information(self, "Warning", "Select a folder first!")
            return
        self.addNote(model, index, data)

    def open(self):
        '''open a new workdir'''
        # Get filename and show only .writer files
        #PYQT5 Returns a tuple in PyQt5, we only need the filename
        #self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")[0]
        # if self.filename:
        #     with open(self.filename,"rt") as file:
        #         self.text.setText(file.read())
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                     "Open work directory",
                     "Open work directory", options=options)
        if not directory:
            return
        #self.basedir = directory
        self._openWorkDir(directory)

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
            self._title()

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

    @MyPyQtSlot()
    def insertImage(self, item):
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
                fpath, cpath = self.fs.imagePath(filename, self.filename)
                if fpath is None:
                    return
                image = QtGui.QImage(fpath)
                cursor = self.text.textCursor()
                cursor.insertImage(image, cpath)

    @MyPyQtSlot()
    def pasteImage(self, item):
        if self.filename == '':
            return
        clipboard = QApplication.clipboard()
        # print(type(clipboard), dir(clipboard) )
        mimeData = clipboard.mimeData()
        if not mimeData.hasImage():
            print("There hasn't a image in clipboard!")
            return
        # print(type(mimeData), dir(mimeData))
        image = clipboard.image()
        fpath, cpath = self.fs.tempImagePath(self.filename, imageType="jpg")
        image.save(fpath, "jpeg")
        cursor = self.text.textCursor()
        cursor.insertImage(image, cpath)