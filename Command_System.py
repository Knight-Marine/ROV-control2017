import pygame
from pygame.locals import *
import serial

GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)



class App:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Frannie")

        # Set up the joystick
        pygame.joystick.init()
        
        self.serReadCount = 0 
        self.amps = 0
        self.distLog = []
        self.graphPoints = []

        self.my_joystick = None
        self.joystick_names = []
        
        #Set up serial connection
        self.ROV = serial.Serial("COM6",9600, timeout=0)
		
        # Motors
        self.motors=[0,0,0,0]
		# 0,1,2,3 IN ORDER
        self.motor_dots=[[BLUE,(485,180)],
		                 [BLUE,(565,180)],
						 [BLUE,(505,230)],
						 [BLUE,(545,230)]]
        
        self.deadzone = .3
        
        
        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()

        max_joy = max(self.my_joystick.get_numaxes(), 
                      self.my_joystick.get_numbuttons(), 
                      self.my_joystick.get_numhats())

        self.screen = pygame.display.set_mode( (700, 400) )

        self.font = pygame.font.SysFont("Courier", 16)

    # A couple of joystick functions...
    def check_axis(self, p_axis):
        if (self.my_joystick):
            if (p_axis < self.my_joystick.get_numaxes()):
                return self.my_joystick.get_axis(p_axis)

        return 0

    def check_button(self, p_button):
        if (self.my_joystick):
            if (p_button < self.my_joystick.get_numbuttons()):
                return self.my_joystick.get_button(p_button)

        return False

    def check_hat(self, p_hat):
        if (self.my_joystick):
            if (p_hat < self.my_joystick.get_numhats()):
                return self.my_joystick.get_hat(p_hat)

        return (0, 0)

    def draw_text(self, text, x, y, color, align_right=False):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey( (0, 0, 0) )

        self.screen.blit(surface, (x, y))

    def center_text(self, text, x, y, color):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey( (0, 0, 0) )

        self.screen.blit(surface, (x - surface.get_width() / 2, y - surface.get_height() / 2))

    def main(self):
        while (True):
            self.g_keys = pygame.event.get()

            self.screen.fill(0)

            for event in self.g_keys:
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.quit()
                    return

                elif (event.type == QUIT):
                    self.quit()
                    return

            self.draw_text("Joystick Name:  %s" % self.joystick_names[0], 5, 5, (0, 255, 0))

            self.draw_text("Axes (%d)" % self.my_joystick.get_numaxes(), 10, 210, (255, 255, 255))
    
            #joystick position indicator
            pygame.draw.rect(self.screen, (178,34,34), (10,230,160,160), 2)
            pygame.draw.rect(self.screen, (178,34,34), (180,230,160,160), 2)
            
            pygame.draw.circle(self.screen, (95,158,160),(90+int(self.my_joystick.get_axis(0)*80),310+int(self.my_joystick.get_axis(1)*80)), 10, 0)
            pygame.draw.circle(self.screen, (95,158,160),(260+int(self.my_joystick.get_axis(2)*80),310+int(self.my_joystick.get_axis(3)*80)),10, 0)
            
            #Use joystick position to set motor states
            if self.my_joystick.get_axis(1)>self.deadzone:
                              # forward/reverse * +/- 300. 1200-1800 absoloute value. axis 1
                self.motors[2]=int((-1 *abs(self.my_joystick.get_axis(1)) * 300) + 1500)
                self.motors[3]=int((-1 *abs(self.my_joystick.get_axis(1)) * 300) + 1500)
            elif self.my_joystick.get_axis(1)<self.deadzone*-1:
                self.motors[2]=int((1 *abs(self.my_joystick.get_axis(1)) * 300) + 1500)
                self.motors[3]=int((1 *abs(self.my_joystick.get_axis(1)) * 300) + 1500)
            else:
                self.motors[2]=1500
                self.motors[3]=1500

            if self.my_joystick.get_axis(2)>self.deadzone:
                self.motors[2]=int((1 *abs(self.my_joystick.get_axis(2)) * 300) + 1500)
                self.motors[3]=int((-1 *abs(self.my_joystick.get_axis(2)) * 300) + 1500)
            elif self.my_joystick.get_axis(2)<self.deadzone*-1:
                self.motors[2]=int((-1 *abs(self.my_joystick.get_axis(2)) * 300) + 1500)
                self.motors[3]=int((1 *abs(self.my_joystick.get_axis(2)) * 300) + 1500)

            if self.my_joystick.get_axis(3)>self.deadzone:
                self.motors[0]=int((-1 *abs(self.my_joystick.get_axis(3)) * 300) + 1500)
                self.motors[1]=int((-1 *abs(self.my_joystick.get_axis(3)) * 300) + 1500)
            elif self.my_joystick.get_axis(3)<self.deadzone*-1:
                self.motors[0]=int((1 *abs(self.my_joystick.get_axis(3)) * 300) + 1500)
                self.motors[1]=int((1 *abs(self.my_joystick.get_axis(3)) * 300) + 1500)
            else:
                self.motors[0]=1500
                self.motors[1]=1500
				
            if self.my_joystick.get_axis(0)>self.deadzone:
                self.motors[0]=int((1 *abs(self.my_joystick.get_axis(0)) * 300) + 1500)
                self.motors[1]=int((-1 *abs(self.my_joystick.get_axis(0)) * 300) + 1500)
            elif self.my_joystick.get_axis(0)<self.deadzone*-1:
                self.motors[0]=int((-1 *abs(self.my_joystick.get_axis(0)) * 300) + 1500)
                self.motors[1]=int((1 *abs(self.my_joystick.get_axis(0)) * 300) + 1500)
            
            pass
            '''         
            #Serail writing of motors re-implement later. 
            self.ser.write (str(self.motors))
            s = self.ser.read(100)
            self.draw_text(s, 100, 200, (255, 255, 255))'''         


            for i,mot in enumerate(self.motors):
                if mot>1500:
                    self.motor_dots[i][0]=GREEN
                elif mot<1500:
                    self.motor_dots[i][0]=RED
                else:
                    self.motor_dots[i][0]=BLUE
            
            
            for dot in self.motor_dots:
                pygame.draw.circle(self.screen, dot[0],dot[1],15,0)			
            

            self.draw_text(str(self.motors), 370,40, (250,0,0))
            
            # Code for reading data from ampmeter
            if (self.ROV.in_waiting > 0):
                instring = ""
                ch = self.ROV.read()
                if ch == "<":
                    reading = True
                
                    while reading:
                        instring += ch
                        ch = self.ROV.read()
                        if ch == ">":
                            instring += ch
                            reading = False
                    
                    
                print instring 
                if len(instring)>3:
                    self.amps = int(instring[1:-1])

                    self.distLog.insert(0,self.amps)
                    if len(self.distLog) > 298 :
                        self.distLog.pop()
                    
                    
                    self.graphPoints = []
                    for x, point in enumerate(self.distLog):
                        if point > 100:
                            point = 100
                        self.graphPoints.append((x+351, 390-point))
                            
                    self.serReadCount=0
            else:
                self.serReadCount+=1
            

            #Draw the graph for amperage
            #prevents line drawing errors when there is only one point
            if(len(self.distLog) > 2):
                pygame.draw.lines(self.screen, (10, 200, 10), False,  self.graphPoints)
           
            pygame.draw.rect(self.screen, (180,220,180), (350,290,300,100), 2)
            self.draw_text(str(self.amps)+" amps", 655,370, (10, 200, 10)) 

            
            #code for buttons
            self.draw_text("Buttons (%d)" % self.my_joystick.get_numbuttons(), 5, 75, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numbuttons()):
                if (self.my_joystick.get_button(i)):
                    pygame.draw.circle(self.screen, (0, 0, 200), (20 + (i * 30), 100), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 200), (20 + (i * 30), 100), 10, 1)

                self.center_text("%d" % i, 20 + (i * 30), 100, (255, 255, 255))

            pygame.display.flip()

    def quit(self):
        self.ROV.close()
        pygame.display.quit()

app = App()
app.main()
