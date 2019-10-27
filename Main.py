from tkinter import * 
import scholarly
import time
import math

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

    def __init__(self, x, y, radius, canvas, currDepth, indAngle, searchQuery=None):

        self.canvas = canvas
        self.x = x 
        self.y = y 
        self.indAngle = indAngle
        self.subNodes = []
        self.depth = currDepth
        self.radius = radius
        self.line = None
        self.leaf = True 

        if (searchQuery != None):
            self.searchQuery = searchQuery
            string = searchQuery.citedby
        else:
            string = "No Value"
        
        header = self.canvas.create_text(self.x, self.y, text=string,
                                         font=("Helvetica", 20 - (3 * currDepth)))
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

    def updateNodePosition(self):
        coords = self.canvas.coords(self.node)
        self.x = (coords[0] + coords[2]) / 2
        self.y = (coords[1] + coords[3]) / 2
        #print ("COORDS: " + str(self.canvas.coords(self.node)) + " vs " + str(self.x)
        #+ " " + str(self.y))

class RNodeCont():

    def __init__(self, ncount, canvas, author):
        self.ncount = ncount
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.searchQuery = RNodeCont.refByAuthor(author)
        self.canvas = canvas
        self.rNode = RNode(self.x, self.y, START_RAD, canvas, 0, 0, 
                           self.searchQuery)
        self.rNode.renderCircle()
        self.generateRoot(self.rNode, DIST_START)

    def generateRoot(self, currNode, distance):
        currAngle = 0
        deltaAngle = ((2 * math.pi) / self.ncount)

        # Full cirle
        while currAngle < (2 * math.pi):
            addNode = RNode(currNode.x + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.cos(currAngle),
                            currNode.y + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.sin(currAngle),
                            (currNode.radius * SIZE_RATIO), 
                            self.canvas, 1, currAngle)
            
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
        
            self.generateRecursive(addNode, distance, 1)
            self.canvas.pack(fill=BOTH, expand=1)
            currAngle += deltaAngle 
    
    def generateRecursive(self, currNode, distance, currDepth):
        currNumNodes = self.ncount - currDepth
        if (currNumNodes == 1):
            return
        
        deltaAngle = 0.6 # 0.523
        currAngle = currNode.indAngle + (2*math.pi) - ((currNumNodes-1)*deltaAngle/2)
        for it in range(0, currNumNodes):
#            print ("GENERATE")            
            addNode = RNode(currNode.x + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.cos(currAngle), 
                            currNode.y + (currNode.radius + distance +
                            (currNode.radius * SIZE_RATIO)) * math.sin(currAngle), 
                            (currNode.radius * SIZE_RATIO), 
                            self.canvas, currDepth, currAngle)
             
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
        #print ("BOUNDING BOX " + str(x0 >= (x - r)) + " " + str(x0 <= (x + r)) +
        #" " + str(y0 >= (y - r)) + " " + str(y0 <= (y + r)))
        #print ("")
        if (((x0 >= (x1 - r)) & (x0 <= (x1 + r))) 
            & ((y0 >= (y1 - r)) & (y0 <= (y1 + r)))): 
            return True 
        else:
            return False 

    def scaleAll(self, currNode, scaleFac):
        if (currNode == self.rNode):
            pass
            
        for subNode in currNode.subNodes:
            self.canvas.scale(subNode.node, scaleFac, scaleFac, subNode.radius,
                              subNode.radius)
            scaleAll(subNode, currNode)
    

    def recenter(self, centerNode):
        deltaX = 960 - centerNode.x 
        deltaY = 540 - centerNode.y
        self.canvas.move(ALL, deltaX, deltaY) 
        self.updateAllPositions(self.rNode)
        if centerNode.leaf == True:
            self.generateRecursive(centerNode, DIST_START, 0) 
            self.scaleAll(self.rNode, 50, self.rNode.radius, self.rNode.radius)

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
        print ("CLICK: " + str(self.x) + " " + str(self.y))
        self.cont.selectNode(self.cont.rNode, self.x, self.y)    
        #self.cont.updateAllPositions(self.cont.rNode)

def main():
    root = Tk()
    gui = GUI()
    canvas = gui.getCanvas()
    root.geometry(RESOLUTION)
    author = "Marty Banks"
    cont = RNodeCont(4, canvas, author) 
    ev = EventHandler(cont)
    canvas.bind("<Button-1>", ev.mouseClick)
    root.mainloop()

if __name__ == '__main__':
    main()




#currAngle = currNode.indAngle + math.pi + ((3 * math.pi) / 4)

#deltaAngle = ((2 * math.pi) / (4 * (currNumNodes - 1)))
#print ("DCURR: " + str(deltaAngle))
#print ("QUANT: " + str((currNode.indAngle + math.pi + (4 * math.pi) /
#3)))

#print ("CURR: " + str(currAngle))

#while (currAngle <= 
        #((currNode.indAngle + math.pi + (5 * math.pi) / 4) + EPSILLON)):
    #print ("ENTERED ")            
#while (currAngle <= currNode.indAngle + (2*math.pi) +
#(currNumNodes*deltaAngle/2) + EPSILLON):


