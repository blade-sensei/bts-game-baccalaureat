# -*- coding: utf-8 -*-

from sqlite3 import *
import csv

global cursor,ma_bdd

ma_bdd = connect(':memory:')

#________TABLES_BDD_______________#

cursor = ma_bdd.cursor()
cursor.execute('''
    CREATE TABLE animal(id INTEGER PRIMARY KEY, nom TEXT)
    ''')
cursor.execute('''
    CREATE TABLE noms(id INTEGER PRIMARY KEY, nom TEXT)
    ''')
cursor.execute('''
    CREATE TABLE fruit(id INTEGER PRIMARY KEY, nom TEXT)
    ''')
cursor.execute('''
    CREATE TABLE pays(id INTEGER PRIMARY KEY, nom TEXT)
    ''')
cursor.execute('''
    CREATE TABLE metier(id INTEGER PRIMARY KEY, nom TEXT)
    ''')
cursor.execute('''
    CREATE TABLE couleur(id INTEGER PRIMARY KEY, nom TEXT)
    ''')






#________FIN_TABLES_BDD___________#



#________INSERT_DONNEES________________#

csvfile = open('animaux.txt', 'r',encoding='utf-8')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')
for t in creader:
    cursor.execute('INSERT INTO animal (nom) VALUES (?)', t )
csvfile.close()

csvfile_1 = open('fruit.txt', 'r',encoding='utf-8')
creader = csv.reader(csvfile_1, delimiter=',', quotechar='"')
for l in creader:
    cursor.execute('INSERT INTO fruit (nom) VALUES (?)', l )
csvfile_1.close()

csvfile_2 = open('pays.txt', 'r',encoding='utf-8',errors='ignore')
creader = csv.reader(csvfile_2, delimiter=',', quotechar='"')
for a in creader:
    cursor.execute('INSERT INTO pays (nom) VALUES (?)', a )
csvfile_2.close()

csvfile_3 = open('metier.txt', 'r',encoding='utf-8',errors='ignore')
creader = csv.reader(csvfile_3, delimiter=',', quotechar='"')
for a in creader:
    cursor.execute('INSERT INTO metier (nom) VALUES (?)', a )
csvfile_3.close()

csvfile_4 = open('prenom.txt', 'r',encoding='utf-16',errors='ignore')
creader = csv.reader(csvfile_4, delimiter=',', quotechar='"')
for a in creader:
    cursor.execute('INSERT INTO noms (nom) VALUES (?)', a )
csvfile_4.close()

csvfile_5 = open('couleur.txt', 'r',encoding='utf-8',errors='ignore')
creader = csv.reader(csvfile_5, delimiter=',', quotechar='"')
for a in creader:
    cursor.execute('INSERT INTO couleur (nom) VALUES (?)', a )
csvfile_5.close()


#______FIN_INSERT__________________#


#________SELECT_DONNES____________________#

def requete(name,n,lettre_debut,lettre):
    resultat = False
    titres=["noms","animal","fruit","pays","metier","couleur","Total_points"]
    if (n==0):
        cursor.execute("SELECT nom FROM noms WHERE nom = (?) and (?) = (?)",(name,lettre_debut,lettre,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    elif (n==1):
        cursor.execute("SELECT nom FROM animal WHERE nom = (?)",(name,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    elif (n==2):
        cursor.execute("SELECT nom FROM fruit WHERE nom = (?)",(name,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    elif (n==3):
        cursor.execute("SELECT nom FROM pays WHERE nom = (?)",(name,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    elif (n==4):
        cursor.execute("SELECT nom FROM metier WHERE nom = (?)",(name,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    else:
        cursor.execute("SELECT nom FROM couleur WHERE nom = (?)",(name,))
        data=cursor.fetchall()
        if len(data)==1:
            print('There is component named %s'%name)
            resultat = True
        else:
            print("Pas trouvé")
    return resultat

def verification_joueur(liste_serveur,liste_clt):
    existe = False
    if (liste_serveur[i] == liste_clt[i]):
        existe = True
    else:
        existe = False


liste=['SOPHIE','CHIEN','POMME','FRANCE','PILOTE','VERT']
for i in range(len(liste)):
    ver = False
    l = liste[i]
    first = l[0]
    
    ver = requete(liste[i],i,first,'C')
    if (ver == True):
        print("Ok")
    


#________FIN_SELECT_______________________#

ma_bdd.commit()




    
    
