#codepylet.platforms.py
import math, random, sys
import pygame
from pygame.locals import *

# exit the program
def events():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.mixer.music.stop()
			pygame.quit()
			sys.exit()

class platform:
	def __init__(self, x, y, width):
		self.x1 = x
		self.y = y
		self.x2 = x + width

	def test(self, player):
		print ("player x %d player y %d  platform1x: %d  platformx2 %d  platformY %d" % (player.x, player.y, self.x1, self.x2, self.y))
		# am I going to fall off the edge
		if (player.x + 50) < self.x1 or (player.x + 50) > self.x2:
			return None
#		standing/landing on a platform
#		if player.y <= self.y and player.y + player.velocity >= self.y:
#		if (player.y + pHeight) <= self.y and (player.y + pHeight) + player.vel >= self.y:
		if player.y + 100 <= self.y and player.y + 100  + player.vel >= self.y:
			return self
		return None

class platforms:
	def __init__(self):
		self.container = list([])

	def add(self, p):
		self.container.append(p)

	def testCollision(self, player):
		if not player.falling:
			return False
		for p in self.container:
			result = p.test(player)
			if result:
				print("collision with platform at y: %d" % p.y)
				player.falling = False
				player.currentPlatform = result
				# snap me back to the platform, plus my height.
				player.y = result.y - 100
				print("stop moving.")
				return True
		return False

	def draw(self):
		global WHITE
		display = pygame.display.get_surface()
		for p in self.container:
			pygame.draw.line(display, WHITE, (p.x1, p.y), (p.x2, p.y), 1)

	def do(self, player):
		self.testCollision(player)
		self.draw()


class player(object):
	walkRight = [pygame.image.load('img/DEATHR01.png'), pygame.image.load('img/DEATHR02.png'), pygame.image.load('img/DEATHR03.png')]
	walkLeft = [pygame.image.load('img/DEATHL01.png'), pygame.image.load('img/DEATHL02.png'), pygame.image.load('img/DEATHL03.png')]
	spReady = [pygame.image.load('img/SPECIAL01.PNG'), pygame.image.load('img/SPECIAL01.PNG'), pygame.image.load('img/SPECIAL02.PNG'),pygame.image.load('img/SPECIAL02.PNG'), pygame.image.load('img/SPECIAL03.PNG'), pygame.image.load('img/SPECIAL03.PNG')]
	spHover = [pygame.image.load('img/SPECIALHOVER01.PNG'), pygame.image.load('img/SPECIALHOVER02.PNG'), pygame.image.load('img/SPECIALHOVER03.PNG'), pygame.image.load('img/SPECIALHOVER04.PNG')]
	hoverFrames = spHover[::] + spHover[::-1] + spHover[::] + spHover[::-1] + spHover[::] + spHover[::-1]

	def __init__(self):
		self.stagePosX = 0
		# new stuff
		self.x = 0
		self.y = 0
		self.width = 50
		self.height = 100
		# a constant
		self.vel = 5
		# how much I should move on the X axis before rendering
		self.xVelocity = 0
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = True
		self.walkCount = 0
		self.standing = True
		self.specialRDY = False
		self.specialHVR = False
		self.frameCount = 0
		self.isBusy = False
		self.renderatX = 0
		self.jumping = False
		self.falling = True
		self.currentPlatform = None

	def keys(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and (not PLAYER.isBusy):
			print("swing")
			weapon.swing = True

		if keys[pygame.K_s] and (not PLAYER.isBusy):
				print("special")
				PLAYER.isBusy = True
				PLAYER.specialRDY = True

		if keys[pygame.K_LEFT]:
			self.xVelocity = -self.vel
			PLAYER.left = True
			PLAYER.right = False
			PLAYER.standing = False

		elif keys[pygame.K_RIGHT]:
			self.xVelocity = self.vel
			PLAYER.left = False
			PLAYER.right = True
			PLAYER.standing = False
		else:
			self.xVelocity = 0
			PLAYER.walkCount = 0

		if not PLAYER.isJump:
			if keys[pygame.K_UP]:
				PLAYER.isJump = True
				PLAYER.walkCount = 0
		else:
			if PLAYER.jumpCount >= -10:
				neg  = 1
				if PLAYER.jumpCount < 0:
					neg = -1
				PLAYER.y -= (PLAYER.jumpCount ** 2) * 0.5 * neg
				PLAYER.jumpCount -= 1
			else:
				PLAYER.isJump = False
				PLAYER.jumpCount = 10

	def move(self):
		if self.y > 1000:
			print("you fell off the world.")
			self.y, self.x, self.renderatX = 0,0,0
		print ("xvel %d  self.x %d self.renderatx %d" % (self.xVelocity, self.x, self.renderatX))
		# actually move player.x coordinate
		self.x += self.xVelocity
		if self.x > stageWidth - charWidth:
			self.x = stageWidth - self.vel
		if self.x < self.vel:
			self.x = self.vel
		# control the background
		if self.x < startScrollingPosX:
			self.renderatX = self.x
		elif self.x > (stageWidth - startScrollingPosX):
			self.renderatX = self.x - stageWidth + W
		else:
			self.renderatX = startScrollingPosX
			self.stagePosX += -self.xVelocity

		if self.currentPlatform:
			if not self.currentPlatform.test(self):
				self.falling = True
				self.currentPlatform = None
		# removed if jumping
		if self.falling:
			self.y += self.vel

	def draw(self):
		win = pygame.display.get_surface()
		if self.walkCount  + 1 >= 9:
			self.walkCount = 0

		if not (self.standing):
			if self.left:
				win.blit(self.walkLeft[self.walkCount // 3], (self.renderatX, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount // 3], (self.renderatX, self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(self.walkRight[self.walkCount // 3], (self.renderatX, self.y))
			else:
				win.blit(self.walkLeft[self.walkCount // 3], (self.renderatX, self.y))

	def renderSpReady(self):
		win = pygame.display.get_surface()
		if self.frameCount > 5:
			self.frameCount = 0
			self.specialRDY = False
			self.specialHVR = True
			specialSound.play()

		if self.specialRDY:
			print("rendering spReady frame %d" % self.frameCount)
			win.blit(self.spReady[self.frameCount], (PLAYER.renderatX, PLAYER.y))
			self.frameCount += 1

	def renderSpHover(self):
		win = pygame.display.get_surface()
		if self.frameCount >= len(self.hoverFrames):
			self.frameCount = 0
			self.specialRDY = False
			self.specialHVR = False
			self.isBusy = False

		if self.specialHVR and self.frameCount < len(self.hoverFrames):
			print("Rendering hover frame %d" % self.frameCount)
			win.blit(self.hoverFrames[self.frameCount], (PLAYER.renderatX, PLAYER.y))
			self.frameCount += 1

	def do(self):
		self.keys()
		self.move()
		if weapon.swing:
			weapon.draw()
			weaponSound.play()
		if self.specialRDY:
			self.renderSpReady()
		if self.specialHVR:
			self.renderSpHover()
# Not busy doing something else? Then he's probably moving or jumping.
# Draw him.
		if not self.isBusy:
			self.draw()
		HUD.draw()

class scythe(object):
	scytheLeft = [pygame.image.load('img/SCYTHEL01.png'), pygame.image.load('img/SWIPEL01.png'), pygame.image.load('img/SWIPEL01.png'), pygame.image.load('img/SWIPEL02.png'), pygame.image.load('img/SWIPEL02.png'), pygame.image.load('img/SWIPEL03.png'), pygame.image.load('img/SWIPEL03.png')]
	scytheRight = [pygame.image.load('img/SCYTHER01.png'), pygame.image.load('img/SWIPER01.png'), pygame.image.load('img/SWIPER01.png'), pygame.image.load('img/SWIPER02.png'), pygame.image.load('img/SWIPER02.png'), pygame.image.load('img/SWIPER03.png'), pygame.image.load('img/SWIPER03.png')]
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.swing = False
		self.frameCount = 0

	def draw(self):
		win = pygame.display.get_surface()
		if self.frameCount > 6:
			self.frameCount = 0
			self.swing = False

		if self.swing:
			if PLAYER.left:
				win.blit(self.scytheLeft[self.frameCount], (PLAYER.renderatX - 80, PLAYER.y + 25))
				self.frameCount += 1
			else:
				win.blit(self.scytheRight[self.frameCount], (PLAYER.renderatX + 45, PLAYER.y + 25))
				self.frameCount += 1

class hud(object):

	def __init__(self, x, y, player):
		self.x = x
		self.y = y
		self.healthCount = 100
		self.specialCount = 3
	
	def draw(self):
		win = pygame.display.get_surface()
		win.blit(hudimage, (self.x, self.y))

class titlescreen(object):
	def __init__(self):
		self.show = True

	def keys(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_p]:
			print("turn off title")
			pygame.mixer.music.stop()
			self.show = False
			#start the bgm
			bgm = pygame.mixer.music.load('audio/bgm.mp3')
			pygame.mixer.music.play(-1)


	def do(self):
		self.keys()
		if self.show:
			win = pygame.display.get_surface()
			win.blit(titleimage, (0,0))


# ----- MAIN BLOCK ------

pygame.init() 

# define display surface
W, H = 800, 600
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Reapy!")
FPS = 24

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
# some background set up
bg = pygame.image.load("img/hugeBG.png").convert()
bgWidth, bgHeight = bg.get_rect().size
stageWidth = bgWidth

titleimage = pygame.image.load('img/TITLE.png').convert()

hudimage = pygame.image.load('img/HUD.png').convert()
hudimage.set_colorkey((84,109,142))

weaponSound = pygame.mixer.Sound('audio/whoosh.wav')
specialSound = pygame.mixer.Sound('audio/thunder.wav')

# HW = W / 2 giving us 400 pixels on either side of player
startScrollingPosX = HW

charWidth = 100

playerPosX = 0
playerPosY = 0
playerVelocityX = 0
playerVelocityY = 0

PLAYER = player()
# PLAYER.setLocation(HW, 0)
weapon = scythe(0, 0)
HUD = hud(10,10,PLAYER)

PLATFORMS = platforms()
# floor 'platform'
PLATFORMS.add(platform(0, 150, 200))

PLATFORMS.add(platform(150, 400, 1000))
# crappy random platforms
#for i in range(0, 50):
#	PLATFORMS.add(platform(random.randint(0, W - 50), random.randint(50, H - 60), 50))

TITLESCREEN = titlescreen()
music = pygame.mixer.music.load("audio/TITLE.mp3")
pygame.mixer.music.play(1)

# play game	
while True:
	events()
	rel_x = PLAYER.stagePosX % bgWidth
	DS.blit(bg, (rel_x - bgWidth,0) )
	if rel_x < W:
		DS.blit(bg, (rel_x,0))
	if TITLESCREEN.show:
		TITLESCREEN.do()
	else:
		PLATFORMS.do(PLAYER)
		PLAYER.do()
		# background (moving)

	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)
