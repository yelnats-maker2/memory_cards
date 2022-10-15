import pygame
import mempuzzle
from mpuzzle_const import *


class Animation:

    def __init__(self, xfps = 10):
        self.images = [] #list of surfaces to display
        self.imagecount = 0 #size of image list
        self.xpos = 0 #where to draw, x
        self.ypos = 0 #where to draw, y
        self.swidth = 0 #width for sprite sheet images
        self.sheight = 0 #height for sprite sheet images
        self.srow = 0 #row for sprite sheet images.
        self.current = 0 #index for the image list. acts as column for a sprite sheet.
        self.xcurrent = 0 #current multiplied by xfps, this lets you change the speed of animation.
        self.xfps = xfps

    def adv(self):
        """advance current sequentially and loop around to 0
        actually only keeps incrementing xcurrent until xcurrent % xfps == 1, in other words lets you slow down the animation by a factor of self.xfps to help deal with high framerates"""
        if self.current < self.imagecount - 1:
            self.xcurrent += 1
            if self.xcurrent % self.xfps == 0:
                self.current += 1
        else:
            self.current = 0
            self.xcurrent = 0

    def draw(self, surf):
        surf.blit(self.images[self.current], (self.xpos, self.ypos))

    def draw_ssheet(self, surf):
        """spritesheet version of draw. row is chosen at load time, column is assumed to be swidth * current"""
        surf.blit(self.images, (self.xpos, self.ypos), (self.swidth * self.current, self.sheight * self.srow, self.swidth, self.sheight))
        
    
    def load(self, imglist):
        """takes a list of strings (imglist) and turns them into pygame surfaces. If there was already a list loaded that list is cleared."""
        self.imagecount = 0
        self.images = []
        for i in imglist:
            self.imagecount += 1
            self.images.append(pygame.image.load(i))

    def load_ssheet(self, ssheet, swidth, sheight, srow, count):
        """load a sprite sheet instead of a list of images, now images will just be 1 image. 
        string ssheet: the file to load as an image
        int swidth, sheight: width and height in pixels of the individual frames in the spritesheet
        srow: the row containing a particular animation (this function assumes the spritesheet is laid out with the animation going through rows) 0 BASED INDEX
        count: how many frames of animation are in the row, or, how many columns that row has. 0 BASED"""
        self.imagecount = count
        self.swidth = swidth
        self.sheight = sheight
        self.images = pygame.image.load(ssheet)
        self.srow = srow

        
    def setpos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def getpos(self):
        return (self.xpos, self.ypos)
    

class Mpuzzle_render:

    FPS = 30 # frames per second, the general speed of the program
    WINDOWWIDTH = 640 # size of window's width in pixels
    WINDOWHEIGHT = 480 # size of windows' height in pixels
    REVEALSPEED = 8 # speed boxes' sliding reveals and covers
    BOXSIZE = 30 # size of box height & width in pixels
    GAPSIZE = 15 # size of gap between boxes in pixels

    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.displaySurf = None
        self.titletext = "memory game!!!"
        self.timeclock = None
        self.xmargin = int((Mpuzzle_render.WINDOWWIDTH - (self.gamestate.BOARDWIDTH * (Mpuzzle_render.BOXSIZE + Mpuzzle_render.GAPSIZE))) / 2)
        self.ymargin = int((Mpuzzle_render.WINDOWHEIGHT - (self.gamestate.BOARDHEIGHT * (Mpuzzle_render.BOXSIZE + Mpuzzle_render.GAPSIZE))) / 2)
        self.boxRects = self.initBoxes()


    def initBoxes(self):
        """create a 2d array containing rectangles for each box on the screen"""
        rects = []
        for x in range(self.gamestate.BOARDWIDTH):
            rects.append([])
            for y in range(self.gamestate.BOARDHEIGHT):
                left = x * (Mpuzzle_render.BOXSIZE + Mpuzzle_render.GAPSIZE) + self.xmargin
                top = y * (Mpuzzle_render.BOXSIZE + Mpuzzle_render.GAPSIZE) + self.ymargin
                rects[x].append( pygame.Rect(left, top, Mpuzzle_render.BOXSIZE, Mpuzzle_render.BOXSIZE) )
        return rects

    def getBoxAtPixel(self, x, y):
        """returns a tuple of board coordinates (x, y) or None if no box is there"""
        for i in range(len(self.boxRects)):
            for j in range(len(self.boxRects[i])):
                if self.boxRects[i][j].collidepoint(x, y):
                    return (i, j)
        return None

    def initScreen(self):
        """initialize pygame"""
        pygame.init()
        self.displaySurf = pygame.display.set_mode((Mpuzzle_render.WINDOWWIDTH, Mpuzzle_render.WINDOWHEIGHT))
        pygame.display.set_caption(self.titletext)
        self.timeclock = pygame.time.Clock()
        self.mainfont = pygame.font.Font(None, 32)
        self.losetext = self.mainfont.render("you lose! please quit!!", True, RED)
        self.wintext = self.mainfont.render("you win! you can quit now!!", True, GREEN)
    def drawBoard(self):
        self.displaySurf.fill(BGCOLOR)
        for boxx in range(len(self.boxRects)):
            for boxy in range(len(self.boxRects[boxx])):
                pygame.draw.rect(self.displaySurf, BOXCOLOR, self.boxRects[boxx][boxy])
                if self.gamestate.getRevealed(boxx, boxy) or self.gamestate.selection1 == (boxx, boxy) or self.gamestate.selection2 == (boxx, boxy):
                    shape, color = self.gamestate.getShapeAndColor(boxx, boxy)
                    self.drawIcon(shape, color, boxx, boxy)

    def drawLoseScreen(self):
        self.displaySurf.fill(BGCOLOR)
        self.displaySurf.blit(self.losetext, (Mpuzzle_render.WINDOWWIDTH//2, Mpuzzle_render.WINDOWHEIGHT//2))
        

    def drawWinScreen(self):
        self.displaySurf.fill(BGCOLOR)
        self.displaySurf.blit(self.wintext, (Mpuzzle_render.WINDOWWIDTH//2, Mpuzzle_render.WINDOWHEIGHT//2))
        
    def drawHighlightBox(self, boxx, boxy):
        thickness = 4
        highlightx = Mpuzzle_render.GAPSIZE // 3
        highlighty = Mpuzzle_render.GAPSIZE // 3
        rect = self.boxRects[boxx][boxy]
        highlightBox = pygame.Rect(rect.left - highlightx, rect.top - highlighty, rect.width + highlightx, rect.height + highlighty)
        pygame.draw.rect(self.displaySurf, HIGHLIGHTCOLOR, highlightBox, thickness)

    def drawIcon(self, shape, color, boxx, boxy):
        quarter = int(Mpuzzle_render.BOXSIZE * 0.25) # syntactic sugar
        half =    int(Mpuzzle_render.BOXSIZE * 0.5)  # syntactic sugar

        rect = self.boxRects[boxx][boxy] # get pixel coords from board coords
        left, top = rect.left, rect.top
        # Draw the shapes
        if shape == DONUT:
            pygame.draw.circle(self.displaySurf, color, (left + half, top + half), half - 5)
            pygame.draw.circle(self.displaySurf, BGCOLOR, (left + half, top + half), quarter - 5)
        elif shape == SQUARE:
            pygame.draw.rect(self.displaySurf, color, (left + quarter, top + quarter, Mpuzzle_render.BOXSIZE - half, Mpuzzle_render.BOXSIZE - half))
        elif shape == DIAMOND:
            pygame.draw.polygon(self.displaySurf, color, ((left + half, top), (left + Mpuzzle_render.BOXSIZE - 1, top + half), (left + half, top + Mpuzzle_render.BOXSIZE - 1), (left, top + half)))
        elif shape == LINES:
            for i in range(0, Mpuzzle_render.BOXSIZE, 4):
                pygame.draw.line(self.displaySurf, color, (left, top + i), (left + i, top))
                pygame.draw.line(self.displaySurf, color, (left + i, top + Mpuzzle_render.BOXSIZE - 1), (left + Mpuzzle_render.BOXSIZE - 1, top + i))
        elif shape == OVAL:
            pygame.draw.ellipse(self.displaySurf, color, (left, top + quarter, Mpuzzle_render.BOXSIZE, half))

    def tick(self):
        self.timeclock.tick(Mpuzzle_render.FPS)
                
        
    
        
