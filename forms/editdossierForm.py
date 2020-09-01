
from PySide2.QtWidgets import QDialog


from PySide2.QtUiTools import loadUiType


class EditForm(QDialog, loadUiType('UI/ViewDossier.ui')[0]):

    def __init__(self, parent, session):
        super(EditForm, self).__init__(parent)
        self.setupUi(self)
        self.session = session