from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt,QAbstractTableModel, QDate
from PySide2.QtGui import QBrush


def definetasktableobject(tasktoupdate):
    if tasktoupdate is not None:
        taskID = QtGui.QStandardItem()
        taskID.setData(tasktoupdate.id, QtCore.Qt.DisplayRole)

        taskname = QtGui.QStandardItem()
        taskname.setData(tasktoupdate.name, QtCore.Qt.DisplayRole)

        taskdossier = QtGui.QStandardItem()
        taskdossier.setData(tasktoupdate.Dossier.nameDossier, QtCore.Qt.DisplayRole)

        taskdatelim = QtGui.QStandardItem()
        taskdatelim.setData(tasktoupdate.datelimit, QtCore.Qt.DisplayRole)

        taskstatus = QtGui.QStandardItem()
        taskstatus.setData(tasktoupdate.status, QtCore.Qt.DisplayRole)

        taskIsdone = QtGui.QStandardItem()
        taskIsdone.setData('Tâche réalisée', QtCore.Qt.DisplayRole)

        return [taskID, taskname, taskdossier, taskdatelim,  taskstatus, taskIsdone]
    else:
        return None


class TaskTableView(QAbstractTableModel):
    def __init__(self, tasksin, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = QtGui.QStandardItemModel(0, 3)
        self.getData(tasksin)
        self.header = ['ID', 'Nom', 'Dossier', 'Date limite', 'Status', '']

    def updateatask(self, index, tasktoupdate):
        mynewline=definetasktableobject(tasktoupdate)
        self.mydata.setItem(index.row(),1,mynewline[1])
        self.mydata.setItem(index.row(), 2, mynewline[2])
        self.mydata.setItem(index.row(), 3, mynewline[3])
        self.mydata.setItem(index.row(), 4, mynewline[4])
        self.mydata.setItem(index.row(), 5, mynewline[5])

    def refresh(self):
        self.layoutChanged.emit()

    def appendtask(self, newtasktoappend):
        if newtasktoappend is not None:
            rc = self.mydata.rowCount()
            self.beginInsertRows(QtCore.QModelIndex(), rc, rc)
            lineForDossier = definetasktableobject(newtasktoappend)
            self.mydata.appendRow(lineForDossier)
            self.endInsertRows()

    def resetdata(self,tasksin):
        self.mydata.clear()
        self.getData(tasksin)
        self.refresh()

    def getData(self, tasksin):
        if tasksin is not None:
            for task in tasksin:
                linefortask = definetasktableobject(task)
                self.mydata.appendRow(linefortask)

    def rowCount(self, index):
        return self.mydata.rowCount()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 3:
                return QDate(self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole))
            else :
                return self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole)
        if role == Qt.BackgroundRole:
            if self.mydata.item(index.row(), 4).data(QtCore.Qt.DisplayRole)== "Réalisée":
                return QBrush(Qt.darkGreen)
            else:
                return QBrush(Qt.white)

    def columnCount(self, index):
        return len(self.header)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[section]