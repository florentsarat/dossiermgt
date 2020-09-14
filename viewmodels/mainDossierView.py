from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt,QAbstractTableModel, QDate
from PySide2.QtGui import QBrush


def definedossiertableboject(dossiertoupdate):
    if dossiertoupdate is not None:
        dossierID = QtGui.QStandardItem()
        dossierID.setData(dossiertoupdate.id, QtCore.Qt.DisplayRole)

        dossiername = QtGui.QStandardItem()
        dossiername.setData(dossiertoupdate.nameDossier, QtCore.Qt.DisplayRole)

        dossiertype = QtGui.QStandardItem()
        dossiertype.setData(dossiertoupdate.typeDossier, QtCore.Qt.DisplayRole)

        dossierprovenance = QtGui.QStandardItem()
        dossierprovenance.setData(dossiertoupdate.dossierprovenance, QtCore.Qt.DisplayRole)

        statusavantContrat = QtGui.QStandardItem()
        statusavantContrat.setData(dossiertoupdate.statusavantContrat, QtCore.Qt.DisplayRole)

        notairevendeurDossier = QtGui.QStandardItem()
        notairevendeurDossier.setData(dossiertoupdate.notairevendeurDossier, QtCore.Qt.DisplayRole)

        notaireacquereurDossier = QtGui.QStandardItem()
        notaireacquereurDossier.setData(dossiertoupdate.notaireacquereurDossier, QtCore.Qt.DisplayRole)

        prixdeVente = QtGui.QStandardItem()
        prixdeVente.setData(dossiertoupdate.priceSalesDossier, QtCore.Qt.DisplayRole)

        parNotaire = QtGui.QStandardItem()
        parNotaire.setData(dossiertoupdate.partNotaire, QtCore.Qt.DisplayRole)

        dossierstatus = QtGui.QStandardItem()
        dossierstatus.setData(dossiertoupdate.statusDossier, QtCore.Qt.DisplayRole)

        dossierdate = QtGui.QStandardItem()
        dossierdate.setData(dossiertoupdate.dateDossier, QtCore.Qt.DisplayRole)

        dateDBPC = QtGui.QStandardItem()
        dateDBPC.setData(dossiertoupdate.deadlinePC, QtCore.Qt.DisplayRole)

        dateDBPret = QtGui.QStandardItem()
        dateDBPret.setData(dossiertoupdate.deadlinePret, QtCore.Qt.DisplayRole)

        dateDBVente = QtGui.QStandardItem()
        dateDBVente.setData(dossiertoupdate.deadlineVente, QtCore.Qt.DisplayRole)

        datebrdv = QtGui.QStandardItem()
        datebrdv.setData(dossiertoupdate.datesignature, QtCore.Qt.DisplayRole)

        editAction = QtGui.QStandardItem()
        editAction.setData('Editer', QtCore.Qt.DisplayRole)

        # afaire = QtGui.QStandardItem()
        # afaire.setData('+Tâche', QtCore.Qt.DisplayRole)

        actionbutton = QtGui.QStandardItem()
        actionbutton.setData('+Ajouter une tâche', QtCore.Qt.DisplayRole)

        return [dossierID, dossiername, dossiertype, dossierprovenance,
                statusavantContrat, notairevendeurDossier, notaireacquereurDossier, prixdeVente,
                parNotaire,dossierstatus, dossierdate,dateDBPC,
                dateDBPret, dateDBVente, datebrdv, editAction,
                actionbutton]
    else:
        return None


class DossiersTableView(QAbstractTableModel):
    def __init__(self, datain, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = QtGui.QStandardItemModel(0, 3)
        self.getdata(datain)
        self.header = ['ID','Dossier', 'Type','Provenance',
                       'Statut Avant Contrat', 'Notaire Revendeur', 'Notaire Acquéreur',
                       'Prix de Vente', 'Part Notaire', 'Statut', 'Date','DB PC', 'DB Prêt', 'DB Vente','Date RDV signature', '', '']

    def updateadossier(self, index, dossiertoupdate):
        mynewline=definedossiertableboject(dossiertoupdate)

        self.mydata.setItem(index.row(),1,mynewline[1])
        self.mydata.setItem(index.row(), 2, mynewline[2])
        self.mydata.setItem(index.row(), 3, mynewline[3])
        self.mydata.setItem(index.row(), 4, mynewline[4])
        self.mydata.setItem(index.row(), 5, mynewline[5])
        self.mydata.setItem(index.row(), 6, mynewline[6])
        self.mydata.setItem(index.row(), 7, mynewline[7])
        self.mydata.setItem(index.row(), 8, mynewline[8])
        self.mydata.setItem(index.row(), 9, mynewline[9])

    def appenddossier(self, newdossiertoappend):
        if newdossiertoappend is not None:
            rc = self.mydata.rowCount()
            self.beginInsertRows(QtCore.QModelIndex(), rc, rc)
            lineForDossier = definedossiertableboject(newdossiertoappend)
            self.mydata.appendRow(lineForDossier)
            self.endInsertRows()

    def getdata(self, datain):
        if datain is not None:
            for dossier in datain:
                lineForDossier= definedossiertableboject(dossier)
                self.mydata.appendRow(lineForDossier)

    # def triggerupdate(self):
    #     self.layoutChanged.emit()

    def rowCount(self, index):
        return self.mydata.rowCount()

    def data(self, index, role):

        # pass
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 10:
                    return QDate(self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole))
                else:
                    return self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole)
        else:
            print('invalid')

    def columnCount(self, index):
        return len(self.header)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[section]
