from tkinter import * 
import math

#Constants
RESOLUTION = "1920x1080"

WINDOW_WIDTH = 1920 
WINDOW_HEIGHT = 1080 

FONT = "times"

TEXT_SIZE = 10

CIRCLE_SIZE = 2
CIRCLE_WIDTH = 100
CIRCLE_HEIGHT = 100

DIST_START = 50

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

    def __init__(self, x, y, canvas, currDepth):
        string = "test"
        self.canvas = canvas
        self.x = x 
        self.y = y 
        self.filledAng = 0
        self.subNodes = []
        self.depth = currDepth
        header = Label(canvas, text=string, fg="black", bg="white", 
                font=("Helvetica, 16"))
        header.place(x=self.x, y=self.y)

    def renderCircle(self):
        self.node = self.canvas.create_oval(
                self.x - CIRCLE_WIDTH, self.y - CIRCLE_HEIGHT, 
                self.x + CIRCLE_WIDTH, self.y + CIRCLE_HEIGHT, 
                width=2)

    def addSubNode(self, x, y, x0, y0, addNode, angle):
        self.filledAng = angle
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

        self.recurseNum = 0

        rNode = RNode(self.x, self.y, canvas, 0)
        rNode.renderCircle()
        self.recursiveDraw(rNode, DIST_START, 0)

    def recursiveDraw(self, currNode, distance, currDepth):
        if (currNode.depth == 1):
            return 
        angle = 0
        theta = angle+math.pi+((2*math.pi)/(self.ncount+1))
        dangle=((2*math.pi)/self.ncount)
        r = 100 

        while angle < self.ncount*dangle:

            addNode = RNode(currNode.x+(r+distance+r)*math.cos(angle), 
                            currNode.y+(r+distance+r)*math.sin(angle), 
                            self.canvas, currDepth)
            addNode.renderCircle()
            currNode.addSubNode(currNode.x+r*math.cos(angle), 
                                currNode.y+r*math.sin(angle),
                                currNode.x+(r+distance)*math.cos(angle),
                                currNode.y+(r+distance)*math.sin(angle), 
                                addNode, angle)
            self.recursiveDraw(addNode, distance, currDepth + 1)
            self.canvas.pack(fill=BOTH, expand=1)
            angle+=dangle 

def main():
    root = Tk()
    gui = GUI()
    canvas = gui.getCanvas()
    root.geometry(RESOLUTION)
    main = RNodeCont(6, canvas) 
    root.mainloop()

if __name__ == '__main__':
    main()
