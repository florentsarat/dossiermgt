import sys

from PySide2.QtWidgets import QApplication

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from init import Base

from mainwindows import home

import resources

#############################
# DB setup and initializationip
#############################
engine = create_engine('sqlite:///dossiers.db', echo = False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


#############################
# Main Program
#############################
app = QApplication(sys.argv)
window = home.Home(session)
app.exec_()
session.close()
