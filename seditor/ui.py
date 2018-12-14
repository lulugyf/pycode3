# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


from PyQt5 import QtPrintSupport


from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from ext import *

class UISetup:
    def initToolbar(self):
        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.png"), "New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("icons/open.png"), "Open file", self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.png"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.printAction = QtWidgets.QAction(QtGui.QIcon("icons/print.png"), "Print document", self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtWidgets.QAction(QtGui.QIcon("icons/preview.png"), "Page view", self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.findAction = QtWidgets.QAction(QtGui.QIcon("icons/find.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.png"), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.png"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)

        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("icons/calender.png"), "Insert current date/time", self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        wordCountAction = QtWidgets.QAction(QtGui.QIcon("icons/count.png"), "See word/symbol count", self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        tableAction = QtWidgets.QAction(QtGui.QIcon("icons/table.png"), "Insert table", self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(table.Table(self).show)

        imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.png"), "Insert image", self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        pasteimgAction = QtWidgets.QAction(QtGui.QIcon("icons/pasteimg.jpg"), "Insert Clipboard", self)
        pasteimgAction.setStatusTip("Insert image from Clipboard")
        pasteimgAction.setShortcut("Ctrl+Shift+I")
        pasteimgAction.triggered.connect(self.pasteImage)

        bulletAction = QtWidgets.QAction(QtGui.QIcon("icons/bullet.png"), "Insert bullet List", self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtWidgets.QAction(QtGui.QIcon("icons/number.png"), "Insert numbered List", self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(dateTimeAction)
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(tableAction)
        self.toolbar.addAction(imageAction)
        self.toolbar.addAction(pasteimgAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)

        self.addToolBarBreak()

    def initFormatbar(self):

        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))

        fontSize = QtWidgets.QSpinBox(self)

        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))

        fontSize.setValue(14)

        fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"),"Change font color",self)
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.italic)

        underlAction = QtWidgets.QAction(QtGui.QIcon("icons/underline.png"),"Underline",self)
        underlAction.triggered.connect(self.underline)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("icons/superscript.png"),"Superscript",self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("icons/subscript.png"),"Subscript",self)
        subAction.triggered.connect(self.subScript)

        alignLeft = QtWidgets.QAction(QtGui.QIcon("icons/align-left.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("icons/align-center.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("icons/align-right.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("icons/align-justify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QtWidgets.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtWidgets.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QtWidgets.QAction(QtGui.QIcon("icons/highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

    def initMenubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        tred = menubar.addMenu("Tree")
        view = menubar.addMenu("View")

        # Add the most important actions to the menubar

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        # Toggling actions for the various bars
        toolbarAction = QtWidgets.QAction("Toggle Toolbar",self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Toggle Formatbar",self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Toggle Statusbar",self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)

        insertRowAction = QtWidgets.QAction("Add Document", self)
        insertRowAction.setShortcut("Ctrl+I, R")
        insertRowAction.triggered.connect(self.insertTreeRow)
        #print("----", type(self.insertTreeRow))
        removeRowAction = QtWidgets.QAction("Remove Row", self)
        removeRowAction.setShortcut("Ctrl+R, R")
        removeRowAction.triggered.connect(self.removeTreeRow)
        insertChildAction = QtWidgets.QAction("Insert Child", self)
        insertChildAction.setShortcut( "Ctrl+N" )
        insertChildAction.triggered.connect(self.insertTreeChild)

        saveTreeAction = QtWidgets.QAction("Save Tree", self)
        saveTreeAction.triggered.connect(self.saveTree)

        tred.addAction(insertRowAction)
        tred.addAction(removeRowAction)
        tred.addAction(insertChildAction)
        tred.addAction(saveTreeAction)

        self.filemenu = file

    def addRecentToFileMenu(self, recent):
        ''' 添加最近打开过的workdir 到 file菜单上'''
        file = self.filemenu
        file.addSeparator()
        recent.reverse()
        for r in recent:
            rAction = QtWidgets.QAction(r, self)
            rAction.setData(r)
            rAction.triggered.connect(lambda _,path=r: self._openWorkDir( path ) ) # thrick is here
            file.addAction(rAction)

    def closeEvent(self, event):
        if self.changesSaved:
            self._beforeClose()
            event.accept()
        else:
            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setText("The document has been modified")
            popup.setInformativeText("Do you want to save your changes?")
            popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                     QtWidgets.QMessageBox.Cancel |
                                     QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)
            answer = popup.exec_()
            if answer == QtWidgets.QMessageBox.Save:
                self.save()
                self._beforeClose()
            elif answer == QtWidgets.QMessageBox.Discard:
                self._beforeClose()
                event.accept()
            else:
                event.ignore()

def showTableContextMenu(table, pos, cursor, self):
    menu = QtWidgets.QMenu(self)

    appendRowAction = QtWidgets.QAction("Append row", self)
    appendRowAction.triggered.connect(lambda: table.appendRows(1))

    appendColAction = QtWidgets.QAction("Append column", self)
    appendColAction.triggered.connect(lambda: table.appendColumns(1))

    removeRowAction = QtWidgets.QAction("Remove row", self)
    removeRowAction.triggered.connect(lambda: table.removeRows(table.cellAt(cursor).row(), 1) )

    removeColAction = QtWidgets.QAction("Remove column", self)
    removeColAction.triggered.connect( lambda: table.removeColumns(table.cellAt(cursor).column(),1)  ) # self.removeCol)

    insertRowAction = QtWidgets.QAction("Insert row", self)
    insertRowAction.triggered.connect(lambda: table.insertRows(table.cellAt(cursor).row(),1) ) # self.insertRow)

    insertColAction = QtWidgets.QAction("Insert column", self)
    insertColAction.triggered.connect(lambda: table.insertColumns(table.cellAt(cursor).column(),1) )  #self.insertCol)

    mergeAction = QtWidgets.QAction("Merge cells", self)
    mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

    # Only allow merging if there is a selection
    if not cursor.hasSelection():
        mergeAction.setEnabled(False)

    splitAction = QtWidgets.QAction("Split cells", self)

    cell = table.cellAt(cursor)

    # Only allow splitting if the current cell is larger
    # than a normal cell
    if cell.rowSpan() > 1 or cell.columnSpan() > 1:
        splitAction.triggered.connect(lambda: table.splitCell(cell.row(), cell.column(), 1, 1))
    else:
        splitAction.setEnabled(False)

    menu.addAction(appendRowAction)
    menu.addAction(appendColAction)

    menu.addSeparator()

    menu.addAction(removeRowAction)
    menu.addAction(removeColAction)

    menu.addSeparator()

    menu.addAction(insertRowAction)
    menu.addAction(insertColAction)

    menu.addSeparator()

    menu.addAction(mergeAction)
    menu.addAction(splitAction)

    # Convert the widget coordinates into global coordinates
    pos = self.text.mapToGlobal(pos)

    # Move the menu to the new position
    menu.move(pos)
    menu.show()

def initTreeView(self):
    tree = QtWidgets.QTreeView()
    FROM, SUBJECT, DATE = range(3)

    def createMailModel(parent):
        model = QtGui.QStandardItemModel(0, 2, parent)
        model.setHeaderData(FROM, Qt.Horizontal, "From")
        model.setHeaderData(SUBJECT, Qt.Horizontal, "Subject")
        # model.setHeaderData(DATE, Qt.Horizontal, "Date")
        return model

    def addMail(model, mailFrom, subject, date, parent=None):
        if parent is not None:
            model.insertRow(1, parent=parent)
        else:
            model.insertRow(0)
        model.setData(model.index(0, FROM), mailFrom)
        model.setData(model.index(0, SUBJECT), subject)
        # model.setData(model.index(0, DATE), date)
        return model.indexFromItem(model.item(0))

    model = createMailModel(self)
    tree.setModel(model)
    i1 = addMail(model, 'service@github.com', 'Your Github Donation', '03/25/2017 02:05 PM')
    addMail(model, 'support@github.com', 'Github Projects', '02/02/2017 03:05 PM')
    addMail(model, 'service@phone.com', 'Your Phone Bill', '01/01/2017 04:05 PM')

    tree.setAnimated(False)
    # tree.setIndentation(20)
    # tree.setSortingEnabled(True)

    # tree.setWindowTitle("Dir View")
    tree.expandAll()

    return tree, model

