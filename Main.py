from tkinter import * 
import math

#Constants
RESOLUTION = "1920x1080"

WINDOW_WIDTH = 1920 
WINDOW_HEIGHT = 1080 

FONT = "times"

TEXT_SIZE = 10

CIRCLE_SIZE = 2
START_RAD = 100
DIST_START = 100 
EPSILLON = .001
SIZE_RATIO = (1/2)


class GUI(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getCanvas(self):
        return self.canvas

    def initUI(self):
        self.master.title("RS")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.configure(background='white')
        self.canvas.pack(fill=BOTH, expand=1)

class RNode():

    def __init__(self, x, y, radius, canvas, currDepth, indAngle):
        string = "test"
        self.canvas = canvas
        self.x = x 
        self.y = y 
        self.indAngle = indAngle
        self.subNodes = []
        self.depth = currDepth
        self.radius = radius
        #header = Label(canvas, text=string, fg="black", bg="white", 
         #       font=("Helvetica, 16"))

        #canvas.update() 
        #print ("ERR: " + str(header.winfo_width()))
        #header.place(x = (self.x - (20)),
        #             y = (self.y - (10)))

    def renderCircle(self):
        self.node = self.canvas.create_oval(
                self.x - self.radius, self.y - self.radius, 
                self.x + self.radius, self.y + self.radius, 
                width=2)

    def addSubNode(self, x, y, x0, y0, addNode):
        #print ("CURR ANLGLE IN ADD: " + str(currAngle))
        #self.indAngle = currAngle
        self.line = self.canvas.create_line(x, y, x0, y0)
        self.subNodes.append(addNode) 

    def moveTo(self):
        pass


class RNodeCont():

    def __init__(self, ncount, canvas):
        self.ncount = ncount
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.canvas = canvas

#        self.recurseNum = 0

        rNode = RNode(self.x, self.y, START_RAD, canvas, 0, 0)
        rNode.renderCircle()
        self.generateRoot(rNode, DIST_START)

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
        
            #print ("GENROOT")        
            self.generateRecursive(addNode, SIZE_RATIO * distance, 1)
            self.canvas.pack(fill=BOTH, expand=1)
            currAngle += deltaAngle 
    
    def generateRecursive(self, currNode, distance, currDepth):
#        if (currNode.depth == 3):
#            return 
        
        currNumNodes = self.ncount - currDepth
        
        if (currNumNodes == 1):
            return

        #print ("IND ANG: " + str(currNode.indAngle))        
        currAngle = currNode.indAngle + math.pi + ((3 * math.pi) / 4)
        deltaAngle = ((2 * math.pi) / (4 * (currNumNodes - 1)))
        #print ("DCURR: " + str(deltaAngle))
        #print ("QUANT: " + str((currNode.indAngle + math.pi + (4 * math.pi) /
        #3)))

        #print ("CURR: " + str(currAngle))
        
        while (currAngle <= 
                ((currNode.indAngle + math.pi + (5 * math.pi) / 4) + EPSILLON)):
            #print ("ENTERED ")            
            
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
            #print ("GENRECURSE: " + str(currAngle))        
            self.generateRecursive(addNode, SIZE_RATIO * distance, currDepth + 1)
            
            #print ("CURR: " + str(currAngle))
            #print ("QUANT: " + str((currNode.indAngle + math.pi + (4 * math.pi) / 3)))

   
            self.canvas.pack(fill=BOTH, expand=1)
            currAngle += deltaAngle 


def main():
    root = Tk()
    gui = GUI()
    canvas = gui.getCanvas()
    root.geometry(RESOLUTION)
    main = RNodeCont(4, canvas) 
    root.mainloop()

if __name__ == '__main__':
    main()
