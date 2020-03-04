import tkinter
import time
import random

class Computer:
    def go(self, grid):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if (self.canGo(grid, (x, y))):
                break
        return (x, y)

    def canGo(self, grid, location):
        if grid[location[1]][location[0]] == "Empty":
            return True
        else:
            return False




def drawGrid(canvas):
    # get canvas dimensions
    canvas.update()
    canvasWidth = canvas.winfo_width()
    canvasHeight = canvas.winfo_height()

    # x and y coordinates at the start and end points of the line
    # draw horizontal lines
    canvas.create_line(0, canvasHeight*(1/3), canvasWidth, canvasHeight*(1/3),width=2)
    canvas.create_line(0, canvasHeight*(2/3), canvasWidth, canvasHeight*(2/3),width=2)
    # draw vertical lines
    canvas.create_line(canvasWidth*(1/3), 0, canvasWidth*(1/3),canvasHeight,width=2)
    canvas.create_line(canvasWidth*(2/3), 0, canvasWidth*(2/3), canvasHeight,width=2)

    global grid
    grid = [["Empty"] * 3 for x in range(3)]

def drawGo(location, type):
    # used to draw both Noughts and Crosses due to the create_oval method requiring a bounding box

    # get canvas dimensions
    c.update()
    canvasWidth = c.winfo_width()
    canvasHeight = c.winfo_height()

    # takes the x,y coordinates and gets the centre points
    x = canvasWidth * ((location[0] + (location[0] + 1)) / 6)
    y = canvasHeight * ((location[1] + (location[1] + 1)) / 6)

    # set length of each line in the cross/size of the diagonals using the segment size and a slight buffer
    buffer = 30
    lineLength = canvasWidth/3 - buffer
    colour = "purple"
    if type == playerSide:
        grid[location[1]][location[0]] = playerSide
        colour = "purple"
    else:
        grid[location[1]][location[0]] = opponentSide
        colour = "gold"

    # draw a nought
    if type == "Noughts":
        c.create_oval(x - lineLength / 2, y - lineLength / 2, x + lineLength / 2, y + lineLength / 2, width=2, outline=colour)
    # draw a cross
    else:
        c.create_line(x-lineLength/2, y-lineLength/2, x+lineLength/2, y+lineLength/2, width=2, fill=colour)
        c.create_line(x-lineLength/2, y+lineLength/2, x+lineLength/2, y-lineLength/2, width=2, fill=colour)


def drawWinLine(startpoint, endpoint):
    # get canvas dimensions
    c.update()
    canvasWidth = c.winfo_width()
    canvasHeight = c.winfo_height()

    global l
    global turn

    # choose colour before losing square information
    colour = "purple"
    if grid[startpoint[0]][startpoint[1]] == playerSide:
        colour = "purple"
        l.config(text="Player 1 Won")
        turn = "None"
    else:
        colour = "gold"
        l.config(text="Player 2 Won")
        turn = "None"

    # from square info, get the start and end points of the line
    startpoint[0] = canvasWidth * ((startpoint[0] + (startpoint[0] + 1)) / 6)
    startpoint[1] = canvasHeight * ((startpoint[1] + (startpoint[1] + 1)) / 6)
    endpoint[0] = canvasWidth * ((endpoint[0] + (endpoint[0] + 1)) / 6)
    endpoint[1] = canvasHeight * ((endpoint[1] + (endpoint[1] + 1)) / 6)

    # draw the line
    c.create_line(startpoint[1], startpoint[0], endpoint[1], endpoint[0], width=2, fill=colour)




def beginGame(side, type):
    # create canvas
    global c
    global canvasActive

    # clear window
    removeChooseSide()

    global l
    l = tkinter.Label(m, text="Player 1's turn")
    l.pack()

    c = tkinter.Canvas(m, width=200, height=200)
    c.pack()
    canvasActive = True

    # draw game grid
    drawGrid(c)
    setSides(side)
    global turn
    turn = "Player 1"

    global restartButton
    restartButton = tkinter.Button(m, text='Restart', width=25, command=lambda: resetHandler())
    restartButton.pack()

    global Opponent
    global Opponent2
    if type == "HvA":
        Opponent = Computer()
    if type == "AvA":
        Opponent = Computer()
        Opponent2 = Computer()

    checkTurn()

def setSides(side):
    global playerSide
    global opponentSide
    if side == "Noughts":
        playerSide = "Noughts"
        opponentSide = "Crosses"
    else:
        playerSide = "Crosses"
        opponentSide = "Noughts"

def displayChooseSide(type):
    # make buttons global so they can be removed by other functions
    global w
    global w2
    global l
    # define label
    l = tkinter.Label(m, text='Player 1, choose a side:')
    l.pack()
    # define buttons
    w = tkinter.Button(m, text='Noughts', width=25, command=lambda: beginGame("Noughts", type))
    w.pack()
    w2 = tkinter.Button(m, text='Crosses', width=25, command=lambda: beginGame("Crosses", type))
    w2.pack()

def removeChooseSide():
    # get rid of buttons etc
    l.destroy()
    w.destroy()
    w2.destroy()

def displayChooseOpponent():
    # make buttons global so they can be removed by other functions
    global w
    global w2
    global w3
    global l
    # define label
    l = tkinter.Label(m, text='Pick a game type:')
    l.pack()
    # define buttons
    w = tkinter.Button(m, text='Human vs Human', width=25, command=lambda: proceedToSideSelection("HvH"))
    w.pack()
    w2 = tkinter.Button(m, text='Human vs AI', width=25, command=lambda: proceedToSideSelection("HvA"))
    w2.pack()
    w3 = tkinter.Button(m, text='AI vs AI', width=25, command=lambda: proceedToSideSelection("AvA"))
    w3.pack()

def removeChooseOpponent():
    # get rid of buttons etc
    l.destroy()
    w.destroy()
    w2.destroy()
    w3.destroy()

def proceedToSideSelection(type):
    global gameType
    gameType = type
    removeChooseOpponent()
    if gameType == "AvA":
        beginGame("Noughts", type)
    else:
        displayChooseSide(gameType)

def handleMouseClick(eventorigin):
    global turn

    # do i need global?
    global x, y
    # record mouse click coordinates
    x = eventorigin.x
    y = eventorigin.y

    if canvasActive == True and eventorigin.widget == c:
        # get canvas dimensions
        c.update()
        canvasWidth = c.winfo_width()
        canvasHeight = c.winfo_height()

        # find which segment the click lays within. (for x and y)
        if x >= 0 and x < canvasWidth*(1/3):
            x = 0
        elif x >= canvasWidth*(1/3) and x <= canvasWidth*(2/3):
            x = 1
        elif x > canvasWidth*(2/3) and x <= canvasWidth:
            x = 2

        if y >= 0 and y < canvasHeight*(1/3):
            y = 0
        elif y >= canvasHeight*(1/3) and y <= canvasHeight*(2/3):
            y = 1
        elif y > canvasHeight*(2/3) and y <= canvasHeight:
            y = 2

        if (canGo((x,y))):
            # draw go within the segment that the mouse clicked, as well as using the player-selected side.
            if turn == "Player 1" and (gameType == "HvH" or gameType == "HvA"):
                drawGo((x, y), playerSide)
                toggleGo()
            elif turn == "Player 2" and gameType == "HvH":
                drawGo((x, y), opponentSide)
                toggleGo()

def canGo(location):
    if grid[location[1]][location[0]] == "Empty":
        return True
    else:
        return False

def toggleGo():
    global turn
    global l
    if not winChecker() and not gridFull():
        if turn == "Player 1":
            l.config(text="Player 2's turn")
            turn = "Player 2"
        else:
            l.config(text="Player 1's turn")
            turn = "Player 1"


def checkTurn():
    while not winChecker() and not gridFull():
        if gameType == "HvH":
            c.update()
        elif gameType == "HvA":
            c.update()
            if turn == "Player 2":
                time.sleep(1.5)
                computerGo()
        elif gameType == "AvA":
            c.update()
            if turn == "Player 1":
                time.sleep(1.5)
                computerGo()
            elif turn == "Player 2":
                time.sleep(1.5)
                computerGo()

def resetHandler():
    resetGame()

def restartHandler():
    restartButton.destroy()
    global playAgainButton
    playAgainButton = tkinter.Button(m, text='Play Again', width=25, command=lambda: resetHandler())
    playAgainButton.pack()

def computerGo():
    if gameType == "HvA":
        while turn == "Player 2":
            drawGo(Opponent.go(grid), opponentSide)
            toggleGo()
            break
    elif gameType == "AvA":
        if turn == "Player 1":
            while turn == "Player 1":
                drawGo(Opponent.go(grid), playerSide)
                toggleGo()
                break
        elif turn == "Player 2":
            while turn == "Player 2":
                drawGo(Opponent2.go(grid), opponentSide)
                toggleGo()
                break

def winChecker():
    # check three horizontals, then three verticals and then two diagonals
    if grid[0][0] == grid[0][1] and grid[0][1] == grid[0][2] and grid[0][0] != "Empty":
        drawWinLine([0,0], [0,2])
        return True
    elif grid[1][0] == grid[1][1] and grid[1][1] == grid[1][2] and grid[1][0] != "Empty":
        drawWinLine([1, 0], [1, 2])
        return True
    elif grid[2][0] == grid[2][1] and grid[2][1] == grid[2][2] and grid[2][0] != "Empty":
        drawWinLine([2, 0], [2, 2])
        return True
    elif grid[0][0] == grid[1][0] and grid[1][0] == grid[2][0] and grid[0][0] != "Empty":
        drawWinLine([0, 0], [2, 0])
        return True
    elif grid[0][1] == grid[1][1] and grid[1][1] == grid[2][1] and grid[0][1] != "Empty":
        drawWinLine([0, 1], [2, 1])
        return True
    elif grid[0][2] == grid[1][2] and grid[1][2] == grid[2][2] and grid[0][2] != "Empty":
        drawWinLine([0, 2], [2, 2])
        return True
    elif grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] and grid[0][0] != "Empty":
        drawWinLine([0, 0], [2, 2])
        return True
    elif grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[0][2] != "Empty":
        drawWinLine([0, 2], [2, 0])
        return True

    return False

def gridFull():
    for x in range(3):
        for y in range(3):
            if grid[x][y] == "Empty":
                return False
    global l
    l.config(text="Game Over")
    return True

def resetGame():
    c.destroy()
    l.destroy()
    restartButton.destroy()
    try:
        playAgainButton.destroy()
    except:
        pass
    beginGame(playerSide,gameType)

def initialise():
    global m
    m = tkinter.Tk()
    m.title("Tic Tac Toe")

    m.resizable(False, False)
    global canvasActive
    canvasActive = False
    m.bind("<Button 1>", handleMouseClick)

    global turn
    turn = "Player 1"

    #menu = tkinter.Menu(m)
    #m.config(menu=menu)
    ##filemenu = tkinter.Menu(menu)
    #menu.add_cascade(label="Game", menu=filemenu)
    #filemenu.add_command(label="Restart", command=lambda: resetHandler())
    #filemenu.add_command(label="Change Sides", command=lambda: resetHandler())
    #filemenu.add_command(label="Exit to menu", command=lambda: resetHandler())

    displayChooseOpponent()
    #displayChooseSide()

initialise()
m.mainloop()

# options:
# human vs human
# human vs computer
# computer vs computer

# need to structure code so that it can cope with these.
