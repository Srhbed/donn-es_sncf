from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, CheckConstraint, ForeignKey, REAL,PrimaryKeyConstraint


engine1 = create_engine('sqlite:///db.sqlite')
Base = declarative_base()

Session1 = sessionmaker(bind=engine1) # On créer une session qui écoute "Engine"
session1 = Session1()


class Gare(Base):
    __tablename__ = "Gare"
    code_uic = Column(String,primary_key= True)
    region = Column(String)
    departement = Column(Integer)

class PerteObjet(Base):
    __tablename__ = "PerteObjet"
    id = Column(Integer,primary_key = True)
    code_uic = Column(String)
    lieu = Column(String)
    date = Column(String)
    objet = Column(String)

class Frequentation(Base):
    __tablename__ = "Frequentation"
    id = Column(Integer,primary_key = True)
    code_uic = Column(String)
    code_postal = Column(Integer)
    nbVoyageur2016 = Column(Integer)
    nbVoyageur2017 = Column(Integer)
    nbVoyageur2018 = Column(Integer)
    nbVoyageur2019 = Column(Integer)
    nbVoyageur2020 = Column(Integer)
    nbVoyageur2021 = Column(Integer)

Base.metadata.create_all(engine1)



