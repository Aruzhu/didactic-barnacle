import pygame.camera
import pygame
from pygame.locals import *
import time
class Analyse(object):
	def main(self):	
		from PIL import Image
		img = Image.open('img.png')
		pix = img.load()
		
		sum = 0
		for x in range(1, img.size[0]):
			for y in range(1, img.size[1]):
				sum += pix[x,y][0]*0.2126 + pix[x,y][1]*0.7152 + pix[x,y][2]*0.0722
		
		precent = float( (100*(sum/(img.size[0]*img.size[1]) )) /255 )
		print (precent, precent*0.05+ 20.19)
		img.close()
		return precent

class Capture(object):
	def __init__(self):
		self.size = (640,480)
		self.display = pygame.display.set_mode(self.size, 0)
		
		self.clist = pygame.camera.list_cameras()
		if not self.clist:
			raise ValueError("Sorry, no cameras detected.")
		self.cam = pygame.camera.Camera(self.clist[0], self.size, "YUV")
		self.cam.start()
		
		self.cam.set_controls(brightness=0)

		self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

	def get_and_flip(self):
		timestart = time.time()
		self.snapshot = self.cam.get_image(self.snapshot)
		timeused = time.time()-timestart

		#save image
		pygame.image.save(self.snapshot, "img.png")
		self.display.blit(self.snapshot, (0,0))
		pygame.display.flip()
		return timeused
	def main(self): 
		going = True
		timeused = 1
		while going:
			events = pygame.event.get()
			
			for e in events:
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					# close the camera safely
					self.cam.stop()
					going = False
					
				if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
					timeused = self.get_and_flip()
					anal = Analyse().main()
		
					
			# print str( (50*0.210)/(timeused*43 ) ) + "	" + str(timeused)
pygame.camera.init()
cam = Capture()
cam.main()