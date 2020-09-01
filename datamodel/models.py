
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
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

    dossierprovenance = Column(String)
    agenceAvantContrat = Column(Boolean)

    statusavantContrat = Column(String)

    notairevendeurDossier = Column(String)
    notaireacquereurDossier = Column(String)

    priceSalesDossier = Column(Integer)
    mobiliersDossier = Column(Integer)

    statusSRU = Column(String)

    statusDia = Column(String)
    DiaSendDate = Column(Date)
    DiaAnsDate = Column(Date)

    deadlineDepotPC = Column(Date)

    deadlinePC = Column(Date)

    pret = Column(String)
    deadlinePret = Column(Date)

    ODPReceived = Column(Boolean)

    deadlineVente = Column(Date)

    datesignature = Column(Date)

    agencePriceDossier = Column(Integer)
    dateDossier = Column(Date)
    statusDossier = Column(String)
    todoactions = relationship("todoelement", backref='dossier')


    def __init__(self, name, type, provenance, notaireV , notaireAc, comment, dateDossier, status):
        self.nameDossier = name
        self.typeDossier = type

        self.dossierprovenance = provenance

        self.notairevendeurDossier = notaireV
        self.notaireacquereurDossier = notaireAc

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
    dossier = relationship("dossier")
    __mapper_args__ = {
        'polymorphic_identity': 'todoRDV',
        'concrete': True
    }

    def __init__(self, name, avec, typedeRDV, datelimit):
        self.name = name
        self.status = 'A réaliser'
        self.avec = avec
        self.typedeRDV = typedeRDV
        self.datelimit= datelimit
