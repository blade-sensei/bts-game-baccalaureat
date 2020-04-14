# coding: utf8 

from tkinter import *
import sys,socket,pickle
from threading import Thread
from random import randint
from imp import reload
import time
from sqlite3 import *
import csv
from tkinter.messagebox import * 


#-------------------BDD------------------------------------------------#




#------------------FIN_BDD---------------------------------------------#


#----------------FONCTION_DU_JEU-------------------#

global thread
def lancer_round():
    x=1    
    
        
def creerTab_head(frame,titres):
    c=1

    lb_lettre = Label(frame,text="Lettre",bg="LightSalmon",fg="Brown",relief=RAISED).grid(row=0, column=0)
    for i in titres:
        Label(frame,text=i,bg="LightSalmon",fg="Brown",relief=RAISED,width=15).grid(row=0, column=c)
        
        c=c+1
        

def creer_lettre(frame,n,lettre):
    noms=[]
    c=0
    lb_lettre = Label(frame,text=lettre,bg="LightSalmon",fg="Brown",relief=RAISED).grid(row=n,column=0)

def creer_row(frame,n,col):
    tb_res = Entry(frame, width=15)
    tb_res.grid(row=n, column=col)
    return tb_res
    
        
        
        
def total_round(frame,n,total):
    lb_lettre = Label(frame,text=total,bg="LightSalmon").grid(row=n,column=7)
    
def get_reponse(): #-----------actions du bouton valider-----------------#
    
    reponses=[]
    #debut récuperation values des textbox#
    nom = tb_nom.get()
    animal = tb_animal.get()
    fruit = tb_fruit.get()
    pays = tb_pays.get()
    metier = tb_metier.get()
    couleur = tb_couleur.get()
    #fin#
    
    reponses.extend([nom,animal,fruit,pays,metier,couleur])
    return reponses
def geler_tb():
    
    tb_nom.config(state=DISABLED)
    tb_animal.config(state=DISABLED)
    tb_fruit.config(state=DISABLED)
    tb_pays.config(state=DISABLED)
    tb_metier.config(state=DISABLED)
    tb_couleur.config(state=DISABLED)

def valide_tour():

    
    global connexion_clt,liste_clt
    if len(tb_nom.get())==0 or len(tb_animal.get())==0 or len(tb_fruit.get()) == 0 or len(tb_pays.get())==0 or len(tb_metier.get())==0 or len(tb_couleur.get())==0:
        showinfo("Information","Veuillez remplir tout les champs")
    else:
        
        msg_arreter = "fin_tour"
        msg_stop = pickle.dumps(msg_arreter)
        connexion_clt.send(msg_stop)
       
        message_envoyer=get_reponse()
     #liste_client = thread.get_liste()
    #    print("message test")
    #    print(liste_client)"""
       
        
        reponse = pickle.dumps(message_envoyer)
        connexion_clt.send(reponse)

     #   ajouter_points(0,message_envoyer,liste_client)    
        geler_tb()

  

def stop_tour():
    global connexion_clt
    
    message_envoyer=get_reponse()
    reponse = pickle.dumps(message_envoyer)
    connexion_clt.send(reponse)
    geler_tb()
    
    
def lancer_round(frame):
    global let
    lettre=[]      
    global tb_nom,tb_animal,tb_fruit,tb_pays,tb_metier,tb_couleur,compteur,col,connexion_clt,infos_connexion 
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","R","S","T","U","V","W","X","Y","Z"]
    x = randint(0,9)
    let = alphabet[x]
    lettre.append(let)
    
    msg = pickle.dumps(lettre)
    connexion_clt.send(msg)
    creer_lettre(frame,compteur,lettre)

    tb_nom=creer_row(frame,compteur,col)

    tb_animal=creer_row(frame,compteur,col+1)
    tb_fruit=creer_row(frame,compteur,col+2)
    tb_pays=creer_row(frame,compteur,col+3)
    tb_metier=creer_row(frame,compteur,col+4)
    tb_couleur=creer_row(frame,compteur,col+5)
    compteur=compteur+1
    return lettre


   
#--------------FIN_FONCTION_JEU----------------------#

#----------------MAIN_JEU----------------------#
#----------------------------------------------#
def jeu():
    global compteur,col,connexion_clt,fenetre,Frame2
    compteur=1
    col=1
    fenetre = Tk()
    fenetre.title("---- Jeu du Bac ----")
    fenetre['bg']='Salmon'


    #---FRAME1---#


    Frame1 = Frame(fenetre,width=100, height=100)
    Frame1.pack(padx=30,pady=30)
    

    Frame2 = Frame(fenetre)
    Frame2.pack(fill=BOTH)
    Frame2['bg']='Salmon'
    #---Contenue_FRAME1---#

    lb_chrono = Label(Frame1, text="Chrono")
    lb_chrono.grid(row=0,column=0)

    bt_round = Button(Frame1,text="Lancer Round",bg="Salmon",command=lambda:lancer_round(Frame2))

    bt_round.grid(row=1,column=0)

    Frame1['bg']='Salmon'


    #---FRAME2----#

    titres=["nom","animal","fruit","pays/ville","metier","couleur","Total_points"]
    nb=len(titres) #nombre de mot dans les titres



    #------CONTENUE_FRAME2-------#

    creerTab_head(Frame2,titres) #entete du tableau

     #afficher score total du round


    bt_valider = Button(Frame2,text="Valider",command=valide_tour)
    bt_valider.grid(row=20,column=0)
    bt_valider['bg']='LightSalmon'
    fenetre.mainloop()


    

#----------------FUN MAIN_JEU----------------------#

global Afficheur,thread,Thread,cursor


class Afficheur(Thread):
    global cursor,thread,fenetre,Frame2,compteur,let
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
    
    def get_liste(self):
        return self.liste_clt

    def requete(self,name,n,cursor,lettre_debut,let):
        resultat = False
        titres=["noms","animal","fruit","pays","metier","couleur","Total_points"]
        if (n==0):
            cursor.execute("SELECT nom FROM noms WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let))
            data=cursor.fetchall()
            if len(data)==1:
                print('There is component named %s'%name)
    
                resultat = True
            else:
                print("Pas trouvé nom")
                print(name)
        elif (n==1):
            cursor.execute("SELECT nom FROM animal WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let,))
            data=cursor.fetchall()
            print("test"+repr(len(data)))
            if len(data)==1:
                print('There is component named %s'%name)
                resultat = True
            else:
                print("Pas trouvé")
        elif (n==2):
            cursor.execute("SELECT nom FROM fruit WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let,))
            data=cursor.fetchall()
            print(len(data))
            if len(data)==1:
                print('There is component named %s'%name)
                resultat = True
            else:
                print("Pas trouvé")
        elif (n==3):
            cursor.execute("SELECT nom FROM pays WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let,))
            data=cursor.fetchall()
            print(len(data))
            if len(data)==1:
                print('There is component named %s'%name)
                resultat = True
            else:
                print("Pas trouvé")
        elif (n==4):
            cursor.execute("SELECT nom FROM metier WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let,))
            data=cursor.fetchall()
            if len(data)==1:
                print('There is component named %s'%name)
                resultat = True
            else:
                print("Pas trouvé")
        else:
            cursor.execute("SELECT nom FROM couleur WHERE nom = (?) and (?) = (?)",(name,lettre_debut,let,))
            data=cursor.fetchall()
            if len(data)==1:
                print('There is component named %s'%name)
                resultat = True
            else:
                print("Pas trouvé")
        return resultat
    
        

    def ajouter_point(self,id_joueur,liste_serveur,liste_clt,cursor):
        
        numcat = 0
        point = 0
        score_serveur = 0
        score_client = 0
        if id_joueur==0: #serveur
            for i in liste_serveur:
                if i=="":
                    point = 0
                
                else:
                    first = i[0]
                    first = first.upper()
                    print(first)
                    if self.requete(i.upper(),numcat,cursor,first,let)==True:
                        point = 2
                        
                        if i.upper() == liste_clt[numcat].upper():
                            point = 1
                         
                    else:
                        point = 0
                score_serveur = score_serveur+point
                print("score serveur :"+repr(score_serveur))
                numcat=numcat+1
            return score_serveur
        
        
        elif id_joueur==1: #client
            for i in liste_clt:
                if i=="":
                    point=0
                    numcat = numcat+1
                    
                    
                else:
                
                    first = i[0]
                    first = first.upper()
                    if self.requete(i.upper(),numcat,cursor,first,let)==True:
                        point = 2
                        if i.upper() == liste_serveur[numcat].upper():
                            point = 1
                     
                    else:
                        point = 0
                score_serveur = score_serveur+point
                print("score client :"+repr(score_serveur))
                numcat = numcat+1
            return score_serveur
        
        
        
    

    def run(self):
        global connexion_clt, infos_connexion,cursor,ma_bdd ,Frame2,fenetre,compteur     

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

        """
        cursor.execute('''SELECT nom FROM fruit''')
        noms = cursor.fetchall()
        for row in noms:
            print(row[0])"""



        #________FIN_SELECT_______________________#

        ma_bdd.commit()

        #FIN_BDD----------#


        
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.bind((self.ip,self.port))
        connexion.listen(5)
        print("Le serveur écoute sur le port {}".format(self.port))

        connexion_clt, infos_connexion = connexion.accept()
        
        msg_recu= b""
        
        i = False
        while i== False:
            while msg_recu !="fin":
                msg_recu = connexion_clt.recv(4024) #si on ne met pas 4000 on peut pas recevoir si le msg est grand
                reponse_question = pickle.loads(msg_recu)
                rep = reponse_question
    
                
                if type(rep)==str:
                    if (rep.upper() == "FIN_TOUR"):
                        stop_tour()
                elif len(rep) == 6: #partie quannd le serveur reçoit la liste des l'adversaire
                    self.liste_clt = rep
                    message_envoyer = get_reponse()
                    
                    
                    scr_serveur = self.ajouter_point(0,message_envoyer,rep,cursor)
                    
                    total_round(Frame2,compteur-1,str(scr_serveur))
                    scr_client = self.ajouter_point(1,message_envoyer,rep,cursor)
                    msg_envoyer_clt = pickle.dumps(scr_client)
                    connexion_clt.send(msg_envoyer_clt)

                        
                else:
                    print("else")                  
            print("Fermeture de la connexion")
            connexion_clt.close()
            connexion.close()




def valider():
    global thread,Afficheur,win
    ip = tb_ip.get()
    port = int(tb_port.get())
    print(ip)
    print(port)
    thread = Afficheur(ip,port) #creation du thread pour la partie
    thread.start() #fait tourner le methode run qui est dans Afficheur()
 #   exec(open('interface_game.py',encoding='utf-8').read())
    win.destroy()
    jeu() #affiche l'interface Graphique du Jeu
    
    
    

    
global win   
#_----connexion------#
win = Tk()
win.title("Connexion Serveur")
win['bg']='SpringGreen'

global connexion_clt,tb_ip,tb_port
#FRAME1
Frame1 = Frame(win,relief=RAISED,borderwidth=6)
Frame1.pack(padx=30,pady=30)

#Dans Frame1
lb = Label(Frame1, text="ADRESSE IP")
lb.grid(row=0,column=0)
tb_ip = Entry(Frame1)
tb_ip.grid(row=0,column=1)

lb_2 = Label(Frame1,text="PORT")
lb_2.grid(row=2,column=0)
tb_port = Entry(Frame1)
print(type(tb_port))
tb_port.grid(row=2, column=1)
print(type(tb_port))



bt_valider = Button(Frame1,text="VALIDER",command=valider)
bt_valider.grid(row=3,column=1)

#---------Connexion_serveur--------------#

win.mainloop()


#---FIN_CONNEXION---#

