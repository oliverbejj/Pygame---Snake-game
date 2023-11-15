'''   /20

1er rendu               :  /4
Objet                   :  /2
Mouvements              :  /2
Interactions            :  /2
Variété des tracés      :  /2
Qualité du code         :  /3
Complexité du jeu       :  /3
Esthétique              :  /2



Description:
Un serpent (cercle bleu) qui bouge de carre en carre.
On lui change sa direction avec les fleches.
Le but est de manger le plus de pommes possible (cercle rouge) sans mourir.
Quand il mange une pomme, le serpent grandit et le joueur gagne 1 point

Pour les prochaines versions du jeu je compte laisser l'utilisateur choisir la vitesse du serpent de plus que lui donner
le choix entre plusieurs couleurs pour le serpent.
J'afficherais aussi le score.
Il y aura une page de debut de plus qu'une page de fin (perdre ou gagner)
'''




import sys, pygame, time, os , couleurs
from pygame.locals import *
from random import choice
pygame.font.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
DIMENSIONS = LARGEUR, HAUT = (500, 500)
fenetre = pygame.display.set_mode(DIMENSIONS)
rafraichissement = pygame.time.Clock()

scores=""
f = open('score.csv',"r")
scores=scores+f.readline()
l_score=scores.split("-")
f.close()



jouer=True
score=0
l=[i+LARGEUR/20 for i in range (0,LARGEUR,LARGEUR//10)]
l_serpent=[]
l2=[]
class Serpent:
    def __init__(self,vitesse,couleur,ab,ordo,h_v,mou_x,mou_y):
        self.x=ab
        self.y=ordo
        self.x2=ab
        self.y2=ordo
        self.hori_ou_vert=h_v
        self.hori_ou_vert2=h_v
        self.vit=vitesse
        self.coul=couleur
        self.m_x=mou_x
        self.m_y=mou_y
    def creer(self):
        pygame.draw.circle(fenetre,self.coul , (self.x, self.y), LARGEUR/20)
            
    def direction(self,clavier):
        self.hori_ou_vert2=self.hori_ou_vert
        for event in clavier:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.hori_ou_vert=True
                    self.m_x=LARGEUR/10
                if event.key == pygame.K_DOWN:
                    self.hori_ou_vert=False
                    self.m_y=HAUT/10
                if event.key == pygame.K_LEFT:
                    self.hori_ou_vert=True 
                    self.m_x=-(LARGEUR/10)
                if event.key == pygame.K_UP:
                    self.hori_ou_vert=False
                    self.m_y=-(HAUT/10)
            
    def bouger_corps(self,other):
        self.x2=self.x
        self.y2=self.y
        self.x=other.x2
        self.y=other.y2
        self.hori_ou_vert2=self.hori_ou_vert
        self.hori_ou_vert=other.hori_ou_vert2
        
       
        
    def bouger(self):
        self.x2=self.x
        self.y2=self.y
        if self.hori_ou_vert:
            self.x+=self.m_x
        else:
            self.y+=self.m_y
            
        
    def perdre(self):
        global jouer
        global score
        if self.x<0 or self.y<0 or self.x>LARGEUR or self.y>HAUT :
            jouer=False
            f2=open('score.csv',"w")
            f2.write(scores+str(score)+"-")
            f2.close()
coul=couleurs.COULEURS['blue']
class Pomme:
    def __init__(self,couleur):
        self.x=choice(l)
        self.y=choice(l)
        self.coul=couleur
    def creer(self):
        pygame.draw.circle(fenetre,self.coul, (self.x, self.y),LARGEUR/20)
    def changer_pos(self):
        global score
        if l_serpent[0].x==self.x and l_serpent[0].y==self.y:
            self.x=choice(l)
            self.y=choice(l)
            score+=1
            if l_serpent[-1].hori_ou_vert:
                l_serpent.append(Serpent(2.5,coul,l_serpent[-1].x-l_serpent[-1].m_x,l_serpent[-1].y,l_serpent[-1].hori_ou_vert,l_serpent[-1].m_x,l_serpent[-1].m_y))
            else:
                l_serpent.append(Serpent(2.5,coul,l_serpent[-1].x,l_serpent[-1].y-l_serpent[-1].m_y,l_serpent[-1].hori_ou_vert,l_serpent[-1].m_x,l_serpent[-1].m_y))
            
class Bouton:
    def __init__(self,ab,ordo,image):
        self.img=image
        self.rect=self.img.get_rect()
        self.rect.x=ab
        self.rect.y=ordo
        
    def afficher(self):
        a=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                a=True
        fenetre.blit(self.img,self.rect)
        return a
        
image_commencer=pygame.image.load("commencer.png")
image_quitter=pygame.image.load("quitter.png")

image_facile=pygame.image.load("facile.png")
image_moyen=pygame.image.load("moyen.png")
image_difficile=pygame.image.load("difficile.png")

image_bleu=pygame.image.load("bleu.png")
image_jaune=pygame.image.load("jaune.png")
image_rose=pygame.image.load("rose.png")

c=Bouton(LARGEUR//2-150,HAUT//2-250,image_commencer)
q=Bouton(LARGEUR//2-100,HAUT//2-200,image_quitter)



facile=Bouton(LARGEUR//2-90,HAUT//2-80,image_facile)
moyen=Bouton(LARGEUR//2-95,HAUT//2-20,image_moyen)
difficile=Bouton(LARGEUR//2-110,HAUT//2+40,image_difficile)

bleu=Bouton(LARGEUR//2-150,HAUT//2+125,image_bleu)
jaune=Bouton(LARGEUR//2-50,HAUT//2+125,image_jaune)
rose=Bouton(LARGEUR//2+50,HAUT//2+125,image_rose)


p=Pomme(couleurs.COULEURS['red'])
l_serpent.append(Serpent(2.5,couleurs.COULEURS['purple'],LARGEUR/20,HAUT/20,True,LARGEUR/10,HAUT/10))

menu=True
font=pygame.font.Font("freesansbold.ttf",20)
n=0
vitesse=300
m=int(l_score[0])
for elt in l_score:
    if elt!="" and int(elt)>m:
        m=int(elt)
while jouer:
    
    rafraichissement.tick(vitesse)
    
    if menu:
        figure=pygame.Surface((LARGEUR, HAUT))
        figure.fill((102, 205, 0, 255))
        fenetre.blit(figure, ((LARGEUR//9999), (LARGEUR//9999)))
        text=font.render("Le meilleur score est "+str(m)+", pouvez-vous le battre?",True,couleurs.COULEURS["white"])
        fenetre.blit(text,(LARGEUR//5-85,HAUT//2-130))
        
        text3=font.render("Difficulté(moyen par défaut):",True,couleurs.COULEURS["white"])
        fenetre.blit(text3,(LARGEUR//5-80,HAUT//2-110))
        
        text2=font.render("Couleur (bleu par défaut):",True,couleurs.COULEURS["white"])
        fenetre.blit(text2,(LARGEUR//2-70,HAUT//2+100))
        
        if bleu.afficher():
            coul=couleurs.COULEURS["blue"]
        if jaune.afficher():
            coul=couleurs.COULEURS["yellow"]
        if rose.afficher():
            coul=couleurs.COULEURS["hotpink"]
        
        if facile.afficher():
            vitesse=150
        if moyen.afficher():
            vitesse=300
        if difficile.afficher():
            vitesse=600
        if c.afficher():
            menu=False
        if q.afficher():
            jouer=False
    else:
        for i in range (10):
            for j in range(10):
                figure=pygame.Surface((LARGEUR//10, HAUT//10))
                if (i+j)%2==0:
                    figure.fill((102, 205, 0, 255))
                else:
                    figure.fill((69, 139, 0, 255))
                fenetre.blit(figure, (i*(LARGEUR//10), j*(LARGEUR//10)))
        
        n+=1
        if n%333==0:
            l_serpent[0].bouger()
            le=len(l_serpent)
            if le>=2:
                for i in range(1,le):
                    l_serpent[i].bouger_corps(l_serpent[i-1])
                
        clavier1=pygame.event.get()
        l_serpent[0].direction(clavier1)
        
        
        
        

       

        p.creer()
        for elt in l_serpent:
            elt.creer()
        
        l_serpent[0].perdre()
        p.changer_pos()   
        
            
    
    



    pygame.display.flip()
    clavier=pygame.event.get()
    for event in clavier:
        if event.type == pygame.QUIT:
            jouer=False
    
pygame.quit()
