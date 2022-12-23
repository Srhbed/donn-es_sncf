from conf import *
import csv


def generateGare():
    with open('gare.csv', 'r') as csvfile:
        gares_csv = csv.reader(csvfile, delimiter=',')
        for row in gares_csv:
            gare = Gare(code_uic=row[0], region=row[1],departement = row[2])
            try:
                session1.add(gare)
                session1.commit()
            except:
                session1.rollback()


generateGare()

def generatePerteObjet():
    with open('test.csv', 'r') as csvfile:
        perteObjet_csv = csv.reader(csvfile, delimiter=',')
        for row in perteObjet_csv:
           
            perteObjet = PerteObjet(lieu=row[0],objet = row[1],date = row[2],code_uic=row[3])
            session1.add(perteObjet)
    session1.commit()
          
generatePerteObjet()

def generateFrequentation():
    with open('freq.csv', 'r') as csvfile:
        frequentation_csv = csv.reader(csvfile, delimiter=',')
        for row in frequentation_csv:
           
            frequentation = Frequentation(code_uic=row[0],
            code_postal = row[1],
            nbVoyageur2016 = row[2],
            nbVoyageur2017=row[3],
            nbVoyageur2018=row[4],
            nbVoyageur2019=row[5],
            nbVoyageur2020=row[6],
            nbVoyageur2021=row[7])
            session1.add(frequentation)
    session1.commit()

generateFrequentation()

session1.close()