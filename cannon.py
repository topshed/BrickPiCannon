import pygame, Image
import io
import time
import picamera
import pygbutton
import sys
from pygame.locals import *
from BrickPi import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 30

BrickPiSetup()  # setup the serial port for communication
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B - Move Target
BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor C - Shoot Balls
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

pygame.init()
FPSCLOCK = pygame.time.Clock()
screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
pygame.mouse.set_visible(1)
#pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
#screen = pygame.display.set_mode(screenSize)
screen = pygame.display.set_mode((640,480))
crosshairs = pygame.image.load('crosshairs.png')

clock = pygame.time.Clock()
BrickPiUpdateValues()
BrickPi.Encoder[PORT_B] = 0
pos = 0
myfont = pygame.font.SysFont("monospace", 50)
labelPos = myfont.render(str(pos),1,(255,255,0))
mywarnfont = pygame.font.SysFont("monospace", 20)
warn1 = mywarnfont.render("Please Zero the cannon!",1,(255,255,0))

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.rotation = 0
camera.brightness = 65
camera.contrast = 50
camera.exposure_mode = 'night'

button_left = pygbutton.PygButton((50, 400, 80, 50), 'Left')
button_right = pygbutton.PygButton((510, 400, 80, 50), 'right')
button_fire = pygbutton.PygButton((270, 390, 100, 60), 'FIRE')
button_cal = pygbutton.PygButton((270, 20, 100, 60), 'ZERO')
zeroed = False
offset = 0

try:
   while(True):

      for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
		if 'click' in button_left.handleEvent(event):
			if pos > (offset -1000):
				motorRotateDegree([400,00],[-30,0],[PORT_B,PORT_C])
            			BrickPiUpdateValues()
				pos = BrickPi.Encoder[PORT_B]
      				labelPos = myfont.render(str(pos),1,(255,255,0))
      				pygame.draw.rect(screen, BLACK, (20, 20, 200,50))
      				screen.blit (labelPos, (20,20))
			else:
      				labelPos = myfont.render(str(pos),1,RED)
      				pygame.draw.rect(screen, BLACK, (20, 20, 200,50))
      				screen.blit (labelPos, (20,20))
		if 'click' in button_right.handleEvent(event):
			if pos < (1000 + offset):
				motorRotateDegree([400,00],[30,0],[PORT_B,PORT_C])
            			BrickPiUpdateValues()
				pos = BrickPi.Encoder[PORT_B]
      				labelPos = myfont.render(str(pos),1,(255,255,0))
      				pygame.draw.rect(screen, BLACK, (20, 20, 200,50))
      				screen.blit (labelPos, (20,20))
			else:
      				labelPos = myfont.render(str(pos),1,RED)
      				pygame.draw.rect(screen, BLACK, (20, 20, 200,50))
      				screen.blit (labelPos, (20,20))
		if 'click' in button_fire.handleEvent(event):
			motorRotateDegree([0,255],[0,260],[PORT_B,PORT_C])
            		time.sleep(.1)
		if 'click' in button_cal.handleEvent(event):
			zeroed = True
            		BrickPiUpdateValues()
			offset = BrickPi.Encoder[PORT_B] 
      			labelPos = myfont.render(str(pos),1,GREEN)
      			pygame.draw.rect(screen, BLACK, (20, 20, 200,50))
      			screen.blit (labelPos, (20,20))
      button_left.draw(screen)
      button_right.draw(screen)
      button_cal.draw(screen)
      stream = io.BytesIO()
      camera.capture(stream, format='jpeg')
      stream.seek(0)
      
      image = pygame.image.load(stream,'jpeg')
      stream.close()
      
     # image = pygame.transform.scale(image.convert(), screenSize)
      image = pygame.transform.scale(image.convert(), (320,240))
      
      screen.blit (image, (160,100))
      screen.blit (crosshairs, (220,120))
      if zeroed:
      	button_fire.draw(screen)
      else:
     	 screen.blit(warn1,(170, 150))
      pygame.display.update()
      FPSCLOCK.tick(FPS)   
   #   clock.tick(-1)
   #   print (clock.get_fps())

finally:
   camera.close()
