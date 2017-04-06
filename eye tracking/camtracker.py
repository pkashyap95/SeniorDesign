
DEBUG = False
# # # # #
# imports
import csv
import os.path


# Try to import VideoCapture Library
# Requires VideoCapture & PIL libraries
vcAvailable = False
import imp
try:
  imp.find_module('VideoCapture')
  vcAvailable = True
  import VideoCapture
except ImportError:
  print "VideoCapture module not available"

try:
	import pygame
	import pygame.camera
	pygame.init()
	pygame.camera.init()
except:
	raise Exception("Error in camtracker: PyGame could not be imported and initialized! :(")


# # # # #
# functions

def available_devices():
	
	"""Returns a list of available device names or numbers; each name or
	number can be used to pass as Setup's device keyword argument
	"""
	
	return pygame.camera.list_cameras()
	

# # # # #
# classes

class Setup:
	
	"""The Setup class provides means to calibrate your webcam to function
	as an eye tracker"""
	
	def __init__(self, device=None, camres=(640,480), disptype='window', dispres=(1024,768), display=None):
		
		"""Initializes a Setup instance
		"""
		
		# DEBUG #
		if DEBUG:
			self.savefile = open('data/savefile.txt','w')
		# # # # #

		# create new Display if none was passed, or use the provided display
		if display == None:
			if disptype == 'window':
				self.disp = pygame.display.set_mode(dispres, pygame.RESIZABLE)
			elif disptype == 'fullscreen':
				self.disp = pygame.display.set_mode(dispres, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
			else:
				raise Exception("Error in camtracker.Setup.__init__: disptype '%s' was not recognized; please use 'window', 'fullscreen'")
		# if a display was specified, use that
		else:
			self.disp = display
			dispres = self.disp.get_size()
		
		# select a device if none was selected
		if device == None:
			available = available_devices()
			if available == []:
				raise Exception("Error in camtracker.Setup.__init__: no available camera devices found (did you forget to plug it in?)")
			else:
				device = available[0]
		
		# create new camera
		self.tracker = CamEyeTracker(device=device, camres=camres)
		
		# find font: first look in directory, if that fails we fall back to default
		try:
			fontname = os.path.join(os.path.split(os.path.abspath(__file__))[0],'resources','roboto_regular-webfont.ttf')
		except:
			fontname = pygame.font.get_default_font()
			print("WARNING: camtracker.Setup.__init__: could not find 'roboto_regular-webfont.ttf' in the resources directory!")
		# create a Font instance
		self.font = pygame.font.Font(fontname, 24)
		self.sfont = pygame.font.Font(fontname, 12)
		
		# set some properties
		self.disptype = disptype
		self.dispsize = dispres
		self.fgc = (255,255,255)
		self.bgc = (0,0,0)
		
		# fill display with background colour
		self.disp.fill(self.bgc)

		# set some more properties
		self.img = pygame.surface.Surface(self.tracker.get_size())	# empty surface, gets filled out with camera images
		self.settings = {       'threshold':96, \
					'nonthresholdcol':(100,100,255,255), \
					'pupilpos': (camres[0]/2,camres[1]/2), \
					'pupilrect':pygame.Rect(camres[0]/2-50,camres[1]/2-25,100,50), \
					'pupilbounds': [0,0,0,0], \
					'':None					
					}
	
	
	def start(self):
		
		"""Starts running the GUI
		"""

		
		
		# DEBUG #
		if DEBUG:
			self.savefile.write(pygame.image.tostring(self.disp,'RGB')+BUFFSEP)
		# # # # #
		
		# create GUI
		self.setup_GUI()
		
		
		# DEBUG #
		if DEBUG:
			self.savefile.write(pygame.image.tostring(self.disp,'RGB')+BUFFSEP)
		# # # # #

		# draw general GUI (no stage information yet)
		self.draw_stage(stagenr=None)
		
		# DEBUG #
		if DEBUG:
			self.savefile.write(pygame.image.tostring(self.disp,'RGB')+BUFFSEP)
		# # # # #
		
		# mouse visibility
		pygame.mouse.set_visible(True)
		
		# start setup (should return a CamEyeTracker instance)
		tracker = self.run_GUI()
		
		return tracker
		
	
	
	
	def setup_GUI(self):
		
		"""Sets up a GUI interface within a PyGame Surface
		"""
		
		# directory
		resdir = os.path.join(os.path.split(os.path.abspath(__file__))[0],'resources')
		if not os.path.exists(resdir):
			raise Exception("Error in camtracker.Setup.setup_GUI: could not find 'resources' directory to access button images; was it relocated or renamed, or is the installation of camtracker incorrect?")
		
		# find image paths
		imgpaths = {}
		buttnames = ['1','up','down','t','space','r','escape']
		buttstates = ['active','inactive']
		for bn in buttnames:
			imgpaths[bn] = {}
			for bs in buttstates:
				filename = "%s_%s.png" % (bn,bs)
				imgpaths[bn][bs] = os.path.join(resdir,filename)
				if not os.path.isfile(imgpaths[bn][bs]):
					print("WARNING: image file '%s' was not found in resources!" % filename)
					imgpaths[bn][bs] = os.path.join(resdir,"blank_%s.png" % bs)
		
		# image positions (image CENTERS!)
		buttsize = (50,50)
		camres = self.tracker.get_size()
		buttpos = {}
		y = self.dispsize[1]/2 + int(camres[1]*0.6)
		buttpos['1'] = int(self.dispsize[0]*(3/6.0) - buttsize[0]/2), y
               
		buttpos['space'] = int(self.dispsize[0]*(5/6.0) - buttsize[0]/2), y
		
		leftx = self.dispsize[0]/2 - (camres[0]/2 + buttsize[0]) # center of the buttons on the right
		rightx = self.dispsize[0]/2 + camres[0]/2 + buttsize[0] # center of the buttons on the left
		buttpos['up'] = rightx, self.dispsize[1]/2-buttsize[1] # above snapshot half, to the right
		buttpos['down'] = rightx, self.dispsize[1]/2+buttsize[1] # below snapshot half, to the right
		buttpos['t'] = leftx, self.dispsize[1]/2+camres[1]/2-buttsize[1]/2 # same level as snapshot bottom, to the left
		buttpos['r'] = leftx, self.dispsize[1]/2 # halfway snapshot (==halfway display), to the left
		buttpos['escape'] = buttsize[0], buttsize[1] # top left
		
                # new dict for button properties (image, position, and rect)
		self.buttons = {}
		# loop through button names
		for bn in imgpaths.keys():
			# new dict for this button name
			self.buttons[bn] = {}
			# recalculate position
			buttpos[bn] = buttpos[bn][0]-buttsize[0]/2, buttpos[bn][1]-buttsize[1]/2
			# loop through button states
			for bs in imgpaths[bn].keys():
				# new dict for this button name and this button state
				self.buttons[bn][bs] = {}
				# load button image
				self.buttons[bn][bs]['img'] = pygame.image.load(imgpaths[bn][bs])
				# save position and rect
				self.buttons[bn][bs]['pos'] = buttpos[bn]
				self.buttons[bn][bs]['rect'] = buttpos[bn][0], buttpos[bn][1], buttsize[0], buttsize[1]
		
		
                
		# save buttsize
		self.buttsize = buttsize
	
	
	def draw_button(self, image, pos):
		
		"""Draws a button on the display
		"""
		
		self.disp.blit(image, pos)
	
	
	def draw_stage(self, stagenr=None):
		
		"""Draws the GUI window for the passed stage 
		"""
		
		# clear display
		self.disp.fill(self.bgc)
		
		# universal buttons
		buttonstodraw = ['1','space','escape','t','r']
		activetodraw = []
		
		# stage specific buttons
		if stagenr == 1:
			title = "running the program"
			buttonstodraw.extend(['up','down'])
			activetodraw.extend(['1'])
		

		else:
			title = "loading, please wait..."

		# draw inactive buttons
		for buttname in buttonstodraw:
			self.draw_button(self.buttons[buttname]['inactive']['img'],self.buttons[buttname]['inactive']['pos'])
		
		# draw active buttons
		for buttname in activetodraw:
			self.draw_button(self.buttons[buttname]['active']['img'],self.buttons[buttname]['active']['pos'])
		
		# draw title
		titsize = self.font.size(title) 
		titpos = self.dispsize[0]/2-titsize[0]/2, self.dispsize[1]/2-(self.tracker.get_size()[1]/2+titsize[1])
		titsurf = self.font.render(title, True, self.fgc)
		self.disp.blit(titsurf,titpos)
	

	def run_GUI(self):
		
		"""Perform a setup to set all settings using a GUI
		"""
		
		# # # # #
		# variables
		
		# general
		stage = 1 # stage is updated by handle_input functions
		
		# stage specific
		stagevars = {}
		
                stagevars[0] = {}
		stagevars[0]['show_threshimg'] = False # False for showing snapshots, True for showing thresholded snapshots
		stagevars[0]['use_prect'] = True # False for no pupil search limits, True for pupul rect
		
                stagevars[1] = {}
		stagevars[1]['thresholdchange'] = None # None, 'up', or 'down'
		
		stagevars[2] = {}
		stagevars[2]['prectsize'] = 100,50 # pupilrectsize
		stagevars[2]['prect'] = pygame.Rect(255,255,stagevars[2]['prectsize'][0],stagevars[2]['prectsize'][1]) # rect around pupil, in which the pupil is expected to be
		stagevars[2]['confirmed'] = False
               
         
		# set Booleans
		running = True			# turns False upon quiting the GUI
		
		# set image variables
		imgsize = self.img.get_size()
		blitpos = (self.dispsize[0]/2-imgsize[0]/2, self.dispsize[1]/2-imgsize[1]/2)
		
		# # # # #
		# run GUI
		while running:
			
			# # # # #
			# general
			
			# draw stage
			self.draw_stage(stagenr=stage)
			
			# get new snapshot, thresholded image, and pupil measures (only use pupil bounding rect after stage 1)
			useprect = stagevars[0]['use_prect'] and stage > 1
			self.img, self.thresholded, pupilpos, pupilsize, pupilbounds = self.tracker.give_me_all(pupilrect=useprect)
			
			# update settings
			self.settings = self.tracker.settings
	
			# check if the thresholded image button is active
			if stagevars[0]['show_threshimg']:
				# draw active button
				self.draw_button(self.buttons['t']['active']['img'], self.buttons['t']['active']['pos'])
			# if threshold button is not active, draw inactive button
			else:
				self.draw_button(self.buttons['t']['inactive']['img'], self.buttons['t']['inactive']['pos'])
	
			# check if the thresholded image button is active
			if stagevars[0]['use_prect']:
				# draw active button
				self.draw_button(self.buttons['r']['active']['img'], self.buttons['r']['active']['pos'])
			# if threshold button is not active, draw inactive button
			else:
				self.draw_button(self.buttons['r']['inactive']['img'], self.buttons['r']['inactive']['pos'])

			# check for input
			inp, inptype = self.check_input()
			
			# handle input, according to the stage (this changes the stagevars!)
			stage, stagevars = self.handle_input(inptype, inp, stage, stagevars)
			
			# # # # #
			# stage specific
			
			# stage 1: setting pupil threshold
			if stage == 1:
				# set camera threshold
				if stagevars[1]['thresholdchange'] != None:
					if stagevars[1]['thresholdchange'] == 'up' and self.settings['threshold'] < 255:
						self.settings['threshold'] += 3
					elif stagevars[1]['thresholdchange'] == 'down' and self.settings['threshold'] > 0:
						self.settings['threshold'] -= 3
					stagevars[1]['thresholdchange'] = None
			
			

				# draw pupil rect
				pygame.draw.rect(self.img, (0,0,255), self.settings['pupilrect'], 2)
				pygame.draw.rect(self.thresholded, (0,0,255), self.settings['pupilrect'], 2)
	
				# draw pupil center and pupilbounds in image
				try: pygame.draw.rect(self.img, (0,255,0),pupilbounds,1); pygame.draw.rect(self.thresholded, (0,255,0),pupilbounds,1)
				except: print("pupilbounds=%s" % pupilbounds)
				try: pygame.draw.circle(self.img, (255,0,0),pupilpos,3,0); pygame.draw.circle(self.thresholded, (255,0,0),pupilpos,3,0)
				except: print("pupilpos=%s" % pupilpos)
                                if stagevars[2]['confirmed']:
                                    running = False
                        
                                csvfile = file('eyeposition.csv','a')
                                writer = csv.writer(csvfile)
                                writer.writerow(self.settings['pupilpos'])
                             
			          

			# draw values
			starty = self.dispsize[1]/2 - imgsize[1]/2
			vtx = self.dispsize[0]/2 - imgsize[0]/2 - 10 # 10 isa
			vals = ['threshold', str(self.settings['threshold']), 'pupil position', str(self.settings['pupilpos']), 'pupil rect', str(self.settings['pupilrect'])]
                        
			for i in range(len(vals)):
				# draw title
				tsize = self.sfont.size(vals[i])
				tpos = vtx-tsize[0], starty+i*20
				tsurf = self.sfont.render(vals[i], True, self.fgc)
				self.disp.blit(tsurf,tpos)
			
			# draw new image
			if stagevars[0]['show_threshimg']:
				self.disp.blit(self.thresholded, blitpos)
			else:
				self.disp.blit(self.img, blitpos)

			# update display
			pygame.display.flip()

			# apply settings
			self.tracker.settings = self.settings
		        
                        
			# DEBUG #
			if DEBUG:
				self.savefile.write(pygame.image.tostring(self.disp,'RGB')+BUFFSEP)
			# # # # #
		
		# DEBUG #
		if DEBUG:
			# close savefile
			self.savefile.close()
			# message
			print("processing images...")
			# open savefile
			savefile = open('data/savefile.txt','r')
			# read ALL contents in once, then close file again
			raw = savefile.read()
			savefile.close()
			# split based on newlines (this leaves one empty entry, because of the final newline)
			raw = raw.split(BUFFSEP)
			# process strings and save image
			for framenr in range(len(raw)-1):
				img = pygame.image.fromstring(raw[framenr],self.dispsize,'RGB')
			pygame.image.save(img,'data/frame%d.png' % framenr)
		# # # # #
		
		return self.tracker

			
	def check_input(self):
		
		"""Checks if there is any keyboard or mouse input, then returns
		input (keyname or clickposition) and inptype ('mouseclick' or
		'keypress') or None, None when no input is registered
		"""
		
		# if nothing happens, None should be returned
		inp = None
		inptype = None
		
		# check events in queue
		for event in pygame.event.get():
			# mouseclicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				inp = pygame.mouse.get_pos()
				inptype = 'mouseclick'
			# keypresses
			elif event.type == pygame.KEYDOWN:
				inp = pygame.key.name(event.key)
				inptype = 'keypress'

		return inp, inptype
	
	
	def handle_input(self, inptype, inp, stage, stagevars):
		
		"""Checks the input, compares this with what is possible in the
		current stage, then returns adjusted stage and adjusted stage
		variables
		"""
		
		# # # # #
		# mouseclicks to keypress value
		
		if inptype == 'mouseclick':
			
			# click position
			pos = inp[:]
			
			# loop through buttons
			for bn in self.buttons.keys():
				# check if click position is on a button
				r = self.buttons[bn]['inactive']['rect']
				if pos[0] > r[0] and pos[0] < r[0]+r[2] and pos[1] > r[1] and pos[1] < r[1]+r[3]:
					# change input to button name
					inp = bn
					# break from loop (we don't want to loop through all the other buttons once we've found the clicked one)
					break
		
		# # # # #
		# keypress (or simulated keypress) handling
		
		# stage 1
		if stage == 1:
			# up should increase threshold, down should decrease threshold
			if inp in ['up','down']:
				stagevars[1]['thresholdchange'] = inp
		
			
		# space should move to next stage (but not in stage 3)
		if inp == 'space' and stage < 2:
		       stagevars[2]['confirmed'] = True
		       #stage += 1
               
		# T should toggle between displays
		if inp == 't':
			if stagevars[0]['show_threshimg']:
				stagevars[0]['show_threshimg'] = False
			else:
				stagevars[0]['show_threshimg'] = True
		
		# R should toggle between using pupil rect or not
		if inp == 'r':
			if stagevars[0]['use_prect']:
				stagevars[0]['use_prect'] = False
			else:
				stagevars[0]['use_prect'] = True
		
		# escape should close down
		if inp == 'escape':
			pygame.display.quit()
			raise Exception("camtracker.Setup: Escape was pressed")
		
		# return the changed variables
		return stage, stagevars


class CamEyeTracker:
	
	"""The CamEyeTracker class uses your webcam as an eye tracker"""
	
	def __init__(self, device=None, camres=(640,480)):
		
		"""Initializes a CamEyeTracker instance
		"""

		global vcAvailable
		if vcAvailable == False:
			# select a device if none was selected
			if device == None:
				available = available_devices()
				if available == []:
					raise Exception("Error in camtracker.CamEyeTracker.__init__: no available camera devices found (did you forget to plug it in?)")
				else:
					device = available[0]
			
			# start the webcam
			self.cam = pygame.camera.Camera(device, camres, 'RGB')
			self.cam.start()
		else:
			self.cam = VideoCapture.Device()
			
		# get the webcam resolution (get_size not available on all systems)
		try:
			self.camres = self.cam.get_size()
		except:
			self.camres = camres

		# default settings
		self.settings = {'pupilcol':(0,0,0), \
					'threshold':96, \
					'nonthresholdcol':(100,100,255,255), \
					'pupilpos':(-1,-1), \
					'pupilrect':pygame.Rect(self.camres[0]/2-50,self.camres[1]/2-25,100,50), \
					'pupilbounds': [0,0,0,0], \
					'':None					
					}
	
	
	def get_size(self):
		
		"""Returns a (w,h) tuple of the image size
		"""
		return self.camres

	
	def get_snapshot(self):
		
		"""Returns a snapshot, without doing any any processing
		"""
		global vcAvailable
		if vcAvailable:
			image = self.cam.getImage()
			mode = image.mode
			size = image.size
			data = image.tostring()
			return pygame.image.fromstring(data, size, mode)
		else:
			return self.cam.get_image()
		
		
	def threshold_image(self, image):
		
		"""Applies a threshold to an image and returns the thresholded
		image
		"""
		
		# surface to apply threshold to surface
		thimg = pygame.surface.Surface(self.get_size(), 0, image)
		
		# perform thresholding
		th = (self.settings['threshold'],self.settings['threshold'],self.settings['threshold'])
		pygame.transform.threshold(thimg, image, self.settings['pupilcol'], th, self.settings['nonthresholdcol'], 1)
		
		return thimg
	
	
	def find_pupil(self, thresholded, pupilrect=False):
		
		"""Get the pupil center, bounds, and size, based on the thresholded
		image; please note that the pupil bounds and size are very
		arbitrary: they provide information on the pupil within the
		thresholded image, meaning that they would appear larger if the
		camera is placed closer towards a subject, even though the
		subject's pupil does not dilate
		"""
		
		
		# cut out pupilrect (but only if pupil bounding rect option is on)
		if pupilrect:
			# pupil rect boundaries
			rectbounds = pygame.Rect(self.settings['pupilrect'])
			# correct rect edges that go beyond image boundaries
			if self.settings['pupilrect'].left < 0:
				rectbounds.left = 0
			if self.settings['pupilrect'].right > self.camres[0]:
				rectbounds.right = self.camres[0]
			if self.settings['pupilrect'].top < 0:
				rectbounds.top = 0
			if self.settings['pupilrect'].bottom > self.camres[1]:
				rectbounds.bottom = self.camres[1]
			# cut rect out of image
			thresholded = thresholded.subsurface(rectbounds)
			ox, oy = thresholded.get_offset()
		
		# find potential pupil areas based on threshold
		th = (self.settings['threshold'],self.settings['threshold'],self.settings['threshold'])
		mask = pygame.mask.from_threshold(thresholded, self.settings['pupilcol'], th)
		
		# get largest connected area within mask (which should be the pupil)
		pupil = mask.connected_component()
		
		# get pupil center
		pupilcenter = pupil.centroid()
		
		# if we can only look within a rect around the pupil, do so
		if pupilrect:
			# compensate for subsurface offset
			pupilcenter = pupilcenter[0]+ox, pupilcenter[1]+oy
			# check if the pupil position is within the rect
			if (self.settings['pupilrect'].left < pupilcenter[0] < self.settings['pupilrect'].right) and (self.settings['pupilrect'].top < pupilcenter[1] < self.settings['pupilrect'].bottom):
				# set new pupil and rect position
				self.settings['pupilpos'] = pupilcenter
				x = pupilcenter[0] - self.settings['pupilrect'][2]/2
				y = pupilcenter[1] - self.settings['pupilrect'][3]/2
				self.settings['pupilrect'] = pygame.Rect(x,y,self.settings['pupilrect'][2],self.settings['pupilrect'][3])
			# if the pupil is outside of the rect, return missing
			else:
				self.settings['pupilpos'] = (-1,-1)
		else:
			self.settings['pupilpos'] = pupilcenter
		
		# get pupil bounds (sometimes failes, hence try-except)
		try:
			self.settings['pupilbounds'] = pupil.get_bounding_rects()[0]
			# if we're using a pupil rect, compensate offset
			if pupilrect:
				self.settings['pupilbounds'].left += ox
				self.settings['pupilbounds'].top += oy
		except:
			# if it fails, we simply use the old rect
			pass
		
		return self.settings['pupilpos'], pupil.count(), self.settings['pupilbounds']
	
	
	def give_me_all(self, pupilrect=False):
		
		"""Returns snapshot, thresholded image, pupil position, pupil area,
		and pupil bounds
		"""
		
		img = self.get_snapshot()
		thimg = self.threshold_image(img)
		ppos, parea, pbounds = self.find_pupil(thimg, pupilrect)
		
		return img, thimg, ppos, parea, pbounds


	
	def close(self):
		
		"""Shuts down connection to the webcam and closes logfile
		"""
		
		# close camera
		self.cam.stop()
                csvfile.close()
