from tkinter import *
from tkinter import colorchooser
import tkinter
#from tkinter import _EntryIndex
from tkinter.tix import DisplayStyle
from turtle import left
from formes import *
from random import randint
import sqlite3
#import pygame
 


class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur,couleur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur)
        self.configure(bg=couleur)


#===================================================================================================================
class MonButton(Button):
    def __init__(self,fenetre,nom,etat,methode):
        Button.__init__(self,fenetre,text=nom)
        self.config(state=etat)
        self.lettre=nom
        self.config(command=self.desactive)
        self.clic=False
        self.methode=methode
        self.__triche=0

    def active(self):
        self.config(state=NORMAL)
    def desactive(self):
        self.config(state=DISABLED)
        self.clic=True
        self.methode(self.lettre)


class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Jeu du Pendu")
        self.configure(bg='deep sky blue')
        self.ChangeMot()
        self.__texteResultat = StringVar()
        self.__CouleurBg="red"
        #pygame.mixer.init()
        self.__score=[0,0,0]
        self.__compteurP=0   
        #self.play_music()
        #===================================================================================================
        #=================================- Partie Data Base -==============================================
        self.__conn=sqlite3.connect("penduu.db")


        #===================================================================================================
        #=================================- Partie Bouton en haut -=========================================
        #On Crée la fenetre des boutons nouvelle partie et quitter
        Frame1 = Frame(bg='white')
        Frame1.pack(side=TOP, padx=10 ,pady=10)

        self.__ButonNewGame = Button(Frame1,bg="white",text="Nouvelle Partie")
        self.__ButonNewGame.pack(side=LEFT,padx=5,pady=5)
        self.__ButonNewGame.config(command=self.MotAlea)
        self.__ButonNewGame.config(state=DISABLED)
        
        self.__BoutonNewP = Button(Frame1, bg="white",text="Log In")
        self.__BoutonNewP.pack(side=LEFT,padx=5,pady=5)
        self.__BoutonNewP.config(command=self.Fen_Message)


        MNU_OngletA = tkinter.Menubutton ( Frame1 , text = "Menu Couleurs" )
        MNU_OptionA = tkinter.Menu ( MNU_OngletA )
        MNU_OptionA.add_command ( label = "Couleur zone Pendu" , command = self.color_ZA )
        MNU_OptionA.add_command ( label = "Couleur arrière plan" , command = self.color_fenetre )
        MNU_OptionA.add_command ( label = "Couleur zone Texte" , command = self.color_zoneText )
        MNU_OngletA [ "menu" ] = MNU_OptionA
        MNU_OngletA.pack(side=LEFT,padx=5,pady=5)


        

        self.__BoutonTriche = Button(Frame1,bg="white",text="Triche")
        self.__BoutonTriche.pack(side=LEFT,padx=5,pady=5)
        self.__BoutonTriche.config(command=self.undo)
        self.__BoutonTriche.config(state=DISABLED)

        boutonQuitter = Button(Frame1,bg="white", text='Quitter')
        boutonQuitter.pack(side=LEFT, padx=5, pady=5)
        boutonQuitter.config(command=self.destroy)

        #===============================- Partie Zone Affichage du pendu -=================================================
        #on crée la zone d'affichage du pendu
        
        self.__canevas=ZoneAffichage(self, 400,300,self.__CouleurBg)
        self.__canevas.pack(side=TOP)
        # Base, Poteau, Traverse, Corde
        self.listeDesRect=[
        Rectangle(self.__canevas, 50,  270, 200,  26, "brown"),\
        Rectangle(self.__canevas, 87,   83,  26, 200, "brown"),\
        Rectangle(self.__canevas, 87,   70, 150,  26, "brown"),\
        Rectangle(self.__canevas, 183,  67,  10,  40, "brown"),\
        Ellipse(self.__canevas, 188, 120,  17,  22, "black"),\
        Rectangle(self.__canevas, 175, 143,  26,  60, "black"),\
        Rectangle(self.__canevas, 133, 150,  40,  10, "black"),\
        Rectangle(self.__canevas, 203, 150,  40,  10, "black"),\
        Rectangle(self.__canevas, 175, 205,  10,  40, "black"),\
        Rectangle(self.__canevas, 191, 205,  10,  40, "black")]






        #=================================- endroit où le mot s'affiche -=============================================
        #on crée la fenetre du mot qu'on doit découvrir
        self.__Frame2 = Frame(bg="red")
        self.__Frame2.pack(side=TOP, padx=10 ,pady=10)
        self.__texteResultat.set('Veuillez appuyer sur "Log In" avant de commencer à jouer')
        self.__labelMot = Label(self.__Frame2,fg="black",textvariable=self.__texteResultat)
        self.__labelMot.pack()
        
        
        #===================================- On crée ici les boutons pour jouer -======================================
        #On Crée la fenetre du clavier
        Frame3 = Frame()
        Frame3.pack(side=TOP, padx=10 ,pady=10)

        self.liste_bouton=[MonButton(Frame3, chr(ord('A')+i),DISABLED,self.traitement) for i in range(0,26)]
        i=0
        for bouton in self.liste_bouton:
            bouton.grid(row=i//7, column=i%7)
            if i>=21:
                bouton.grid(row=i//7, column=(i%7) +1)
            i=i+1

#======================================- Partie menu couleur -====================================================================
    def color_ZA(self):
        colours=colorchooser.askcolor(title="Tkinter Color Chooser")
        self.__canevas.configure(bg=colours[1])
    
    def color_fenetre(self):
        colours=colorchooser.askcolor(title="Tkinter Color Chooser")
        self.configure(bg=colours[1])

    def color_zoneText(self):
        colours=colorchooser.askcolor(title="Tkinter Color Chooser")
        self.__labelMot.configure(bg=colours[1])


    def ChangeMot(self):
        f = open('mots.txt', 'r')
        s = f.read()
        self.__mots = s.split('\n')
        f.close()

#======================================- Code du NewGame et triche -====================================================================
    def MotAlea(self):
        self.__score[2]=0
        self.__gg=0
        self.__triche=0
        self.__cpt=0
        self.__cptWin=0
        self.__BoutonTriche.config(state=DISABLED)
        nb = randint(1, len(self.__mots))
        self.__lemot=self.__mots[nb]
        #print(self.__lemot)
        self.__MotHidden='*'*len(self.__mots[nb])
        self.__texteResultat.set('le mot est : '+self.__MotHidden)
        self.__mot_affiche=list(self.__MotHidden)
        for r in self.listeDesRect:
            r.setState("hidden")
        for i in range(0,26):
            self.liste_bouton[i].config(state=NORMAL)
        self.__compteurP+=1  
    
    def undo(self):
        self.listeDesRect[self.__cpt - 1].setState("hidden")
        self.__cpt-=1
        if self.__cpt<=0:
            self.__BoutonTriche.config(state=DISABLED)
        self.__triche=1

#==========================================- Partie code de la fenetre Log In -================================================================
    
    def LogIn(self,fen=[]):
        self.__compteurP=0
        global entry
        self.__pseudo= self.__entryLogIn.get()
        curseur = self.__conn.cursor()
        a = "SELECT Pseudo FROM Joueurs WHERE Pseudo = '{}'".format(self.__pseudo)
        curseur.execute(a)
        liste_P=curseur.fetchall()
        b = "SELECT ID FROM Joueurs"
        curseur.execute(b)
        liste_ID=curseur.fetchall()
        self.__texteResultat.set('Veuillez appuyer sur "Nouvelle Partie" pour commencer à jouer')
        if self.__pseudo=='' or self.__pseudo==' ':
            self.__labelMsg.configure(text='Veuiller entrer un pseudo valide')
        else:
            if liste_P == []:
                self.__labelMsg.configure(text='Bienvenue parmi nous, {}\nVous pouvez fermer cette fenêtre et commencer à jouer'.format(self.__pseudo))
                if liste_ID==[]:
                    self.__tempID=1
                    self.__newID=[1]
                else:
                    self.__tempID=int(liste_ID[-1][0]) + 1
                    self.__newID=[self.__tempID]
                c = "INSERT INTO Joueurs VALUES('{}','{}')".format(self.__tempID,self.__pseudo)
                curseur.execute(c)
                self.__conn.commit()
                z = "INSERT INTO Partie VALUES('{}','{}','{}','{}')".format(self.__tempID,0,0,0)
                curseur.execute(z)
                self.__conn.commit()

                self.__FrameMsg.unbind('<Return>')
                self.__boutonEntrer.config(state=DISABLED)
                self.__ButonNewGame.config(state=NORMAL)
            else:
                b = "SELECT ID FROM Joueurs WHERE Pseudo = '{}'".format(self.__pseudo)
                curseur.execute(b)
                self.__newID=curseur.fetchone()
                self.__labelMsg.configure(text='Re-Bienvenue parmi nous, {}\nVous pouvez fermer cette fenêtre et commencer à jouer'.format(self.__pseudo))
                self.__FrameMsg.unbind('<Return>')
                self.__boutonEntrer.config(state=DISABLED)
                self.__ButonNewGame.config(state=NORMAL)
        

    def Fen_Message(self):
        self.__FrameMsg=Toplevel(self)
        self.__FrameMsg.config(bg='cyan')
        self.__FrameMsg.title("Log In")
        self.__FrameMsg.geometry("750x250")

        self.__boutonEntrer = Button(self.__FrameMsg,bg="white", text='Entrer')
        boutonQuitter = Button(self.__FrameMsg,bg="white", text='Fermer')
        boutonQuitter.config(command=self.__FrameMsg.destroy)
        
        self.__labelMsg=Label(self.__FrameMsg, text="Veuillez entrer votre pseudo", font=("Courier 22 bold"))
        self.__labelMsg.pack()
        self.__entryLogIn= Entry(self.__FrameMsg, width= 40)
        self.__entryLogIn.focus_set()


        
        self.__entryLogIn.pack()
        
        
        self.__boutonEntrer.pack(side=TOP, padx=5, pady=5)
        boutonQuitter.pack(side=TOP, padx=5, pady=5)

        self.__FrameMsg.bind('<Return>',self.LogIn)
        self.__boutonEntrer.config(command=self.LogIn)
        #self.__BoutonNewP.config(state=DISABLED)

#============================-Methode pour mettre à jour le score dans la data base -================================================================
    def update_score(self):
        curseur = self.__conn.cursor()
        t = "SELECT NbPartie,NbWin,Score FROM Partie WHERE ID = '{}'".format(self.__newID[0])
        curseur.execute(t)
        temp_score=curseur.fetchone()
        if temp_score[0]==None:
            temp_score=[0,0,0]
        self.__score[0]=temp_score[0]+1
        self.__score[1]=temp_score[1]
        if self.__gg==1:
            self.__score[1]+=1
        self.__score[2]+=temp_score[2]
        a = "UPDATE Partie SET NbPartie = '{}' WHERE ID = '{}'".format(temp_score[0]+1,self.__newID[0])
        curseur.execute(a)
        self.__conn.commit()
        a = "UPDATE Partie SET NbWin = '{}' WHERE ID = '{}'".format(self.__score[1],self.__newID[0])
        curseur.execute(a)
        self.__conn.commit()
        a = "UPDATE Partie SET Score = '{}' WHERE ID = '{}'".format(self.__score[2],self.__newID[0])
        curseur.execute(a)
        self.__conn.commit()
#==========================================- Partie code des musiques et sons-================================================================
        
    #def play_music(self): 
    #    pygame.mixer.music.load("menu.mp3") 
    #    pygame.mixer.music.play(loops=100)

#================================================- Fonction traitement -================================================================================

    def traitement(self,lettre):
        lettres_dumot=list(self.__lemot)
        if self.__cpt<0:
            self.__cpt=0
        #On compte le nombre de fois que le joueur échoue à trouver une bonne lettre
        if lettre not in lettres_dumot:
            self.listeDesRect[self.__cpt].setState("normal")
            self.__cpt+=1
            self.__BoutonTriche.config(state=NORMAL)
        
        
        
        #Si le joueur trouve une bonne lettre on l'affiche :
        for i in range(0,len(lettres_dumot)):
            if lettres_dumot[i] == lettre:
                self.__mot_affiche[i]=lettre
                self.__texteResultat.set('le mot est : '+ "".join(self.__mot_affiche))
                self.__cptWin+=1
        #Cette partie du code permet de faire une fin de partie
        if self.__cpt==10:
            for bouton in self.liste_bouton:
                bouton.config(state=DISABLED)
            self.__texteResultat.set('C\'est une fin de game pour vous. Le mot était {}'.format("".join(lettres_dumot)))
            self.__BoutonTriche.config(state=DISABLED)
            self.update_score()
            print("---------------------------------------------------------")
            print("Votre score est :")
            print("nombre de partie jouées : {}".format(self.__score[0]))
            print("nombre de partie gagnées : {}".format(self.__score[1]))
            print("Score cumulé : {}".format(self.__score[2]))
        if self.__cptWin==len(lettres_dumot):
            
            self.__score[2]=self.__cptWin/(self.__cptWin + self.__cpt)
            for bouton in self.liste_bouton:
                bouton.config(state=DISABLED)
            if self.__triche==0:
                self.__texteResultat.set('Bravo vous avez gagné! Le mot était bien {}'.format("".join(lettres_dumot)))
                self.__BoutonTriche.config(state=DISABLED)
                self.__gg=1
                self.update_score()
                print("---------------------------------------------------------")
                print("Votre score est :")
                print("nombre de partie jouées : {}".format(self.__score[0]))
                print("nombre de partie gagnées : {}".format(self.__score[1]))
                print("Score cumulé : {}".format(self.__score[2]))
            if self.__triche==1:
                self.__texteResultat.set("A vaincre sans péril on triomphe sans gloire. En trichant vous ne gagnez pas "+\
                    "de points.\nRejouez sans tricher pour en gagner.\nLe mot était {}".format("".join(lettres_dumot)))
                self.__score[2]=0
                self.__BoutonTriche.config(state=DISABLED)
                self.update_score()
                print("---------------------------------------------------------")
                print("Votre score est :")
                print("nombre de partie jouées : {}".format(self.__score[0]))
                print("nombre de partie gagnées : {}".format(self.__score[1]))
                print("Score cumulé : {}".format(self.__score[2]))
        
        






if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()