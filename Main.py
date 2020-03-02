import tkinter
import random

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

    # draw a nought
    if type == "Noughts":
        c.create_oval(x - lineLength / 2, y - lineLength / 2, x + lineLength / 2, y + lineLength / 2, width=2)
    # draw a cross
    else:
        c.create_line(x-lineLength/2, y-lineLength/2, x+lineLength/2, y+lineLength/2, width=2)
        c.create_line(x-lineLength/2, y+lineLength/2, x+lineLength/2, y-lineLength/2, width=2)

    if type == playerSide:
        grid[location[1]][location[0]] = playerSide
    else:
        grid[location[1]][location[0]] = computerSide

    print(grid)
    toggleGo()

def drawWinLine(startpoint, endpoint):
    # get canvas dimensions
    c.update()
    canvasWidth = c.winfo_width()
    canvasHeight = c.winfo_height()

    startpoint[0] = canvasWidth * ((startpoint[0] + (startpoint[0] + 1)) / 6)
    startpoint[1] = canvasHeight * ((startpoint[1] + (startpoint[1] + 1)) / 6)
    endpoint[0] = canvasWidth * ((endpoint[0] + (endpoint[0] + 1)) / 6)
    endpoint[1] = canvasHeight * ((endpoint[1] + (endpoint[1] + 1)) / 6)

    c.create_line(startpoint[1], startpoint[0], endpoint[1], endpoint[0], width=2)

def beginGame(side):
    # create canvas
    global c
    global canvasActive
    c = tkinter.Canvas(m, width=200, height=200)
    c.pack()
    canvasActive = True
    # clear window
    removeChooseSide()
    # draw game grid
    drawGrid(c)
    setSides(side)

def setSides(side):
    global playerSide
    global computerSide
    if side == "Noughts":
        playerSide = "Noughts"
        computerSide = "Crosses"
    else:
        playerSide = "Crosses"
        computerSide = "Noughts"

def displayChooseSide():
    # make buttons global so they can be removed by other functions
    global w
    global w2
    global l
    # define label
    l = tkinter.Label(m, text='Pick a side:')
    l.pack()
    # define buttons
    w = tkinter.Button(m, text='Noughts', width=25, command=lambda: beginGame("Noughts"))
    w.pack()
    w2 = tkinter.Button(m, text='Crosses', width=25, command=lambda: beginGame("Crosses"))
    w2.pack()

def removeChooseSide():
    # get rid of buttons etc
    l.destroy()
    w.destroy()
    w2.destroy()

def handleMouseClick(eventorigin):
    global turn
    if turn == "Player":
        # do i need global?
        global x, y
        # record mouse click coordinates
        x = eventorigin.x
        y = eventorigin.y

        if canvasActive == True:
            # get canvas dimensions
            c.update()
            canvasWidth = c.winfo_width()
            canvasHeight = c.winfo_height()

            # find which segment the click lays within. (for x and y)
            if x < canvasWidth*(1/3):
                x = 0
            elif x > canvasWidth*(1/3) and x < canvasWidth*(2/3):
                x = 1
            else:
                x = 2

            if y < canvasHeight*(1/3):
                y = 0
            elif y > canvasHeight*(1/3) and y < canvasHeight*(2/3):
                y = 1
            else:
                y = 2

            if (canGo((x,y))):
                # draw go within the segment that the mouse clicked, as well as using the player-selected side.
                drawGo((x, y), playerSide)

def canGo(location):
    if grid[location[1]][location[0]] == "Empty":
        return True
    else:
        return False

def toggleGo():
    global turn
    if not gridFull() and not winChecker():
        if turn == "Player":
            turn = "Computer"
            computerGo()
        else:
            turn = "Player"
    else:
        print("Game won")
        turn = "None"

def computerGo():
    while turn == "Computer":
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if (canGo((x, y))):
            drawGo((x, y), computerSide)
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
    return True

def initialise():
    global m
    m = tkinter.Tk()
    m.title("Tic Tac Toe")
    m.resizable(False, False)
    global canvasActive
    canvasActive = False
    m.bind("<Button 1>", handleMouseClick)

    displayChooseSide()

    global turn
    turn = "Player"

    m.mainloop()



initialise()