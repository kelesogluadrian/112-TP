from tkinter import *
import time
import random
import math
import pygame

# inspiration from huahanq
pygame.mixer.music.load()
pygame.mixer.music.play(-1,0.0)

### Levels

#levels are 2D lists that have topLeft and bottomRight of the blocks
level1 = [[(9,46),(16,47)],[(16,45),(19,46)],[(19,44),(20,45)],
            [(17,43),(18,44)],
            [(15,42),(16,46)],[(9,41),(10,46)],[(11,42),(15,43)],
            [(11,41),(14,42)],[(6,40),(10,41)],[(6,41),(7,42)],
            [(3,42),(6,43)],[(2,38),(3,42)],[(4,39),(5,40)],
            [(3,37),(5,38)],[(4,34),(5,37)],[(1,33),(5,34)],[(0,26),(1,33)],
            [(1,27),(2,28)],[(1,25),(8,26)],[(2,30),(4,32)],[(4,30),(6,31)],
            [(6,27),(7,38)],[(7,38),(14,39)],[(13,39),(14,40)],
            [(14,41),(15,42)],[(15,38),(16,40)],[(16,40),(18,41)],
            [(18,40),(19,43)],[(20,39),(21,44)],[(18,38),(21,39)],
            [(17,36),(18,39)],[(13,35),(17,37)],[(11,35),(12,38)],
            [(8,35),(11,36)],[(8,28),(9,35)],[(7,22),(8,26)],[(7,27),(11,28)],
            [(8,28),(10,29)],[(12,27),(13,34)],[(11,29),(14,30)],
            [(14,34),(19,35)],[(19,30),(20,35)],[(19,30),(23,31)],
            [(22,27),(23,31)],[(22,27),(25,28)],[(25,26),(27,27)],
            [(26,22),(27,27)],[(22,22),(26,23)],[(23,25),(24,26)],
            [(20,22),(22,25)],[(18,28),(21,29)],[(19,26),(21,29)],
            [(17,26),(18,27)],[(9,24),(12,26)],[(9,17),(12,18)],
            [(15,28),(17,29)],[(16,29),(17,30)],[(16,30),(18,33)],
            [(12,25),(15,26)],[(14,26),(15,28)],[(8,22),(11,23)],
            [(18,23),(19,25)],[(12,22),(15,23)],[(13,21),(15,24)],
            [(16,23),(17,25)],[(15,23),(16,24)],[(16,20),(17,22)],
            [(17,21),(21,22)],[(14,12),(16,20)],[(11,19),(21,20)],
            [(11,20),(12,21)],[(9,19),(10,22)],[(16,17),(17,20)],
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
                
stars = [(1.5,26.5),(3.5,6.5),(10.5,31.5),(25.5,23.5),(8.5,16.5),(12.5,16.5)]

endpoint = [(13,1),(14,2)]



### Classes
class Wall(object):
    def __init__(self, topLeft, bottomRight):
        #topLeft and bottomRight are tuples (x,y)
        self.top = topLeft[1]
        self.left = topLeft[0]
        self.bottom = bottomRight[1]
        self.right = bottomRight[0]
            
    def moveWall(self, dx, dy):
        self.left += dx
        self.right += dx
        self.top -= dy
        self.bottom -= dy
    
    def __repr__(self):
        return ("Wall: " + str(self.top))

class Cannon(Wall):
    def __init__(self, topLeft, bottomRight, direction):
        super().__init__(topLeft, bottomRight)
        self.direction = direction
        self.cx = (self.left + self.right)/2
        self.cy = (self.top + self.bottom)/2
        
    def makeBullet(self):
        # Generates a bullet heading in the direction the cannon is facing
        offset = 21 #data.pixel/2 + 1 (plus something)
        x = self.cx + offset*self.direction[0]
        y = self.cy - offset*self.direction[1]
        
        return Bullet(x, y, self.direction) 
        
    def __repr__(self):
        return("Cannon: "+str(self.top))
        
class Bullet(object):
    #some of the code for the bullet class is taken from hw11
    # Model
    def __init__(self, cx, cy, direction):
        # A bullet has a position, a size, a direction
        self.cx = cx
        self.cy = cy
        self.r = 3
        self.direction = direction
        self.speed = 0.5
    
    # View
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill="white", outline=None)

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += self.direction[0]*self.speed
        self.cy += self.direction[1]*self.speed

    def collidesWithWall(self, other):
        # Check if the bullet and wall overlap at all
        if not isinstance(other, Wall): 
        # Other must be a Wall, not a Cannon
            return False
        else:
            return abs(other.left-self.cx) < self.r or\
             abs(other.right-self.cx) < self.r or\
              abs(other.top-self.cy) < self.r or \
              abs(other.bottom-self.cy) < self.r
            

    def collidesWithPlayer(self, other, data):
        # Check if the bullet and player overlap at all
        if(not isinstance(other, Player)): # Other must be a Player
            return False
        else:
            dist = ((((other.x-data.sX)/data.pixel - self.cx)**2 + ((other.y-data.sY)/data.pixel - self.cy)**2)**0.5)*data.pixel
            return dist < self.r + other.r

class Player(object):
    def __init__(self, x, y, size):
        # self.avatar = avatar
        self.speed = 40
        self.r = size
        self.x = x
        self.y = y

def getPlayerLocation(data, player):
    x = (player.x-data.sX)/data.pixel
    y = (player.y-data.sY)/data.pixel
    return (x,y)
        
class Enemy(Player):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
    #A* search algorithm with Manhattan heuristics
    #inspiration:https://www.geeksforgeeks.org/a-search-algorithm/
    def findPath(self, data, x=None, y=None, moves=None, visited=None):
        if visited == None:
            visited = []
        if moves == None:
            moves = []
        if x == None:
            x = self.x
        if y == None:
            y = self.y
        #this will return a list of moves needed to get to the player
        #backtracking template taken from 112 website        
        nextCells = [(x+0,y+1),(x+0,y-1),(x+1,y+0),(x-1,y+0)]      
        
        if getPlayerLocation(data, data.player)==(x,y) or (len(moves)>0 and\
                            moves[-1] == getPlayerLocation(data, data.player)):
            return moves
            
        lengths={}
        for cell in nextCells:
            if isValid(cell, data) and cell not in visited:
                dist = findDistToPlayer(cell, data)
                if dist not in lengths.keys():
                    lengths[dist] = [cell]
                else:
                    lengths[dist].append(cell)
        # print(lengths)
        
        # print(getPlayerLocation(data, data.player))
        print(moves)
        for cell in nextCells:
            nextMove = lengths[min(lengths.keys())][0]
            
            moves.append(nextMove)
            visited.append((x,y))
                
                # visited.append(nextMove)
            tmpSolution = self.findPath(data, nextMove[0], nextMove[1], moves, visited)
            if tmpSolution != None:
                return tmpSolution
            moves.remove(nextMove)
            lengths[min(lengths.keys())].pop(0)
            if lengths[min(lengths.keys())]==[]:
                del lengths[min(lengths.keys())]
            visited.remove((x,y))
        return None

    def draw(self, canvas, data):
        canvas.create_rectangle(data.pixel*self.x-self.r+data.sX, data.pixel*self.y-self.r+data.sY, data.pixel*self.x+self.r+data.sX, data.pixel*self.y+self.r+data.sY, fill="blue")
                
                
def isValid(cell, data):
    for wallBlock in data.walls:
        if (wallBlock.left < cell[0] < wallBlock.right and wallBlock.top < cell[1] < wallBlock.bottom):
            return False
    return True

def findDistToPlayer(cell, data):
    x = abs(cell[0]-((data.player.x-data.sX)/data.pixel))
    y = abs(cell[1]-((data.player.y-data.sY)/data.pixel))
    return x+y
        

class Button(object):
    def __init__(self, name, cx, cy, color):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.name = name
        self.top = self.cy-10
        self.left = self.cx-30
        self.bottom = self.cy+10
        self.right = self.cx+30
    
    def draw(self, canvas, data):
        canvas.create_rectangle(self.left, self.top,\
                        self.right,self.bottom,\
                        fill=self.color)
        canvas.create_text((self.left+self.right)/2,\
                    (self.top+self.bottom)/2,text=self.name, fill="white")

class PauseButton(Button):
    def __init__(self, cx, cy, color):
        self.size = 20
        self.top = cy-self.size
        self.left = cx-self.size
        self.bottom = cy+self.size
        self.right = cx+self.size
        self.color = color


### Graphics
#the animation framework is taken from 15-112 website
def init(data):
    data.timerCount = 0
    data.dx = 0
    data.dy = 0
    data.prevdx = 0
    data.prevdy = 0
    data.lvl = level1
    data.can = level1Cannons
    data.stars = stars
    data.endpoint = Wall(endpoint[0], endpoint[1])
    data.path = None
    data.walls = []
    data.bullets = []
    data.cannons = []
    data.speed = 10
    data.mode = "start"
    data.collected = 0
    data.pixel = 40 #the unit length in the game
    data.margin = 10 # margin for the pause button
    # and scrollY
    data.sX = -200
    data.sY = -1520
    #center coordinates for the player
    data.cX = data.width/2
    data.cY = data.height//2
    data.buttonColor = "blue"
    data.clickColor = "red"
    data.player = Player(data.cX, data.cY, data.pixel/2.5)
    data.enemy = None 
    data.playButton = Button("PLAY", data.width/2, 3*data.height//5,\
                            data.buttonColor)
    data.menuButton = Button("MENU", data.width//2, 4*data.height//5,\
                            data.buttonColor)
    data.pauseButton = PauseButton(data.width-data.margin-(data.pixel/2),\
                                data.margin+data.pixel/2, data.buttonColor)
    data.resumeButton = Button("RESUME",data.width/2, 3*data.height/5,\
                                data.buttonColor)
    data.quitButton = Button("QUIT", data.width/2, 4*data.height/5,\
                                data.buttonColor)
    data.mainMenuButton = Button("PLAY AGAIN", data.width/2, 4*data.height/6,\
                            data.buttonColor)
    data.responses = ["Better luck next time!", "Every step you take.",\
                "Not so smart, huh?", "There's no shame in losing."]
    data.response = random.choice(data.responses)
    createWalls(data)
    createCannons(data)

def movePlayer(dx, dy, data):
    #move until it hits a wall
    
    data.sX += dx*data.speed
    data.sY -= dy*data.speed
    
    if hitsWall(data):
        data.prevdx = dx
        data.prevdy = dy
        data.dx = 0
        data.dy = 0
        undo(dx, dy, data)
        if data.enemy != None:
            data.path = data.enemy.findPath(data)
        
def undo(dx, dy, data):
    data.sX -= dx*data.speed
    data.sY += dy*data.speed
        

### Mode Dispatcher
def mousePressed(event,data):
    if data.mode == "menu":     menuMousePressed(event, data)
    elif data.mode == "start":  startMousePressed(event, data)
    elif data.mode == "pause":  pauseMousePressed(event, data)
    elif data.mode == "game":   gameMousePressed(event, data)
    elif data.mode == "gameOver":gameOverMousePressed(event, data)
    
def keyPressed(event, data):
    if data.mode == "start":    startKeyPressed(event,data)
    elif data.mode == "game":   gameKeyPressed(event,data)
    elif data.mode == "pause":  pauseKeyPressed(event,data)
    elif data.mode == "menu":   menuKeyPressed(event,data)
    elif data.mode == "gameOver":gameOverKeyPressed(event,data)

def timerFired(data):
    if data.mode == "game":     gameTimerFired(data)
    elif data.mode == "menu":   menuTimerFired(data)
    elif data.mode == "pause":  pauseTimerFired(data)
    elif data.mode == "start":  startTimerFired(data)
    elif data.mode == "gameOver":gameOverTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "game":     gameRedrawAll(canvas, data)
    elif data.mode == "start":  startRedrawAll(canvas, data)
    elif data.mode == "menu":   menuRedrawAll(canvas, data)
    elif data.mode == "pause":  pauseRedrawAll(canvas, data)
    elif data.mode == "gameOver":gameOverRedrawAll(canvas, data)
    
    
    
### Start Mode
"""title, menu, play """
def startMousePressed(event, data):
    if data.playButton.left<event.x<data.playButton.right and\
     data.playButton.bottom>event.y>data.playButton.top:
        data.playButton.color = data.clickColor
        data.mode = "game"
        pygame.mixer.music.rewind()
        
        data.playButton.color = data.buttonColor
    elif data.menuButton.left<event.x<data.menuButton.right and\
     data.menuButton.bottom>event.y>data.menuButton.top:
        data.mode = "menu"

def startKeyPressed(event, data):
    pass
    
def startTimerFired(data):
    pass
    
    
def startRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text="Tomb of Tut", font="Arial 72 bold")
    data.playButton.draw(canvas, data)
    data.menuButton.draw(canvas, data)


### Game Mode #############
"""also there should be powerups along the way"""
def gameMousePressed(event, data):
    if data.pauseButton.left<event.x<data.pauseButton.right and\
     data.pauseButton.bottom>event.y>data.pauseButton.top:
        data.pauseButton.color = data.clickColor
        data.mode = "pause"
        data.pauseButton.color = data.buttonColor

def gameKeyPressed(event, data):
    if event.keysym == "Up" and data.dx==0 and data.dy==0 and\
                        not(data.prevdx==0 and data.prevdy==-1) :
        data.dx = 0
        data.dy = -1
        
        
    if event.keysym == "Down" and data.dx==0 and data.dy==0 and\
                        not(data.prevdx==0 and data.prevdy==1) :
        data.dx = 0
        data.dy = 1
        
    if event.keysym == "Left" and data.dx==0 and data.dy==0 and\
                        not(data.prevdx==1 and data.prevdy==0) :
        data.dx = 1
        data.dy = 0 
        
    if event.keysym == "Right" and data.dx==0 and data.dy==0 and\
                        not(data.prevdx==-1 and data.prevdy==0) :
        data.dx = -1
        data.dy = 0
        
    if event.keysym == "p":
        data.mode = "pause"
    print("--------")
        
def gameTimerFired(data):
    data.timerCount += 1
    movePlayer(data.dx, data.dy, data)
    if data.timerCount % 25 == 0:
    #from hw11
        for cannon in data.cannons:
            data.bullets.append(createBullet(cannon, data))
    #from hw11
    if data.bullets != []:
        for bullet in data.bullets:
            if data.timerCount % 2 == 0: 
                bullet.moveBullet()
            #if data.timerCount % 5 == 0:
            if bulletHitsWall(bullet, data):
                # no need to keep track of off-screen bullets
                data.bullets.remove(bullet)
            if bullet.collidesWithPlayer(data.player, data):
                data.bullets.remove(bullet)
                print(bullet.cx, bullet.cy)
                print((data.player.x-data.sX)/data.pixel, (data.player.y-data.sY)/data.pixel)
                data.mode = "gameOver"
                
                
    if data.timerCount % 70 == 0 and data.enemy == None:
        data.enemy = Enemy(12.5, 45.5, data.pixel/2.5)
        
        """"[(9,46),(16,47)]--> the wall above which the player starts
        9+16/2 = 12.5 = cx
        45.5 = cy
        """
    if data.timerCount % 30 == 0:
        if data.enemy != None:
            if data.path != None:
                if data.path == []:
                    data.mode = "gameOver"
                else:
                    data.enemy.x = data.path[0][0]
                    data.enemy.y = data.path[0][1]
                    data.path.pop(0)  
         
    pX = (data.player.x-data.sX)/data.pixel
    pY = (data.player.y-data.sY)/data.pixel  
    for star in data.stars:
        if star[0]==pX and star[1]==pY:
            data.stars.remove(star)
            data.collected += 1
    e = data.endpoint
    if e.left<pX<e.right and e.top<pY<e.bottom:
        data.mode = "Win"
                

    
def createBullet(cannon, data):
        offset = 21/data.pixel #data.pixel/2 + 1 (plus something)
        x = cannon.cx + offset*cannon.direction[0]
        y = cannon.cy + offset*cannon.direction[1]
        
        return Bullet(x, y, cannon.direction) 

def drawBullets(canvas, data):
    for bullet in data.bullets:
        canvas.create_oval(data.sX + data.pixel*bullet.cx - bullet.r,\
                        data.sY + data.pixel*bullet.cy - bullet.r,\
                        data.sX + data.pixel*bullet.cx + bullet.r,\
                        data.sY + data.pixel*bullet.cy + bullet.r,
                           fill="white", outline=None)

def drawPauseButton(pauseButton, canvas, data):
    canvas.create_rectangle(pauseButton.left, pauseButton.top, \
                            pauseButton.right, pauseButton.bottom,\
                            fill=data.pauseButton.color)
    canvas.create_rectangle(pauseButton.left+5, pauseButton.top+2, \
                            pauseButton.right-25, pauseButton.bottom-2,\
                            fill="yellow")
    canvas.create_rectangle(pauseButton.left+25, pauseButton.top+2, \
                           pauseButton.right-5, pauseButton.bottom-2,\
                           fill="yellow")

def createCannons(data):
    for cannon in data.can:
        data.cannons.append(Cannon(cannon[0],cannon[1],cannon[2]))

def drawCannons(canvas, data):
    for cannon in data.cannons:
        canvas.create_rectangle(data.sX+cannon.left*data.pixel, data.sY+cannon.top*data.pixel, data.sX+cannon.right*data.pixel, data.sY+cannon.bottom*data.pixel, fill="green")
    for cannon in data.cannons:
        offset=20
        centerx = (data.sX+cannon.left*data.pixel+data.sX+cannon.right*data.pixel)/2
        centery = (data.sY+cannon.top*data.pixel+data.sY+cannon.bottom*data.pixel)/2
        canvas.create_line(centerx,centery,centerx+cannon.direction[0]*offset,\
                centery+cannon.direction[1]*offset, width=5, fill="black")
        canvas.create_rectangle(centerx-2,centery-2,centerx+2,centery+2, fill="black")
        

def createWalls(data):
    #todo: define a level chooser, like a mode dispatcher?
    for block in data.lvl:
        a = Wall(block[0],block[1])
        data.walls.append(a)

def drawWalls(canvas,data):
    for wallBlock in data.walls:
        canvas.create_rectangle(data.sX + data.pixel*(wallBlock.left),\
                        data.sY + data.pixel*(wallBlock.top),\
                        data.sX + data.pixel*(wallBlock.right), \
                        data.sY + data.pixel*(wallBlock.bottom), fill ="black")


def drawPlayer(canvas, data):
    #placeholder for now
    #TODO: define images, or shapes for the player and replace the rect
    canvas.create_rectangle(data.player.x - data.player.r,\
                            data.player.y - data.player.r,\
                            data.player.x + data.player.r,\
                            data.player.y + data.player.r, fill="red")

def drawCollected(canvas, data):
    x1=data.margin
    y1=data.height-40
    x2=140
    y2=data.height-data.margin
    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
    canvas.create_text((x1+x2)/2, (y1+y2)/2, text="Stars: "+str(data.collected))
    
def drawEndpoint(canvas, data):
    e = data.endpoint
    canvas.create_rectangle(e.left, e.top, e.right, e.bottom, fill="gold")
    
def gameRedrawAll(canvas, data):
    drawWalls(canvas, data)
    drawCannons(canvas, data)
    drawStars(canvas, data)
    drawPlayer(canvas, data)
    drawPauseButton(data.pauseButton, canvas, data)
    drawBullets(canvas, data)
    drawEndpoint(canvas, data)
    if data.enemy != None:
        data.enemy.draw(canvas, data)
    drawCollected(canvas, data)
    canvas.create_text(data.width/2, data.height-10, text=str(data.timerCount))

    
    
    
### Pause Mode
def pauseMousePressed(event, data):
    if data.resumeButton.left<event.x<data.resumeButton.right and\
     data.resumeButton.bottom>event.y>data.resumeButton.top:
         data.mode = "game"
         
    if data.quitButton.left<event.x<data.quitButton.right and\
     data.quitButton.bottom>event.y>data.quitButton.top:
         init(data)
    pass

def pauseKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "game"
    
def pauseTimerFired(data):
    pass
    
def pauseRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height,fill="light grey")
    canvas.create_text(data.width/2, data.height/3, text="GAME PAUSED")
    canvas.create_text(data.width/2, data.height/2, text="Press 'p' to resume")
    data.resumeButton.draw(canvas, data)
    data.quitButton.draw(canvas, data)
    

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

### Game Over Mode

            
def gameOverMousePressed(event, data):
    if data.mainMenuButton.left<event.x<data.mainMenuButton.right and\
     data.mainMenuButton.bottom>event.y>data.mainMenuButton.top:
        init(data)
        
def gameOverKeyPressed(event,data):
    return

def gameOverTimerFired(data):
    return
            
def gameOverRedrawAll(canvas, data):
    drawWalls(canvas, data)
    drawCannons(canvas, data)
    drawPlayer(canvas, data)
    drawPauseButton(data.pauseButton, canvas, data)
    drawBullets(canvas, data)
    if data.enemy != None:
        data.enemy.draw(canvas, data)
    width = data.width/3
    height = data.height/3
    canvas.create_rectangle(data.width/2-width, data.height/2-height, data.width/2+width, data.height/2+height, fill="blue")
    
    canvas.create_text(data.width/2, data.height/2-data.height/8, text=data.response, fill="white")
    data.mainMenuButton.draw(canvas, data)
    
    

### Mode-blind functions

    
def hitsWall(data):
    for wallBlock in data.walls:
        #hit from the left,right,below,above respectively
        #right-->(block is on the right of the player)
        if (data.pixel*wallBlock.left + data.sX <= data.player.x-data.player.r <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.player.y <= data.pixel*wallBlock.bottom + data.sY) or\
         (data.pixel*wallBlock.left + data.sX <= data.player.x+data.player.r <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.player.y <= data.pixel*wallBlock.bottom + data.sY) or\
         (data.pixel*wallBlock.left + data.sX <= data.player.x <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.player.y-data.player.r <= data.pixel*wallBlock.bottom + data.sY) or\
         (data.pixel*wallBlock.left + data.sX <= data.player.x <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.player.y+data.player.r <= data.pixel*wallBlock.bottom + data.sY):
            return True
    return False
    
def bulletHitsWall(bullet, data):
    for wallBlock in data.walls:
        if (data.pixel*wallBlock.left + data.sX <= data.sX + data.pixel*bullet.cx <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.sY + data.pixel*bullet.cy <= data.pixel*wallBlock.bottom + data.sY) or\
         (data.pixel*wallBlock.left + data.sX <= data.sX + data.pixel*bullet.cx <= data.pixel*wallBlock.right + data.sX and data.pixel*wallBlock.top + data.sY <= data.sY+ data.pixel*bullet.cy <= data.pixel*wallBlock.bottom + data.sY):
            return True
    return False

def drawStars(canvas, data):
    for star in data.stars:
        drawStar(star[0],star[1], canvas, data)

def drawStar(cX, cY, canvas, data, diameter=15, numPoints=5, color="gold"):
    radius = diameter/2
    centerX = data.pixel*cX + data.sX
    centerY = data.pixel*cY + data.sY
    #the inner circle
    canvas.create_oval(centerX-radius, centerY-radius, centerX+radius,\
                        centerY+radius, fill = color,width=0) 
    outerRadius = 2*(2**(1/2))*radius/(3**(1/2))+ radius 
    #the radius of the outer points
    dAngle = 2*math.pi/numPoints
    for i in range(numPoints):
        outerPointX = centerX+outerRadius*math.cos((math.pi/2)+i*dAngle) 
        outerPointY = centerY-outerRadius*math.sin((math.pi/2)+i*dAngle)
        
        #one to the left...
        innerPt1X = centerX+radius*math.cos((math.pi/2)+i*dAngle+dAngle/2) 
        innerPt1Y = centerY-radius*math.sin((math.pi/2)+i*dAngle+dAngle/2)
        #...and one to the right
        innerPt2X = centerX+radius*math.cos((math.pi/2)+i*dAngle-dAngle/2)
        innerPt2Y = centerY-radius*math.sin((math.pi/2)+i*dAngle-dAngle/2)
        
        canvas.create_polygon(outerPointX,outerPointY,innerPt1X,innerPt1Y,\
        innerPt2X,innerPt2Y, fill=color)
    
    
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
    data.timerDelay = 5 # milliseconds
    root = Tk()
    root.title("Tomb of Tut")
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
    # inspiration from huahanq
    try:
        pygame.mixer.music.stop()
    except:
        pass
    print("bye!")

run(600, 600)
