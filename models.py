
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import ConcreteBase

from init import Base

#############################
# Models
#############################


class dossier(Base):
    __tablename__ = 'dossier'
    id = Column(Integer, primary_key=True)
    nameDossier = Column(String)
    typeDossier = Column(String)
    particulaDossier = Column(String)
    commentsDossier = Column(String)
    nvDossier = Column(String)
    naDossier = Column(String)
    priceSalesDossier = Column(Integer)
    mobiliersDossier = Column(Integer)
    agenceDossier = Column(Boolean)
    agencePriceDossier = Column(Integer)
    dateDossier = Column(Date)
    statusDossier = Column(String)
    todoactions = relationship("todoelement", backref='dossier')


    def __init__(self, name, type, comment, dateDossier, status):
        self.nameDossier = name
        self.typeDossier = type
        self.commentsDossier = comment
        self.dateDossier = dateDossier
        self.statusDossier = status


class todoelement(ConcreteBase, Base):
    __tablename__ = 'todoelement'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dossier_id = Column(Integer, ForeignKey('dossier.id'))
    status = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'todoelement',
        'concrete': True
    }

class todoRDV(todoelement):
    __tablename__ = 'todoRDV'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    avec = Column(String(100))
    status = Column(String(100))
    typedeRDV =Column(String(100))
    datelimit = Column(Date)
    dossier_id = Column(Integer, ForeignKey('dossier.id'))
    __mapper_args__ = {
        'polymorphic_identity': 'todoRDV',
        'concrete': True
    }

    def __init__(self, name):
        self.name = name
