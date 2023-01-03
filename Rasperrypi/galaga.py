
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
import speech_recognition as sr
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
import threading as th
from PIL import Image
import numpy as np

import time
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#  ****************************************************************************
# Método principal
#  ****************************************************************************

def main():

     

    matrix = Matrix() 
    player = Player(matrix)
    print(f"{bcolors.OKGREEN}Warning:Game initializated!{bcolors.ENDC}")

    
    t1 = th.Thread(target=player.play)    
    # t2 = th.Thread(target=matrix.draw_matrix)
    
    t1.start()
    matrix.draw_matrix()
    while 1:
        if(player.get_stop()):
            t1.join()
    # t2.start()
    
    
        
        
 
        
        
        
        
        
        # Movimientos verticales

        # if key.read_key  == "up" or key.read_key  == "w":
           
        #     matrix.move_to_up()
        #     key.wait("up")
            
        # elif key.read_key  =="down" or key.read_key  == "s":
        #     matrix.move_to_down()
        #     key.wait("down")

        #Movimientos diagonales
        # elif(entry == "c"):
        #     matrix.move_to_down()
        #     matrix.move_to_rigth()

        # elif(entry == "z"):
        #     matrix.move_to_down()
        #     matrix.move_to_left()

        # elif(entry == "e"):
        #     matrix.move_to_up()
        #     matrix.move_to_rigth()

        # elif(entry == "q"):
        #     matrix.move_to_up()
        #     matrix.move_to_left()
        
        #Movimientos horizontales
        # elif key.read_key  == "rigth" or key.read_key  == "d":
        #     matrix.move_to_rigth()
        #     key.wait("rigth")
           
        # elif key.read_key  =="a"or key.read_key  =="left":
        #     matrix.move_to_left()
        #     key.wait("left")

        # else:
        #     print("por favor ingrese una tecla válida")
            
#  ****************************************************************************             
#  Clasé matrix, encargada de encender y apagar
#  cada uno de los leds que se encuentran en la matrix de leds
#  ****************************************************************************

class Matrix(object):

    #Creación de constructor --------------------------------------------------------------------
    def __init__(self):

        super(Matrix, self).__init__()
        self.device = self.create_matrix_device(1,0,0)
        self.screen_enemies = np.zeros((8,8),int)
        self.screen_shoots = np.zeros((8,8),int)
        self.screen_player = np.zeros((8,8),int)
        self.bitmap = np.zeros((8,8),int)

    # Setters y getters -------------------------------------------------------------------------
    def set_matrix_general(self):
        for i in range (8):
            for j in range(8):
                self.get_bitmap()[j,i] = self.get_screen_player()[i,j] | self.get_screen_shoots()[i,j] | self.get_screen_enemies()[i,j]

    def set_screen_enemies(self, point):
        self.screen_enemies[point.get_position_X(),point.get_position_Y()] = point.get_state()
      
    
    def set_screen_shoots(self, point):
        if(point.get_position_X() and point.get_position_Y() < 8):
            self.screen_shoots[point.get_position_X(),point.get_position_Y()] = point.get_state()
    
    def set_screen_player(self, point):
        self.screen_player[point.get_position_X(),point.get_position_Y()] = point.get_state()
        

    def get_screen_enemies(self):
        return self.screen_enemies
    
    def get_screen_shoots(self):
        return self.screen_shoots

    def get_bitmap(self):
        return self.bitmap
    
    def get_screen_player(self):
        return self.screen_player
        


    
    # Método que se encarga de pintar la matrix de leds 

    def draw_matrix(self):
        #self.device.clear()
        # vector_on =[]
        # vector_off = []
        # for i in range(8):
        #     for j in range(8):
        #         if(self.get_screen_enemies()[i,j] == 1 or self.get_screen_shoots()[i,j] == 1 or self.get_screen_player()[i,j] == 1):
        #             punto = (i,j)
        #             vector_on.append(punto)                  
        #         else:
        #             punto = (i,j)
        #             vector_off.append(punto)
        self.set_matrix_general()
        bitmap = Image.fromarray(self.get_bitmap())
        bitmap = bitmap.resize((8, 8))
        bitmap = bitmap.convert("L")
        with canvas(self.device) as draw:            
            draw.bitmap((0, 0), bitmap, fill="white") 
        # self.device.show()
        #time.sleep(0.1)

    def show_lifes(self,lifes):
        msg="3"
        if lifes == 2:
            msg = "2"
        elif lifes == 1:
            msg ="1"

        with canvas(self.device) as draw:            
            text(draw,(1, 1), msg, fill="white", font=proportional(CP437_FONT))
        time.sleep(5)

    def show_init(self):
        print("Iniciando Juego!")

    def show_lose(self):        
        print("Game Over!")

    def show_win(self):        
        print("congratulations!")


    #métodos auxiliares -----------------------------------------------------------------------

    def create_matrix_device(self,n,block_orientation,rotate):
        # Create matrix device
        print("Creating device...")
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial,cascaded=n,block_orientation=block_orientation,rotate=rotate)
        print("Device created.")
        return device
        
    def draw_point(self,x,y,value):
    
        with canvas(self.device) as draw:            
            draw.point((x,y), fill=value)

       
    

    # def createenemies(self):
    #     with canvas(self.device) as draw:
    #         for i in range(8):
    #             for j in range(2):
    #                 draw.point((i,j), fill="green")

    # def shoot(self, direction):
    #     i = 7
    #     point = Matrix(self.getpositionX(), self.getpositionY())
    #     while i > 0:
    #         if(direction == "up"):
    #             point.move_to_up()
    #         elif(direction == "down"):
    #             point.move_to_down()
    #         time.sleep(1)
            
    #         i = i-1

#  ****************************************************************************
# Creación de classe principal, la cual es la encargada de darle los actributos y principales comportamientos
# a cada uno de los puntos.
#  ****************************************************************************

class Point():

    # Constructor ------------------------------------------------------------------

    def __init__(self, matrix, x, y, vm,hm,type):
        #print(f"{bcolors.HEADER}Warning: point have been created!{bcolors.ENDC}")
        self.x = x
        self.y = y 
        self.state = 1 
        self.type= type
        self.verticalmovement = vm
        self.horizontalmovement = hm
        self.screen = matrix
    #    self.screen.draw_point(self) 

   # Getters -----------------------------------------------------------------------
    def get_state(self):
        return self.state

    def get_position_X(self):
        return self.x

    def get_position_Y(self):
        return self.y

    def get_screen(self):
        return self.screen

    def get_verticalmovement(self):
        return self.verticalmovement

    def get_horizontalmovement(self):
        return self.horizontalmovement


    # Setters ----------------------------------------------------------------------
    def set_state1(self):
        if self.get_state()== 1:
            self.state = 0
        else:
            self.state = 1    

        if(self.type == "enemy"):
            self.get_screen().set_screen_enemies(self) 
        elif(self.type  == "shoot"):
            self.get_screen().set_screen_shoots(self) 
        elif(self.type  == "player"):   
            self.get_screen().set_screen_player(self)     
        self.get_screen().draw_matrix()
    def set_state2(self, state):
        self.state = state 
        
        if(self.type == "enemy"):
            self.get_screen().set_screen_enemies(self) 
        elif(self.type  == "shoot"):
            self.get_screen().set_screen_shoots(self) 
        elif(self.type  == "player"):   
            self.get_screen().set_screen_player(self)
        self.get_screen().draw_matrix()
    def set_position_X(self, new_x):
        self.set_state1()         
        self.x = new_x
        self.set_state1()
          

    def set_position_Y(self, new_y):
        self.set_state1()        
        self.y = new_y
        self.set_state1()
         


    #Métodos principales -----------------------------------------------------------
    def delete_point(self):
        self.set_state2(False)
        del self



    def is_In_The_Same_Position(self, punto):
        if(self.get_position_X() == punto.get_position_X() and self.get_position_Y() == punto.get_position_Y() ):
            #print("Verificando colisión!")
            return True
        else:
            return False
            
    def move_to_right(self):
        if(self.x<7 and self.get_horizontalmovement() == True):     
            self.set_position_X(self.get_position_X()+1)
            # self.get_screen().draw_matrix()         


    def move_to_left(self):
        if(self.x>0 and self.get_horizontalmovement() == True):     
            self.set_position_X(self.get_position_X()-1)
            # self.get_screen().draw_matrix()  
             

    def move_to_up(self):
        if(self.y>0 and self.get_verticalmovement() == True):     
            self.set_position_Y(self.get_position_Y()-1)
            # self.get_screen().draw_matrix()  
               

    def move_to_down(self):
        if(self.y<7 and self.get_verticalmovement() == True):     
            self.set_position_Y(self.get_position_Y()+1)
            # self.get_screen().draw_matrix()  


#  ****************************************************************************
# Clase que modela el comportamiento de los disparos
#  ****************************************************************************
class Shoot(Point):

    # Constructor ---------------------------------------------------------------------

    def __init__(self,matrix,x,y,dir):
        
        super().__init__(matrix, x,y,True, False,"shoot")
        self.direction = dir


    # Getters y Setters --------------------------------------------------------------
    def get_direction(self):
        return self.direction

    def set_direction(self, dir):
        self.direction = dir
        
    
    # Métodos principales -------------------------------------------------------------
    
    def shoot(self,point,shooter):
        #print(f"{bcolors.WARNING}Warning: point have been shooted!{bcolors.ENDC}")
        i = 7
        while i > 0:
            if(self.get_direction() == "up"):
                if shooter.verify_colision(self) != True:
                    #print("Not today")
                    self.move_to_up()
                    return False
                else:
                    self.delete_point()
                    return True
                    
            elif(self.get_direction()  == "down"):
                if shooter.verify_colision(point) != True:
                    #print("Not today but in green")
                    self.move_to_down()
                    return False
                else:
                    self.delete_point()                    
                    return True
            
            time.sleep(0.1)
            i=i-1
        if i == 0 :
            #print("Punto llegó a su destino")
            self.delete_point()
            return True
                
        

#  ****************************************************************************
# Creación Clase Enemy, encargada de modelar el comportamiento de los enemigos
#  ****************************************************************************
    
class Enemy(Point):

    # Constructor ------------------------------------------------------------------------
    def __init__(self,matrix,x,y):
        
        super().__init__(matrix, x,y,False,False,"enemy")
        self.shoot = []
    
    def add_shoot(self, shoot):
        self.shoot.append(shoot)
        
    def get_shoot(self):
        return self.shoot

    def shoot_otherside(self):
        if(self.get_shoot()[0].get_position_Y() == 7):
            return True

    def verify_colision(self, player):
        if(self.get_shoot()[0].is_In_The_Same_Position(player)):
            
            print("Jugador -1 vida")
            self.get_shoot()[0].delete_point()
            self.get_shoot().clear()
            player.set_lifes()
            player.show_lifes()
            return True
    # Métodos principales ----------------------------------------------------------------
    def enemy_shoot(self,player):
         
        ps = Shoot(self.get_screen(),self.get_position_X(), self.get_position_Y(),"down")
        self.add_shoot(ps)
        return ps.shoot(player,self)
        
        

#  ****************************************************************************
# Creación de clase Jugador, encargada de modelar el comportamiento del jugador 
#  y las principales caracteristicas del juego.
#  ****************************************************************************

class Player(Point):

    # COnstructor -----------------------------------------------------------------------
    def __init__(self,matrix):
        super().__init__(matrix, 3,7,False,True,"player")
        #print(f"{bcolors.OKGREEN}Warning: Player have been created!{bcolors.ENDC}")
        self.lifes = 3
        self.enemies = []
        self.formation = 0
        self.counter_shoot_enemies = 0
        self.counter_shoot_total = 0
        self.stop = False
        self.get_screen().set_screen_player(self)
        self.enemies_init()

    # Setters  --------------------------------------------------------------------------
    def set_lifes(self):
        if self.get_lifes() > 0:
            self.lifes = self.lifes -1

    def set_formation(self,formation):
        enemies_list = self.get_enemies()
        if formation == 0:
            for i in range (0,len(enemies_list)):
                enemies_list[i].set_state2(1)  # type: ignore

        if formation == 1:
            for i in range (1,len(enemies_list),2):
                enemies_list[i].set_state1()   # type: ignore
        if formation == 2:
            for i in range (0,len(enemies_list ),random.randint(1,4)):
                enemies_list[i].set_state1()         # type: ignore
        if formation == 3:
            for i in range (0,len(enemies_list ),random.randint(1,3)):
                enemies_list[i].set_state1()  # type: ignore


    # Getters  --------------------------------------------------------------------------
    def get_enemies(self):
        return self.enemies

    def get_formation(self):
        return self.formation

    def get_lifes(self):
        return self.lifes

    def not_more_life(self):
        if self.get_lifes() >= 1:
            return False
        else :
            self.show_lose()
            return True
    
    def not_more_enemies(self):
        if len(self.get_enemies())>= 1:
            return False
        else: 
            self.show_win()
            return True

    # Métodos jugador -------------------------------------------------------------------

    def player_shoot(self):
        if (self.counter_shoot_total < 6):
            ps = Shoot(self.get_screen(),self.get_position_X(), self.get_position_Y(),"up")
            self.counter_shoot_total += 1            
            if(ps.shoot(self.get_enemies(), self)):
                #print("Counter = ", self.counter_shoot_total)
                self.counter_shoot_total = self.counter_shoot_total-1
            
            

        time.sleep(2)
    def set_stop(self):
        self.set_stop= True

    def play(self):
        self.show_init()
        while self.not_more_enemies()== False or self.not_more_life() == False:

            entry= input("muevete:")

            if entry == "d":
                self.move_to_right()
            elif entry == "a":
                self.move_to_left()
            elif entry == "w":
                self.player_shoot()
            if(self.not_more_enemies() or self.not_more_life() ):
                self.set_stop()
                break
                        
            # r = sr.Recognizer()

            # with sr.Microphone() as source:
            #     print("Puedes hablar ahora...")
            #     audio = r.listen(source)
                
            #     try:                
            #         text = r.recognize_google(audio, language='en-US')
            #         if text == "right":
            #             self.move_to_right()
            #         elif text == "shoot":
            #             self.player_shoot()
            #         elif text == "left":
            #             self.move_to_left()

            #     except:
            #         print("Prueba de nuevo")
            #         audio = r.listen(source)

    def show_lifes(self):
        self.get_screen().show_lifes(self.get_lifes())

    def show_init(self):
        self.get_screen().show_init()
    def show_lose(self):
        self.get_screen().show_lose()
    def show_win(self):
        self.get_screen().show_win()

    def verify_colision(self,point):
        for i in self.get_enemies():
            if(point.is_In_The_Same_Position(i) and i.get_state() == 1 ):
                print("Enemigo Eliminado" , i.get_position_X(),i.get_position_Y()  )
                self.get_enemies().remove(i)
                i.delete_point()
                if(len(self.get_enemies())==0):
                    self.not_more_enemies()
                return True
            
        

   

    # Métodos enemigos --------------------------------------------------------------------

    def create_enemies_formation(self):
        print(f"{bcolors.FAIL}Warning: Enemy have been created!{bcolors.ENDC}")
        for i in range(8):
            for j in range(2):                
                self.enemies.append(Enemy(self.get_screen(),i,j))
        self.set_formation(0)
        
    

    def change_enemies_formation(self):
        while True:
            forma = random.randint(0,4)
            if(forma == 0):
                self.set_formation(0)
            elif(forma == 1):
                self.set_formation(1)
            elif(forma == 2):
                self.set_formation(2)
            elif(forma == 3):
                self.set_formation(3)
            else:
                self.set_formation(3)
            time.sleep(5)

    def enemies_shoot(self):
         
        while 1:
            sh = random.randint(0,1)
            enemies = self.get_enemies()
            if(sh == 1 and self.counter_shoot_enemies < 5 and self.counter_shoot_total < 6):
                
                sn = random.randint(2,4)
                sp = np.zeros(sn)
                for i in range(sp.size):
                    sp[i]=random.randint(0,(len(self.get_enemies()))-1)                    
                    self.counter_shoot_enemies = self.counter_shoot_enemies + 1
                    self.counter_shoot_total = self.counter_shoot_total + 1
                    #print("Counter = ", self.counter_shoot_total)
                    if(enemies[int(sp[i])].enemy_shoot(self)):
                        self.counter_shoot_enemies = self.counter_shoot_enemies - 1
                        self.counter_shoot_total = self.counter_shoot_total -1
            
            time.sleep(1)

    def get_stop(self):
        return self.stop
        
        
    def enemies_init(self):
        self.create_enemies_formation()
        t3 = th.Thread(target=self.change_enemies_formation)
        t4 = th.Thread(target=self.enemies_shoot)
        t3.start()
        t4.start()
        if(self.get_stop()):
            t3.join()
            t4.join()
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass              