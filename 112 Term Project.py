### Levels
#todo: write the coordinates of the wall blocks
#levels are 2D lists that have topLeft and bottomRight of the blocks
level1 = [[(9,46),(16,47)],[(16,45),(19,46)],[(19,44),(20,45)],
            [(17,43),(18,44)],
            [(15,42),(16,46)],[(9,41),(10,46)],[(11,42),(15,43)],
            [(11,41),(14,42)],[(6,40),(10,41)],[(6,41),(7,42)],
            [(3,42),(6,43)],[(2,38),(3,42)],[(4,39),(5,40)],
            [(3,37),(5,38)],[(4,34),(5,37)],[(1,33),(5,34)],[(0,26),(1,33)],
            [(1,27),(2,28)],[(1,25),(6,26)],[(2,30),(4,32)],[(4,30),(6,31)],
            [(6,25),(7,48)],[(7,48),(14,39)],[(13,39),(14,40)],
            [(14,41),(15,42)],[(15,38),(16,40)],[(16,40),(18,41)],
            [(18,40),(19,43)],[(20,39),(21,44)],[(18,38),(21,39)],
            [(17,36),(18,39)],[(13,35),(17,37)],[(11,35),(12,38)],
            [(8,35),(11,36)],[(8,28),(9,35)],[(7,22),(8,28)],[(8,27),(11,28)],
            [(8,28),(10,29)],[(12,27),(13,34)],[(11,29),(14,30)],
            [(15,34),(19,35)],[(19,30),(20,35)],[(19,30),(23,31)],
            [(22,27),(23,31)],[(22,27),(25,28)],[(25,26),(27,27)],
            [(26,22),(27,27)],[(22,22),(26,23)],[(23,25),(24,26)],
            [(20,22),(22,25)],[(18,28),(21,29)],[(19,26),(21,29)],
            [(20,25),(21,26)],[(17,26),(18,27)],[(9,24),(12,26)],
            [(15,28),(17,29)],[(16,29),(17,30)],[(16,30),(18,33)],
            [(12,25),(15,26)],[(14,26),(15,28)],[(8,22),(11,23)],
            [(18,23),(19,25)],[(12,22),(15,23)],[(13,21),(15,24)],
            [(16,23),(17,25)],[(15,23),(16,24)],[(16,20),(17,22)],
            [(17,21),(21,22)],[(14,12),(16,20)],[(11,19),(21,20)],
            [(12,21),(11,20)],[(9,19),(10,22)],[(16,17),(17,20)],
            [(6,19),(9,20)],[(6,13),(7,19)],[(7,13),(9,14)],[(9,17),(12,18)],
            [(10,14),(11,17)],[(12,12),(14,13)],[(20,8),(21,19)],
            [(19,12),(20,14)],[(18,15),(19,18)],[(17,11),(18,16)],
            [(14,10),(19,11)],[(12,8),(15,10)],[(6,10),(13,11)],
            [(8,11),(10,12)],[(8,12),(9,13)],[(16,8),(20,9)],
            [(16,6),(17,8)],[(11,6),(16,7)],
            [(8,6),(11,9)],[(6,5),(10,6)],[(6,7),(7,10)],
            [(1,7),(6,8),[(4,5),(5,7)],[(1,1),(2,7)],
            [(2,1),(9,2)],[(8,2),(9,4)],[(9,3),(13,4)],
            [(3,3),(6,4)],[(6,3),(7,5)],[(12,1),(13,3)],
            [(12,0),(15,1)],[(14,1),(15,6)],[(11,4),(13,5)]]



### Classes
class Wall:
    def __init__(self, topLeft, bottomRight):
        #topLeft and bottomRight are tuples (x,y)
        self.top = topLeft[1]
        self.left = topLeft[0]
        self.bottom = bottomRight[1]
        self.right = bottomRight[0]
            
    def moveWall(self, dx, dy):
        self.top += dx
        self.bottom += dx
        self.right -= dy
        self.left -= dy

class Cannon(Wall):
    def init(self, topLeft, bottomRight, direction):
        super().__init__(topLeft, bottomRight)
        self.direction = direction
        
        

class Player:
    def __init__(self, avatar, x, y, size):
        self.avatar = avatar
        self.speed = 40
        self.r = size
        self.x = x
        self.y = y
        
    
class Button:
    def __init__(self, name, cx, cy, color):
        self.color = color
        self.name = name
        self.top = cy-10
        self.left = cx-30
        self.bottom = cy+10
        self.right = cx+30
        
class PauseButton(Button):
    def __init__(self, cx, cy, color):
        self.size = 20
        self.top = cy-self.size
        self.left = cx-self.size
        self.bottom = cy+self.size
        self.right = cx+self.size


### Graphics
from tkinter import *

def init(data):
    data.walls = []
    data.mode = "start"
    data.pixel = 40 #the unit length in the game
    data.margin = 10 # margin for the pause button
    # and scrollY
    #todo: figure out correct sX and sY to start player in middle of screen
    #todo: and at the bottom of the map
    data.sX = 0
    data.sY = 0
    #center coordinates for the player
    data.cX = data.width//data.pixel//2
    data.cY = data.height//data.pixel//2
    data.buttonColor = "green"
    data.clickColor = "red"
    data.player = Player(avatar, data.cX, data.cY, data.pixel/2)
    data.playButton = Button("PLAY", data.width//2, 3*data.height//5,\
                            data.buttonColor)
    data.menuButton = Button("MENU", data.width//2, 4*data.height//5, \
                                data.buttonColor)
    data.pauseButton = PauseButton(data.width-data.margin-(data.pixel/2),\
                                data.margin+data.pixel/2, data.buttonColor)
    
def movePlayer(dx, dy, data):
    #move bit by bit, not until it hits a wall
    data.sX += dx*data.pixel
    data.sY -= dy*data.pixel

### Mode Dispatcher
def mousePressed(event,data):
    if data.mode == "menu":     menuMousePressed(event, data)
    elif data.mode == "start":  startMousePressed(event, data)
    elif data.mode == "pause":  pauseMousePressed(event, data)
    elif data.mode == "game":   gameMousePressed(event, data)
    
def keyPressed(event, data):
    if data.mode == "start":    startKeyPressed(event,data)
    elif data.mode == "game":   gameKeyPressed(event,data)
    elif data.mode == "pause":  pauseKeyPressed(event,data)
    elif data.mode == "menu":   menuKeyPressed(event,data)
    
def timerFired(data):
    if data.mode == "game":     gameTimerFired(data)
    elif data.mode == "menu":   menuTimerFired(data)
    elif data.mode == "pause":  pauseTimerFired(data)
    elif data.mode == "start":  startTimerFired(data)
    
def redrawAll(canvas, data):
    if data.mode == "game":     gameRedrawAll(canvas, data)
    elif data.mode == "start":  startRedrawAll(canvas, data)
    elif data.mode == "menu":   menuRedrawAll(canvas, data)
    elif data.mode == "pause":  pauseRedrawAll(canvas, data)
    
    
    
### Start Mode
def startMousePressed(event, data):
    if data.playButton.left>event.x>data.playButton.right and\
     data.playButton.bottom>event.y>data.playButton.top:
        data.playButton.color = data.clickColor
        data.mode = "game"
        data.playButton.color = data.buttonColor
    elif data.menuButton.left>event.x>data.menuButton.right and\
     data.menuButton.bottom>event.y>data.menuButton.top:
        data.mode = "menu"

def startKeyPressed(event, data):
    pass
    
def startTimerFired(data):
    pass
    
def drawPlayButton(playButton, canvas, data):
    size = 30
    canvas.create_rectangle(playButton.left, playButton.top, playButton.right,\
                            playButton.bottom, fill=data.playButton.color)

def drawMenuButton(menuButton, canvas, data):
    size = 30
    canvas.create_rectangle(menuButton.left, menuButton.top, menuButton.right,\
                            menuButton.bottom, fill=data.menuButton.color)
    
def startRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text="Tomb of Tut")
    drawPlayButton(data.playButton, canvas, data)
    drawMenuButton(data.menuButton, canvas, data)


### Game Mode
def gameMousePressed(event, data):
    pass

def gameKeyPressed(event, data):
    if event.keysym == "Up":
        moveWalls(data, 0, -1)
        data.directionX = 0
        data.directionY = -1
        movePlayer(0, -1, data)
        
    if event.keysym == "Down":
        moveWalls(data, 0, 1)
        data.directionX = 0
        data.directionY = 1
        movePlayer(0, 1, data)
        
    if event.keysym == "Left":
        moveWalls(data, -1, 0)
        data.directionX = -1
        data.directionY = 0
        movePlayer(-1, 0, data)   
             
    if event.keysym == "Right":
        moveWalls(data, 1, 0)
        data.directionX = 1
        data.directionY = 0
        movePlayer(1, 0, data)
        
def gameTimerFired(data):
    pass
    
def drawPauseButton(pauseButton, canvas, data):
    canvas.create_rectangle(pauseButton.left, pauseButton.top, \
                            pauseButton.right, pauseButton.bottom,\
                            fill=data.pauseButton.color)

def gameRedrawAll(canvas, data):
    drawWalls(canvas, data)
    drawPlayer(canvas, data)
    drawPauseButton(data.pauseButton, canvas, data)
    
### Pause Mode
def pauseMousePressed(event, data):
    pass

def pauseKeyPressed(event, data):
    pass
    
def pauseTimerFired(data):
    pass
    
def pauseRedrawAll(canvas, data):
    pass

### Menu Mode
def menuMousePressed(event, data):
    pass

def menuKeyPressed(event, data):
    pass
    
def menuTimerFired(data):
    pass

def menuRedrawAll(canvas, data):
    pass

### Mode-blind functions

def hitsWall(data):
    for wallBlock in data.walls:
        #hit from the left (block is on the right of the player)
        if wallBlock.left < data.player.x + data.player.size < wallBlock.right\
        #hit from the right
        or wallBlock.left < data.player.x - data.player.size < wallBlock.right\
        #hit from below
        or wallBlock.top < data.player.y - data.player.size < wallBlock.bottom\
        #hit from above
        or wallBlock.top < data.player.y + data.player.size < wallBlock.bottom:
            return True
    return False
    
def createWalls(data):
    #todo: define a level chooser, like a mode dispatcher?
    for block in data.lvl: 
        data.walls.append(Wall(lvl[block[0]],data.lvl[block[1]]))
        
def drawWalls(canvas,data):
    for wallBlock in data.walls:
        canvas.create_rectangle(data.pixel*(data.sX + wallBlock.left),\
        data.pixel*(data.sY + wallBlock.top),\
        data.pixel*(data.sX + wallBlock.right), \
        data.pixel*(data.sY + wallBlock.bottom), fill ="green")

def moveWalls(data, dx, dy):
    for wallBlock in data.walls:
        time.sleep(0.1) #the delayed motion
        wallBlock.moveWall(dx, dy)
    
def drawPlayer(canvas, data):
    #placeholder for now
    #TODO: define images, or shapes for the player and replace the rect
    canvas.create_rectangle(data.player.x - data.pixel/2,\
            data.player.y - data.pixel/2,\
            data.player.x + data.pixel/2,\
            data.player.y + data.pixel/2)


### Run Function

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)
