import random
from mpuzzle_const import *
class Mpuzzle_state:

    BOARDWIDTH = 4
    BOARDHEIGHT = 5

    #game states
    MODE_START = 0
    MODE_PLAYING = 1 #on the screen with the boxes before winning
    MODE_WON = 2 #victory screen
    MODE_LOST = 3 #lose
    #class functions
    def getRandomizedBoard():
        """ Get a list of every possible shape in every possible color.
        list format: board[x][y][z]
        x = x coordinate of box
        y = y coordinate of box
        z = list: [(shape, color), revealed] where revealed is a bool"""
        icons = []
        for color in ALLCOLORS:
            for shape in ALLSHAPES:
                icons.append( (shape, color) )

        random.shuffle(icons) # randomize the order of the icons list
        numIconsUsed = int(Mpuzzle_state.BOARDWIDTH * Mpuzzle_state.BOARDHEIGHT / 2) # calculate how many icons are needed
        icons = icons[:numIconsUsed] * 2 # make two of each
        random.shuffle(icons)

        # Create the board data structure, with randomly placed icons.
        board = []
        for x in range(Mpuzzle_state.BOARDWIDTH):
            column = []
            for y in range(Mpuzzle_state.BOARDHEIGHT):
                column.append([icons[0], False])
                del icons[0] # remove the icons as we assign them
            board.append(column)
        return board

    #methods
    def __init__(self):
        self.gameBoard = Mpuzzle_state.getRandomizedBoard()
        self.selection1 = None
        self.selection2 = None
        self.state = Mpuzzle_state.MODE_START
        self.tries = 0
        self.maxtries = 20

    def begin(self):
        self.state = Mpuzzle_state.MODE_PLAYING
    
    def getShapeAndColor(self, boxx, boxy):
        """ shape value for x, y spot is stored in board[x][y][0][0]
        color value for x, y spot is stored in board[x][y][0][1]"""
        return self.gameBoard[boxx][boxy][0][0], self.gameBoard[boxx][boxy][0][1]


    def isMatch(self, box1, box2):
        """box1 and box2 are both individual elements of the gameBoard at the [x][y] level, that is, a 2 element list of [(shape, color), reveal_status]
        however they cannot literally be the same box"""
        if box1 == box2:
            return False
        elif self.getShapeAndColor(box1[0], box1[1]) == self.getShapeAndColor(box2[0], box2[1]):
            return True

    def setRevealed(self, boxx, boxy):
        """set the box to be revealed(True)"""
        self.gameBoard[boxx][boxy][1] = True

    def setNotRevealed(self, boxx, boxy):
        """set the box to be not revealed(False)"""
        self.gameBoard[boxx][boxy][1] = False
        
    def getRevealed(self, boxx, boxy):
        """get whether box is revealed (True) or not (False)"""
        return self.gameBoard[boxx][boxy][1]

    def selectBox(self, boxx, boxy):
        """ put a box in selection, selection1 first then selection2. The selections are a special status that isn't "revealed" but the display should show their contents.
        Returns True if a selection was added or False if they were both full beforehand. Also tests for victory/loss and changes self.state accordingly.
        """
        # both selections empty, put it in selection 1:
        if self.selection1 == None:
            self.selection1 = (boxx, boxy)

        # selection 1 has something, put it in selection 2:
        elif self.selection1 != None and self.selection2 == None:
            self.selection2 = (boxx, boxy)

            #if select1 and 2 match, reveal them
            if self.isMatch(self.selection1, self.selection2):
                self.setRevealed(self.selection2[0], self.selection2[1])
                self.setRevealed(self.selection1[0], self.selection1[1])

                #test for victory
                hasWon = True
                for i in self.gameBoard:  #gameboard[x] = i
                    for j in i:           #gameboard[x][y] = j
                        if j[1] == False: #gameboard[x][y][1]
                            hasWon = False
                if hasWon:
                    self.state=Mpuzzle_state.MODE_WON
                    
            #if they don't match and they're not the same square then increment self.tries and test for loss
            elif self.selection1 != self.selection2:
                self.tries += 1
                if self.tries >= self.maxtries:
                    self.state = Mpuzzle_state.MODE_LOST

        #if both are full return false and clear selections
        elif self.selection1 != None and self.selection2 != None:
            self.clearSelection()
            return False


    def clearSelection(self):
        """clear the selections"""
        self.selection1 = None
        self.selection2 = None
        
    def revealAll(self):
        for i in range(Mpuzzle_state.BOARDWIDTH):
            for j in range(Mpuzzle_state.BOARDHEIGHT):
                self.setRevealed(i, j)

    def unrevealAll(self):
        for i in range(Mpuzzle_state.BOARDWIDTH):
            for j in range(Mpuzzle_state.BOARDHEIGHT):
                self.setNotRevealed(i, j)
        
