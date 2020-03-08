import tkinter
import time
import random
import math

class Computer:
    def __init__(self, side):
        # initialise the computer and ensure that it knows which side it is,
        # as well as its opponent's side.
        self.side = side
        if self.side == "Noughts":
            self.opponentSide = "Crosses"
        else:
            self.opponentSide = "Noughts"

    # pretty unnecessary functions, just tidier.
    def go(self, currentGrid):
        return self.findBestMove(currentGrid)

    def goRandom(self, currentGrid):
        return self.randomMove(currentGrid)

    def goTactical(self, currentGrid):
        return self.tacticalMove(currentGrid)


    def randomMove(self, currentGrid):
        # keep finding random locations and checking whether they are empty, as soon as one is found then return it.
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if (self.canGo(currentGrid, (x, y))):
                break
        return (x, y)

    def canGo(self, currentGrid, location):
        # check whether either player has made a move in this square.
        if currentGrid[location[1]][location[0]] == "Empty":
            return True
        else:
            return False

    def isGridFull(self, currentGrid):
        # iterate through each square in the grid.
        for x in range(3):
            for y in range(3):
                # if any square is empty then the grid cannot be full.
                if currentGrid[y][x] == "Empty":
                    return False
        # if no squares are empty then the grid must be full.
        return True

    def findBestMove(self, currentGrid):
        # begins the recursive process of the miniMax algorithm.
        # initialise the variables to a default/empty state.
        bestScore = -math.inf
        bestMove = ()
        # check each square in the grid.
        for x in range(3):
            for y in range(3):
                # if the square is empty, it is a potential location for a move.
                if currentGrid[y][x] == "Empty":
                    # therefore, this "move" is checked.
                    # temporarily make that move.
                    currentGrid[y][x] = self.side
                    # call the miniMax function to begin the tree traversal.
                    # set the first level of recursion to minimising (false),
                    # as this current step is doing the maximising.
                    # also sets alpha and beta to values that will be overwritten.
                    score = self.miniMax(currentGrid, -math.inf, +math.inf, False)
                    # then undo the "move".
                    currentGrid[y][x] = "Empty"
                    # this will ensure that the move with the highest score is used.
                    if score > bestScore:
                        bestScore = score
                        bestMove = (x,y)
        # return the best move so that it can be made.
        return bestMove

    # might look to reduce the bulk of this code by combining minimising/maximising
    # and just change the appropriate sections dynamically.
    def miniMax(self, currentGrid, alpha, beta, maximising):
        # the miniMax algorithm method.
        # called many times recursively.

        # check if the game is in a terminal state due to the move made.
        # has either player won as a result of the move?
        if self.winChecker(currentGrid) != 0:
            # the returned "score" is either +10 or -10.
            return self.winChecker(currentGrid)

        # is the grid full now?
        if (self.isGridFull(currentGrid)):
            return 0

        # simulating the move/choice of the maximising player.
        if (maximising):
            # initialise the best score to a value that will be overwritten.
            bestScore = -math.inf
            # check each square from this current state.
            for x in range(3):
                for y in range(3):
                    # if the square is empty, then it is a potential move.
                    # this will obviously decrease, the deeper this algorithm goes.
                    if currentGrid[y][x] == "Empty":
                        # temporarily make the move.
                        currentGrid[y][x] = self.side
                        # call the miniMax algorithm again, setting the maximising to false,
                        # to emulate the other player's move.
                        # also pass through the current alpha and beta values
                        # compare the result of this to the current best score and take the largest value.
                        bestScore = max(self.miniMax(currentGrid, alpha, beta, False), bestScore)
                        # undo the temporary move.
                        currentGrid[y][x] = "Empty"
                        # alpha-beta pruning.
                        alpha = max(alpha, bestScore)
                        # if branch is worse.
                        if alpha >= beta:
                            # "prunes" the branch of the tree with the worst option.
                            break
            # return the score up the tree.
            return bestScore
        else:
            # if "minimising".
            bestScore = math.inf
            # check each square.
            for x in range(3):
                for y in range(3):
                    # find the potential moves.
                    if currentGrid[y][x] == "Empty":
                        # test that move.
                        currentGrid[y][x] = self.opponentSide
                        # recursively call the miniMax algorithm, but set maximising to True
                        # so that it emulates the alternate player.
                        bestScore = min(self.miniMax(currentGrid, alpha, beta, True), bestScore)
                        # undo the temporary move.
                        currentGrid[y][x] = "Empty"
                        # alpha-beta pruning.
                        beta = min(beta, bestScore)
                        if alpha >= beta:
                            break
            # pass the value back up the tree
            return bestScore

    def tacticalMove(self, currentGrid):
        # based on how I would play...

        # check for any winning moves.
        for x in range(3):
            for y in range(3):
                if currentGrid[y][x] == "Empty":
                    currentGrid[y][x] = self.side
                    result = self.winChecker(currentGrid)
                    currentGrid[y][x] = "Empty"
                    if result == 10:
                        return (x,y)

        # check for any moves to block.
        for x in range(3):
            for y in range(3):
                if currentGrid[y][x] == "Empty":
                    currentGrid[y][x] = self.opponentSide
                    result = self.winChecker(currentGrid)
                    currentGrid[y][x] = "Empty"
                    if result == -10:
                        return (x,y)

        # try centre.
        if currentGrid[1][1] == "Empty":
            return (1,1)

        # try corners.
        corners = [[0,0], [0,2], [2,0], [2,2]]
        for corner in corners:
            if currentGrid[corner[1]][corner[0]] == "Empty":
                return corner

        # pick a remaining square.
        remaining = [[0,1],[1,0],[2,1],[1,2]]
        for square in remaining:
            if currentGrid[square[1]][square[0]] == "Empty":
                return square



    def winChecker(self, grid):
        # used to check for any "three-in-a-row" conditions.
        # potentially quite an inefficient method.
        # check three horizontals, then three verticals and then two diagonals.
        if grid[0][0] == self.side and grid[0][1] == self.side and grid[0][2] == self.side:
            return 10
        elif grid[0][0] == self.opponentSide and grid[0][1] == self.opponentSide and grid[0][2] == self.opponentSide:
            return -10

        elif grid[1][0] == self.side and grid[1][1] == self.side and grid[1][2] == self.side:
            return 10
        elif grid[1][0] == self.opponentSide and grid[1][1] == self.opponentSide and grid[1][2] == self.opponentSide:
            return -10

        elif grid[2][0] == self.side and grid[2][1] == self.side and grid[2][2] == self.side:
            return 10
        elif grid[2][0] == self.opponentSide and grid[2][1] == self.opponentSide and grid[2][2] == self.opponentSide:
            return -10

        elif grid[0][0] == self.side and grid[1][0] == self.side and grid[2][0] == self.side:
            return 10
        elif grid[0][0] == self.opponentSide and grid[1][0] == self.opponentSide and grid[2][0] == self.opponentSide:
            return -10

        elif grid[0][1] == self.side and grid[1][1] == self.side and grid[2][1] == self.side:
            return 10
        elif grid[0][1] == self.opponentSide and grid[1][1] == self.opponentSide and grid[2][1] == self.opponentSide:
            return -10

        elif grid[0][2] == self.side and grid[1][2] == self.side and grid[2][2] == self.side:
            return 10
        elif grid[0][2] == self.opponentSide and grid[1][2] == self.opponentSide and grid[2][2] == self.opponentSide:
            return -10

        elif grid[0][0] == self.side and grid[1][1] == self.side and grid[2][2] == self.side:
            return 10
        elif grid[0][0] == self.opponentSide and grid[1][1] == self.opponentSide and grid[2][2] == self.opponentSide:
            return -10

        elif grid[0][2] == self.side and grid[1][1] == self.side and grid[2][0] == self.side:
            return 10
        elif grid[0][2] == self.opponentSide and grid[1][1] == self.opponentSide and grid[2][0] == self.opponentSide:
            return -10
        return 0



# game
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
        Opponent = Computer(opponentSide)
    if type == "AvA":
        Opponent = Computer(playerSide)
        Opponent2 = Computer(opponentSide)

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
                time.sleep(1)
                computerGo()
        elif gameType == "AvA":
            c.update()
            if turn == "Player 1":
                time.sleep(1)
                computerGo()
            elif turn == "Player 2":
                time.sleep(1)
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
            #drawGo(Opponent.go(grid), opponentSide)
            drawGo(Opponent.goTactical(grid), opponentSide)
            toggleGo()
            break
    elif gameType == "AvA":
        if turn == "Player 1":
            while turn == "Player 1":
                if (gridEmpty()):
                    drawGo(Opponent.goRandom(grid), playerSide)
                else:
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

def gridEmpty():
    for x in range(3):
        for y in range(3):
            if grid[x][y] != "Empty":
                return False
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

