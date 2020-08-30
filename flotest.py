import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QDialog, QDialogButtonBox, QTableWidget,QTableWidgetItem, QTableView, QAbstractItemView
from PyQt5.QtCore import Qt

from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime

from init import Base
from models import dossier, todoelement, todoRDV

#############################
# DB setup and initialization
#############################
engine = create_engine('sqlite:///sales.db', echo = False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



#############################
# UI
#############################

class dossiersTableView(QAbstractTableModel):
    def __init__(self, datain, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = []
        self.getData()


    def getData(self):
        query = "select id, nameDossier, typeDossier, dateDossier, statusDossier, '' from dossier"
        self.mydata = session.execute(query).fetchall()

    def rowCount(self, index):
        return len(self.mydata)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.mydata[index.row()][index.column()]

    def columnCount(self, index):
        if self.mydata is None:
            return len(self.mydata[0])
        else:
            return 5

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        header = ['ID','Dossier', 'Type', 'Date', 'Statut', 'Actions']
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return header[section]


class rdvTableView(QAbstractTableModel):
    def __init__(self, rdvData, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = QtGui.QStandardItemModel(0, 3)
        # self.mydata =[]
        self.rdvData = rdvData
        self.getData()
        print(self.mydata)


    def getData(self):
        for rdv in self.rdvData:
            # modelRDV = QtGui.QStandardItemModel(0, 3) QStandardItem
            print(rdv)
            it1 = QtGui.QStandardItem()
            it1.setData(rdv.id, QtCore.Qt.DisplayRole)
            it2 = QtGui.QStandardItem()
            it2.setData(rdv.name, QtCore.Qt.DisplayRole)
            it3 = QtGui.QStandardItem()
            it3.setData(rdv.datelimit, QtCore.Qt.DisplayRole)
            it4 = QtGui.QStandardItem()
            it4.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
            # modelRDV.appendRow([it1, it2, it3])
            # self.mydata.append(modelRDV)
            self.mydata.appendRow([it1, it2, it3,it4])


    def rowCount(self, index):
        return self.mydata.rowCount()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 3:
                # print (self.mydata.item(index.row(),index.column()).data(QtCore.Qt.DisplayRole))
                # return QtCore.QVariant(QtCore.Qt.Checked)
                pass
            else :
                return QtCore.QVariant(self.mydata.item(index.row(),index.column()).data(QtCore.Qt.DisplayRole))
        if role == Qt.CheckStateRole:
            if index.column() == 3:
                print (self.mydata.item(index.row(),index.column()).data(QtCore.Qt.DisplayRole))
                return QtCore.QVariant(QtCore.Qt.Checked)

    def columnCount(self, index):
        if self.mydata is  None:
            return len(self.mydata.item(0))
        else:
            return 4

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        header = ['ID','RDV Name', 'Date limite', 'Status']
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return header[section]


class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        uic.loadUi("UI/TestFlo.ui", self)
        self.dossiers = []
        self.myRDVTodos =[]

        self.button = self.findChild(QPushButton, "addNewCase")
        self.button.clicked.connect(self.clickedNewDossierBtn)

        self.mydossiersTable = self.findChild(QTableView,"tabledesdossiers")
        self.myrdvtable = self.findChild(QTableView, 'listedeRDV')
        self.loadRDV()
        self.prepareRDVTable()
        self.loadDossier()

        self.model = dossiersTableView(self.dossiers)
        self.mydossiersTable.setModel(self.model)
        self.mydossiersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.addRDVButton()
        self.show()

    def prepareRDVTable(self):
        # modelRDV = QtGui.QStandardItemModel(0, 3)
        # for rdv in self.myRDVTodos:
        #     print(rdv)
        #     it1 = QtGui.QStandardItem()
        #     it1.setData(rdv.id, QtCore.Qt.DisplayRole)
        #     it2 = QtGui.QStandardItem()
        #     it2.setData(rdv.name, QtCore.Qt.DisplayRole)
        #     it3 = QtGui.QStandardItem()
        #     it3.setData(rdv.datelimit, QtCore.Qt.DisplayRole)
        #     modelRDV.appendRow([it1, it2, it3])
        modelRDV = rdvTableView(self.myRDVTodos)
        # modelRDV.setHorizontalHeaderLabels(['Column1', 'Column2', 'Column3'])
        self.myrdvtable.setModel(modelRDV)


    def addRDVButton(self):
        for index in range(len(self.model.mydata)):
            self.btn_sell = QPushButton('RDV à planifier')
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.mydossiersTable.setIndexWidget(self.model.index(index, 4), self.btn_sell)

    def handleButtonClicked(self):
        # mondos = session.query(dossier).get(1)
        # print (mondos.todoactions)
        button = QApplication.focusWidget()
        index = self.mydossiersTable.indexAt(button.pos())
        if index.isValid():
            self.CreateRDVTodo = CreateRDVTodo(self, self.model.mydata[index.row()])
            self.CreateRDVTodo.show()

    def clickedNewDossierBtn(self):
        self.NewForm = CreateForm(self)
        self.NewForm.mySignal.connect(self.updatelist)
        self.NewForm.show()

    def updatelist(self):
        self.model.getData()
        self.model.layoutChanged.emit()
        self.addRDVButton()

    def loadDossier(self):
        dossiers = session.query(dossier).all()
        for mydossier in dossiers:
            self.dossiers.append([mydossier.nameDossier, mydossier.typeDossier])

    def loadRDV(self):
        self.myRDVTodos = session.query(todoRDV).all()

class CreateForm(QDialog):
    mySignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(CreateForm, self).__init__(parent)
        uic.loadUi("UI/FormCreate.ui", self)
        self.validatedossierNewButton = self.findChild(QDialogButtonBox, "validatenewdossier")
        self.validatedossierNewButton.accepted.connect(self.clickedBtnCreateDossier)

    def clickedBtnCreateDossier(self):
        anewdossier = dossier(self.namedossier.text(), "Appartement", "comment", datetime.today(), 'En cours')
        session.add(anewdossier)
        session.commit()
        self.mySignal.emit()


class CreateRDVTodo(QDialog):
    def __init__(self, parent, dossier):
        super(CreateRDVTodo, self).__init__(parent)
        uic.loadUi("UI/RDVTodo.ui", self)
        self.validateRDVtodo = self.findChild(QDialogButtonBox, "validateRDVtodo")
        self.validateRDVtodo.accepted.connect(self.addRDV2todo)
        self.dossier =dossier

    def addRDV2todo(self):
        newtodoRDV = todoRDV("toto")
        newtodoRDV.dossier_id= self.dossier[0]
        session.add(newtodoRDV)
        session.commit()


#############################
# Main Program
#############################


app = QApplication(sys.argv)
window = Home()
app.exec_()
session.close()
