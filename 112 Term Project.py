### Levels

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
            [(17,26),(18,27)],[(9,24),(12,26)],[(9,17),(12,18)],
            [(15,28),(17,29)],[(16,29),(17,30)],[(16,30),(18,33)],
            [(12,25),(15,26)],[(14,26),(15,28)],[(8,22),(11,23)],
            [(18,23),(19,25)],[(12,22),(15,23)],[(13,21),(15,24)],
            [(16,23),(17,25)],[(15,23),(16,24)],[(16,20),(17,22)],
            [(17,21),(21,22)],[(14,12),(16,20)],[(11,19),(21,20)],
            [(12,21),(11,20)],[(9,19),(10,22)],[(16,17),(17,20)],
            [(6,19),(9,20)],[(6,13),(7,19)],[(7,13),(9,14)],
            [(10,14),(11,17)],[(12,12),(14,13)],[(20,8),(21,19)],
            [(19,12),(20,14)],[(18,15),(19,18)],[(17,11),(18,16)],
            [(14,10),(19,11)],[(12,8),(15,10)],[(6,10),(13,11)],
            [(8,11),(10,12)],[(8,12),(9,13)],[(16,8),(20,9)],
            [(16,6),(17,8)],[(11,6),(16,7)],
            [(8,6),(11,9)],[(6,5),(10,6)],[(6,7),(7,10)],
            [(1,7),(6,8)],[(4,5),(5,7)],[(1,1),(2,7)],
            [(2,1),(9,2)],[(8,2),(9,4)],[(9,3),(13,4)],
            [(3,3),(6,4)],[(6,3),(7,5)],[(12,1),(13,3)],
            [(12,0),(15,1)],[(14,1),(15,6)],[(11,4),(13,5)]]

level1Cannons = [ [(14,41),(15,42),(0,-1)],[(2,25),(3,26),(0,1)],
                [(8,30),(9,31),(1,0)],[(8,32),(9,33),(1,0)],
                [(16,30),(17,31),(-1,0)],[(16,32),(17,33),(-1,0)],
                [(17,26),(18,27),(0,-1)],[(23,25),(24,26),(1,0)],
                [(23,25),(24,26),(0,-1)],[(6,14),(7,15),(1,0)],
                [(6,16),(7,17),(1,0)],[(14,14),(15,15),(-1,0)],
                [(14,16),(15,17),(-1,0)],[(19,13),(20,14),(-1,0)],
                [(11,6),(12,7),(0,-1)],[(12,6),(13,7),(0,1)],
                [(14,6),(15,7),(0,1)],[(3,3),(4,4),(0,1)],
                [(13,9),(14,10),(0,1)]]
                
#todo: put coordinates for powerups




### Classes
class Wall(object):
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
    def __init__(self, topLeft, bottomRight, direction):
        super().__init__(topLeft, bottomRight)
        self.direction = direction
        
    def makeBullet(self):
        # Generates a bullet heading in the direction the cannon is facing
        offset = 21 #data.pixel/2 + 1 (plus something)
        x = self.cx + offset*self.direction[0]
        y = self.cy - offset*self.direction[1]
        
        return Bullet(x, y, self.direction) 
        
class Bullet(object):
    #some of the code for the bullet class is taken from hw11
    # Model
    def __init__(self, cx, cy, direction):
        # A bullet has a position, a size, a direction
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.direction = direction
        self.speed = speed
    
    # View
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill="white", outline=None)

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += self.direction[0]*self.speed
        self.cy -= self.direction[1]*self.speed

    def collidesWithWall(self, other):
        # Check if the bullet and wall overlap at all
        if(not isinstance(other, Wall)): # Other must be a Wall
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r

    def collidesWithPlayer(self, other):
        # Check if the bullet and player overlap at all
        if(not isinstance(other, Player)): # Other must be a Player
            return False
        else:
            dist = ((other.x - self.cx)**2 + (other.y - self.cy)**2)**0.5
            return dist < self.r + other.r

class Player(object):
    def __init__(self, x, y, size):
        # self.avatar = avatar
        self.speed = 40
        self.r = size
        self.x = x
        self.y = y
        
    
class Button(object):
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
    data.timerCount = 0
    data.walls = level1
    data.bullets = []
    data.cannons = level1Cannons
    data.mode = "start"
    data.pixel = 40 #the unit length in the game
    data.margin = 10 # margin for the pause button
    # and scrollY
    #todo: figure out correct sX and sY to start player in middle of screen
    #todo:                                      and at the bottom of the map
    data.sX = 0
    data.sY = 0
    #center coordinates for the player
    data.cX = data.width//data.pixel//2
    data.cY = data.height//data.pixel//2
    data.buttonColor = "green"
    data.clickColor = "red"
    data.player = Player(data.cX, data.cY, data.pixel/2)
    data.playButton = Button("PLAY", data.width/2, 3*data.height//5,\
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
"""title, menu, play """
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
"""also there should be powerups along the way"""
def gameMousePressed(event, data):
    if data.pauseButton.left>event.x>data.pauseButton.right and\
     data.pauseButton.bottom>event.y>data.pauseButton.top:
        data.pauseButton.color = data.clickColor
        data.mode = "pause"
        data.playButton.color = data.buttonColor

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
        
    if event.keysym == "p":
        data.mode = "pause"
    
        
def gameTimerFired(data):
    data.timerCount += 1
    
    if data.timerCount % 5 = 0:
    #from hw11
        for cannon in data.cannons:
            data.bullets.append(cannon.makeBullet())
    #from hw11
    for bullet in data.bullets:
        bullet.moveBullet()
        if bullet.isOffscreen(data.width, data.height):
            #no need to keep track of off-screen bullets
            data.bullets.remove(bullet)
        for wall in data.walls:
            if bullet.collidesWithWall(wall):
                data.bullets.remove(bullet)
    
def drawPauseButton(pauseButton, canvas, data):
    canvas.create_rectangle(pauseButton.left, pauseButton.top, \
                            pauseButton.right, pauseButton.bottom,\
                            fill=data.pauseButton.color)

def gameRedrawAll(canvas, data):
    drawWalls(canvas, data)
    drawCannons(canvas, data)
    drawPlayer(canvas, data)
    drawPauseButton(data.pauseButton, canvas, data)
    
### Pause Mode
"""menu, quit buttons, also when you press the pause button again(or press p)
you go back to playing

"""

def pauseMousePressed(event, data):
    pass

def pauseKeyPressed(event, data):
    pass
    
def pauseTimerFired(data):
    pass
    
def pauseRedrawAll(canvas, data):
    pass

### Menu Mode
"""different players to choose from, settings (and powerups) """
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
        #hit from the left,right,below,above respectively
        #right-->(block is on the right of the player)
        if wallBlock.left < data.player.x + data.player.size < wallBlock.right\
        or wallBlock.left < data.player.x - data.player.size < wallBlock.right\
        or wallBlock.top < data.player.y - data.player.size < wallBlock.bottom\
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
#from 112 website
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
