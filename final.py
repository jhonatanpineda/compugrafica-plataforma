# coding: utf-8
#------------------------------------------------------------------------------------------------------------------------------------------------
############################################################## poder cientifico ############################################################## 
#------------------------------------------------------------------------------------------------------------------------------------------------
#Librerias
import os
import pygame
import sys
from pygame.locals import *
import time
import threading
import random
#------------------------------------------------------------------------------------------------------------------------------------------------
ANCHO = 1366
ALTO = 768
BASE_PERSONAJE = 705
VELOCIDAD = +5
nivelador=0
centSeg=0
unidSeg=0
deceSeg=0
unidMin=0
deceMin=0
#------------------------------------------------------------------------------------------------------------------------------------------------

class TextoTiempo:
    def __init__(self, TipoFuente = 'Zombified.ttf', Tamano = 40):
        pygame.font.init()
        self.font = pygame.font.Font(TipoFuente, Tamano)
        self.size = Tamano
 
    def render(self, surface, text, color, pos):
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size 
             
def TiempoJuego():
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, nivelador, ReiniciarTiempo 
    nivelador+=1
    if nivelador == 7:
       nivelador=0
       centSeg+=1
    if centSeg==9:
       centSeg=0
       unidSeg+=1
    if unidSeg==10:
       unidSeg=0
       deceSeg+=1
    if deceSeg==6:
       deceSeg=0
       unidMin+=1
    if unidMin==10:
       unidMin=0
       deceMin+=1
    if deceMin==10:
       deceMin=0
                                     
def ConcatenacionTiempo(decMin ,uniMin ,decSeg ,uniSeg ,cenSeg):  
    timeText=''
    timeText+=str(decMin)+str(uniMin)+":"+str(decSeg)+str(uniSeg)+":"+str(cenSeg)
    return timeText
#------------------------------------------------------------------------------------------------------------------------------------------------
class Personaje(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    nivel = None
    nivel2 = None 
    posicion = None
    def __init__( self ):
        pygame.sprite.Sprite.__init__( self )
        self.Avanzar = pygame.image.load('PersonajeAvanzar.png').convert_alpha() 
        self.Retroceder = pygame.image.load('PersonajeRetroceder.png').convert_alpha() 
        self.InvencibleAvanzar = pygame.image.load('PersonajeInvencibleAvanzar.png').convert_alpha()
        self.InvencibleRetroceder = pygame.image.load('PersonajeInvencibleRetroceder.png').convert_alpha() 

        self.PersonajeAvanzar = {}
        self.PersonajeAvanzar[0] = (631, 0, 76, 116) #Agacharse
        self.PersonajeAvanzar[1] = (514, 0, 117, 116) #Saltar
        self.PersonajeAvanzar[2] = (400, 0, 111, 116) #Quieto
        self.PersonajeAvanzar[3] = (0, 0, 128, 116)
        self.PersonajeAvanzar[4] = (128, 0, 80, 116)
        self.PersonajeAvanzar[5] = (209, 0, 112, 116)
        self.PersonajeAvanzar[6] = (320, 0, 79, 116)

        self.PersonajeRetroceder = {}
        self.PersonajeRetroceder[0] = (0, 0, 76, 116) #Agacharse
        self.PersonajeRetroceder[1] = (76, 0, 117, 116) #Saltar
        self.PersonajeRetroceder[2] = (195, 0, 113, 116) #Quieto
        self.PersonajeRetroceder[3] = (578, 0, 129, 116)
        self.PersonajeRetroceder[4] = (496, 0, 81, 116) 
        self.PersonajeRetroceder[5] = (386, 0, 112, 116) 
        self.PersonajeRetroceder[6] = (308, 0, 79, 116)

        self.PersonajeInvencibleAvanzar = {}
        self.PersonajeInvencibleAvanzar[0] = (631, 0, 76, 116) #Agacharse
        self.PersonajeInvencibleAvanzar[1] = (514, 0, 117, 116) #Saltar
        self.PersonajeInvencibleAvanzar[2] = (400, 0, 111, 116) #Quieto
        self.PersonajeInvencibleAvanzar[3] = (0, 0, 128, 116)
        self.PersonajeInvencibleAvanzar[4] = (128, 0, 80, 116)
        self.PersonajeInvencibleAvanzar[5] = (209, 0, 112, 116)
        self.PersonajeInvencibleAvanzar[6] = (320, 0, 79, 116)

        self.PersonajeInvencibleRetroceder = {}
        self.PersonajeInvencibleRetroceder[0] = (0, 0, 76, 116) #Agacharse
        self.PersonajeInvencibleRetroceder[1] = (76, 0, 117, 116) #Saltar
        self.PersonajeInvencibleRetroceder[2] = (195, 0, 113, 116) #Quieto
        self.PersonajeInvencibleRetroceder[3] = (578, 0, 129, 116)
        self.PersonajeInvencibleRetroceder[4] = (496, 0, 81, 116) 
        self.PersonajeInvencibleRetroceder[5] = (386, 0, 112, 116) 
        self.PersonajeInvencibleRetroceder[6] = (308, 0, 79, 116)

        self.cual = 2
        self.cuanto = 100
        self.tiempo = 0
        self.izquierda = False
        self.DibujoInvencible = False
        self.ObtenerDibujoPersonaje()
        self.rect = self.image.get_rect()

    def ObtenerDibujoPersonaje(self):
        if self.izquierda == True:
           if self.DibujoInvencible == True:
              self.image=self.InvencibleRetroceder.subsurface(self.PersonajeInvencibleRetroceder[self.cual])
           else:
              self.image=self.Retroceder.subsurface(self.PersonajeRetroceder[self.cual])
        if self.izquierda == False:
           if self.DibujoInvencible == True:
              self.image=self.InvencibleAvanzar.subsurface(self.PersonajeInvencibleAvanzar[self.cual])
           else:
              self.image=self.Avanzar.subsurface(self.PersonajeAvanzar[self.cual])
      
    def update(self): 
        if self.cual > 6:
           self.cual = 3
        self.ObtenerDibujoPersonaje()
        self.Gravedad()

        self.rect.x += self.cambio_x
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        for bloque in ImpactosBloques:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right

        self.rect.y += self.cambio_y
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False) 
        for bloque in ImpactosBloques:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top + 7
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0

   
    def Gravedad(self):
        if self.cambio_y == 0:
           self.cambio_y = 1
        else:
           self.cambio_y += .35
        if self.rect.y >= BASE_PERSONAJE - self.rect.height and self.cambio_y >= 0:
           self.cambio_y = 0
           self.rect.y = BASE_PERSONAJE - self.rect.height

    def Saltar(self):
        self.rect.y += 2
        ImpactosPlataformasY = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        self.rect.y -= 2
        if len(ImpactosPlataformasY) > 0 or self.rect.bottom >= BASE_PERSONAJE:
            self.cambio_y = -12

    def SaltarMismoPunto(self):
        self.cambio_x = 0

    def AvanzarIzquierda(self):
        self.cambio_x = -5

    def AvanzarDerecha(self):
        self.cambio_x = +5

    def Detenerse(self):
        self.cambio_x = 0

    def Agacharse(self):
        self.cambio_x = 0     
#------------------------------------------------------------------------------------------------------------------------------------------------
class DisparoDerecha( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('BalaDerecha.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((15,0))
        if self.rect.left >= ANCHO or EliminarDisparo == True:
           self.kill()

class DisparoIzquierda( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('BalaIzquierda.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((-15,0))
        if self.rect.right <= 0 or EliminarDisparo == True:
           self.kill() 
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('FondoNivel1.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)

    def update( self ):
        if scroll:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado2( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('FondoNivel2.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)
        self.scroll2 = False

    def update( self ):
        if self.scroll2 == True:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
        if scroll:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)

#------------------------------------------------------------------------------------------------------------------------------------------------
class Plataforma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('PlataformaNivel1.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class Plataforma2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('PlataformaNivel222.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)                 
                 
class PlataformasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas = pygame.sprite.Group()
        nivel = [[800, 260],
                 [850, 510],
                 [1200, 340],
                 [1800, 500],
                 [2800, 500],
                 [3000, 350],
                 [3200, 200],
                 [3500, 500],
                 [3600, 200],
                 [4000, 300],
                 [4200, 500],
                 [4700, 300],
                 [4800, 500],
                 [5500, 200],
                 [5100, 350]
                   ]
        for plataforma in nivel:
            bloque = Plataforma()
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            self.ListaPlataformas.add(bloque) 

    def update(self):
        self.ListaPlataformas.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas.draw(pantalla)      
#------------------------------------------------------------------------------------------------------------------------------------------------
                 
class PlataformasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas = pygame.sprite.Group()
        nivel = [[800, 280],[3200,295],[4400,300],[3400,120],
                 [1000, 510],[1200, 280],[3600,295],[4000, 300],
                 [1400, 510],[2000, 280],
                 [1600, 510],[2200, 280],
                 [1800,510],[2400, 280],
                 [3000,510],[2600,280],
                 [3800,510],[2800,280],
                 [4500,510],
                 ]

        for plataforma in nivel:
            bloque = Plataforma2()
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            self.ListaPlataformas.add(bloque) 

    def update(self):
        self.ListaPlataformas.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas.draw(pantalla)      
         
#------------------------------------------------------------------------------------------------------------------------------------------------
class Monedas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenCompleta = imagen
        cual=0
        self.AnimacionMoneda=[]
        while cual < 7:
            self.AnimacionMoneda.append(self.ImagenCompleta.subsurface((cual*40,0,40,38)))
            cual += 1
        self.animacion= 0
        self.actualizacion = pygame.time.get_ticks()
        self.image = self.AnimacionMoneda[self.animacion]
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
            self.animacion= self.animacion + 1
            if self.animacion > 6:
                self.animacion = 0
            self.image = self.AnimacionMoneda[self.animacion]
            self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MonedasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMonedas = pygame.sprite.Group()
        self.Moneda = pygame.image.load("MonedaAnimada.png")
        self.transparente = self.Moneda.get_at((0,0))
        self.Moneda.set_colorkey(self.transparente)
        posicionmoneda = [[825, 230],
                          [865, 230],
                          [905, 230],
                          [945, 230],
                          [845, 190],
                          [885, 190],
                          [925, 190],
                          [865, 150],
                          [905, 150],
                          [885, 110],

                          [1810, 650],
                          [1850, 650],
                          [1890, 650],
                          [1930, 650],
                          [1970, 650],

                          [2400, 400],
                          [2440, 400],
                          [2480, 400],
                          [2520, 400],
                          [2560, 400],

                          [4225, 465],
                          [4265, 465],
                          [4305, 465],
                          [4345, 465],
                          [4245, 425],
                          [4285, 425],
                          [4325, 425],
                          [4265, 385],
                          [4304, 385],
                          [4285, 345]]
        for recorrido in posicionmoneda:
            moneda = Monedas((recorrido[0],recorrido[1]), self.Moneda)
            self.ListaMonedas.add(moneda) 

    def update(self):
        self.ListaMonedas.update()
     
    def draw(self, pantalla):
        self.ListaMonedas.draw(pantalla)  
#------------------------------------------------------------------------------------------------------------------------------------------------
class Zombies(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Zombie1 = pygame.image.load("EnemigoZombie.png").convert_alpha()
        self.Zombie2 = pygame.transform.flip(self.Zombie1, True, False)
      

        self.zombie1 = {}
        self.zombie1[0] = (0, 0, 60, 86)
        self.zombie1[1] = (60, 0, 80, 86)
        self.zombie1[2] = (140, 0, 70, 86)
        self.zombie1[3] = (210, 0, 70, 86)
        self.zombie1[4] = (280, 0, 70, 86)
        self.zombie1[5] = (350, 0, 80, 86)
        self.zombie1[6] = (430, 0, 70, 86)
        self.zombie1[7] = (500, 0, 60, 86)

        self.zombie2 = {}
        self.zombie2[0] = (500, 0, 60, 86)
        self.zombie2[1] = (430, 0, 70, 86)
        self.zombie2[2] = (350, 0, 80, 86)
        self.zombie2[3] = (280, 0, 70, 86)
        self.zombie2[4] = (210, 0, 70, 86)
        self.zombie2[5] = (140, 0, 70, 86)
        self.zombie2[6] = (60, 0, 80, 86)
        self.zombie2[7] = (0, 0, 60, 86)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Zombie2.subsurface(self.zombie2[self.cual])
        else:
            self.image=self.Zombie1.subsurface(self.zombie1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 7:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)
        
class ZombiesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaZombies = pygame.sprite.Group()

        posicionzombie = [[1270, 260],
                          [915, 430],
                          [1500, 620],
                          [1600, 620],
                          [1700, 620],
                          [2200, 620],
                          [3900, 620],
                          [5200, 610],
                          [5050, 610],
                          [4850, 610]]
        for recorrido in posicionzombie:
            zombie = Zombies(recorrido[0],recorrido[1])
            self.ListaZombies.add(zombie) 

    def update(self):
        self.ListaZombies.update()
     
    def draw(self, pantalla):
        self.ListaZombies.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Fantasmas(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Fantasma1 = pygame.image.load("EnemigoFantasma.png").convert_alpha()
        self.Fantasma2 = pygame.transform.flip(self.Fantasma1, True, False)
        
        self.fantasma1 = {}
        self.fantasma1[0] = (0, 0, 70, 87)
        self.fantasma1[1] = (70, 0, 70, 87)
        self.fantasma1[2] = (140, 0, 70, 87)

        self.fantasma2 = {}
        self.fantasma2[0] = (140, 0, 70, 87)
        self.fantasma2[1] = (70, 0, 70, 87)
        self.fantasma2[2] = (0, 0, 70, 87)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.Fantasma2.subsurface(self.fantasma2[self.cual])
        else:
           self.image=self.Fantasma1.subsurface(self.fantasma1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 2:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class FantasmasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaFantasmas = pygame.sprite.Group()

        posicionfantasma = [[1530, 610],
                            [1750, 620],
                            [1870, 415],
                            [2700, 610],
                            [3280, 120],
                            [5150, 610],
                            [5000, 610],
                            [4800, 610]
                            ]
        for recorrido in posicionfantasma:
            fantasma = Fantasmas(recorrido[0],recorrido[1])
            self.ListaFantasmas.add(fantasma) 

    def update(self):
        self.ListaFantasmas.update()
     
    def draw(self, pantalla):
        self.ListaFantasmas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#JEFE NIVEL 1
class Dragones(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Dragon1 = pygame.image.load("EnemigoDragon.png").convert_alpha()
        self.Dragon2 = pygame.transform.flip(self.Dragon1, True, False)
        
        self.dragon1 = {}
        self.dragon1[0] = (0, 0, 100, 96)
        self.dragon1[1] = (100, 0, 100, 96)
        self.dragon1[2] = (200, 0, 100, 96)
        self.dragon1[3] = (300, 0, 100, 96)

        self.dragon2 = {}
        self.dragon2[0] = (300, 0, 100, 96)
        self.dragon2[1] = (200, 0, 100, 96)
        self.dragon2[2] = (100, 0, 100, 96)
        self.dragon2[3] = (0, 0, 100, 96)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Dragon2.subsurface(self.dragon2[self.cual])
        else:
            self.image=self.Dragon1.subsurface(self.dragon1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 3:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class DragonesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaDragones = pygame.sprite.Group()

        posiciondragon = [[5150, 260]]
        for recorrido in posiciondragon:
            dragon = Dragones(recorrido[0],recorrido[1])
            self.ListaDragones.add(dragon) 

    def update(self):
        self.ListaDragones.update()
     
    def draw(self, pantalla):
        self.ListaDragones.draw(pantalla) 


#nivel 2

class Dragones2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Dragon1 = pygame.image.load("EnemigoDragon3.png").convert_alpha()
        self.Dragon2 = pygame.transform.flip(self.Dragon1, True, False)
        
        self.dragon1 = {}
        self.dragon1[0] = (0, 0, 100, 96)
        self.dragon1[1] = (100, 0, 100, 96)
        self.dragon1[2] = (200, 0, 100, 96)
        self.dragon1[3] = (300, 0, 100, 96)

        self.dragon2 = {}
        self.dragon2[0] = (300, 0, 100, 96)
        self.dragon2[1] = (200, 0, 100, 96)
        self.dragon2[2] = (100, 0, 100, 96)
        self.dragon2[3] = (0, 0, 100, 96)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Dragon2.subsurface(self.dragon2[self.cual])
        else:
            self.image=self.Dragon1.subsurface(self.dragon1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 3:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)


#JEFE NIVEL 2
class DragonesNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaDragones = pygame.sprite.Group()

        posiciondragon2 = [[5400, 610]
                          ]
        for recorrido in posiciondragon2:
            dragon = Dragones2(recorrido[0],recorrido[1])
            self.ListaDragones.add(dragon) 

    def update(self):
        self.ListaDragones.update()
     
    def draw(self, pantalla):
        self.ListaDragones.draw(pantalla) 


class Zombies2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Zombie1 = pygame.image.load("EnemigoZombie2.png").convert_alpha()
        self.Zombie2 = pygame.transform.flip(self.Zombie1, True, False)
        
        self.zombie1 = {}
        self.zombie1[0] = (0, 0, 60, 86)
        self.zombie1[1] = (60, 0, 80, 86)
        self.zombie1[2] = (140, 0, 70, 86)
        self.zombie1[3] = (210, 0, 70, 86)
        self.zombie1[4] = (280, 0, 70, 86)
        self.zombie1[5] = (350, 0, 80, 86)
        self.zombie1[6] = (430, 0, 70, 86)
        self.zombie1[7] = (500, 0, 60, 86)

        self.zombie2 = {}
        self.zombie2[0] = (500, 0, 60, 86)
        self.zombie2[1] = (430, 0, 70, 86)
        self.zombie2[2] = (350, 0, 80, 86)
        self.zombie2[3] = (280, 0, 70, 86)
        self.zombie2[4] = (210, 0, 70, 86)
        self.zombie2[5] = (140, 0, 70, 86)
        self.zombie2[6] = (60, 0, 80, 86)
        self.zombie2[7] = (0, 0, 60, 86)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Zombie2.subsurface(self.zombie2[self.cual])
        else:
            self.image=self.Zombie1.subsurface(self.zombie1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 7:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)
        
class ZombiesNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaZombies = pygame.sprite.Group()

        posicionzombie2 = [ [800, 620],[900, 620],[1000, 620],[1100, 620],
                            [1200, 620],[1300, 620],[1400, 620],[1500, 620],
                            [1420,435],[1820,435],[2500, 620],[2600, 620],
                            [2700, 620],[2800, 620],[2900, 620],[3000, 620],
                            [2220,200],[2620,200],[3220,220],

                            [3500, 620],[4000, 620],
                            [4100, 620],[4200, 620],[4300, 620],[4500, 620],
                            [4800,620],[4900,620],[5000,620],[5100,620]
                           ]
        for recorrido in posicionzombie2:
            zombie = Zombies2(recorrido[0],recorrido[1])
            self.ListaZombies.add(zombie) 

    def update(self):
        self.ListaZombies.update()
     
    def draw(self, pantalla):
        self.ListaZombies.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Fantasmas2(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Fantasma1 = pygame.image.load("EnemigoFantasma2.png").convert_alpha()
        self.Fantasma2 = pygame.transform.flip(self.Fantasma1, True, False)
        
        self.fantasma1 = {}
        self.fantasma1[0] = (0, 0, 70, 87)
        self.fantasma1[1] = (70, 0, 70, 87)
        self.fantasma1[2] = (140, 0, 70, 87)

        self.fantasma2 = {}
        self.fantasma2[0] = (140, 0, 70, 87)
        self.fantasma2[1] = (70, 0, 70, 87)
        self.fantasma2[2] = (0, 0, 70, 87)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.Fantasma2.subsurface(self.fantasma2[self.cual])
        else:
           self.image=self.Fantasma1.subsurface(self.fantasma1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 2:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class FantasmasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaFantasmas = pygame.sprite.Group()

        posicionfantasma2 = [[850, 620],[950, 620],[1050, 620],[1150, 620],
                            [1250, 620],[1350, 620],[1450, 620],[1550, 620],
                            [1220,200],[1620,435],[2550, 620],[2650, 620],
                            [2750, 620],[2850, 620],[2950, 620],[3050, 620],
                            [2420,200],[2820,200],

                            [3550, 620],[4050, 620],
                            [4150, 620],[4250, 620],[4350, 620],[4550, 620],
                            [4850,620],[4950,620],[5050,620],[5150,620]

                            ]
        for recorrido in posicionfantasma2:
            fantasma = Fantasmas2(recorrido[0],recorrido[1])
            self.ListaFantasmas.add(fantasma) 

    def update(self):
        self.ListaFantasmas.update()
     
    def draw(self, pantalla):
        self.ListaFantasmas.draw(pantalla)
#------------------------------------------------------------------------------------------------------------------------------------------------
class Vidas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Vidas.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class VidasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaVidas = pygame.sprite.Group()
        self.Vida = pygame.image.load("Vidas.png")
        self.transparente = self.Vida.get_at((0,0))
        self.Vida.set_colorkey(self.transparente)
        posicionvida = [[1270, 100],
                        [3690, 100],
                        [2999, 300],
                        [4000, 100],
                        [5000, 100]
                        ]
        for recorrido in posicionvida:
            vida = Vidas((recorrido[0],recorrido[1]), self.Vida)
            self.ListaVidas.add(vida) 

    def update(self):
        self.ListaVidas.update()
     
    def draw(self, pantalla):
        self.ListaVidas.draw(pantalla) 

class VidasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaVidas = pygame.sprite.Group()
        self.Vida = pygame.image.load("Vidas.png")
        self.transparente = self.Vida.get_at((0,0))
        self.Vida.set_colorkey(self.transparente)
        posicionvida = [[800, 200],
                        [1200, 190],
                        [3500, 100],
                        [2000, 190],
                        [2800, 190],
                        ]
        for recorrido in posicionvida:
            vida = Vidas((recorrido[0],recorrido[1]), self.Vida)
            self.ListaVidas.add(vida) 

    def update(self):
        self.ListaVidas.update()
     
    def draw(self, pantalla):
        self.ListaVidas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Balas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Balas.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class BalasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBalas = pygame.sprite.Group()
        self.Bala = pygame.image.load("Balas.png")
        self.transparente = self.Bala.get_at((0,0))
        self.Bala.set_colorkey(self.transparente)
        posicionbala = [[1870, 250],
                        [3490, 400],
                        ]
        for recorrido in posicionbala:
            bala = Balas((recorrido[0],recorrido[1]), self.Bala)
            self.ListaBalas.add(bala) 

    def update(self):
        self.ListaBalas.update()
     
    def draw(self, pantalla):
        self.ListaBalas.draw(pantalla) 

class BalasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBalas = pygame.sprite.Group()
        self.Bala = pygame.image.load("Balas.png")
        self.transparente = self.Bala.get_at((0,0))
        self.Bala.set_colorkey(self.transparente)
        posicionbala = [[1870, 200],
                        [3490, 400],
                        [3000, 500],
                        [900,500],
                        [1000,200],
                        [4400,200]
                        ]
        for recorrido in posicionbala:
            bala = Balas((recorrido[0],recorrido[1]), self.Bala)
            self.ListaBalas.add(bala) 

    def update(self):
        self.ListaBalas.update()
     
    def draw(self, pantalla):
        self.ListaBalas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Invencibles(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Invencible1.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class InvenciblesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaInvencibles = pygame.sprite.Group()
        self.Invencible = pygame.image.load("Invencible.png")
        self.transparente = self.Invencible.get_at((0,0))
        self.Invencible.set_colorkey(self.transparente)
        posicioninvencible = [[3290, 100],[2800, 550]]
        for recorrido in posicioninvencible:
            invencible = Invencibles((recorrido[0],recorrido[1]), self.Invencible)
            self.ListaInvencibles.add(invencible) 

    def update(self):
        self.ListaInvencibles.update()
     
    def draw(self, pantalla):
        self.ListaInvencibles.draw(pantalla)

#------------------------------------------------------------------------------------------------------------------------------------------------
class Meta(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Meta.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MetaNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMeta = pygame.sprite.Group()
        self.Meta = pygame.image.load("Meta.png")
        self.transparente = self.Meta.get_at((0,0))
        self.Meta.set_colorkey(self.transparente)
        posicionmeta = [[600,600],[5600, 150]]
        for recorrido in posicionmeta:
            meta = Meta((recorrido[0],recorrido[1]), self.Meta)
            self.ListaMeta.add(meta) 

    def update(self):
        self.ListaMeta.update()
     
    def draw(self, pantalla):
        self.ListaMeta.draw(pantalla) 

class MetaNivel2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMeta = pygame.sprite.Group()
        self.Meta = pygame.image.load("Metaf.png")
        self.transparente = self.Meta.get_at((0,0))
        self.Meta.set_colorkey(self.transparente)
        posicionmeta = [[5600, 610]]
        for recorrido in posicionmeta:
            meta = Meta((recorrido[0],recorrido[1]), self.Meta)
            self.ListaMeta.add(meta) 

    def update(self):
        self.ListaMeta.update()
     
    def draw(self, pantalla):
        self.ListaMeta.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Sounds():
    def __init__(self):
       self.OpcionMenu = pygame.mixer.Sound(os.path.join("OpcionMenu.wav"))
       self.OpcionMenu.set_volume(1)
       self.EnterMenu = pygame.mixer.Sound(os.path.join("EnterMenu.wav"))
       self.EnterMenu.set_volume(1)
       self.Pausa = pygame.mixer.Sound(os.path.join("Pausa.wav"))
       self.Pausa.set_volume(1)
       self.Salto = pygame.mixer.Sound(os.path.join("Saltar.wav"))
       self.Salto.set_volume(0.2)
       self.Disparo = pygame.mixer.Sound(os.path.join("Disparar.wav"))
       self.Disparo.set_volume(0.8)
       self.Destruido = pygame.mixer.Sound(os.path.join("Destruido.wav"))
       self.Destruido.set_volume(1)
       self.VidaMenos = pygame.mixer.Sound(os.path.join("VidaMenos.wav"))
       self.VidaMenos.set_volume(1)
       self.GameOver = pygame.mixer.Sound(os.path.join("GameOver.wav"))
       self.GameOver.set_volume(1)
       self.MasVida = pygame.mixer.Sound(os.path.join("VidaMas.wav"))
       self.MasVida.set_volume(1)
       self.MasMoneda = pygame.mixer.Sound(os.path.join("Moneda.wav"))
       self.MasMoneda.set_volume(1)
       self.MasBala = pygame.mixer.Sound(os.path.join("Balas.wav"))
       self.MasBala.set_volume(1)
       self.MasVelocidad = pygame.mixer.Sound(os.path.join("Velocidad.wav"))
       self.MasVelocidad.set_volume(1)
       self.Invencible = pygame.mixer.Sound(os.path.join("Invencible.wav"))
       self.Invencible.set_volume(1)
       self.MusicaInvencible = pygame.mixer.Sound(os.path.join("MusicaInvencible.wav"))
       self.MusicaInvencible.set_volume(1)
       self.Meta = pygame.mixer.Sound(os.path.join("Meta.wav"))
       self.Meta.set_volume(1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#INICIALIZACION DE VARIABLES
pygame.init()
pygame.mixer.init()
#------------------------------------------------------------------------------------------------------------------------------------------------
#COLORES
blanco = (255,255,255)
negro = (0,0,0)
amarillo = (255,255,0)
dorado = (231,174,24)
azulclaro = (0,255,255)
violeta = (204,0,102)
rojo = (255,0,0)
rojooscuro = (190,17,17)
verde = (0,255,0)
azul = (0,0,255)
morado = (153,51,255)
naranja = (255,128,0)
gris = (128,128,128)
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DE LA VENTANA
pantalla = pygame.display.set_mode((ANCHO,ALTO),pygame.FULLSCREEN)
pygame.display.set_caption("PODER CIENTIFICO")
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU
MenuX = 410
MenuY = 478
DimensionMenu = [MenuX,MenuY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU DE PAUSA
MenuPausaX = 410
MenuPausaY = 478
DimensionMenuPausa = [MenuPausaX,MenuPausaY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#IMAGENES Y MUSICA DEL MENU
Seleccion = pygame.image.load('Seleccion.png').convert_alpha()
pygame.mixer.music.load('PiratasDelCaribe.mp3')
pygame.mixer.music.play(-1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#MUSICA Y SONIDOS
sounds = Sounds()
#------------------------------------------------------------------------------------------------------------------------------------------------
#PERSONAJE
personaje = Personaje()
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#TIPOS DE FUENTES TEXTOS
FuenteEstadisticas = pygame.font.Font('Zombified.ttf', 40)
FuenteGameOver = pygame.font.Font('Zombified.ttf', 110)
FuenteMisionCompleta = pygame.font.Font('Zombified.ttf', 80)
FuentePresioneEspacio = pygame.font.Font('Zombified.ttf', 50)
FuentePuntaje = pygame.font.Font('Zombified.ttf', 30)
#------------------------------------------------------------------------------------------------------------------------------------------------
#VARIABLES DE JUEGO
salir = False
scroll = False
FondoDerecha = False
reloj = pygame.time.Clock() 
textoTiempo = TextoTiempo()
EliminarDisparo = False
ReiniciarTiempo = False 
CambioNivel2 = False
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU 
def TextoMenu(texto, posx, posy, negro):
    fuente = pygame.font.Font("bloodcrow.ttf", 35)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU DE PAUSA
def TextoMenuPausa(texto, posx, posy, negro):
    fuente = pygame.font.Font("Zombified.ttf", 60)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
ImagenMoneda = {}
ImagenMoneda[0] = (0, 0, 40, 40)
ImagenMoneda[1] = (40, 0, 40, 40)
ImagenMoneda[2] = (80, 0, 30, 40)
ImagenMoneda[3] = (110, 0, 16 , 40)
ImagenMoneda[4] = (126, 0, 30 , 40)
ImagenMoneda[5] = (156, 0, 38, 40)
ImagenMoneda[6] = (194, 0, 38, 40)
cual1 = 0
cuanto1 = 100
tiempo1 = 0
def IconoAnimadoMonedas():
   global cual1, tiempo1
   if pygame.time.get_ticks()-tiempo1 > cuanto1:
      tiempo1 = pygame.time.get_ticks()
      cual1 = cual1 + 1
      if cual1 > 6:
         cual1 = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
pos4 = -150
tiempo4 = 0
def MovimientoCalavera():
   global pos4, tiempo4
   pos4 = pos4 + 1
   if pos4 > 10:
      pos4 = 10
#------------------------------------------------------------------------------------------------------------------------------------------------
pos5 = -350
tiempo5 = 0
def MovimientoTitulo():
   global pos5, tiempo5
   pos5 = pos5 + 5
   if pos5 > 500:
      pos5 = 500
#------------------------------------------------------------------------------------------------------------------------------------------------
pos6 = -500
tiempo6 = 0
def MovimientoGameOver():
   global pos6, tiempo6
   pos6 = pos6 + 3
   if pos6 > 500:
      pos6 = 500
#------------------------------------------------------------------------------------------------------------------------------------------------
pos7 = -350
tiempo7 = 0
def MovimientoNivel1Completo():
   global pos7, tiempo7
   pos7 = pos7 + 2
   if pos7 > 250:
      pos7 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos8 = 1000
def MovimientoLogoUniversidad():
   global pos8
   pos8 = pos8 - 4
   if pos8 < 250:
      pos8 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos9 = 2200
def MovimientoComputador():
   global pos9
   pos9 = pos9 - 4
   if pos9 < 600:
      pos9 = 600
#------------------------------------------------------------------------------------------------------------------------------------------------
pos10 = 1700
def MovimientoComputacionGrafica():
   global pos10
   pos10 = pos10 - 2
   if pos10 < 670:
      pos10 = 670
#------------------------------------------------------------------------------------------------------------------------------------------------
pos11 = 1900
def MovimientoNombre1():
   global pos11
   pos11 = pos11 - 2
   if pos11 < 660:
      pos11 = 660
#------------------------------------------------------------------------------------------------------------------------------------------------
pos12 = 2000
def MovimientoNombre2():
   global pos12
   pos12 = pos12 - 2
   if pos12 < 710:
      pos12 = 710
#------------------------------------------------------------------------------------------------------------------------------------------------
pos13 = -200
def MovimientoMision1Completa():
   global pos13
   pos13 = pos13 + 2
   if pos13 > 485:
      pos13 = 485
#------------------------------------------------------------------------------------------------------------------------------------------------
pos14 = 1400
def MovimientoPresioneEspacioMeta():
   global pos14
   pos14 = pos14 - 2
   if pos14 < 430:
      pos14 = 430
#------------------------------------------------------------------------------------------------------------------------------------------------
pos15 = 1400
def MovimientoPresioneEspacioGameOver():
   global pos15
   pos15 = pos15 - 2
   if pos15 < 400:
      pos15 = 400
#------------------------------------------------------------------------------------------------------------------------------------------------
#################################################### FUNCION PRINCIPAL DE INICIO DEL JUEGO #################################################### 
#------------------------------------------------------------------------------------------------------------------------------------------------
def IniciarJuego():
    Puntaje = 0
    CantidadVidas = 5
    CantidadBalas = 20
    CantidadMonedas = 0
    #IMAGEN DE FONDO NIVEL 1
    FondoAnimado1 = FondoAnimado(0,0)
    FondoAnimadoGrupo = pygame.sprite.RenderUpdates(FondoAnimado1)
    #IMAGEN DE FONDO NIVEL 2
    FondoAnimadoNivel2 = FondoAnimado2(0,0)
    FondoAnimadoGrupo2 = pygame.sprite.RenderUpdates(FondoAnimadoNivel2)
    #CREACION DE PLATAFORMAS NIVEL 1
    GrupoPlataformas = []
    GrupoPlataformas.append(PlataformasNivel1())
    DibujoPlataformas = GrupoPlataformas[0]
    personaje.nivel = DibujoPlataformas
    #CREACION DE PLATAFORMAS NIVEL 2

    GrupoPlataformas2 = []
    GrupoPlataformas2.append(PlataformasNivel2())
    DibujoPlataformas2 = GrupoPlataformas2[0]
    

    #CREACION DE MONEDAS
    GrupoMonedas = []
    GrupoMonedas.append(MonedasNivel1())
    DibujoMonedas = GrupoMonedas[0]
    personaje.posicionmoneda = DibujoMonedas
    #CREACION DE ZOMBIES
    GrupoZombies = []
    GrupoZombies.append(ZombiesNivel1())
    DibujoZombies = GrupoZombies[0]
    personaje.posicionzombie = DibujoZombies
    #CREACION DE FANTASMAS
    GrupoFantasmas = []
    GrupoFantasmas.append(FantasmasNivel1())
    DibujoFantasmas = GrupoFantasmas[0]
    personaje.posicionfantasma = DibujoFantasmas

    GrupoZombies2 = []
    GrupoZombies2.append(ZombiesNivel2())
    DibujoZombies2 = GrupoZombies2[0]
    personaje.posicionzombie2 = DibujoZombies2
    #CREACION DE FANTASMAS
    GrupoFantasmas2 = []
    GrupoFantasmas2.append(FantasmasNivel2())
    DibujoFantasmas2 = GrupoFantasmas2[0]
    personaje.posicionfantasma2 = DibujoFantasmas2

    #CREACION DE DRAGONES
    GrupoDragones = []
    GrupoDragones.append(DragonesNivel1())
    DibujoDragones = GrupoDragones[0]
    personaje.posiciondragon = DibujoDragones

    GrupoDragones2 = []
    GrupoDragones2.append(DragonesNivel2())
    DibujoDragones2 = GrupoDragones2[0]
    personaje.posiciondragon2 = DibujoDragones2
    #CREACION DE MODIFICADOR VIDAS
    GrupoVidas = []
    GrupoVidas.append(VidasNivel1())
    DibujoVidas = GrupoVidas[0]
    personaje.posicionvida = DibujoVidas

    GrupoVidas2 = []
    GrupoVidas2.append(VidasNivel2())
    DibujoVidas2 = GrupoVidas2[0]
    
    #CREACION DE MODIFICADOR BALAS
    GrupoBalas = []
    GrupoBalas.append(BalasNivel1())
    DibujoBalas = GrupoBalas[0]
    personaje.posicionbala = DibujoBalas

    GrupoBalas2 = []
    GrupoBalas2.append(BalasNivel2())
    DibujoBalas2 = GrupoBalas2[0]
    #CREACION DE MODIFICADOR INVENCIBLE
    GrupoInvencibles = []
    GrupoInvencibles.append(InvenciblesNivel1())
    DibujoInvencibles = GrupoInvencibles[0]
    personaje.posicioninvencible = DibujoInvencibles

    #CREACION DE META
    j=1
    GrupoMeta = []
    GrupoMeta.append(MetaNivel1())
    DibujoMeta = GrupoMeta[0]
    personaje.posicionmeta = DibujoMeta

    GrupoMeta2 = []
    GrupoMeta2.append(MetaNivel2())
    DibujoMeta2 = GrupoMeta2[0]
    
    #ICONOS DE OBJETOS
    IconoVidas = pygame.image.load('Vidas.png').convert_alpha()
    IconoBalas = pygame.image.load('Balas.png').convert_alpha()
    IconoMoneda = pygame.image.load('IconoMonedaAnimada.png').convert_alpha()
    IconoReloj = pygame.image.load('Reloj.png').convert_alpha()
    MonedaInstrucciones = pygame.image.load('Moneda.png').convert_alpha()
    #PERSONAJE
    PersonajeGrupo = pygame.sprite.RenderUpdates(personaje)
    personaje.rect.x = 50
    personaje.rect.y = BASE_PERSONAJE
    ListaSpritesActivos = pygame.sprite.Group()
    ListaSpritesActivos.add(personaje)
    #DISPAROS
    DisparosGrupo = pygame.sprite.RenderUpdates()
#------------------------------------------------------------------------------------------------------------------------------------------------
    pygame.event.clear
    os.system('clear')
    salir = False
    FinGameOver = False
    FinMeta = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load('MisionImposible.mp3')
    pygame.mixer.music.play(-1)

    FondoGameOver = pygame.image.load('FondoGameOver.png').convert_alpha() 
    EsqueletoGameOver = pygame.image.load('EsqueletoGameOver.png').convert_alpha()
    FondoMensajeMeta = pygame.image.load('FondoMensajeMeta.png').convert_alpha() 
    PersonajeMeta = pygame.image.load('PersonajeMeta.png').convert_alpha() 
    CalaveraMeta = pygame.image.load('CalaveraMeta.png').convert_alpha() 

    TextoGameOver = FuenteGameOver.render("GAME OVER", 1, (negro))
    TextoMision1Completa = FuenteMisionCompleta.render("MUY BIEN, AHORA LA OLEADA FINAL??", 1, (blanco))
    TextoMision1Completaf = FuenteMisionCompleta.render("GANASTE????", 1, (blanco))
    TextoPresioneEspacioMeta = FuentePresioneEspacio.render("PRESIONE ESPACIO PARA CONTINUAR", 1, (amarillo))
    TextoPresioneEspacioGameOver = FuentePresioneEspacio.render("PRESIONE ESPACIO PARA CONTINUAR", 1, (azulclaro))

    Mas100Puntos = FuentePuntaje.render("+100", 1, (blanco))

    global event, scroll, FondoDerecha, EliminarDisparo, MenuPausaY, DimensionMenuPausa
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, PausaTiempo, CambioNivel2 
    while salir != True: 
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()
       for event in pygame.event.get():   
           if event.type == pygame.QUIT:
              salir = True
           if tecla[pygame.K_s]:
              sys.exit()
           if tecla[pygame.K_SPACE]:
                print "Disparar"
                scroll = False
                if CantidadBalas == 0 or CantidadVidas == 0 or FinMeta == True:
                   CantidadBalas = CantidadBalas
                else:
                   sounds.Disparo.play()
                   CantidadBalas -= 1
                   if personaje.izquierda == True:
                      DisparosGrupo.add(DisparoIzquierda(personaje.rect.left-30, personaje.rect.y+20))
                   if personaje.izquierda == False:
                      DisparosGrupo.add(DisparoDerecha(personaje.rect.right-30, personaje.rect.y+20))
#------------------------------------------------------------------------------------------------------------------------------------------------   
       if event.type == pygame.KEYDOWN:

          if tecla[pygame.K_RIGHT]:
             personaje.izquierda = False
             if CambioNivel2 == True:

                FondoDerecha = True
                if CantidadVidas == 0 or FinMeta == True:
                   FondoAnimado2.scroll2 = False
                   scroll=False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x >= 680:
                      FondoAnimado2.scroll2 = True
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x < 680:    
                      FondoAnimado2.scroll2 = False
                      scroll = False
                      personaje.AvanzarDerecha()

                
             else:
                FondoDerecha = True
                if CantidadVidas == 0 or FinMeta == True:
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x >= 680:
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x < 680:    
                      scroll = False
                      personaje.AvanzarDerecha()

          if tecla[pygame.K_LEFT]:
             personaje.izquierda = True
             if CambioNivel2 == True:
                FondoDerecha = False
                if CantidadVidas == 0 or FinMeta == True:
                   FondoAnimado2.scroll2 = False
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x <= 680:
                      FondoAnimado2.scroll2 = True
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x > 680:    
                      FondoAnimado2.scroll2 = False
                      scroll = False
                      personaje.AvanzarIzquierda()

             else:
                FondoDerecha = False
                if CantidadVidas == 0 or FinMeta == True:
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x <= 680:
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x > 680:    
                      scroll = False
                      personaje.AvanzarIzquierda()

          if tecla[pygame.K_UP]:
             FondoAnimado2.scroll2 = True
             sounds.Salto.play()
             personaje.Saltar()
             personaje.cual = 1


          if tecla[pygame.K_DOWN]:
             scroll = False
             personaje.Agacharse()
             personaje.cual = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
          if tecla[pygame.K_ESCAPE]:
             if FinMeta == True or FinGameOver == True:
                Pausa = False
             else:
                Pausa = True
                OpcionMenuPausa = 1
                pygame.mixer.music.pause()
                sounds.Pausa.play(-1)
                while Pausa:
                   reloj.tick(60) 
                   tecla = pygame.key.get_pressed()
                   for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                         pygame.quit()
                      if tecla[pygame.K_UP] and OpcionMenuPausa > 1 and MenuPausaY > DimensionMenuPausa[1]:
                         sounds.OpcionMenu.play()
                         OpcionMenuPausa -= 1
                         MenuPausaY = MenuPausaY-40
                      if tecla[pygame.K_DOWN] and OpcionMenuPausa < 3 and MenuPausaY > DimensionMenuPausa[0]:
                         sounds.OpcionMenu.play()
                         OpcionMenuPausa += 1
                         MenuPausaY = MenuPausaY+40
                      if tecla[K_RETURN]:
	                 if OpcionMenuPausa == 1:
	                    print "REANUDAR JUEGO"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
                            Pausa = False
                            pygame.mixer.music.unpause()
	                 if OpcionMenuPausa == 2:
                            print "VOLVER AL MENU PRINCIPAL"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
	                    salir = True
                            Pausa = False
                            pygame.mixer.music.load('PiratasDelCaribe.mp3')
                            pygame.mixer.music.play(-1)
                            Menu(opcion)
	                 if OpcionMenuPausa == 3:
                            sounds.EnterMenu.play()
                            sys.exit()
                   MenuPausa(OpcionMenuPausa)
                   pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------                   
       if event.type == pygame.KEYUP:
          personaje.cual = 2

          if tecla[pygame.K_RIGHT]:
             personaje.Detenerse()
             scroll = False

          if tecla[pygame.K_LEFT]:
             personaje.Detenerse()
             scroll = False
#------------------------------------------------------------------------------------------------------------------------------------------------
       Puntos = FuenteEstadisticas.render("Puntaje = " + str(Puntaje), True, verde)

       ColisionBalasZombies = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionzombie.ListaZombies, True, True)
       for zombie in ColisionBalasZombies:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          zombie.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasFantasmas = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionfantasma.ListaFantasmas, True, True)
       for fantasma in ColisionBalasFantasmas:
          print "+200 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          fantasma.kill()
          Puntaje += 200

       ColisionBalasFantasmas2 = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionfantasma2.ListaFantasmas, True, True)
       for fantasma in ColisionBalasFantasmas2:
          print "+200 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          fantasma.kill()
          Puntaje += 200

       ColisionBalasZombies2 = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionzombie2.ListaZombies, True, True)
       for zombie in ColisionBalasZombies2:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          zombie.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasDragones = pygame.sprite.groupcollide(DisparosGrupo, personaje.posiciondragon.ListaDragones, True, True)
       for dragon in ColisionBalasDragones:
          print "+300 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          dragon.kill()
          Puntaje += 300

       ColisionBalasDragones2 = pygame.sprite.groupcollide(DisparosGrupo, personaje.posiciondragon2.ListaDragones, True, True)
       for dragon in ColisionBalasDragones2:
          print "+300 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          dragon.kill()
          Puntaje += 300
#------------------------------------------------------------------------------------------------------------------------------------------------
       Vidas = FuenteEstadisticas.render("Vidas = " + str(CantidadVidas), True, rojooscuro)

       ColisionModificableVidas = pygame.sprite.spritecollide(personaje, personaje.posicionvida.ListaVidas, False)
       for vida in ColisionModificableVidas:
          print "+1 Vida"
          sounds.Salto.stop()
          sounds.MasVida.play()
          vida.kill()
          CantidadVidas += 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "+100 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             zombie.kill()
             Puntaje += 100

       else:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                zombie.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                zombie.kill()

       if personaje.DibujoInvencible==True:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie2.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "+100 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             zombie.kill()
             Puntaje += 100

       else:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie2.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                zombie.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                zombie.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "+200 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             fantasma.kill()
             Puntaje += 200

       else:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                fantasma.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                fantasma.kill()

       if personaje.DibujoInvencible==True:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma2.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "+200 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             fantasma.kill()
             Puntaje += 200

       else:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma2.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                fantasma.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                fantasma.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeDragon = pygame.sprite.spritecollide(personaje, personaje.posiciondragon.ListaDragones, False)
          for dragon in ColisionPersonajeDragon:
             print "+300 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             dragon.kill()
             Puntaje += 300

       else:
          ColisionPersonajeDragon = pygame.sprite.spritecollide(personaje, personaje.posiciondragon.ListaDragones, False)
          for dragon in ColisionPersonajeDragon:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                dragon.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                dragon.kill()


       if personaje.DibujoInvencible==True:
          ColisionPersonajeDragon2 = pygame.sprite.spritecollide(personaje, personaje.posiciondragon2.ListaDragones, False)
          for dragon in ColisionPersonajeDragon2:
             print "+300 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             dragon.kill()
             Puntaje += 300

       else:
          ColisionPersonajeDragon2 = pygame.sprite.spritecollide(personaje, personaje.posiciondragon2.ListaDragones, False)
          for dragon in ColisionPersonajeDragon2:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                dragon.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                dragon.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Balas = FuenteEstadisticas.render("Monos = " + str(CantidadBalas), True, gris)
       ColisionModificableBalas = pygame.sprite.spritecollide(personaje, personaje.posicionbala.ListaBalas, False)
       for bala in ColisionModificableBalas:
          print "+5 Balas"
          sounds.Salto.stop()
          sounds.MasBala.play()
          bala.kill()
          CantidadBalas += 5
#------------------------------------------------------------------------------------------------------------------------------------------------
       Monedas = FuenteEstadisticas.render("Energia= " + str(CantidadMonedas), True, dorado)
       ColisionMonedas = pygame.sprite.spritecollide(personaje, personaje.posicionmoneda.ListaMonedas, False)
       for moneda in ColisionMonedas:
          print "+1 Moneda"
          sounds.Salto.stop()
          sounds.MasMoneda.play()
          moneda.kill()
          CantidadMonedas += 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionModificableInvencibles = pygame.sprite.spritecollide(personaje, personaje.posicioninvencible.ListaInvencibles, False)
       for invencible in ColisionModificableInvencibles:
          print "Invencible"
          sounds.Salto.stop()
          sounds.Invencible.play()
          invencible.kill()
          personaje.DibujoInvencible = True
          sounds.MusicaInvencible.play()

       if personaje.DibujoInvencible==True:
          pygame.mixer.music.pause()
          sounds.Salto.stop()
          tiempo=pygame.time.get_ticks()/4000
          if tiempo == 12:
            personaje.DibujoInvencible=False
            sounds.MusicaInvencible.stop()
            pygame.mixer.music.unpause()
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionMeta = pygame.sprite.spritecollide(personaje, personaje.posicionmeta.ListaMeta, False)
       for meta in ColisionMeta:
          print "META, FIN DE NIVEL"
          FinMeta = True
          personaje.kill()
          meta.kill()
          EliminarDisparo = True
          PausaTiempo = True
          sounds.Meta.play()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Tiempo = FuenteEstadisticas.render("Tiempo = ", True, blanco)

       if CambioNivel2 == True:
          j=2
          personaje.nivel = DibujoPlataformas2
          personaje.posicionmeta = DibujoMeta2
          personaje.posicionvida = DibujoVidas2
          personaje.posicionbala = DibujoBalas2
          ListaSpritesActivos.add(personaje)
          FondoAnimadoGrupo2.update()
          FondoAnimadoGrupo2.draw(pantalla)
          DibujoPlataformas2.update()
          DibujoPlataformas2.draw(pantalla)
          DibujoZombies2.update()
          DibujoZombies2.draw(pantalla)
          DibujoFantasmas2.update()
          DibujoFantasmas2.draw(pantalla)
          DibujoDragones2.update()
          DibujoDragones2.draw(pantalla)
          DibujoMeta2.update()
          DibujoMeta2.draw(pantalla)
          DibujoVidas2.update()
          DibujoVidas2.draw(pantalla)
          DibujoBalas2.update()
          DibujoBalas2.draw(pantalla)
          DibujoInvencibles.update()
          DibujoInvencibles.draw(pantalla)
          
       else:
          FondoAnimadoGrupo.update()
          FondoAnimadoGrupo.draw(pantalla)
          DibujoPlataformas.update()
          DibujoPlataformas.draw(pantalla)
          DibujoMonedas.update()
          DibujoMonedas.draw(pantalla)
          DibujoZombies.update()
          DibujoZombies.draw(pantalla)
          DibujoFantasmas.update()
          DibujoFantasmas.draw(pantalla)
          DibujoDragones.update()
          DibujoDragones.draw(pantalla)
          DibujoVidas.update()
          DibujoVidas.draw(pantalla)
          DibujoBalas.update()
          DibujoBalas.draw(pantalla)
          DibujoInvencibles.update()
          DibujoInvencibles.draw(pantalla)
          DibujoMeta.update()
          DibujoMeta.draw(pantalla)

       if personaje.rect.right > ANCHO:
          personaje.rect.right = ANCHO
       if personaje.rect.left < 0:
          personaje.rect.left = 0

       ListaSpritesActivos.update()
       ListaSpritesActivos.draw(pantalla)
       DisparosGrupo.update()
       DisparosGrupo.draw(pantalla)

       pantalla.blit(Seleccion,(4,4))
       pantalla.blit(IconoVidas,(300,4))
       pantalla.blit(IconoBalas,(530,4))
       IconoAnimadoMonedas()
       pantalla.blit(IconoMoneda,(810,10),ImagenMoneda[cual1])
       pantalla.blit(IconoReloj,(1085,4))
       pantalla.blit(Puntos,(59,8))
       pantalla.blit(Vidas,(355,8))
       pantalla.blit(Balas,(595,8))
       pantalla.blit(Monedas,(855,8))
       pantalla.blit(Tiempo,(1140,8))

       if FinGameOver == True or CantidadVidas == 0:
          personaje.kill()
          pygame.mixer.music.stop()
          sounds.GameOver.play(-1)
          pantalla.blit(FondoGameOver,(200,100))
          pantalla.blit(EsqueletoGameOver,(800,50))
          MovimientoGameOver()
          pantalla.blit(TextoGameOver,(pos6,280))
          MovimientoPresioneEspacioGameOver()
          pantalla.blit(TextoPresioneEspacioGameOver,(400,pos15))
          if tecla[pygame.K_SPACE]:
             sounds.GameOver.stop()
             pygame.mixer.music.load('PiratasDelCaribe.mp3')
             pygame.mixer.music.play(-1)
             salir = True

       if FinMeta == True:
          pygame.mixer.music.stop()
          pantalla.blit(FondoMensajeMeta,(200,100))
          pantalla.blit(PersonajeMeta,(380,280))
          pantalla.blit(CalaveraMeta,(600,50))
          MovimientoMision1Completa()
          if j == 1:
            pantalla.blit(TextoMision1Completa,(pos13,340))
            MovimientoPresioneEspacioMeta()
            pantalla.blit(TextoPresioneEspacioMeta,(450,pos14))
          if j == 2:
            pantalla.blit(TextoMision1Completaf,(pos13,340))
            if tecla[pygame.K_ESCAPE]:
              salir = True
          
          if tecla[pygame.K_SPACE]:
             sounds.Meta.stop()
             pygame.mixer.music.load('PiratasDelCaribe.mp3')
             pygame.mixer.music.play(-1)
             EliminarDisparo = False
             CambioNivel2 = True
             FinMeta = False

       TiempoJuego()
       cadena=ConcatenacionTiempo(deceMin,unidMin,deceSeg,unidSeg,centSeg)
       textoTiempo.render(pantalla, cadena, blanco, (1265, 8))

       pygame.display.update()    
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
def Instrucciones():
    salir = False
    FondoInstrucciones = pygame.image.load('FondoInstrucciones.png').convert()
    Calavera = pygame.image.load('Calavera.png').convert_alpha()
    fuente = pygame.font.Font('Zombified.ttf', 80)
    fuente2 = pygame.font.Font('Zombified.ttf', 30)
    Titulo = fuente.render("PODER CIENTIFICO", 1, (negro))
    Avanzar = fuente2.render("Avanzar", 1, (azul))
    Retroceder = fuente2.render("Retroceder", 1, (azul))
    Saltar = fuente2.render("Saltar", 1, (azul))
    Agacharse = fuente2.render("Agacharse", 1, (azul))
    Disparar = fuente2.render("Disparar", 1, (azul))
    Pausar = fuente2.render("Pausar", 1, (azul))
    VolverAlMenu = fuente2.render("Volver al Menu", 1, (dorado))
    Vida = fuente2.render("+1 Vida", 1, (dorado))
    Velocidad = fuente2.render("+ Velocidad", 1, (dorado))
    Escudo = fuente2.render("Invencible", 1, (dorado))
    Moneda = fuente2.render("+1 Moneda", 1, (dorado))
    Balas = fuente2.render("+10 Balas", 1, (dorado))
    pantalla.blit(FondoInstrucciones,(0,0))
    pantalla.blit(Titulo,(500,120))
    pantalla.blit(Avanzar,(403,570))
    pantalla.blit(Retroceder,(160,570))
    pantalla.blit(Saltar,(310,500))
    pantalla.blit(Agacharse,(288,605))
    pantalla.blit(Disparar,(618,605))
    pantalla.blit(Pausar,(845,605))
    pantalla.blit(Vida,(330,650))
    pantalla.blit(Velocidad,(440,650))
    pantalla.blit(Escudo,(590,650))
    pantalla.blit(Moneda,(730,650))
    pantalla.blit(Balas,(890,650))
    pantalla.blit(Calavera,(650,10))

    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
def Creditos():
    salir = False
    FondoCreditos = pygame.image.load('FondoCreditos.png').convert()
    Calavera = pygame.image.load('Calavera.png').convert_alpha()
    LogoUniversidad = pygame.image.load('LogoUniversidad.png').convert_alpha()
    Computador = pygame.image.load('Computador.png').convert_alpha()
    fuente = pygame.font.Font('Zombified.ttf', 80)
    fuente2 = pygame.font.Font('Zombified.ttf', 50)
    fuente3 = pygame.font.Font('Zombified.ttf', 50)
    Titulo = fuente.render("PODER CIENTIFICO", 1, (dorado))
    ComputacionGrafica = fuente2.render("COMPUTACION GRAFICA", 1, (dorado))
    Nombre1 = fuente3.render("Jhonatan Pineda", 1, (rojooscuro))
    Nombre2 = fuente3.render("Juan Suarez", 1, (rojooscuro))
    while salir != True:
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pantalla.blit(FondoCreditos,(0,0))
       pantalla.blit(Titulo,(500,120))
       pantalla.blit(Calavera,(650,10))
       MovimientoLogoUniversidad()
       pantalla.blit(LogoUniversidad,(pos8,500))
       MovimientoComputador()
       pantalla.blit(Computador,(pos9,500))
       MovimientoComputacionGrafica()
       pantalla.blit(ComputacionGrafica,(300,pos10))
       MovimientoNombre1()
       pantalla.blit(Nombre1,(800,pos11))
       MovimientoNombre2()
       pantalla.blit(Nombre2,(800,pos12))
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
# Menu Inicial
def Menu(opcion):
    Fondo = pygame.image.load('FondoMenu.jpg').convert()
    Personaje = pygame.image.load('PersonajeMenu.png').convert_alpha()
    Calavera = pygame.image.load('Calavera.png').convert_alpha()
    Seleccion = pygame.image.load('Seleccion.png').convert_alpha() 
    fuente = pygame.font.Font('Zombified.ttf', 80)
    Titulo = fuente.render("PODER CIENTIFICO", 1, (dorado))
    pantalla.blit(Fondo,(0,0))
    pantalla.blit(Personaje,(400,500))
    MovimientoTitulo()
    pantalla.blit(Titulo,(pos5,120))
    MovimientoCalavera()
    pantalla.blit(Calavera,(650,pos4))
    if opcion == 1:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(azul))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(rojo))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(rojo))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(rojo))
       Salir,opcion5 = TextoMenu("SALIR",900,740,(rojo))
       pantalla.blit(Seleccion,(MenuX+260,MenuY+35))
    if opcion == 2:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(rojo))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(azul))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(rojo))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(rojo))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(rojo))
       pantalla.blit(Seleccion,(MenuX+245,MenuY+45))
    if opcion == 3:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(rojo))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(rojo))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(azul))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(rojo))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(rojo))
       pantalla.blit(Seleccion,(MenuX+320,MenuY+55))
    if opcion == 4:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(rojo))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(rojo))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(rojo))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(azul))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(rojo))
       pantalla.blit(Seleccion,(MenuX+320,MenuY+65))  
    if opcion == 5:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(rojo))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(rojo))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(rojo))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(rojo))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(azul))
       pantalla.blit(Seleccion,(MenuX+360,MenuY+75))
    pantalla.blit(IniciarJuego,opcion1)
    pantalla.blit(Instrucciones,opcion2)
    pantalla.blit(Historia,opcion3)
    pantalla.blit(Creditos,opcion4)
    pantalla.blit(Salir,opcion5)
#------------------------------------------------------------------------------------------------------------------------------------------------
def Historia():
    salir = False
    FondoInstrucciones = pygame.image.load('FondoMenu1.png').convert()
    pantalla.blit(FondoInstrucciones,(0,0))
    Personaje = pygame.image.load('PersonajeMenu.png').convert_alpha()
    Zombie = pygame.image.load('ZombiePausa1.png').convert_alpha()
    Zombie2 = pygame.image.load('ZombiePausa2.png').convert_alpha()
    Invencible = pygame.image.load("Invencible.png")
    EsqueletoGameOver = pygame.image.load('EsqueletoGameOver.png').convert_alpha()
    ManoPausa = pygame.image.load('ManoPausa.png').convert_alpha()
    Calavera = pygame.image.load('Calavera.png').convert_alpha()
    IconoVidas = pygame.image.load('Vidas.png').convert_alpha()
    IconoBalas = pygame.image.load('Balas.png').convert_alpha()
    Recarga = pygame.image.load('Recarga.png').convert_alpha()
    fuente3 = pygame.font.Font('Zombified.ttf', 40)
    w1 = fuente3.render("Bienvenido al modo historia de PODER CIENTIFICO, ", 1, (negro))
    w2 = fuente3.render("aqui conoceras mas de este apasionante juego", 1, (negro))
    pantalla.blit(w1,(490,200))
    pantalla.blit(w2,(490,250))
    
    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if tecla[pygame.K_UP]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Zombified.ttf', 50)
                  intro1 = fuente3.render("Los Zombies se apoderaron del mundo", 1, (blanco))
                  intro2 = fuente3.render("mataron y exterminaron",1,(blanco))
                  intro3 = fuente3.render("a todos los humanos" , 1, (blanco))
                  intro4 = fuente3.render("sin dejar rastro de algun sobreviviente" , 1, (blanco))
                  intro5 = fuente3.render("pero lo que no sabian era que Charles Darwin " , 1, (blanco))
                  intro6 = fuente3.render("habia resucitado y evolucionado" , 1, (blanco))
                  intro7 = fuente3.render("y estaba en la tierra para convatirlos..." , 1, (blanco))
                  
                  pantalla.blit(intro1,(490,200))
                  pantalla.blit(intro2,(490,250))
                  pantalla.blit(intro3,(490,300))
                  pantalla.blit(intro4,(490,350))
                  pantalla.blit(intro5,(490,400))
                  pantalla.blit(intro6,(490,450))
                  pantalla.blit(intro7,(490,500))
                  pantalla.blit(ManoPausa,(200,300))
                  pantalla.blit(Calavera,(1000,500))

          if tecla[pygame.K_DOWN]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Zombified.ttf', 50)
                  p1 = fuente3.render("Darwin es este ser valiente que nos ayudara", 1, (blanco))
                  p2 = fuente3.render("a destruir a estos zombies",1,(blanco))
                  p3 = fuente3.render("ya que el desarrollo" , 1, (blanco))
                  p4 = fuente3.render("un arma que dispara monos" , 1, (blanco))
                  p5 = fuente3.render("los cuales al impactar con estos zombies los" , 1, (blanco))
                  p6 = fuente3.render("exterminara completamente..." , 1, (blanco))
                  pantalla.blit(p1,(490,200))
                  pantalla.blit(p2,(490,250))
                  pantalla.blit(p3,(490,300))
                  pantalla.blit(p4,(490,350))
                  pantalla.blit(p5,(490,400))
                  pantalla.blit(p6,(490,500))
                  pantalla.blit(Personaje,(200,480))
                  pantalla.blit(EsqueletoGameOver,(800,500))

          if tecla[pygame.K_LEFT]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Zombified.ttf', 50)
                  p1 = fuente3.render("Gracias a su inteligencia", 1, (blanco))
                  p2 = fuente3.render("y a su astucia",1,(blanco))
                  p3 = fuente3.render("Darwin piensa" , 1, (blanco))
                  p4 = fuente3.render("en aplicar su teoria " , 1, (blanco))
                  p5 = fuente3.render("de la evolucion" , 1, (blanco))
                  p7 = fuente3.render("para que la humanidad vuelva a renacer" , 1, (blanco))
                  p6 = fuente3.render("?podra Darwin exterminar a los zombies?" , 1, (blanco))
                  pantalla.blit(p1,(490,200))
                  pantalla.blit(p2,(490,250))
                  pantalla.blit(p3,(490,300))
                  pantalla.blit(p4,(490,350))
                  pantalla.blit(p5,(490,400))
                  pantalla.blit(p7,(490,450))
                  pantalla.blit(p6,(490,500))
                  pantalla.blit(Recarga,(200,480))

          if tecla[pygame.K_RIGHT]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Zombified.ttf', 50)
                  p1 = fuente3.render("Darwin ha sido uno de los cientificos", 1, (blanco))
                  p2 = fuente3.render("mas influyentes en la historia de la humanidad",1,(blanco))
                  p3 = fuente3.render("y con estas palabras nos motiva a luchar" , 1, (blanco))
                  p4 = fuente3.render("No es la mas fuerte de las especies la que sobrevive" , 1, (blanco))
                  p5 = fuente3.render("y tampoco la mas inteligente" , 1, (blanco))
                  p6 = fuente3.render("Sobrevive aquella que mas se adapta al cambio" , 1, (blanco))
                  pantalla.blit(p1,(490,200))
                  pantalla.blit(p2,(490,250))
                  pantalla.blit(p3,(490,300))
                  pantalla.blit(p4,(490,350))
                  pantalla.blit(p5,(490,400))
                  pantalla.blit(p6,(490,450))
                  pantalla.blit(Zombie,(20,100))

          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
def MenuPausa(OpcionMenuPausa):
    SeleccionPausa = pygame.image.load('Seleccion.png').convert_alpha() 
    FondoMenuPausa = pygame.image.load('FondoMenuPausa.png').convert_alpha() 
    ZombiePausa1 = pygame.image.load('ZombiePausa1.png').convert_alpha() 
    ZombiePausa2 = pygame.image.load('ZombiePausa2.png').convert_alpha() 
    ManoPausa = pygame.image.load('ManoPausa.png').convert_alpha()
    pantalla.blit(FondoMenuPausa,(200,100))
    pantalla.blit(ZombiePausa1,(20,100))
    pantalla.blit(ZombiePausa2,(950,100))
    pantalla.blit(ManoPausa,(600,480))
    if OpcionMenuPausa == 1:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(azulclaro))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(negro))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO",710,440,(negro))
       pantalla.blit(SeleccionPausa,(MenuX+90,MenuY-205))
    if OpcionMenuPausa == 2:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(negro))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(azulclaro))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(negro))
       pantalla.blit(SeleccionPausa,(MenuX-2,MenuY-133))
    if OpcionMenuPausa == 3:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(negro))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(negro))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(azulclaro))
       pantalla.blit(SeleccionPausa,(MenuX+55,MenuY-62))
    pantalla.blit(ReanudarJuego,OpcionMenuPausa1)
    pantalla.blit(VolverMenuPrincipal,OpcionMenuPausa2)
    pantalla.blit(SalirEscritorio,OpcionMenuPausa3)
#------------------------------------------------------------------------------------------------------------------------------------------------
opcion = 1
while salir != True:
    reloj.tick(60) 
    tecla = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir = True
        if tecla[pygame.K_s]:
	    sys.exit()
        if tecla[pygame.K_UP] and opcion > 1 and MenuY > DimensionMenu[1]:
            sounds.OpcionMenu.play()
            opcion -= 1
            MenuY = MenuY-40
            Seleccion
        if tecla[pygame.K_DOWN] and opcion < 5 and MenuY > DimensionMenu[0]:
            sounds.OpcionMenu.play()
            opcion += 1
            MenuY = MenuY+40
            Seleccion
	if tecla[K_RETURN]:
	    if opcion == 1:
	       print "ACCEDER AL JUEGO"
               sounds.EnterMenu.play()
               IniciarJuego()
               ReiniciarTiempo = True
	    if opcion == 2:
               print "ACCEDER A LAS INSTRUCCIONES"
               sounds.EnterMenu.play()
               Instrucciones()
	    if opcion==3:
	       print "ACCEDER A HISTORIA"
	       sounds.EnterMenu.play()
	       Historia()
	    if opcion == 4:
               print "ACCEDER A LOS CREDITOS"
               sounds.EnterMenu.play()
               Creditos()
	    if opcion == 5:
	       sys.exit()
    Menu(opcion)
    pygame.display.flip()
pygame.quit()

