# -*- coding: utf-8 -*-

from tkinter import *
import sys,socket,pickle
from threading import Thread
from random import randint
from imp import reload
import time
from tkinter.messagebox import *

#----------------FONCTION_DU_JEU-------------------#


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
    lb_lettre = Label(frame,text=lettre,bg="LightSalmon",fg="Brown").grid(row=n,column=0)
    

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
    print(reponses)
    return reponses
def geler_tb():
    
    tb_nom.config(state=DISABLED)
    tb_animal.config(state=DISABLED)
    tb_fruit.config(state=DISABLED)
    tb_pays.config(state=DISABLED)
    tb_metier.config(state=DISABLED)
    tb_couleur.config(state=DISABLED)

def valide_tour():
    global connexion_clt,connexion_serveur
    message_envoyer=get_reponse()
    reponse = pickle.dumps(message_envoyer)
    connexion_serveur.send(reponse)
    geler_tb()

def valide_tour_clt():
    global connexion_clt,connexion_serveur
    
    if len(tb_nom.get())==0 or len(tb_animal.get())==0 or len(tb_fruit.get()) == 0 or len(tb_pays.get())==0 or len(tb_metier.get())==0 or len(tb_couleur.get())==0:
        showinfo("Information","Veuillez remplir tout les champs")
    else:
        msg_arreter = 'fin_tour' #message pour arreter le tour de l'autre
        msg_stop = pickle.dumps(msg_arreter)
        connexion_serveur.send(msg_stop)
        
        message_envoyer=get_reponse() #message pour envoyer les reponses
        reponse = pickle.dumps(message_envoyer)
        connexion_serveur.send(reponse)
        geler_tb()

    

    
def lancer_round(frame):
    
    global tb_nom,tb_animal,tb_fruit,tb_pays,tb_metier,tb_couleur,compteur,col
    alphabet = ["A","B","C","D","E","F","G","H","I","J"]
    x = randint(0,9)
    lettre = alphabet[x]
    creer_lettre(frame,compteur,lettre)

    tb_nom=creer_row(frame,compteur,col)
    tb_animal=creer_row(frame,compteur,col+1)
    tb_fruit=creer_row(frame,compteur,col+2)
    tb_pays=creer_row(frame,compteur,col+3)
    tb_metier=creer_row(frame,compteur,col+4)
    tb_couleur=creer_row(frame,compteur,col+5)
    compteur=compteur+1
    return lettre

def lancer_round_clt(frame,lettre):
    global tb_nom,tb_animal,tb_fruit,tb_pays,tb_metier,tb_couleur,compteur,col,Frame2
    creer_lettre(frame,compteur,lettre)
    tb_nom=creer_row(frame,compteur,col)
    tb_animal=creer_row(frame,compteur,col+1)
    tb_fruit=creer_row(frame,compteur,col+2)
    tb_pays=creer_row(frame,compteur,col+3)
    tb_metier=creer_row(frame,compteur,col+4)
    tb_couleur=creer_row(frame,compteur,col+5)
    compteur=compteur+1
    


   
#--------------FIN_FONCTION_JEU----------------------#

#----------------MAIN_JEU----------------------#
#----------------------------------------------#
def jeu():
    global compteur,col,Frame2
    compteur=1
    col=1
    fenetre = Tk()
    fenetre.title("Game")
    fenetre['bg']='Salmon'


    #---FRAME1---#


    Frame1 = Frame(fenetre,width=100, height=100)
    Frame1.pack(padx=30,pady=30)
    Frame1['bg']='Salmon'

    Frame2 = Frame(fenetre)
    Frame2.pack(fill=BOTH)
    Frame2['bg']='Salmon'
    #---Contenue_FRAME1---#

    lb_chrono = Label(Frame1, text="Info",bg="LightSalmon")
    lb_chrono.grid(row=0,column=0)

    lb_attendre = Label(Frame1,text="Attendre que l'admin lance la lettre",fg="Crimson")

    lb_attendre.grid(row=1,column=0)


    #---FRAME2----#

    titres=["nom","animal","fruit","pays/ville","metier","couleur","Total_points"]
    nb=len(titres) #nombre de mot dans les titres



    #------CONTENUE_FRAME2-------#

    creerTab_head(Frame2,titres) #entete du tableau

     #afficher score total du round


    bt_valider = Button(Frame2,text="Valider",bg='LightSalmon',command=valide_tour_clt)
    bt_valider.grid(row=20,column=0)
    fenetre.mainloop()

#----------------FUN MAIN_JEU----------------------#




class Afficheur(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        global connexion_clt, infos_connexion
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.bind((self.ip,self.port))
        connexion.listen(5)
        print("Le serveur écoute sur le port {}".format(self.port))

        connexion_clt, infos_connexion = connexion.accept()
        print(type(connexion_clt))
        
        msg_recu= b""
        i = False
        while i== False:
            while msg_recu !="fin":
                msg_recu = connexion_clt.recv(4024) #si on ne met pas 4000 on peut pas recevoir si le msg est grand
                reponse_question = pickle.loads(msg_recu)
                print(repr(reponse_question))
                
                

            print("Fermeture de la connexion")
            connexion_clt.close()
            connexion.close()
class Afficheur_clt(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
        global connexion_serveur,Frame2
        connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_serveur.connect((self.ip,self.port))
        print("connexion établie")

        msg_recu = b""
        while msg_recu != b"fin": #le serveur fait que ecouteur il decode les message qui
            #ont été envoyer en bytes
            msg_recu = connexion_serveur.recv(4024) 
            reponse_question = pickle.loads(msg_recu)
            rep = reponse_question
            print(type(rep))
            
            
            if type(rep)==str:
                print(rep)
                if (rep.upper() == "FIN_TOUR"):
                    valide_tour()
                    print("Fin du tour")
            elif type(rep)==int:
                total_round(Frame2,compteur-1,str(rep))
                
            elif(len(rep)==1):
                lancer_round_clt(Frame2,rep)
            elif(len(rep)==6):
                print(rep)
            else:
                x=1
                

        print("Fermeture de la connexion")
        connexion_clt.close()
        connexion.close()



def valider():
    
    ip = tb_ip.get()
    port = int(tb_port.get())
    print(ip)
    print(port)
    thread = Afficheur(ip,port) #creation du thread pour la partie
    thread.start() #fait tourner le methode run qui est dans Afficheur()
 #   exec(open('interface_game.py',encoding='utf-8').read())
    win.destroy()
    jeu() #affiche l'interface Graphique du Jeu



#----------------------------CLIENT-------------------------------->
def creerServeur(ip,port):
    global connexion,connexion_clt
    hote= ip
    no_port= port

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.bind((hote,no_port))
    connexion.listen(5)
    print("Le serveur écoute sur le port {}".format(no_port))

    connexion_clt, infos_connexion = connexion.accept()


def connecterServeur(ip,port):
    global connexion_serveur
    hote = ip
    port = port

    connexion_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_serveur.connect((hote,port))
    print("connexion établie")

    msg_recu = b""
    while msg_recu != b"fin": #le serveur fait que ecouteur il decode les message qui
        #ont été envoyer en bytes
        msg_recu = connexion_serveur.recv(4024) 
        reponse_question = pickle.loads(msg_recu)
        print(repr(reponse_question))
        msg_ack ="5/5"
        msg_envoyer = pickle.dumps(msg_ack)
        connexion_serveur.send(msg_envoyer)

    print("Fermeture de la connexion")
    connexion_clt.close()
    connexion.close()
    
def valider_2():
    ip = tb_ip.get()
    port = int(tb_port.get())
    print(ip)
    print(port)
    thread = Afficheur_clt(ip,port)
    thread.start()
    jeu()
    



win = Tk()
win.title("Connexion")
win['bg']='Turquoise'

#FRAME1
Frame1 = Frame(win,relief=RAISED,borderwidth=2)
Frame1.pack(padx=10,pady=10)

#Dans Frame1
lb = Label(Frame1, text="ADRESSE IP")
lb.grid(row=0,column=0)
tb_ip = Entry(Frame1)
tb_ip.grid(row=0,column=1)

lb_2 = Label(Frame1,text="PORT")
lb_2.grid(row=2,column=0)
tb_port = Entry(Frame1)
tb_port.grid(row=2, column=1)

bt_valider = Button(Frame1,text="VALIDER",command=valider_2)
bt_valider.grid(row=3,column=1)

#Frame2


win.mainloop()
