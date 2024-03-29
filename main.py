import pygame
import cv2
import math
from random import randint

cam = cv2.VideoCapture(0)
palm = cv2.CascadeClassifier('palm.xml')
#introduction de la pome de la main
pygame.init()
a = []
myfont = pygame.font.SysFont("monospace", 20) #crée un objet pour le fond, (nom, taille)
myfont = pygame.font.Font('ZombieApocalypse.ttf',20)

win = pygame.display.set_mode((900, 506)) #crée un ecran de la taille 1500x822
bg = pygame.image.load('fond.jpg') #charge un image comme fonnd

#crée les image des zombie
zombie1 = [pygame.image.load('Zombie1_1.png'), pygame.image.load('Zombie1_2.png'),
              pygame.image.load('Zombie1_3.png')]
zombie2 = [pygame.image.load('Zombie2_1.png'), pygame.image.load('Zombie2_2.png'),
              pygame.image.load('Zombie2_3.png')]
zombie3 = [pygame.image.load('Zombie3_1.png'), pygame.image.load('Zombie3_2.png'),
              pygame.image.load('Zombie3_3.png')]
zombie4 = [pygame.image.load('Zombie4_1.png'), pygame.image.load('Zombie4_2.png'),
              pygame.image.load('Zombie4_3.png')]

#crée l'arme
axe= pygame.image.load('Axe1.png')
#crée le titre
pygame.display.set_caption("Zombie Slayer")
#crée le chronometre
clock = pygame.time.Clock()

#definir une classe objects avec la physique des zombie
class img(object):
    def __init__(self, x, y, pic, u=12, g=-1, t=0):
        self.x = x
        self.y = y
        self.pic = pic
        self.u = u
        self.pos = x
        self.g = g
        self.t = t
    def show(self,angle):  #definion de la rortation des tete
        self.angle = angle
        win.blit(pygame.transform.rotate(self.pic, self.angle), (self.x, self.y))

win.blit(bg, (0, 0))
pygame.display.update()
vx = 0
vy = 0
run = True
angle = 0
x = []
score = 0

#code opencv pour capter la pome de la main
while run:
    ret, frame = cam.read()
    correct = cv2.flip(frame, 1)
    gray = cv2.cvtColor(correct, cv2.COLOR_BGR2GRAY)
    palmcord = palm.detectMultiScale(gray, 1.3, 5)
    for (p, q, r, s) in palmcord:
        centery = (2 * q + s) / 2
        centerx = (2 * p + r) / 2
        cv2.rectangle(correct, (p, q), (p + r, q + s), (0, 255, 0), 2)
        vy = int((centery / 480) * 506)
        vx = int((centerx / 640) * 900)
    cv2.imshow("output", correct)
    win.blit(axe, (vx, vy)) #assosier la main a la hache
    number = randint(0, 3)
    maskp = pygame.mask.from_surface(axe)


# definition du saut des tête ainsi que du choix de la tête
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if a == x:
        for i in range(number):
            pos = randint(50, 546)
            ypos = randint(200, 940)
            zombie_type = randint(0, 3)

            if zombie_type == 0:
                zombie = zombie1[0]
            if zombie_type == 1:
                zombie = zombie2[0]
            if zombie_type == 2:
                zombie = zombie3[0]
            if zombie_type == 3:
                zombie = zombie4[0]
            a.append(img(pos, ypos, zombie))

    for z in a:
        z.y = z.y - (z.u*z.t)
        z.u = z.u + (z.g*z.t)
        z.t = z.t + 0.01
        if z.pos <= 546:
            z.x = z.x + 1.3
        if z.pos > 546:
            z.x = z.x - 1.3
        if z.u == 0:
            z.t = 0
        z.show(angle)

        #Mort des zombies si la hache passe sur eux
        mask = pygame.mask.from_surface(z.pic)
        if not(mask.overlap(maskp,(int(z.x - vx), int(z.y - vy))) == None):

            if z.pic == zombie1[0] or z.pic == zombie2[0] or z.pic == zombie3[0] or z.pic == zombie4[0]:
                score +=1
                index_value = a.index(z)
                xposition = z.x
                yposition = z.y
                grav = z.g
                vel = z.u
                tim = z.t
                if z.pic == zombie1[0]:
                    a.append(img(xposition +9, yposition + 9, zombie1[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, zombie1[2], vel, grav, tim)
                if z.pic == zombie2[0]:
                    a.append(img(xposition + 9, yposition + 9, zombie2[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, zombie2[2], vel, grav, tim)
                if z.pic == zombie3[0]:
                    a.append(img(xposition +9, yposition + 9, zombie3[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, zombie3[2], vel, grav, tim)
                if z.pic == zombie4[0]:
                    a.append(img(xposition +9, yposition + 9, zombie4[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, zombie4[2], vel, grav, tim)

        scoretext = myfont.render("Zombie Counter = " + str(score) + " Dead", True, (100, 153, 0))
        win.blit(scoretext, (5, 10))
        if z.y > 550:
            a = []

    pygame.display.update()
    win.blit(bg, (0, 0))


    angle = angle + 1
    if angle == 259:
        angle = 0
    clock.tick(6000)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
pygame.quit()
cv2.destroyAllWindows()
