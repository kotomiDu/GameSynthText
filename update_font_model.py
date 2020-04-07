# Author: Ankush Gupta
# Date: 2015
"Script to generate font-models."

import pygame
from pygame import freetype
from text_utils import FontState
import numpy as np 
import matplotlib.pyplot as plt 
import _pickle as cp

def start():
	pygame.init()


	ys = np.arange(8,200)
	A = np.c_[ys,np.ones_like(ys)]

	xs = []
	models = {} #linear model

	FS = FontState()
	#plt.figure()
	#plt.hold(True)
	for i in range(len(FS.fonts)):
		
		font = freetype.Font(FS.fonts[i],size=40)
		print(font.size,font.get_sized_height)
		h = []
		for y in ys:
			h.append(font.get_sized_glyph_height(float(y)))
		h = np.array(h)
		#print(h)
		m,_,_,_ = np.linalg.lstsq(A,h)
		models[font.name] = m
		xs.append(h)
		#print(font.name)

	with open('data/models/font_px2pt.cp','wb') as f:
		cp.dump(models,f)
	#plt.plot(xs,ys[i])
	#plt.show()

#general_text = u"大吉大利，今晚吃鸡"
general_text = "WINNER WINNER CHICKEN DINNER"
from pathlib import Path
from pygame.locals import *
import glob 
def show_text():
	SCREEN_WIDTH = 600
	SCREEN_HEIGHT = 800
	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


	text = ""
	fonts = []
	#text_surface = []
	fontsize = 26
	fontlist = glob.glob("C:\\Users\\yarudu\\Documents\\project\\synth_tool\\SynthText\\data\\fonts\\game_font\\*")
	for i,fontfile in enumerate(fontlist):
		#font = freetype.Font(FS.fonts[i], size=12)
		font = pygame.font.Font(fontfile, fontsize)
		fonts.append(font)
		text = Path(fontfile).stem
		text += " " + general_text 
		textimage = font.render(text, True,  [0, 0, 0], [255, 255, 255])
		#text_surface.append(textimage.subsurface(pygame.Rect(10, (i+1)*fontsize  , len(text)*10, fontsize )))
		#pygame.image.save(image,'temp.jpeg')
		screen.blit(textimage,pygame.Rect(10, (i+1)*fontsize  , len(text)*10, fontsize ))
		#if i == 3:
		#	break
	pygame.display.set_caption("Text Font")
	pygame.display.update()
	while True:													
		for event in pygame.event.get():					
			if event.type == QUIT:							
				return

	
if __name__ == '__main__':
	#show_text()
	start()