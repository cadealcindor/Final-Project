import networkx as nx
import random
import pygame

pygame.init()

quitStatus = False

#define the pygame window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#print( pygame.display.list_modes() )

#define fonts
mainFont = pygame.font.SysFont("cambria", 50)
labelFont = pygame.font.SysFont("cambria", 25)

#global gamerule variables
p1Colour = (255, 0, 0)
p2Colour = (0, 0, 255)
timerOn = False
p1Timer = 2
p2Timer = 2
p1MaxRemoveX = 2
p1MaxRemoveY = 2
p2MaxRemoveX = 2
p2MaxRemoveY = 2
p1Turn = True
singlePlayerMode = False
playerTurn = True



class Button():
    def __init__(self, colour, xpos, ypos, xsize, ysize, textInput):
        
        #defines the colour of the button (r, g, b)
        self.colour = colour

        #defines the position of the button
        self.xpos = xpos
        self.ypos = ypos

        #define size of the button
        self.xsize = xsize
        self.ysize = ysize

        #defines the box of the button
        self.rect = pygame.Rect((self.xpos, self.ypos, self.xsize, self.ysize))

        #difines the text of the button
        self.textInput = textInput
        self.text = mainFont.render(self.textInput, True, (255, 255, 255))

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.xsize/2), self.ypos + (self.ysize/2)))

    #draws the button
    def update(self):
        pygame.draw.rect(screen, self.colour, self.rect)
            
        #.blit() is used to display images
        screen.blit(self.text, self.text_rect)

    #function that checks if the button is clicked.
    def checkClicked(self, mousePosition):
          
        #if the the mouse is within the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    #changes the colour of the button when the mouse hovers over it
    def changeColour(self, mousePosition):
        
        #if the mouse is withing the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            
            #changes the colour of the text to its hover colour
            self.text = mainFont.render(self.textInput, True, (127, 127, 127))
        
        else:

            #otherwise the colour of the text is changed to its default colour
            self.text = mainFont.render(self.textInput, True, (255, 255, 255))

class CheckBox():
    def __init__(self, colour, xpos, ypos, xsize, ysize):
        
        #defines the colour of the check box (r, g, b)
        self.colour = colour

        #defines the position of the checkbox
        self.xpos = xpos
        self.ypos = ypos

        #define size of the checkbox
        self.xsize = xsize
        self.ysize = ysize

        #defines the box of the checkbox
        self.rect = pygame.Rect((self.xpos, self.ypos, self.xsize, self.ysize))

        #difines the text of the checkbox
        self.text = mainFont.render("X", True, (0, 0, 0))

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.xsize/2), self.ypos + (self.ysize/2)))

        #defines the output value of the check box
        self.value = True

    #draws the checkbox
    def update(self):
        pygame.draw.rect(screen, self.colour, self.rect)
           
        #displays a cross in the check box if it's value is True
        if self.value:

            #.blit() is used to display images
            screen.blit(self.text, self.text_rect)

    #function that checks if the checkbox is clicked.
    def checkClicked(self, mousePosition):
          
        #if the the mouse is within the box of the checkbox...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            self.value = not self.value

    #changes the colour of the checkbox when the mouse hovers over it
    def changeColour(self, mousePosition):
        
        #if the mouse is withing the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            
            #changes the colour of the text to its hover colour
            self.colour = (127, 127, 127)
        
        else:

            #otherwise the colour of the text is changed to its default colour
            self.colour = (255, 255, 255)

class NumberTextBox():
    def __init__(self, colour, xpos, ypos, xsize, ysize, minValue, maxValue):
        
        #defines the colour of the text box (r, g, b)
        self.colour = colour

        #defines the position of the text box
        self.xpos = xpos
        self.ypos = ypos

        #define size of the text box
        self.xsize = xsize
        self.ysize = ysize

        #defines the box of the text box
        self.rect = pygame.Rect((self.xpos, self.ypos, self.xsize, self.ysize))

        #difines the text of the text box
        self.textValue = ""
        self.text = mainFont.render(self.textValue, True, (0, 0, 0))

        self.numValue = 0

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.xsize/2), self.ypos + (self.ysize/2)))

        #a variable to contain whether or not the text box is currently selected
        self.isSelected = False

        #defines the minimum and maximum values
        self.minValue = minValue
        self.maxValue = maxValue

    #draws the text box
    def update(self):
        global buttonImg
        pygame.draw.rect(screen, self.colour, self.rect)
        
        tempTextValue = self.textValue

        #adds | to the end to show that the text box is selected
        if self.isSelected:
            tempTextValue += "|" 

        #updates the text
        self.text = mainFont.render(tempTextValue, True, (0, 0, 0))

        #recenters the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.xsize/2), self.ypos + (self.ysize/2)))

        #.blit() is used to display images
        screen.blit(self.text, self.text_rect)

    #function that checks if the text box is clicked.
    def checkClicked(self, mousePosition):
          
        #if the the mouse is within the box of the text box...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            self.isSelected = True
        else:
            self.isSelected =  False
            
            self.updateNumValue()
            self.textValue = str(self.numValue)

    #changes the colour of the text box when the mouse hovers over it
    def changeColour(self, mousePosition):
        
        #if the mouse is withing the box of the text box...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            
            #changes the colour of the text to its hover colour
            self.colour = (127, 127, 127)
        
        else:

            #otherwise the colour of the text is changed to its default colour
            self.colour = (255, 255, 255)

    def appendText(self, digit):

        #if the inputted character is a numerical digit
        if digit in str("1234567890"):

            #append it to the text box's text
            self.textValue += digit

    def backspace(self):

        #removes the character at the end of the string
        self.textValue = self.textValue[:-1]

    def updateNumValue(self):

        #if the text box is empty...
        if self.textValue == "":

            #set the numerical value to 0
            self.numValue = 0
        
        #otherwise...
        else:

            #set the numerical value to that of the string
            self.numValue = int(self.textValue)

        #makes sure that the numerical value is within it's valid range
        if self.numValue > self.maxValue:
            self.numValue = self.maxValue
        elif self.numValue < self.minValue:
            self.numValue = self.minValue

class BoardSelectSlot():
    def __init__(self, colour, xpos, ypos, xsize, ysize, textInput):
        
        #defines the colour of the slot (r, g, b)
        self.colour = colour

        #defines the position of the slot
        self.xpos = xpos
        self.ypos = ypos

        #define size of the slot
        self.xsize = xsize
        self.ysize = ysize

        #defines the box of the slot
        self.rect = pygame.Rect((self.xpos, self.ypos, self.xsize, self.ysize))

        #difines the text of the slot
        self.textInput = textInput
        self.text = labelFont.render(self.textInput, True, (255, 255, 255))

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.xsize/2 - 50), self.ypos + (self.ysize/2)))

        self.isSelcted = False

    #draws the slot
    def update(self):

        pygame.draw.rect(screen, self.colour, self.rect)
            
        #.blit() is used to display images
        screen.blit(self.text, self.text_rect)

    #function that checks if the slot is clicked.
    def checkClicked(self, mousePosition):
          
        #if the the mouse is within the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    #changes the colour of the button when the mouse hovers over it
    def changeColour(self, mousePosition):
        
        #if the mouse is withing the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            
            #changes the colour of the text to its hover colour
            self.text = labelFont.render(self.textInput, True, (127, 127, 127))
        
        else:

            #otherwise the colour of the text is changed to its default colour
            self.text = labelFont.render(self.textInput, True, (255, 255, 255))

class BoardSquare():
    def __init__(self,  xpos, ypos, width, height):
        
        #defines the size of the board sqaure
        self.width = width
        self.height = height

        #defines the position of the board square
        self.xpos = xpos
        self.ypos = ypos

        #defines the box of the board square
        self.rect = pygame.Rect(xpos, ypos, width, height)

        #defines the value contained in the board square
        self.value = "X"

        #defines the text of the baord square
        self.text = mainFont.render(self.value, True, (0, 0, 0))

        #keeps track of whether or not the board square is currently selected
        self.isSelected = False

        #contains the id of the node in the graph that represents this square
        self.node = -1

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.width/2), self.ypos + (self.height/2)))

    #draws the board square
    def update(self):

        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
        #if the board square is currently selected...
        if self.isSelected == True:
            
            #change the colour of the text to that of the player whose turn it is
            if p1Turn:
                self.text = mainFont.render(self.value, True, p1Colour)
            else:
                self.text = mainFont.render(self.value, True, p2Colour)
        
        else:
            self.text = mainFont.render(self.value, True, (0, 0, 0))
        
        screen.blit(self.text, self.text_rect)

    def checkClicked(self, mousePosition):
        
        if self.value == "X":
            
            #if the the mouse is within the box of the button...
            if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
                self.isSelected = not self.isSelected

class CustomBoardSquare():
    def __init__(self,  xpos, ypos, width, height):
        
        #defines the size of the board sqaure
        self.width = width
        self.height = height

        #defines teh position of the board square
        self.xpos = xpos
        self.ypos = ypos

        #defines the box of the board square
        self.rect = pygame.Rect(xpos, ypos, width, height)
        
        #defines the value contained in the board square
        self.value = " "

        #defines the tex tof the board square
        self.text = mainFont.render(self.value, True, (0, 0, 0))

        #defines the box of the text
        self.text_rect = self.text.get_rect(center=(self.xpos + (self.width/2), self.ypos + (self.height/2)))

    #draws the board square
    def update(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        #.blit() is used to display images
        screen.blit(self.text, self.text_rect)

    def checkClicked(self, mousePosition):
          
        #if the the mouse is within the box of the button...
        if mousePosition[0] in range(self.rect.left, self.rect.right) and mousePosition[1] in range(self.rect.top, self.rect.bottom):
            
            #flips the value of the board square
            if self.value == "X":
                self.value = " "
            else:
                self.value = "X"

            #updates the text to match the value
            self.text = mainFont.render(self.value, True, (0, 0, 0))  
  
class TheBoard():
    def __init__(self, xpos, ypos, width, height):
        
        #defines the position of the board
        self.xpos = xpos
        self.ypos = ypos

        #dimensions of the board on the screen
        self.width = width
        self.height = height

        #contains the squares that make up the board
        self.squaresList = []

        #the graph is used to determine whether or not a node should 'fall'
        self.graph = nx.Graph()

    #generates an array of  board squares from an array of characters
    def createBoard(self, boardArr):
        
        #makes sure that the array and the graph are empty
        self.squaresList = []
        self.graph = nx.Graph()

        #calculate the size of the squares
        squareWidth = (self.width / len(boardArr[0])) - 10
        squareHeight = (self.height / len(boardArr)) - 10

        #the number that is assigned to the next added node
        nextNode = 1

        #adds the root node
        self.graph.add_node(0)

        #populate the board with squares
        for i in range(len(boardArr)):
            self.squaresList.append([])
            for j in range(len(boardArr[0])):
                
                #add a square to the list of squares to represent this position of the arrasy
                self.squaresList[i].append(BoardSquare((self.xpos + j * squareWidth), (self.ypos + i * squareHeight), squareWidth - 5, squareHeight - 5))
                self.squaresList[i][j].value = boardArr[i][j]
                
                #if this position contains an element...
                if self.squaresList[i][j].value == "X":
                
                    #add a node to the graph to represent the element
                    self.graph.add_node(nextNode)
                    self.squaresList[i][j].node = nextNode
                    
                    #if the node is on the ground level...
                    if i == len(boardArr) - 1:

                        #adds an edge from the current node to the ground
                        self.graph.add_edge(nextNode, 0)

                    #adds edges to adjacent nodes
                    #Makes sure that the adjacent space isn't out of bounds
                    if i - 1 > -1:

                        #If the node to the right of this node contains an element...
                        if self.squaresList[i - 1][j].value == "X":

                            #add an edge from this node to the node to the right
                            self.graph.add_edge(nextNode, self.squaresList[i - 1][j].node)  

                    #Makes sure that the adjacent space isn't out of bounds
                    if j - 1 > -1:

                        #If the node below this node contains an element...
                        if self.squaresList[i][j - 1].value == "X":

                            #add an edge from this node to the node below
                            self.graph.add_edge(nextNode, self.squaresList[i][j - 1].node)

                    #increment the value to be assigned to the next ndoe
                    nextNode = nextNode + 1

    #draws the board
    def update(self):

        #draws each board square in the list
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                self.squaresList[i][j].update()

    def checkClicked(self, mousePosition):
         
        #goes through each board square and checks if it has been clicked
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                self.squaresList[i][j].checkClicked(mousePosition)

    def remove(self):

        #goes through each board square and removes it if it is selected
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                if self.squaresList[i][j].isSelected:

                    #deselect the board square
                    self.squaresList[i][j].isSelected = False

                    #remove the value of the board sqaure
                    self.squaresList[i][j].value = " "

                    #removes the node that represents the board square from the graph
                    self.graph.remove_node(self.squaresList[i][j].node)

                    #removes the board squares reference to its node in the grpah
                    self.squaresList[i][j].node = -1

    def getSelectedSquares(self):
        
        #a list to contain the coordinates of the selcted board squares
        selectedList = []

        #goes though each board square and appends its coordinates to the list if it is selected
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                if self.squaresList[i][j].isSelected:
                    selectedList.append([i, j])

        return selectedList

    #checks to see if a players move is legal or not
    def validateMove(self):
        
        #sets the area that the player is allowed to remove depending on which turn it is
        if p1Turn:
            maxRemoveX = p1MaxRemoveX
            maxRemoveY = p1MaxRemoveY
        else:
            maxRemoveX = p2MaxRemoveX
            maxRemoveY = p2MaxRemoveY

        #gets the coordinates of all the selected board squares
        selectedList = self.getSelectedSquares()

        #lits to sperate x and y coordinates into
        xCoords = []
        yCoords = []

        #if no squares are selected...
        if len(selectedList) == 0:

            #the move is invalide
            return False

        for i in range(len(selectedList)):
            
            #get each distinct x coordinate
            if selectedList[i][1] not in xCoords:
                xCoords.append(selectedList[i][1])

            #get  each distinct y coordinate
            if selectedList[i][0] not in yCoords:  
                yCoords.append(selectedList[i][0])

        #checks that the width of the remove area is legal
        xCoords.sort()

        #if the difference between the smallest x coordinate and largest x coordinate is larger than the maximum range allowed...
        if xCoords[len(xCoords) - 1] - xCoords[0] > maxRemoveX - 1:
            
            #the move is invalid
            return False

        #checks that the height of the remove area is legal
        yCoords.sort()

        #if the difference between the smallest y coordinate and largest y coordinate is larger than the maximum range allowed...
        if yCoords[len(yCoords) - 1] - yCoords[0] > maxRemoveY - 1:
            
            #the move is invlaid
            return False

        #if all previous tests have been passed then the move is valid
        return True

    def deselect(self):

        #goes through each board square and deselects it
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                self.squaresList[i][j].isSelected = False

    def falls(self):

        #go through each square
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
            
                #if square contains an element...
                if self.squaresList[i][j].value == "X":
                
                    #get all connected nodes
                    connectedElements = list(nx.descendants(self.graph, self.squaresList[i][j].node))

                    #if root is not in connected nodes...
                    if 0 not in connectedElements:

                        #remove all connected nodes
                        for k in range(i, len(self.squaresList)):
                            for l in range(j, len(self.squaresList[k])):
                                if self.squaresList[k][l].node in connectedElements:
                                    self.squaresList[k][l].isSelected = False
                                    self.squaresList[k][l].value = " "
                                    self.graph.remove_node(self.squaresList[k][l].node)
                                    self.squaresList[k][l].node = -1
                        
                        #remove the current square
                        self.squaresList[i][j].isSelected = False
                        self.squaresList[i][j].value = " "
                        self.graph.remove_node(self.squaresList[i][j].node)
                        self.squaresList[i][j].node = -1

    def getMaxLength(self):
        maxLength = 0

        #checks every row
        for i in range(len(self.squaresList)):

            #If the current row size is larger than the largest row size
            if len(self.squaresList[i]) > maxLength:

                #sets current row size as the largest row size
                maxLength = len(self.squaresList[i])

            #returns the largest row size
            return maxLength

    def computerMove(self):
        #global variables
        global playerTurn
        global p1MaxRemoveX
        global p1MaxRemoveY
        global p2MaxRemoveX
        global p2MaxRemoveY

        #sets the area that the computer is allowed to remove depending on which turn it is
        if playerTurn:
            maxRemoveX = p2MaxRemoveX
            maxRemoveY = p2MaxRemoveY
        else:
            maxRemoveX = p1MaxRemoveX
            maxRemoveY = p1MaxRemoveY


        maxLength = self.getMaxLength()

        #calculate the mirror move

        #I despise the amount of for loops used here

        #go through each position on the board
        for i in range(len(self.squaresList)):
            for j in range(maxLength):

                #select every possible move from that position on of the board
                for k in range(maxRemoveY):
                    for l in range(maxRemoveX):

                        #I need to copy the board so that i don't change the real board during move calculkation
                        potentialBoard = TheBoard(0,0,0,0)
                        
                        #get copy of list. Decause the list contains calss objects (i think) .copy() and .deepcopy() don't work, so i have to copy the squares list manually
                        for i2 in range(len(self.squaresList)):
                            potentialBoard.squaresList.append([])
                            for j2 in range(len(self.squaresList[i2])):

                                #because python treats assigning a varible to an object as a pointer to that object (for some reason), i have to create new objects and assign their values manualy
                                potentialBoard.squaresList[i2].append(BoardSquare(self.squaresList[i2][j2].xpos,self.squaresList[i2][j2].ypos,self.squaresList[i2][j2].width,self.squaresList[i2][j2].height))
                                potentialBoard.squaresList[i2][j2].value = self.squaresList[i2][j2].value
                                potentialBoard.squaresList[i2][j2].node = self.squaresList[i2][j2].node

                        #get copy of graph
                        potentialBoard.graph = self.graph.copy()

                        #makes sure that the move is allowed
                        legal = False

                        #attempt to perform selected move
                        for m in range(k + 1):
                            for n in range(l + 1):

                                #makes sure that the selected position is within range of the list
                                if (i + m) < len(potentialBoard.squaresList) and (j + n) < maxLength:

                                    #if the position contains an element...
                                    if potentialBoard.squaresList[i + m][j + n].value == "X":

                                        #remove the element from the board
                                        potentialBoard.squaresList[i + m][j + n].value = " "

                                        #remove the node from the graph version of the board
                                        potentialBoard.graph.remove_node(potentialBoard.squaresList[i + m][j + n].node)
                                        potentialBoard.squaresList[i + m][j + n].node = -1

                                        #flag the move as legal
                                        legal = True
                        
                        if legal:

                            #part of for loop l
                            #check for falling elements
                            potentialBoard.falls()

                            #checks if a winning move has been found
                            if potentialBoard.graph.number_of_nodes() == 1:

                                #perform the winning move
                                for m in range(k + 1):
                                    for n in range(l + 1):

                                        #makes sure that the selected position is within range of the list
                                        if (i + m) < len(self.squaresList) and (j + n) < maxLength:

                                            #if the position contains an element...
                                            if self.squaresList[i + m][j + n].value == "X":

                                                #remove the element from the board
                                                self.squaresList[i + m][j + n].isSelected = True

                                return


                            #check if move is a mirror move
                            #split into two seperate games
                            splitGBoard = potentialBoard.graph.copy()
                            splitGBoard.remove_node(0)
                            subGraphs = list((splitGBoard.subgraph(c).copy() for c in nx.connected_components(splitGBoard)))

                            #checks if a mirror move has been found
                            if len(subGraphs) > 1:

                                #check if the two games are isomorphic
                                if nx.is_isomorphic(subGraphs[0], subGraphs[1]) == True and self.squaresList != potentialBoard.squaresList:

                                    #perform the mirror move
                                    for m in range(k + 1):
                                        for n in range(l + 1):

                                            #makes sure that the selected position is within range of the list
                                            if (i + m) < len(self.squaresList) and (j + n) < maxLength:

                                                #if the position contains an element...
                                                if self.squaresList[i + m][j + n].value == "X":

                                                    #remove the element from the board
                                                    self.squaresList[i + m][j + n].isSelected = True
                                    
                                    return
                            

        #if no 'optimal' move is found, perform a random move
        self.randomMove()

    #this method could *technically* cause an infinte loop but it's probably fine... probably...
    def randomMove(self):
        
        #global variables
        global playerTurn
        global p1MaxRemoveX
        global p1MaxRemoveY
        global p2MaxRemoveX
        global p2MaxRemoveY

        #sets the area that the computer is allowed to remove depending on which turn it is
        if playerTurn:
            maxRemoveX = p2MaxRemoveX
            maxRemoveY = p2MaxRemoveY
        else:
            maxRemoveX = p1MaxRemoveX
            maxRemoveY = p1MaxRemoveY

        maxLength = self.getMaxLength()

        #choose starting x
        xPos = random.randint(0, maxLength - 1)

        #choose starting y
        yPos = random.randint(0, (len(self.squaresList) - 1))

        #choose remove x
        if (maxRemoveX + xPos) > maxLength:
            xRemove = random.randint(1, (maxLength - xPos))
        else:
            xRemove = random.randint(1, maxRemoveX)

        #choose remove y
        if (maxRemoveY + yPos) > len(self.squaresList):
            yRemove = random.randint(1, (len(self.squaresList) - yPos))
        else:
            yRemove = random.randint(1, maxRemoveY)

        #check that the move removes at least 1 element
        valid = False

        #checks each row
        for i in range(yRemove):

            #checks each column
            for j in range(xRemove):
                if valid == False:

                    #checks if there is an element
                    if self.squaresList[yPos + i][xPos + j].value == "X":
                        valid = True

        #if the move is valid...
        if valid == True:
            #Removes the elements in the selected area

            #goes thorugh each row
            for i in range(yRemove):

                #goes through each column
                for j in range(xRemove):

                    #if the position contains an element...
                    if self.squaresList[yPos + i][xPos + j].value == "X":

                        #remove the element from the board
                        self.squaresList[yPos + i][xPos + j].isSelected = True

        #starts again if the move doesn't remove at least one element
        else:
            self.randomMove()

    def printBoard(self):
        for i in range(len(self.squaresList)):
            outString = ""
            for j in range(len(self.squaresList[i])):
                outString = outString + self.squaresList[i][j].value
            print(outString)

    def checkSelection(self, selection):
        
        #check each sqaure...
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):

                #if the square is within the selection...
                if pygame.Rect.colliderect(self.squaresList[i][j].rect, selection) and self.squaresList[i][j].value == "X":
                    self.squaresList[i][j].isSelected = True

                else:
                    self.squaresList[i][j].isSelected = False

    def getRemainingElements(self):
        
        remaining = 0
        
        #counts how many board squares contain an element
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                if self.squaresList[i][j].value == "X":
                    remaining = remaining + 1

        return remaining

class TheCustomBoard():
    def __init__(self, xpos, ypos, width, height):
        
        #the position of the board template
        self.xpos = xpos
        self.ypos = ypos

        #dimensions of the board template on the screen
        self.width = width
        self.height = height

        #contains the squares that make up the board template
        self.squaresList = []

    def createBoard(self):
        
        #makes sure that the array
        self.squaresList = []

        #calculate the size of the squares
        squareWidth = (self.width / 5) - 10
        squareHeight = (self.height / 5) - 10

        #populate the board with squares
        for i in range(5):
            self.squaresList.append([])
            for j in range(5):
                
                #add a square to the list of squares to represent this position of the array
                self.squaresList[i].append(CustomBoardSquare((self.xpos + j * squareWidth), (self.ypos + i * squareHeight), squareWidth - 5, squareHeight - 5))
                self.squaresList[i][j].value = " "
                
    #Changes the width of the board template
    def updateXSquares(self, newXSquares):
        
        #calculate the size of the squares
        squareWidth = (self.width / newXSquares) - 10
        squareHeight = self.squaresList[0][0].height

        #updates all existing squares whilst also adding any new ones
        for i in range(len(self.squaresList)):
            for j in range(newXSquares):

                #if the boardsquare already exists...
                if j < len(self.squaresList[i]):

                    #change the size of the boardsquare
                    self.squaresList[i][j].width = squareWidth
                    self.squaresList[i][j].height = squareHeight
                    self.squaresList[i][j].xpos = self.xpos + j * (squareWidth + 5)
                    self.squaresList[i][j].ypos = self.ypos + i * (squareHeight + 5)

                    self.squaresList[i][j].rect = pygame.Rect((self.xpos + j * (self.squaresList[i][j].width + 5)), (self.ypos + i * (self.squaresList[i][j].height + 5)), self.squaresList[i][j].width, self.squaresList[i][j].height)
                    self.squaresList[i][j].text_rect = self.squaresList[i][j].text.get_rect(center=(self.squaresList[i][j].xpos + (self.squaresList[i][j].width/2), self.squaresList[i][j].ypos + (self.squaresList[i][j].height/2)))
                
                else:

                    #add a new board square
                    self.squaresList[i].append(CustomBoardSquare((self.xpos + j * (squareWidth + 5)), (self.ypos + i * (squareHeight + 5)), squareWidth, squareHeight))
                    self.squaresList[i][j].text_rect = self.squaresList[i][j].text.get_rect(center=(self.squaresList[i][j].xpos + (self.squaresList[i][j].width/2), self.squaresList[i][j].ypos + (self.squaresList[i][j].height/2)))
                    self.squaresList[i][j].value = " "
        
        #removes columns if the new width is shorter than the old width
        currentXSquares = self.getMaxLength()
        while currentXSquares > newXSquares:
            for i in range(len(self.squaresList)):
                self.squaresList[i].pop()
            
            currentXSquares = currentXSquares - 1

    #changes the height of the board template
    def updateYSquares(self, newYSquares):
        
        #calculate the size of the squares
        squareWidth = self.squaresList[0][0].width
        squareHeight = (self.height / newYSquares) - 10

        xSquares = self.getMaxLength()

        #updates all existing squares whilst also adding any new ones
        for i in range(newYSquares):
            
            newRow = False

            #if the row already exists...
            if i >= len(self.squaresList):
                
                #add a new row
                self.squaresList.append([])
                newRow = True

            for j in range(xSquares):
                
                #if a new row has been added
                if newRow:

                    #add a new board square
                    self.squaresList[i].append(CustomBoardSquare((self.xpos + j * (squareWidth + 5)), (self.ypos + i * (squareHeight + 5)), squareWidth, squareHeight))
                    self.squaresList[i][j].text_rect = self.squaresList[i][j].text.get_rect(center=(self.squaresList[i][j].xpos + (self.squaresList[i][j].width/2), self.squaresList[i][j].ypos + (self.squaresList[i][j].height/2)))
                    self.squaresList[i][j].value = " "

                else:

                    #change the size of the boardsquare
                    self.squaresList[i][j].width = squareWidth
                    self.squaresList[i][j].height = squareHeight
                    self.squaresList[i][j].xpos = self.xpos + j * (squareWidth + 5)
                    self.squaresList[i][j].ypos = self.ypos + i * (squareHeight + 5)

                    self.squaresList[i][j].rect = pygame.Rect((self.xpos + j * (self.squaresList[i][j].width + 5)), (self.ypos + i * (self.squaresList[i][j].height + 5)), self.squaresList[i][j].width, self.squaresList[i][j].height)
                    self.squaresList[i][j].text_rect = self.squaresList[i][j].text.get_rect(center=(self.squaresList[i][j].xpos + (self.squaresList[i][j].width/2), self.squaresList[i][j].ypos + (self.squaresList[i][j].height/2)))
                
        #removes rows if the old height is shorter than the new height
        currentYSquares = len(self.squaresList)
        while currentYSquares > newYSquares:

            self.squaresList.pop()
     
            currentYSquares = currentYSquares - 1

    def update(self):

        #draws each square in the board tempalte
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                self.squaresList[i][j].update()

    def checkClicked(self, mousePosition):
         
        #goes through eahc square in the board template and checks if it has been clicked
        for i in range(len(self.squaresList)):
            for j in range(len(self.squaresList[i])):
                self.squaresList[i][j].checkClicked(mousePosition)

    def printBoard(self):
        for i in range(len(self.squaresList)):
            outString = ""
            for j in range(len(self.squaresList[i])):
                outString = outString + self.squaresList[i][j].value
            print(outString)

    def getMaxLength(self):
        maxLength = 0

        #checks every row
        for i in range(len(self.squaresList)):

            #If the current row size is larger than the largest row size
            if len(self.squaresList[i]) > maxLength:

                #sets current row size as the largest row size
                maxLength = len(self.squaresList[i])

            #returns the largest row size
            return maxLength

    #outputs the board template as a 2D array of characters so that it can be used to generate the real board
    def generateBooardArr(self):
        
        boardArr = []
        
        #appedns the value of each square to the board array
        for i in range(len(self.squaresList)):
            
            boardArr.append([])
            

            for j in range(len(self.squaresList[i])):

                boardArr[i].append(self.squaresList[i][j].value)

        return boardArr

def mainMenu():
    global quitStatus

    #define the buttons
    onePlayerButton = Button((100, 100, 100), 250, 100, 300, 75, "One Player")
    twoPlayerButton = Button((100, 100, 100), 250, 200, 300, 75, "Two Player")
    howToPlayButton = Button((100, 100, 100), 250, 300, 300, 75, "How To Play")
    aboutMeButton = Button((100, 100, 100), 250, 400, 300, 75, "About Me")
    quitButton = Button((100, 100, 100), 250, 500, 300, 75, "Quit")


    #define labels
    titleText = mainFont.render("Cade's Crosses", True, (255,255,255))
    titleTextRect = pygame.Rect((285, 25, 50, 50))

    #game loop
    run = True

    #runs once per frame
    while run:

        #simple way to clear the drawings on a screen
        #fill(colour(r,g,b))
        screen.fill((0,0,0))

        #display the screen title
        screen.blit(titleText, titleTextRect)
        
        #display the buttons
        onePlayerButton.update()
        twoPlayerButton.update()
        howToPlayButton.update()
        aboutMeButton.update()
        quitButton.update()
        


        #changes the colour of the button if the mouse is hovering over it
        onePlayerButton.changeColour(pygame.mouse.get_pos())
        twoPlayerButton.changeColour(pygame.mouse.get_pos())
        howToPlayButton.changeColour(pygame.mouse.get_pos())
        aboutMeButton.changeColour(pygame.mouse.get_pos())
        quitButton.changeColour(pygame.mouse.get_pos())
        

        
        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:

                #if the one player button has been clicked...
                if onePlayerButton.checkClicked(pygame.mouse.get_pos()):

                    #go to one player mode screen
                    onePlayerMode()

                #if the two player button has been clicked...
                if twoPlayerButton.checkClicked(pygame.mouse.get_pos()):

                    #go to two player mode screen
                    twoPlayerMode()                 

                #if the how to play button has been clicked...
                if howToPlayButton.checkClicked(pygame.mouse.get_pos()):

                    #go to how to play screen
                    howToPlay()
                    

                #if the about me button has been clicked...
                if aboutMeButton.checkClicked(pygame.mouse.get_pos()):

                    #go to about me screen
                    aboutMe()

                #if the quit button has been clicked...
                if quitButton.checkClicked(pygame.mouse.get_pos()):

                    quitStatus = True

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed during any screen...
        if quitStatus:
            run = False

def onePlayerMode():
    
    #define global variables
    global quitStatus
    global singlePlayerMode
    global playerTurn

    #define the title
    titleText = mainFont.render("One Player Mode", True, (255,255,255))
    titleTextRect = pygame.Rect((200, 25, 50, 50))

    #define the buttons
    optionsButton = Button((100, 100, 100), 575, 25, 200, 75, "Options")
    backButton = Button((100, 100, 100), 25, 25, 150, 75, "Back")

    #define labels
    p1Label = labelFont.render("Go First", True, (255, 255, 255))
    p1Rect = pygame.Rect((200, 150, 50, 50))
    p2Label = labelFont.render("Go Second", True, (255, 255, 255))
    p2Rect = pygame.Rect((375, 150, 50, 50))
    boardSelectLabel = labelFont.render("Select Your Board", True, (255, 255, 255))
    boardSelectRect = pygame.Rect((275, 300, 50, 50))
    
    #define checkboxes
    p1Checkbox = CheckBox((255, 255, 255), 300, 150, 50, 50)
    p2Checkbox = CheckBox((255, 255, 255), 500, 150, 50, 50)
    p2Checkbox.value = False

    #define board select thing
    boards = ["Random", "Custom", "Preset"]

    boardSlot1 = BoardSelectSlot((100, 100, 100), 100, 350, 150, 150, "")
    boardSlot2 = BoardSelectSlot((100, 100, 100), 300, 350, 150, 150, "")
    boardSlot3 = BoardSelectSlot((100, 100, 100), 500, 350, 150, 150, "")

    displayedBoards = 0
    startgame = False

    #game loop
    run = True
    while run:

        #update the values of the board selector
        boardSlot1.textInput = boards[displayedBoards]
        boardSlot2.textInput = boards[displayedBoards + 1]
        boardSlot3.textInput = boards[displayedBoards + 2]


        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(titleText, titleTextRect)
        screen.blit(p1Label, p1Rect)
        screen.blit(p2Label, p2Rect)
        screen.blit(boardSelectLabel, boardSelectRect)

        #display checkboxes
        p1Checkbox.update()
        p2Checkbox.update()

        #display three boards
        boardSlot1.update()
        boardSlot2.update()
        boardSlot3.update()

        #display the buttons
        optionsButton.update()
        backButton.update()

        #changes the colour of the button if the mouse is hovering over it
        optionsButton.changeColour(pygame.mouse.get_pos())
        backButton.changeColour(pygame.mouse.get_pos())
        boardSlot1.changeColour(pygame.mouse.get_pos())
        boardSlot2.changeColour(pygame.mouse.get_pos())
        boardSlot3.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:

                #if the back has been clicked...
                if backButton.checkClicked(pygame.mouse.get_pos()):

                    #end game loop to go to the previous screen
                    run = False

                #if the options button has been clicked...
                if optionsButton.checkClicked(pygame.mouse.get_pos()):

                    #go to options screen
                    print("Options button has been clicked")
                    options()

                #if a board selector slot is clicked, select that slot, deselect the others, and start the game
                if boardSlot1.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = True
                    boardSlot2.isSelected = False
                    boardSlot3.isSelected = False
                    startgame = True

                if boardSlot2.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = False
                    boardSlot2.isSelected = True
                    boardSlot3.isSelected = False
                    startgame = True


                if boardSlot3.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = False
                    boardSlot2.isSelected = False
                    boardSlot3.isSelected = True
                    startgame = True

                p1Checkbox.checkClicked(pygame.mouse.get_pos())
                
                #if Player 1 is going first, deselect the player 2 going first checkbox
                if p1Checkbox.value:
                    p2Checkbox.value = False
                else:
                    p2Checkbox.value = True

                p2Checkbox.checkClicked(pygame.mouse.get_pos())

                #if Player 2 is going first, deselect the player 1 going first checkbox
                if p2Checkbox.value:
                    p1Checkbox.value = False
                else:
                    p1Checkbox.value = True

        if startgame == True:
            
            #set the selected board
            if boardSlot1.isSelected:
                chosenBoard = boardSlot1.textInput
            elif boardSlot2.isSelected:
                chosenBoard = boardSlot2.textInput
            elif boardSlot3.isSelected:
                chosenBoard = boardSlot3.textInput
            else:
                chosenBoard = "None"

            if chosenBoard == "Random":
                boardArr = randomBoardScreen()
            elif chosenBoard == "Custom":
                boardArr = customBoardScreen()

            elif chosenBoard == "Preset":
                boardArr = [
                    ["X", "X", " ", " ", "X", "X"],
                    ["X", "X", " ", " ", "X", "X"],
                    ["X", "X", "X", "X", "X", "X"],
                    ["X", "X", "X", "X", "X", "X"]
                ]
            else: 
                boardArr = []

            #set the global variables
            singlePlayerMode = True
            playerTurn = p1Checkbox.value
            
            #if a valid board has been selected...    
            if boardArr != []:

                #start the game
                TheGame(boardArr)

            startgame = False
                    
        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

def twoPlayerMode():

    #define the global variables
    global quitStatus
    global singlePlayerMode
    global playerTurn

    #define the title
    titleText = mainFont.render("Two Player Mode", True, (255,255,255))
    titleTextRect = pygame.Rect((200, 25, 50, 50))

    #define the buttons
    optionsButton = Button((100, 100, 100), 575, 25, 200, 75, "Options")
    backButton = Button((100, 100, 100), 25, 25, 150, 75, "Back")

    #define board selector
    boards = ["Random", "Custom", "Preset"]

    boardSlot1 = BoardSelectSlot((100, 100, 100), 100, 250, 150, 150, "")
    boardSlot2 = BoardSelectSlot((100, 100, 100), 300, 250, 150, 150, "")
    boardSlot3 = BoardSelectSlot((100, 100, 100), 500, 250, 150, 150, "")

    displayedBoards = 0
    startgame = False

    #game loop
    run = True
    while run:

        #update the values of the boar selector slots
        boardSlot1.textInput = boards[displayedBoards]
        boardSlot2.textInput = boards[displayedBoards + 1]
        boardSlot3.textInput = boards[displayedBoards + 2]


        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(titleText, titleTextRect)

        #display three boards
        boardSlot1.update()
        boardSlot2.update()
        boardSlot3.update()

        #display the buttons
        optionsButton.update()
        backButton.update()

        #changes the colour of the button if the mouse is hovering over it
        optionsButton.changeColour(pygame.mouse.get_pos())
        backButton.changeColour(pygame.mouse.get_pos())
        boardSlot1.changeColour(pygame.mouse.get_pos())
        boardSlot2.changeColour(pygame.mouse.get_pos())
        boardSlot3.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True
      
            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:

                #if the back has been clicked...
                if backButton.checkClicked(pygame.mouse.get_pos()):

                    #end game loop to go to the previous screen
                    run = False

                #if the options button has been clicked...
                if optionsButton.checkClicked(pygame.mouse.get_pos()):

                    #go to options screen
                    options()

                #if a board selector slot is clicked, select that slot, deselect the others, and start the game
                if boardSlot1.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = True
                    boardSlot2.isSelected = False
                    boardSlot3.isSelected = False
                    startgame = True

                if boardSlot2.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = False
                    boardSlot2.isSelected = True
                    boardSlot3.isSelected = False
                    startgame = True

                if boardSlot3.checkClicked(pygame.mouse.get_pos()):
                    boardSlot1.isSelected = False
                    boardSlot2.isSelected = False
                    boardSlot3.isSelected = True
                    startgame = True

        if startgame == True: 

            #set the selected board
            if boardSlot1.isSelected:
                chosenBoard = boardSlot1.textInput
            elif boardSlot2.isSelected:
                chosenBoard = boardSlot2.textInput
            elif boardSlot3.isSelected:
                chosenBoard = boardSlot3.textInput
            else:
                chosenBoard = "None"
            
            if chosenBoard == "Random":
                boardArr = randomBoardScreen()
            elif chosenBoard == "Custom":
                boardArr = customBoardScreen()

            elif chosenBoard == "Preset":
                boardArr = [
                    ["X", "X", " ", " ", "X", "X"],
                    ["X", "X", " ", " ", "X", "X"],
                    ["X", "X", "X", "X", "X", "X"],
                    ["X", "X", "X", "X", "X", "X"]
                ]
            else: 
                boardArr = []

            #set the global variables
            singlePlayerMode = False
                    
            #if a valid board has been selected...
            if boardArr != []:

                #start the game
                TheGame(boardArr)

            startgame = False

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

def options():
    
    #define global variables
    global quitStatus
    global p1Colour
    global p2Colour
    global timerOn
    global p1Timer
    global p2Timer
    global p1MaxRemoveX
    global p1MaxRemoveY
    global p2MaxRemoveX
    global p2MaxRemoveY

    #define tmeporary local variables
    tempP1Colour = p1Colour
    tempP2Colour = p2Colour
    tempTimerOn = timerOn
    tempP1Timer = p1Timer
    tempP2Timer = p2Timer
    tempP1MaxRemoveX = p1MaxRemoveX
    tempP1MaxRemoveY = p1MaxRemoveY
    tempP2MaxRemoveX = p2MaxRemoveX
    tempP2MaxRemoveY = p2MaxRemoveY

    #define labels
    titleText = mainFont.render("Game Options", True, (255,255,255))
    titleTextRect = pygame.Rect((285, 15, 50, 50))
    p1ColourLabel = labelFont.render("Player 1 Colour:", True, (255, 255, 255))
    p1ColourLabelRect = pygame.Rect((25, 100, 50, 50))
    p2ColourLabel = labelFont.render("Player 2 Colour:", True, (255, 255, 255))
    p2ColourLabelRect = pygame.Rect((25, 150, 50, 50))
    timerLabel = labelFont.render("Timer:", True, (255, 255, 255))
    timerLabelRect = pygame.Rect((25, 200, 50, 50))
    p1TimerLabel = labelFont.render("Player 1 Timer:", True, (255, 255, 255))
    p1TimerLabelRect = pygame.Rect((75, 250, 50, 50))
    p2TimerLabel = labelFont.render("Player 2 Timer:", True, (255, 255, 255))
    p2TimerLabelRect = pygame.Rect((75, 300, 50, 50))
    p1RemoveLabel = labelFont.render("Player 1 Remove Max:", True, (255, 255, 255))
    p1RemoveLabelRect = pygame.Rect((25, 350, 50, 50))
    p2RemoveLabel = labelFont.render("Player 2 Remove Max:", True, (255, 255, 255))
    p2RemoveLabelRect = pygame.Rect((25, 400, 50, 50))

    #define the buttons
    cancelButton = Button((100, 100, 100), 25, 10, 200, 75, "Cancel")
    saveButton = Button((100, 100, 100), 500, 450, 200, 75, "Save")
    resetButton = Button ((100, 100, 100), 50, 450, 400, 75, "Reset to Default")

    #define the checkboxes
    timerCheckBox = CheckBox((255, 255, 255), 100, 190, 40, 40)
    timerCheckBox.value = tempTimerOn

    #define textboxes
    p1RTextBox = NumberTextBox((255, 255, 255), 275, 90, 85, 40, 0, 255)
    p1RTextBox.textValue = str(p1Colour[0])
    p1GTextBox = NumberTextBox((255, 255, 255), 375, 90, 85, 40, 0, 255)
    p1GTextBox.textValue = str(p1Colour[1])
    p1BTextBox = NumberTextBox((255, 255, 255), 475, 90, 85, 40, 0, 255)
    p1BTextBox.textValue = str(p1Colour[2])
    p2RTextBox = NumberTextBox((255, 255, 255), 275, 140, 85, 40, 0, 255)
    p2RTextBox.textValue = str(p2Colour[0])
    p2GTextBox = NumberTextBox((255, 255, 255), 375, 140, 85, 40, 0, 255)
    p2GTextBox.textValue = str(p2Colour[1])
    p2BTextBox = NumberTextBox((255, 255, 255), 475, 140, 85, 40, 0, 255)
    p2BTextBox.textValue = str(p2Colour[2])
    p1TimeTextBox = NumberTextBox((255,255,255), 275, 240, 40, 40, 1, 60)
    p1TimeTextBox.textValue = str(p1Timer)
    p2TimeTextBox = NumberTextBox((255,255,255), 275, 290, 40, 40, 1, 60)
    p2TimeTextBox.textValue = str(p2Timer)
    p1RemoveXTextBox = NumberTextBox((255,255,255), 275, 340, 40, 40, 1, 10)
    p1RemoveXTextBox.textValue = str(p1MaxRemoveX)
    p1RemoveYTextBox = NumberTextBox((255,255,255), 350, 340, 40, 40, 1, 10)
    p1RemoveYTextBox.textValue = str(p1MaxRemoveY)
    p2RemoveXTextBox = NumberTextBox((255,255,255), 275, 390, 40, 40, 1, 10)
    p2RemoveXTextBox.textValue = str(p2MaxRemoveX)
    p2RemoveYTextBox = NumberTextBox((255,255,255), 350, 390, 40, 40, 1, 10)
    p2RemoveYTextBox.textValue = str(p2MaxRemoveY)


    textBoxList = [
        p1RTextBox, p1GTextBox, p1BTextBox, 
        p2RTextBox, p2GTextBox, p2BTextBox, 
        p1TimeTextBox, p2TimeTextBox, 
        p1RemoveXTextBox, p1RemoveYTextBox,
        p2RemoveXTextBox, p2RemoveYTextBox,
                   ]

    for i in range(len(textBoxList)):
        textBoxList[i].updateNumValue()
    
    #Define other objects
    p1ColourSquare = pygame.Rect((200, 90, 40, 40))
    p2ColourSquare = pygame.Rect((200, 140, 40, 40))

    #game loop
    run = True

    #runs once per frame
    while run:

        #simple way to clear the drawings on a screen
        screen.fill((0,0,0))

        #display the screen title
        screen.blit(titleText, titleTextRect)
        
        #display labels
        screen.blit(p1ColourLabel, p1ColourLabelRect)
        screen.blit(p2ColourLabel, p2ColourLabelRect)
        screen.blit(timerLabel, timerLabelRect)
        screen.blit(p1TimerLabel, p1TimerLabelRect)
        screen.blit(p2TimerLabel, p2TimerLabelRect)
        screen.blit(p1RemoveLabel, p1RemoveLabelRect)
        screen.blit(p2RemoveLabel, p2RemoveLabelRect)
 
        #display the buttons
        cancelButton.update()
        saveButton.update()
        resetButton.update()

        #display checkboxes
        timerCheckBox.update()

        #display text boxes
        for i in range(len(textBoxList)):
            textBoxList[i].update()


        #displayer other objects
        tempP1Colour = (p1RTextBox.numValue, p1GTextBox.numValue, p1BTextBox.numValue)
        pygame.draw.rect(screen, tempP1Colour, p1ColourSquare)
        tempP2Colour = (p2RTextBox.numValue, p2GTextBox.numValue, p2BTextBox.numValue)
        pygame.draw.rect(screen, tempP2Colour, p2ColourSquare)

        #changes the colour of the button or checkbox if the mouse is hovering over it
        cancelButton.changeColour(pygame.mouse.get_pos())
        saveButton.changeColour(pygame.mouse.get_pos())
        resetButton.changeColour(pygame.mouse.get_pos())
        timerCheckBox.changeColour(pygame.mouse.get_pos())

        for i in range(len(textBoxList)):
            textBoxList[i].changeColour(pygame.mouse.get_pos())

        
        #event handler
        for event in pygame.event.get():
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True



            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:

                #check if checkboxes have been clicked
                timerCheckBox.checkClicked(pygame.mouse.get_pos())

                #checks if any text boxes have been clicked
                for i in range(len(textBoxList)):
                    textBoxList[i].checkClicked(pygame.mouse.get_pos())

                #if the cancle button has been clicked...
                if cancelButton.checkClicked(pygame.mouse.get_pos()):

                    #go to the previous screen
                    run = False

                #if the save button has been clicked...
                if saveButton.checkClicked(pygame.mouse.get_pos()):
                    
                    #get values from textboxes
                    tempP1Colour = (p1RTextBox.numValue, p1GTextBox.numValue, p1BTextBox.numValue)
                    tempP2Colour = (p2RTextBox.numValue, p2GTextBox.numValue, p2BTextBox.numValue)
                    tempP1Timer = p1TimeTextBox.numValue
                    tempP2Timer = p2TimeTextBox.numValue
                    tempP1MaxRemoveX = p1RemoveXTextBox.numValue
                    tempP1MaxRemoveY = p1RemoveYTextBox.numValue
                    tempP2MaxRemoveX = p2RemoveXTextBox.numValue
                    tempP2MaxRemoveY = p2RemoveYTextBox.numValue                 

                    #get values from chec boxes
                    tempTimerOn = timerCheckBox.value

                    #change global gamerule variables
                    p1Colour = tempP1Colour
                    p2Colour = tempP2Colour
                    p1Timer = tempP1Timer
                    p2Timer = tempP2Timer
                    p1MaxRemoveX = tempP1MaxRemoveX
                    p1MaxRemoveY = tempP1MaxRemoveY
                    p2MaxRemoveX = tempP2MaxRemoveX
                    p2MaxRemoveY = tempP2MaxRemoveY
                    timerOn = tempTimerOn

                    #go to the previous screen
                    return

                #if the reset button has been clicked...
                if resetButton.checkClicked(pygame.mouse.get_pos()):

                    #reset all global variables to their default values
                    tempP1Colour = (255, 0, 0)
                    tempP2Colour = (0, 0, 255)
                    tempTimerOn = False
                    timerCheckBox.value = False
                    tempP1Timer = 2
                    tempP2Timer = 2
                    tempP1MaxRemoveX = 2
                    tempP1MaxRemoveY = 2
                    tempP2MaxRemoveX = 2
                    tempP2MaxRemoveY = 2
                    
                    #resets all text boxes to their default values
                    p1RTextBox.textValue = str(p1Colour[0])                    
                    p1GTextBox.textValue = str(p1Colour[1])
                    p1BTextBox.textValue = str(p1Colour[2])
                    p2RTextBox.textValue = str(p2Colour[0])
                    p2GTextBox.textValue = str(p2Colour[1])
                    p2BTextBox.textValue = str(p2Colour[2])
                    p1TimeTextBox.textValue = str(p1Timer)
                    p2TimeTextBox.textValue = str(p2Timer)
                    p1RemoveXTextBox.textValue = str(p1MaxRemoveX)
                    p1RemoveYTextBox.textValue = str(p1MaxRemoveY)
                    p2RemoveXTextBox.textValue = str(p2MaxRemoveX)
                    p2RemoveYTextBox.textValue = str(p2MaxRemoveY)

                    for i in range(len(textBoxList)):
                        textBoxList[i].updateNumValue()

            #gets text input from the user and adds it to the currently selected textbox
            if event.type == pygame.TEXTINPUT:
                for i in range(len(textBoxList)):
                    if textBoxList[i].isSelected:
                        textBoxList[i].appendText(event.text)


            if event.type == pygame.KEYDOWN:

                #if the back space key is pressed, remove the character at the end of the currently selected text box
                if event.key == pygame.K_BACKSPACE:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].backspace()

                #if the enter key is pressed, update the numerical value of the currently selected text box and deselect it
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].isSelected = False
                            textBoxList[i].updateNumValue()
                            textBoxList[i].textValue = str(textBoxList[i].numValue)

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed during any screen...
        if quitStatus:
            run = False

def TheGame(boardArr):
    global quitStatus

    #global gamerule variables
    global p1Colour
    global p2Colour
    global timerOn
    global p1Timer
    global p2Timer
    global advDisplayOn
    global p1MaxRemoveX
    global p1MaxRemoveY
    global p2MaxRemoveX
    global p2MaxRemoveY
    global p1Turn
    global singlePlayerMode
    global playerTurn

    #define the board
    board = TheBoard(250, 100, 400, 400)
    board.createBoard(boardArr)
    board.falls()

    #define the buttons
    forfeitButton = Button((100, 100, 100), 25, 100, 150, 75, "Forfeit")

    #define labels
    p1TurnLabel = labelFont.render("Player 1's", True, p1Colour)
    p1TurnLabelRect = pygame.Rect((125, 25, 50, 50))
    p2TurnLabel = labelFont.render("Player 2's", True, p2Colour)
    p2TurnLabelRect = pygame.Rect((125, 25, 50, 50))
    turnLabel = labelFont.render("Turn", True, (255, 255, 255))
    turnLabelRect = pygame.Rect((250, 25, 50, 50))
    p1TimerLabel = labelFont.render("1:37", True, p1Colour)
    p1TimerRect = pygame.Rect((350, 25, 50, 50))
    p2TimerLabel = labelFont.render("2:00", True, p2Colour)
    p2TimerRect = pygame.Rect((410, 25, 50, 50))
    timerLabel = labelFont.render("|", True, (255, 255, 255))
    timerRect = pygame.Rect((400, 25, 50, 50))
    invalidLabel = mainFont.render("INVALID MOVE", True, (255, 255, 255))
    invalidLabelRect = pygame.Rect((25, 200, 50, 50))

    #define the selection box
    selectRect = pygame.Rect((0,0,50,50))
    showSelect = False
    selectRectOrigin = (0, 0)

    #define the clocks
    gameClock = pygame.time.Clock()
    p1TimeRemaining = p1Timer * 60000
    p2TimeRemaining = p2Timer * 60000

    #timers so that temporary displays are show for the correct amount of time
    invalidLabelCounter = 0
    compMoveCounter = 0
    compMoveShown = False

    #start on player 1's turn
    p1Turn = True
    
    #game loop
    run = True
    while run:

        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(turnLabel, turnLabelRect)
        
        #change the colour of the forfeit button dependning on whose turn it is, and update the current players clock
        if p1Turn:
            screen.blit(p1TurnLabel, p1TurnLabelRect)
            p1TimeRemaining = p1TimeRemaining - gameClock.get_time() * int(timerOn)
            forfeitButton = Button(p1Colour, 25, 100, 150, 75, "Forfeit")
        else:
            screen.blit(p2TurnLabel, p2TurnLabelRect)
            p2TimeRemaining = p2TimeRemaining - gameClock.get_time() * int(timerOn)
            forfeitButton = Button(p2Colour, 25, 100, 150, 75, "Forfeit")
        
        #change the colour of a button's text when the mous hovers over it
        forfeitButton.changeColour(pygame.mouse.get_pos())
        
        #display buttons
        forfeitButton.update()

        #calculate and display the digits for the player's clocks
        p1Mins = p1TimeRemaining // 60000
        p1Tens = (p1TimeRemaining - p1Mins * 60000) // 10000
        p1Secs = (p1TimeRemaining - p1Mins * 60000 - p1Tens * 10000) // 1000
        p1TimerLabel = labelFont.render(str(p1Mins) + ":" + str(p1Tens) + str(p1Secs), True, p1Colour)

        p2Mins = p2TimeRemaining // 60000
        p2Tens = (p2TimeRemaining - p2Mins * 60000) // 10000
        p2Secs = (p2TimeRemaining - p2Mins * 60000 - p2Tens * 10000) // 1000
        p2TimerLabel = labelFont.render(str(p2Mins) + ":" + str(p2Tens) + str(p2Secs), True, p2Colour)

        #if the timer is on
        if timerOn:

            #idsplay the player's clocks
            screen.blit(p1TimerLabel, p1TimerRect)
            screen.blit(p2TimerLabel, p2TimerRect)
            screen.blit(timerLabel, timerRect)
        
        #if a player is making a selection
        if showSelect:

            #calculate the size of the selection box
            selectRect.width = pygame.mouse.get_pos()[0] - selectRectOrigin[0]
            selectRect.height = pygame.mouse.get_pos()[1] - selectRectOrigin[1]

            #corrects the size of the box in case of negative values
            if selectRect.width < 0:
                selectRect.left = pygame.mouse.get_pos()[0]
                selectRect.width = selectRect.width * -1

            if selectRect.height < 0:
                selectRect.top = pygame.mouse.get_pos()[1]
                selectRect.height = selectRect.height * -1

            #determines the colour of the box depending on whose turn it is
            if p1Turn:
                pygame.draw.rect(screen, p1Colour, selectRect)
            else:
                pygame.draw.rect(screen, p2Colour, selectRect)
            
            #selects elements that are within the selection box
            board.checkSelection(selectRect)

        #displays the 'invalid move' label for the correct amount of time
        if invalidLabelCounter > 0:
            screen.blit(invalidLabel, invalidLabelRect)
            invalidLabelCounter = invalidLabelCounter - gameClock.get_time()

        #display the board
        board.update()

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been released and it is not the computer's turn...
            if event.type == pygame.MOUSEBUTTONDOWN and compMoveShown == False:
                showSelect = True
                selectRectOrigin = pygame.mouse.get_pos()
                selectRect.topleft = selectRectOrigin

            #if the left mouse button has been released and it is not the computer's turn...
            if event.type == pygame.MOUSEBUTTONUP and compMoveShown == False:

                #if the forfiet button was pressed
                if forfeitButton.checkClicked(pygame.mouse.get_pos()):
                    
                    #end the game
                    winscreen(boardArr)
                
                #if the selected elements are a legal move...
                if board.validateMove():
                    
                    #remove the selected elements from the board
                    board.remove()

                    #check if any elements need to fall
                    board.falls()
                    
                    #change the turn
                    p1Turn = not p1Turn

                    #stop displaying the 'invalid move' label
                    invalidLabelCounter = 0
                    
                    #if there are no elements remaining
                    if board.getRemainingElements() == 0:
                        
                        #end the game
                        winscreen(boardArr)

                #otherwise
                else:
                    #deslect the selected elemnts
                    board.deselect()

                    #display the 'invalid move' label for 1.5 seconds
                    invalidLabelCounter = 1500

                    #changes the colour of the invalid move label to that of the current player
                    if p1Turn:
                        invalidLabel = labelFont.render("INVALID MOVE", True, p1Colour)
                    else:
                        invalidLabel = labelFont.render("INVALID MOVE", True, p2Colour)
                
                #remove the selection box
                showSelect = False
                selectRect.bottomright = (0, 0)

        #if it is single player and it is not the players turn and the computer has already made a move and the move is finished being displayed
        if singlePlayerMode and p1Turn != playerTurn and compMoveCounter <= 0 and compMoveShown:
            
            #remove the selected elements from the board
            board.remove()

            #check if any elements need to fall
            board.falls()

            #stop displaying the move
            compMoveShown = False

            #if there are no elements left in the board...
            if board.getRemainingElements() == 0:
                #end the game
                winscreen(boardArr)

            #change the turn
            p1Turn = not p1Turn
                
        #if it is single player and it is not the players turn and the computer has not made a move
        if singlePlayerMode and p1Turn != playerTurn and compMoveShown == False:
            
            #calculate the computer's move
            board.computerMove()

            #display the computer's move for 1.5 seconds
            compMoveCounter = 1500
            compMoveShown = True
              
        #make sure that the computer's move is displayed for the correct amount of time
        if compMoveCounter > 0:
            compMoveCounter = compMoveCounter - gameClock.get_time()
        
            
        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

        #ends the game if either player has run out of time
        if p1Turn and p1TimeRemaining <= 0:
            winscreen(boardArr)
        elif p2TimeRemaining <= 0:
            winscreen(boardArr)

        #advances the clock
        gameClock.tick(60)

def winscreen(boardArr):
    
    #deifine global variables
    global quitStatus
    global p1Turn

    #define the buttons
    rematchButton = Button((100, 100, 100), 200, 300, 450, 75, "Rematch")
    mainMenuButton = Button((100, 100, 100), 200, 400, 450, 75, "Return to Main Menu")
    quitButton = Button((100, 100, 100), 200, 500, 450, 75, "Quit")

    #define labels
    if p1Turn == False:
        winLabel = mainFont.render("Player 1 Wins", True, p1Colour)
        winLabelRect = pygame.Rect((200, 25, 50, 50))
    else:
        winLabel = mainFont.render("Player 2 Wins", True, p2Colour)
        winLabelRect = pygame.Rect((200, 25, 50, 50))

    #game loop
    run = True
    while run:

        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(winLabel, winLabelRect)

        #display the buttons
        rematchButton.update()
        mainMenuButton.update()
        quitButton.update()

        #changes the colour of the button if the mouse is hovering over it
        rematchButton.changeColour(pygame.mouse.get_pos())
        mainMenuButton.changeColour(pygame.mouse.get_pos())
        quitButton.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:
                if rematchButton.checkClicked(pygame.mouse.get_pos()):
                    TheGame(boardArr)
                if mainMenuButton.checkClicked(pygame.mouse.get_pos()):
                    mainMenu()
                if quitButton.checkClicked(pygame.mouse.get_pos()):
                    quitStatus = True

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

def randomBoardScreen():
    global quitStatus

    #define text boxes
    widthTextBox = NumberTextBox((255, 255, 255), 200, 100, 75, 50, 1, 10)
    widthTextBox.numValue = 5
    widthTextBox.textValue = "5"
    heightTextBox = NumberTextBox((255, 255, 255), 200, 175, 75, 50, 1, 10)
    heightTextBox.numValue = 5
    heightTextBox.textValue = "5"
    rateTextBox = NumberTextBox((255, 255, 255), 200, 250, 75, 50, 1, 100)
    rateTextBox.numValue = 70
    rateTextBox.textValue = "70"

    #define the buttons
    generateButton = Button((100, 100, 100), 200, 400, 400, 75, "Generate Board")
    backButton = Button((100, 100, 100), 25, 25, 150, 75, "Back")

    #define labels
    widthLabel = mainFont.render("Width:", True, (255, 255, 255))
    widthLabelRect = pygame.Rect((25, 100, 50, 50))
    heightLabel = mainFont.render("Height:", True, (255, 255, 255))
    heightLabelRect = pygame.Rect((25, 175, 50, 50))
    rateLabel = mainFont.render("Rate:", True, (255, 255, 255))
    rateLabelRect = pygame.Rect((25, 250, 50, 50))

    textBoxList = [
        widthTextBox, heightTextBox, rateTextBox
    ]

    #game loop
    run = True
    while run:

        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(widthLabel, widthLabelRect)
        screen.blit(heightLabel, heightLabelRect)
        screen.blit(rateLabel, rateLabelRect)

        #display the buttons
        generateButton.update()
        backButton.update()

        #display text boxes
        widthTextBox.update()
        heightTextBox.update()
        rateTextBox.update()

        #changes the colour of the button if the mouse is hovering over it
        generateButton.changeColour(pygame.mouse.get_pos())
        widthTextBox.changeColour(pygame.mouse.get_pos())
        heightTextBox.changeColour(pygame.mouse.get_pos())
        rateTextBox.changeColour(pygame.mouse.get_pos())
        backButton.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:
                if  backButton.checkClicked(pygame.mouse.get_pos()):
                    return []

                #if the generate button has been clicekd
                if generateButton.checkClicked(pygame.mouse.get_pos()):
                    
                    
                    bottomCrosses = 0

                    #while there are no elements connected to the ground
                    while bottomCrosses == 0:

                        #generate a new random board
                        boardArr = randomBoard(widthTextBox.numValue, heightTextBox.numValue, rateTextBox.numValue)

                        #count how many elements are connected to the ground
                        for i in range(len(boardArr[len(boardArr) - 1])):
                            if boardArr[len(boardArr) - 1][i] == "X":
                                bottomCrosses = bottomCrosses + 1

                    return boardArr

                #checks if any text boxes have been clicked
                for i in range(len(textBoxList)):
                    textBoxList[i].checkClicked(pygame.mouse.get_pos())
             
            #gets text input from the user and adds it to the currently selected text box
            if event.type == pygame.TEXTINPUT:
                for i in range(len(textBoxList)):
                    if textBoxList[i].isSelected:
                        textBoxList[i].appendText(event.text)


            if event.type == pygame.KEYDOWN:
                
                #if the backspace key is pressed, remove the last character from the currently selected text box
                if event.key == pygame.K_BACKSPACE:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].backspace()

                #if the enter key is pressed, update the numerical values of the currently selected text box and deselect it
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].isSelected = False
                            textBoxList[i].updateNumValue()
                            textBoxList[i].textValue = str(textBoxList[i].numValue)

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

def customBoardScreen():

    quitStatus = False

    #define text boxes
    widthTextBox = NumberTextBox((255, 255, 255), 150, 25, 75, 50, 1, 10)
    widthTextBox.numValue = 5
    widthTextBox.textValue = "5"
    heightTextBox = NumberTextBox((255, 255, 255), 400, 25, 75, 50, 1, 10)
    heightTextBox.numValue = 5
    heightTextBox.textValue = "5"

    #define the buttons
    generateButton = Button((100, 100, 100), 200, 500, 400, 75, "Generate Board")
    backButton = Button((100, 100, 100), 25, 100, 150, 75, "Back")


    #define labels
    widthLabel = mainFont.render("Width:", True, (255, 255, 255))
    widthLabelRect = pygame.Rect((0, 25, 50, 50))
    heightLabel = mainFont.render("Height:", True, (255, 255, 255))
    heightLabelRect = pygame.Rect((240, 25, 50, 50))
    invalidLabel = mainFont.render("INVALID", True, (255, 0, 0))
    invalidLabelRect = pygame.Rect((25, 200, 50, 50))
    boardLabel = mainFont.render("BOARD", True, (255, 0, 0))
    boardLabelRect = pygame.Rect((25, 250, 50, 50))

    textBoxList = [
        widthTextBox, heightTextBox
    ]

    #define the board template
    board = TheCustomBoard(250, 100, 400, 400)
    board.createBoard()

    #define the clocks
    gameClock = pygame.time.Clock()

    #timers so that temporary displays are show for the correct amount of time
    invalidLabelCounter = 0

    #game loop
    run = True
    while run:

        #simple way to clear the screen of things from the previous refresh
        screen.fill((0,0,0))

        #Display labels
        screen.blit(widthLabel, widthLabelRect)
        screen.blit(heightLabel, heightLabelRect)

        #displays the 'invalid move' label for the correct amount of time
        if invalidLabelCounter > 0:
            screen.blit(invalidLabel, invalidLabelRect)
            screen.blit(boardLabel, boardLabelRect)
            invalidLabelCounter = invalidLabelCounter - gameClock.get_time()

        #display the buttons
        generateButton.update()
        backButton.update()

        #display text boxes
        widthTextBox.update()
        heightTextBox.update()

        #changes the colour of the button if the mouse is hovering over it
        generateButton.changeColour(pygame.mouse.get_pos())
        widthTextBox.changeColour(pygame.mouse.get_pos())
        heightTextBox.changeColour(pygame.mouse.get_pos())
        backButton.changeColour(pygame.mouse.get_pos())

        #display the board template
        board.update()

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:
                
                #if the back button has been clicked
                if backButton.checkClicked(pygame.mouse.get_pos()):
                    
                    #return an invalid board
                    return []

                #if the generate button has been clicked
                if generateButton.checkClicked(pygame.mouse.get_pos()):
                
                    #check that there are elements connected to the ground
                    for i in range(len(board.squaresList[len(board.squaresList) - 1])):

                        if board.squaresList[len(board.squaresList) - 1][i].value == "X":
                            
                            #return the board template as an array of characters
                            return board.generateBooardArr()
                     
                    #display the 'invalid move' label for 1.5 seconds
                    invalidLabelCounter = 1500

                #checks if any text boxes have been clicked
                for i in range(len(textBoxList)):
                    textBoxList[i].checkClicked(pygame.mouse.get_pos())

                #checks if any board squares have been clicked
                board.checkClicked(pygame.mouse.get_pos())

                #updates the size of the board template
                board.updateXSquares(widthTextBox.numValue)
                board.updateYSquares(heightTextBox.numValue)
                
            #gets text input from the user and adds it to the currently selected text box
            if event.type == pygame.TEXTINPUT:
                for i in range(len(textBoxList)):
                    if textBoxList[i].isSelected:
                        textBoxList[i].appendText(event.text)

            if event.type == pygame.KEYDOWN:

                #if the backspace key is pressed, remove the last character from the currently selected text box and deslect it
                if event.key == pygame.K_BACKSPACE:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].backspace()

                #if the enter key is pressed, update the numerical value of the currently selected text box and deselect it
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    for i in range(len(textBoxList)):
                        if textBoxList[i].isSelected:
                            textBoxList[i].isSelected = False
                            textBoxList[i].updateNumValue()
                            textBoxList[i].textValue = str(textBoxList[i].numValue)
                    
                    #updates the size of the board template
                    board.updateXSquares(widthTextBox.numValue)
                    board.updateYSquares(heightTextBox.numValue)

        #refreshes the screen to show changes that were made earlier in the loop
        pygame.display.update()

        #advances the clock
        gameClock.tick(60)

        #if the quit button has been pressed in any screen...
        if quitStatus:
            run = False

def howToPlay():
    global quitStatus

    #loads images that will be needed
    rulesPage = pygame.image.load('TheRulesPage.png')
    controlsPage = pygame.image.load('TheControlsPage.png')

    #defines the buttons
    backButton = Button((100, 100, 100), 10, 10, 125, 75, "Back")
    nextButton = Button((100, 100, 100), 665, 260, 125, 75, "Next")
    prevButton = Button((100, 100, 100), 10, 260, 125, 75, "Prev")

    page = 0

    run = True

    while run:
        screen.fill((0, 0, 0))
        
        #displays the buttons
        backButton.update()

        if page == 0:
            nextButton.update()
            screen.blit(rulesPage, (155, 7))
        else:
            prevButton.update()
            screen.blit(controlsPage, (155, 7))

        #changes the colour of the buttons if the mouse is hovering over them
        backButton.changeColour(pygame.mouse.get_pos())
        nextButton.changeColour(pygame.mouse.get_pos())
        prevButton.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:
                
                if backButton.checkClicked(pygame.mouse.get_pos()):
                    run = False

                if nextButton.checkClicked(pygame.mouse.get_pos()):
                    page = 1

                if prevButton.checkClicked(pygame.mouse.get_pos()):
                    page = 0

        if quitStatus:
            run = False

        pygame.display.update()

def randomBoard(x, y, rate):
    #create an empty board
    board = []

    #create the rows
    for i in range(y):
        board.append([])

        #create the columns
        for j in range(x):

            #decide whether or not current position contains an element
            if random.randint(0, 100) < rate: 
                board[i].append("X")
            else:
                board[i].append(" ")

    return board

def aboutMe():
    global quitStatus

    #loads images that will be needed
    aboutMePage = pygame.image.load('AboutMePage.png')


    #defines the buttons
    backButton = Button((100, 100, 100), 10, 10, 125, 75, "Back")

    run = True

    while run:
        screen.fill((0, 0, 0))
        
        #displays the buttons
        backButton.update()

        screen.blit(aboutMePage, (155, 7))


        #changes the colour of the buttons if the mouse is hovering over them
        backButton.changeColour(pygame.mouse.get_pos())

        #event handler
        for event in pygame.event.get():
            
            #if the 'x' icon on the window is clicked...
            if event.type == pygame.QUIT:
                quitStatus = True

            #if the left mouse button has been pressed...
            if event.type == pygame.MOUSEBUTTONUP:
                
                if backButton.checkClicked(pygame.mouse.get_pos()):
                    run = False

        if quitStatus:
            run = False

        pygame.display.update()

mainMenu()
pygame.quit()

