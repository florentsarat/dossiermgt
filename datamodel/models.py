from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship


from init import Base

#############################
# Models
#############################


class Dossier(Base):
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
    partNotaire = Column(Float)

    statusSRU = Column(String)

    statusDia = Column(String)
    DiaSendDate = Column(Date)
    DiaAnsDate = Column(Date)

    statusPC = Column(String)
    deadlineDepotPC = Column(Date)
    deadlinePC = Column(Date)

    pret = Column(String)

    deadlinePretRdy = Column(Boolean)
    deadlinePret = Column(Date)

    ODPReceived = Column(String)

    deadlineVenteRdy = Column(Boolean)
    deadlineVente = Column(Date)

    RDVFixe = Column(Boolean)
    datesignature = Column(DateTime)

    agencePriceDossier = Column(Integer)
    dateDossier = Column(Date)
    statusDossier = Column(String)
    todoactions = relationship("Todoelement", backref='Dossier')

    dossierReady = Column(Boolean)

    def __init__(self, name, typed, provenance, notairev ,
                 notaireac, statusavantcontrat, comment,
                 datedossier, status):
        self.nameDossier = name
        self.typeDossier = typed

        self.dossierprovenance = provenance

        self.notairevendeurDossier = notairev
        self.notaireacquereurDossier = notaireac

        self.statusavantContrat = statusavantcontrat

        self.ODPReceived = "Pas reçu"
        self.statusSRU = "A vérifier"
        self.pret = "Je ne sais pas"
        self.statusDia = "Non"

        self.statusPC = "A Faire"

        self.commentsDossier = comment
        self.dateDossier = datedossier
        self.statusDossier = status

        self.dossierReady = False
        self.RDVFixe = False

        self.deadlinePretRdy = False
        self.deadlineVenteRdy = False

class Todoelement(Base):
    __tablename__ = 'todoelement'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    dossier_id = Column(Integer, ForeignKey('dossier.id'))
    status = Column(String(100))
    datelimit = Column(Date)
    # dossier = relationship("dossier")
    __mapper_args__ = {
        'polymorphic_identity': 'Todoelement'
    }

    def __init__(self, name, datelimit):
        self.name = name
        self.status = 'A Faire'
        self.datelimit = datelimit


# class TodoRDV(Todoelement):
#
#     avec = Column(String(100))
#     typedeRDV =Column(String(100))
#     __mapper_args__ = {
#         'polymorphic_identity': 'TodoRDV',
#     }
#
#     def __init__(self, name, avec, typederdv, datelimit):
#         # super().__init__(name)
#         self.name = name
#         self.status = 'A réaliser'
#         self.avec = avec
#         self.typedeRDV = typederdv
#         self.datelimit= datelimit