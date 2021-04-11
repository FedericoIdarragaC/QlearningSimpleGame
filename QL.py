import pygame
import numpy as np
import random
import time

AZUL = [59,124,255]
VERDE = [118,252,37]
ROJO = [214,6,6]
NEGRO = [0,0,0]
GRIS = [170,170,170]


ANCHO = 600
ALTO = 600

tablero = []
puntajes = []
estados = []
for x in range(1,5):
    col = (600/5)*x
    fila = []
    for y in range(1,5):
        fila.append([col,y*(600/5)]) 
        estados.append([x-1,y-1])
    puntajes.append([-0.01,-0.01,-0.01,-0.01])
    tablero.append(fila)
    
class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,pos_init,color = AZUL):
        super().__init__()
        self.image = pygame.Surface([40,40])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        
        self.position = [pos_init[0],pos_init[1]]
        
        
        self.rect.x,self.rect.y = tablero[self.position[0]][self.position[1]]

    def move(self,action):
        
        if action == 1:
            movement = [self.position[0],self.position[1]-1]      
        elif action == 2:
            movement = [self.position[0]+1,self.position[1]]
        elif action == 3:
            movement = [self.position[0],self.position[1]+1]
        elif action == 4:
            movement = [self.position[0]-1,self.position[1]]
            
        if(movement[0] <= 3 and movement[0] >= 0 and movement[1] <= 3 and movement[1] >= 0):
            self.rect.x,self.rect.y = tablero[movement[0]][movement[1]]
        else:
            movement = [self.position[0],self.position[1]]
        
        self.position = movement
        
        puntaje = puntajes[self.position[0]][self.position[1]]
        next_state = estados.index([self.position[0],self.position[1]])
        
        self.position = movement
        return puntaje,next_state
    
    def reiniciar(self):
        movement = [0,3]
        self.rect.x,self.rect.y = tablero[movement[0]][movement[1]]
        self.position = movement
        

class Hoyo(pygame.sprite.Sprite):
    
    def __init__(self,pos_init,color = ROJO):
        super().__init__()
        self.image = pygame.Surface([40,40])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = pos_init[0]
        self.rect.y = pos_init[1]
        
class Premio(pygame.sprite.Sprite):
    
    def __init__(self,pos_init,color = VERDE):
        super().__init__()
        self.image = pygame.Surface([40,40])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = pos_init[0]
        self.rect.y = pos_init[1]    


if __name__ == "__main__":
    
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    
    jugadores = pygame.sprite.Group()
    hoyos = pygame.sprite.Group()
    premios = pygame.sprite.Group()
    
    jug = Jugador([0,3])
    jugadores.add(jug)
        
    hoyo1 = Hoyo(tablero[0][2])
    puntajes[0][2] = -1
    hoyo2 = Hoyo(tablero[2][1])
    puntajes[2][1] = -1
    hoyo3 = Hoyo(tablero[3][3])
    puntajes[3][3] = -1
    hoyos.add(hoyo1)
    hoyos.add(hoyo2)
    hoyos.add(hoyo3)
    
    premio = Premio(tablero[3][0])
    puntajes[3][0] = 2
    premios.add(premio)
 
    
    puntaje = 0
    
    qtable = np.zeros((16,4))
    learning_rate = 0.8
    max_steps = 99
    gamma = 0.95
    
    epsilon = 1.0                
    max_epsilon = 1.0             
    min_epsilon = 0.01            
    decay_rate = 0.005             
    
    cont = 0
    
    fin = False
    
    state = 0
    actions = [1,2,3,4]
    
    rewards = []
    
    while not fin:
        score = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

        jugadores.draw(pantalla)
        hoyos.draw(pantalla)
        premios.draw(pantalla)
        pygame.display.flip()
        
        time.sleep(0.1)
        
        exp_exp_tradeoff = random.uniform(0, 1)
        
        if exp_exp_tradeoff > epsilon:
            action = np.argmax(qtable[state,:])
            action += 1
        else:
            action = random.sample(actions,1)[0]
                     
        pantalla.fill(NEGRO)                      
        score,new_state = jug.move(action)
        action -= 1
        qtable[state, action] = qtable[state, action] + learning_rate * (score + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
       
        state = new_state
        
        puntaje += score
        
        #print(puntaje)
        if puntaje <= -1 or puntaje >= 1:
            epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*cont) 
            rewards.append(puntaje)
            jug.reiniciar()
            cont += 1
            print("Puntaje =",puntaje)
            puntaje = 0
        
        
        
        