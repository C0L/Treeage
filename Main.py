from tkinter import * 
import scholarly
import time
import math
from bs4 import BeautifulSoup

#Constants
RESOLUTION = "1920x1080"

WINDOW_WIDTH = 1920 
WINDOW_HEIGHT = 1080 

FONT = "times"

TEXT_SIZE = 10

CIRCLE_SIZE = 2
START_RAD = 100
DIST_START = 80 
EPSILLON = .001
SIZE_RATIO = (2/3)


class GUI(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getCanvas(self):
        return self.canvas

    def initUI(self):
        self.master.title("TREEAGE")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.configure(background='white')
        self.canvas.pack(fill=BOTH, expand=1)

class RNode():

    def __init__(self, x, y, radius, canvas, currDepth, indAngle, pub = None):
        self.canvas = canvas
        self.x = x 
        self.y = y 
        self.indAngle = indAngle
        self.subNodes = []
        self.depth = currDepth
        self.radius = radius
        self.line = None
        self.leaf = True 
        
        if (pub != None):
            self.pub = pub 
            self.string = pub.citedby
        else:
            self.string = "None" 
        
        self.header = self.canvas.create_text(self.x, self.y, text = self.string,
                                         font=("Helvetica", 20 - (3 * currDepth)))
            
        absString = str(self.pub.bib['abstract'])

        abstract = ("Title: " + self.pub.bib['title'] + "\n Author: " 
              + self.pub.bib['author'] + " \n Abstract: " + absString)

        self.wind = Label(canvas, borderwidth = 5, width=23, 
            font='helvetica', text = abstract, wraplength = 200)



        canvas.update() 

    def renderCircle(self):
        self.node = self.canvas.create_oval(
                self.x - self.radius, self.y - self.radius, 
                self.x + self.radius, self.y + self.radius, 
                width=2)
         
    def addSubNode(self, x, y, x0, y0, addNode):
        self.leaf = False
        self.line = self.canvas.create_line(x, y, x0, y0)
        self.subNodes.append(addNode) 

    def resize(self, newRad):
        oldRad = self.radius
        self.radius = newRad
        self.canvas.delete(self.node)
        self.node = self.canvas.create_oval(
                self.x + (self.radius - oldRad) * math.cos(self.indAngle) - self.radius,
                self.y + (self.radius - oldRad) * math.sin(self.indAngle) - self.radius,
                self.x + (self.radius-oldRad) * math.cos(self.indAngle)
                +self.radius, self.y + (self.radius-oldRad) *
                math.sin(self.indAngle) + self.radius, 
                width=2)


        self.x = self.x + (self.radius - oldRad) * math.cos(self.indAngle)
        self.y = self.y + (self.radius - oldRad) * math.sin(self.indAngle)
        
        self.canvas.delete(self.header)
        self.header = self.canvas.create_text(self.x, self.y, text=self.string,
                                     font=("Helvetica", 20))
        

    def updateNodePosition(self):
        coords = self.canvas.coords(self.node)
        self.x = (coords[0] + coords[2]) / 2
        self.y = (coords[1] + coords[3]) / 2
        self.wind.place_forget()

class RNodeCont():

    def __init__(self, ncount, canvas, author):
        self.ncount = ncount
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2

        self.searchQuery = scholarly.search_author(author)
        self.author = next(self.searchQuery).fill()
        self.pub = self.author.publications[0].fill()
        
        self.canvas = canvas
        self.rNode = RNode(self.x, self.y, START_RAD, canvas, 0, 0, self.pub)
        self.rNode.renderCircle()
        self.generateRoot(self.rNode, DIST_START)

    def generateRoot(self, currNode, distance):
        currAngle = 0
        deltaAngle = ((2 * math.pi) / self.ncount)
         
        currCite = currNode.pub.get_citedby()
        currPub = next(currCite)
    
        # Full cirle
        while currAngle < (2 * math.pi):
            #print (pubs[0]) 
            addNode = RNode(currNode.x + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.cos(currAngle),
                            currNode.y + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.sin(currAngle),
                            (currNode.radius * SIZE_RATIO), 
                            self.canvas, 1, currAngle, currPub)
            
            addNode.renderCircle()
            currNode.addSubNode(currNode.x + currNode.radius * 
                                math.cos(currAngle),
                                currNode.y + currNode.radius * 
                                math.sin(currAngle),
                                currNode.x + (currNode.radius + distance) 
                                * math.cos(currAngle),
                                currNode.y + (currNode.radius + distance) 
                                * math.sin(currAngle), 
                                addNode)
        
            currPub = next(currCite)
            self.generateRecursive(addNode, distance, 1)
            self.canvas.pack(fill=BOTH, expand=1)
            currAngle += deltaAngle 


    def generateRecursive(self, currNode, distance, currDepth):
        currNumNodes = self.ncount - currDepth
        if (currNumNodes == 1):
            return
        
        currCite = currNode.pub.get_citedby()
        currPub = next(currCite)

        deltaAngle = 0.6 # 0.523
        currAngle = currNode.indAngle + (2*math.pi) - ((currNumNodes-1)*deltaAngle/2)
        #count = 0
        for it in range(0, currNumNodes):
            addNode = RNode(currNode.x + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.cos(currAngle),
                            currNode.y + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.sin(currAngle),
                            (currNode.radius * SIZE_RATIO), 
                            self.canvas, currDepth, currAngle, currPub)
             
            addNode.renderCircle()
            currNode.addSubNode(currNode.x + currNode.radius * 
                                math.cos(currAngle),
                                currNode.y + currNode.radius * 
                                math.sin(currAngle),
                                currNode.x + (currNode.radius + distance) 
                                * math.cos(currAngle),
                                currNode.y + (currNode.radius + distance) 
                                * math.sin(currAngle), 
                                addNode)
            
            currPub = next(currCite)
            self.generateRecursive(addNode, distance, currDepth + 1)
            self.canvas.pack(fill=BOTH, expand=1)
            currAngle += deltaAngle 

    def selectNode(self, currNode, xIn, yIn):
        if ((currNode == self.rNode)  
            & RNodeCont.contains(currNode.x, currNode.y, currNode.radius, xIn,
            yIn)):
            self.recenter(currNode)
            return

        for subNode in currNode.subNodes:
            if (RNodeCont.contains(subNode.x, subNode.y, subNode.radius, xIn,
            yIn)):
                self.recenter(subNode)
                return
            
            self.selectNode(subNode, xIn, yIn)

    def contains(x1, y1, r, x0, y0):
        if (((x0 >= (x1 - r)) & (x0 <= (x1 + r))) 
            & ((y0 >= (y1 - r)) & (y0 <= (y1 + r)))): 
            return True 
        else:
            return False 

    def recenter(self, centerNode):
        deltaX = 960 - centerNode.x 
        deltaY = 540 - centerNode.y
        self.canvas.move(ALL, deltaX, deltaY) 
        self.updateAllPositions(self.rNode)
        centerNode.wind.place(relx=1.0, rely=0.0, anchor='ne')
        if centerNode.leaf == True:
            centerNode.resize(START_RAD - 20)
            self.generateRecursive(centerNode, DIST_START, 1) 


    def updateAllPositions(self, currNode):
        if (currNode == self.rNode):  
            self.rNode.updateNodePosition()
        
        for subNode in currNode.subNodes:
            subNode.updateNodePosition() 
            self.updateAllPositions(subNode)

    def refByAuthor(author):
        searchQuery = scholarly.search_author(author)
        return next(searchQuery)
   
    def refByPaper(paper):
        searchQuery = scholarly.search_pubs_query(paper)
        return next(searchQuery)

    def refByKeyword(paper):
        searchQuery = scholarly.search_keyword(keyword)
        return next(searchQuery)
            

class EventHandler():
    def __init__(self, cont):
        self.cont = cont
    
    def mouseClick(self, event):
        self.x = event.x
        self.y = event.y
        self.cont.selectNode(self.cont.rNode, self.x, self.y)    

def main():
    root = Tk()
    gui = GUI()
    canvas = gui.getCanvas()
    root.geometry(RESOLUTION)
    author = sys.argv[0]
    cont = RNodeCont(4, canvas, author) 
    ev = EventHandler(cont)
    canvas.bind("<Button-1>", ev.mouseClick)
    root.mainloop()

if __name__ == '__main__':
    main()
