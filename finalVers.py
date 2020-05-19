import pygame     #initialization                      
pygame.init()

#defining default fonts
font = pygame.font.SysFont('timesnewroman', 40)
titleFont = pygame.font.SysFont('timesnewroman', 60, bold = True)

#defining variables to be used during game
currentSelected = ()
validMoves = []
graveSelected = -1
switchOrient = True
turn = "white"
inPlay = True
currentScreen = 0


whiteCap = []
whitePCap = []
blackCap = []
blackPCap = []

#defining dictionary of moves used for castling
castlingMoves = {(1,0):((0,0),(2,0)), (5,0):((7,0),(4,0)), (1,7):((0,7),(2,7)), (5,7):((7,7),(4,7))}

#defining colors
pale = (243,223,184)
brown = (201,146,92)
yellow = (238, 244, 127)
darkYellow = (222,209,91)
white = (255,255,255)
black = (0,0,0)

#defining text and wrappers used for buttons and title in title/rules screen
titleText = titleFont.render('CHESS - PAWN PUSH', 3, black, (248, 236, 211))
textRect = titleText.get_rect()
textRect.center = (400,120)
buttonText = font.render('Play', 3, black, white)
buttonTextRect = buttonText.get_rect()
buttonTextWrapper = (325,175,150,50) 
buttonTextRect.center = (400, 200)
rulesText = font.render('Rules', 3, black, white)
rulesTextRect = rulesText.get_rect()
rulesTextWrapper = (325,250,150,50)
rulesTextRect.center = (400, 275)
backText = font.render('Back', 3, black, white)
backTextRect = backText.get_rect()
backTextRect.center = (55, 35)
backTextWrapper = (10,10,90,50)

#tuples for specific moves for knights and kings
knightMoves = ((2,1), (2,-1), (1,2), (1,-2), (-1,2), (-1, -2), (-2, 1), (-2, -1))
kingMoves = ((1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1))

#creating window
win = pygame.display.set_mode((800,480))
win.fill((248, 236, 211))
pygame.display.set_caption('Chess - Pawn Push')

#pawn class for objects used on board
class pawn:
    global validMoves
    global highlight
    moved = False #variable which checks if piece is moved (if it can move 2 spaces or not)
    def __init__(self, pos, color, moves): #initialization (define color, coordinates, image, valid moves)
        self.color = color
        self.pX = pos[0]
        self.pY = pos[1]
        self.moves = moves
        if color == 'black':
            self.image = 'bPawn.png'
        else:
            self.image = 'wPawn.png'
            
    def moveUpdate(self): #function for updating valid moves
        self.moves = []
        if self.color == "black":
            if self.pY != 7:
                if board[self.pX][self.pY+1] == 0:
                    self.moves.append((self.pX, self.pY+1))
                if not self.moved and board[self.pX][self.pY+2] == 0 and board[self.pX][self.pY+1] == 0:
                    self.moves.append((self.pX, self.pY+2))
                try:
                    if board[self.pX+1][self.pY+1] != 0:
                        if board[self.pX+1][self.pY+1].color != self.color:
                            self.moves.append((self.pX+1, self.pY+1))
                except:
                    pass
                try:
                    if board[self.pX-1][self.pY+1] != 0:
                        if board[self.pX-1][self.pY+1].color != self.color:
                            self.moves.append((self.pX-1, self.pY+1))
                except:
                    pass
        else:
            if self.pY != 0:
                if board[self.pX][self.pY-1] == 0:
                    self.moves.append((self.pX, self.pY-1))
                if not self.moved and board[self.pX][self.pY-2] == 0 and board[self.pX][self.pY-1] == 0:
                    self.moves.append((self.pX, self.pY-2))
                try:
                    if board[self.pX+1][self.pY-1] != 0:
                        if board[self.pX+1][self.pY-1].color != self.color:
                            self.moves.append((self.pX+1, self.pY-1))
                except:
                    pass
                try:
                    if board[self.pX-1][self.pY-1] != 0:
                        if board[self.pX-1][self.pY-1].color != self.color:
                            self.moves.append((self.pX-1, self.pY-1))
                except:
                    pass
#rook class
class rook:
    moved = False #variable stores if rook has moved (used for castling)
    def __init__(self, pos, color, moves):
        self.color = color
        self.pX = pos[0]
        self.pY = pos[1]
        self.moves = set(moves)
        if color == 'black':
            self.image = 'bRook.png'
        else:
            self.image = 'wRook.png'
    def moveUpdate(self):
        self.moves = set()
        for sq in range(self.pX-1, -1, -1):
            if board[sq][self.pY] == 0:
                self.moves.add((sq,self.pY))
            elif board[sq][self.pY].color == self.color:
                break
            else:
                self.moves.add((sq,self.pY))
                break
        for sq in range(self.pX+1, 8):
            if board[sq][self.pY] == 0:
                self.moves.add((sq,self.pY))
            elif board[sq][self.pY].color == self.color:
                break
            else:
                self.moves.add((sq,self.pY))
                break
        for sq in range(self.pY-1, -1, -1):
            if board[self.pX][sq] == 0:
                self.moves.add((self.pX,sq))
            elif board[self.pX][sq].color == self.color:
                break
            else:
                self.moves.add((self.pX,sq))
                break
        for sq in range(self.pY+1, 8):
            if board[self.pX][sq] == 0:
                self.moves.add((self.pX,sq))
            elif board[self.pX][sq].color == self.color:
                break
            else:
                self.moves.add((self.pX,sq))
                break
                        

class knight:
    def __init__(self, pos, color, moves):
        self.color = color
        self.pX = pos[0]
        self.pY = pos[1]
        self.moves = moves
        if color == 'black':
            self.image = 'bKnight.png'
        else:
            self.image = 'wKnight.png'
    def moveUpdate(self):
        global knightMoves
        self.moves = []
        for move in knightMoves:
            try:
                if board[self.pX + move[0]][self.pY + move[1]] == 0:
                    self.moves.append((self.pX + move[0], self.pY + move[1]))
                elif board[self.pX + move[0]][self.pY + move[1]].color != self.color:
                    self.moves.append((self.pX + move[0], self.pY + move[1]))
            except:
                pass
        

class bishop:
    def __init__(self, pos, color, moves):
        self.color = color
        self.pX = pos[0]
        self.pY = pos[1]
        self.moves = set(moves)
        if color == 'black':
            self.image = 'bBishop.png'
        else:
            self.image = 'wBishop.png'
    def moveUpdate(self):
        self.moves = []
        for tile in range(1,min(self.pX, self.pY)+1):
            if board[self.pX-tile][self.pY-tile] == 0:
                self.moves.append((self.pX-tile, self.pY-tile))
            elif board[self.pX-tile][self.pY-tile].color == self.color:
                break
            else:
                self.moves.append((self.pX-tile, self.pY-tile))
                break
        for tile in range(1,8-max(self.pX, self.pY)):
            if board[self.pX+tile][self.pY+tile] == 0:
                self.moves.append((self.pX+tile, self.pY+tile))
            elif board[self.pX+tile][self.pY+tile].color == self.color:
                break
            else:
                self.moves.append((self.pX+tile, self.pY+tile))
                break
        for tile in range(1,min(7-self.pX, self.pY)+1):
            if board[self.pX+tile][self.pY-tile] == 0:
                self.moves.append((self.pX+tile, self.pY-tile))
            elif board[self.pX+tile][self.pY-tile].color == self.color:
                break
            else:
                self.moves.append((self.pX+tile, self.pY-tile))
                break
        for tile in range(1,8-max(7-self.pX, self.pY)):
            if board[self.pX-tile][self.pY+tile] == 0:
                self.moves.append((self.pX-tile, self.pY+tile))
            elif board[self.pX-tile][self.pY+tile].color == self.color:
                break
            else:
                self.moves.append((self.pX-tile, self.pY+tile))
                break
        
class king:
    moved = False
    def __init__(self, pos, color, moves):
        self.color = color
        self.pX = pos[0]
        self.pY = pos[1]
        self.moves = moves
        if color == 'black':
            self.image = 'bKing.png'
        else:
            self.image = 'wKing.png'
    def moveUpdate(self):
        global kingMoves
        self.moves = []
        for move in kingMoves:
            try:
                if board[self.pX + move[0]][self.pY + move[1]] == 0:
                    self.moves.append((self.pX + move[0], self.pY + move[1]))
                elif board[self.pX + move[0]][self.pY + move[1]].color != self.color:
                    self.moves.append((self.pX + move[0], self.pY + move[1]))
            except:
                pass
        if not self.moved and not inCheck((3,self.pY), self.color):
            if self.color == "black":
                if isinstance(board[0][0], rook) and not inCheck((2,0), "black"):
                    if not board[0][0].moved and not board[1][0] and not board[2][0]:
                        self.moves.append((1,0))
                if isinstance(board[7][0], rook) and not inCheck((4,0), "black"):
                    if not board[7][0].moved and not board[4][0] and not board[5][0] and not board[6][0]:
                        self.moves.append((5,0))
            else:
                if isinstance(board[0][7], rook) and not inCheck((2,7), "white"):
                    if not board[0][7].moved and not board[1][7] and not board[2][7]:
                        self.moves.append((1,7))
                if isinstance(board[7][7], rook) and not inCheck((4,7), "white"):
                    if not board[7][7].moved and not board[4][7] and not board[5][7] and not board[6][7]:
                        self.moves.append((5,7))
                

class queen:
    def __init__(self, pos, color, moves):
        self.pX = pos[0]
        self.pY = pos[1]
        self.color = color
        self.moves = moves
        if color == 'black':
            self.image = 'bQueen.png'
        else:
            self.image = 'wQueen.png'
    def moveUpdate(self):
        self.moves = []
        for sq in range(self.pX-1, -1, -1):
            if board[sq][self.pY] == 0:
                self.moves.append((sq,self.pY))
            elif board[sq][self.pY].color == self.color:
                break
            else:
                self.moves.append((sq,self.pY))
                break
        for sq in range(self.pX+1, 8):
            if board[sq][self.pY] == 0:
                self.moves.append((sq,self.pY))
            elif board[sq][self.pY].color == self.color:
                break
            else:
                self.moves.append((sq,self.pY))
                break
        for sq in range(self.pY-1, -1, -1):
            if board[self.pX][sq] == 0:
                self.moves.append((self.pX,sq))
            elif board[self.pX][sq].color == self.color:
                break
            else:
                self.moves.append((self.pX,sq))
                break
        for sq in range(self.pY+1, 8):
            if board[self.pX][sq] == 0:
                self.moves.append((self.pX,sq))
            elif board[self.pX][sq].color == self.color:
                break
            else:
                self.moves.append((self.pX,sq))
                break
        for tile in range(1,min(self.pX, self.pY)+1):
            if board[self.pX-tile][self.pY-tile] == 0:
                self.moves.append((self.pX-tile, self.pY-tile))
            elif board[self.pX-tile][self.pY-tile].color == self.color:
                break
            else:
                self.moves.append((self.pX-tile, self.pY-tile))
                break
        for tile in range(1,8-max(self.pX, self.pY)):
            if board[self.pX+tile][self.pY+tile] == 0:
                self.moves.append((self.pX+tile, self.pY+tile))
            elif board[self.pX+tile][self.pY+tile].color == self.color:
                break
            else:
                self.moves.append((self.pX+tile, self.pY+tile))
                break
        for tile in range(1,min(7-self.pX, self.pY)+1):
            if board[self.pX+tile][self.pY-tile] == 0:
                self.moves.append((self.pX+tile, self.pY-tile))
            elif board[self.pX+tile][self.pY-tile].color == self.color:
                break
            else:
                self.moves.append((self.pX+tile, self.pY-tile))
                break
        for tile in range(1,8-max(7-self.pX, self.pY)):
            if board[self.pX-tile][self.pY+tile] == 0:
                self.moves.append((self.pX-tile, self.pY+tile))
            elif board[self.pX-tile][self.pY+tile].color == self.color:
                break
            else:
                self.moves.append((self.pX-tile, self.pY+tile))
                break

#function for resetting board and variables
def resetGame():
    global board
    global turn
    global currentSelected
    global validMoves
    global whiteCap
    global blackCap
    global whitePCap
    global blackPCap
    global graveSelected
    board = []
    board.append([rook((0,0), 'black', []), pawn((0,1), 'black', [(0, 2), (0,3)]), 0, 0, 0, 0, pawn((0,6), 'white', [(0, 4), (0,5)]), rook((0,7), 'white', [])])
    board.append([knight((1,0), 'black', [(0, 2), (2, 2)]), pawn((1,1), 'black', [(1, 2), (1,3)]), 0, 0, 0, 0, pawn((1,6), 'white', [(1, 4), (1,5)]), knight((1,7), 'white', [(0, 5), (2, 5)])])
    board.append([bishop((2,0), 'black', []), pawn((2,1), 'black', [(2, 2), (2,3)]), 0, 0, 0, 0, pawn((2,6), 'white', [(2, 4), (2,5)]), bishop((2,7), 'white', [])])
    board.append([king((3,0), 'black', []),  pawn((3,1), 'black', [(3, 2), (3,3)]), 0, 0, 0, 0, pawn((3,6), 'white', [(3, 4), (3,5)]), king((3,7), 'white', [])])
    board.append([queen((4,0), 'black', []), pawn((4,1), 'black', [(4, 2), (4,3)]), 0, 0, 0, 0, pawn((4,6), 'white', [(4, 4), (4,5)]), queen((4,7), 'white', [])])
    board.append([bishop((5,0), 'black', []), pawn((5,1), 'black', [(5, 2), (5,3)]), 0, 0, 0, 0, pawn((5,6), 'white', [(5, 4), (5,5)]), bishop((5,7), 'white', [])])
    board.append([knight((6,0), 'black', [(5, 2), (7, 2)]), pawn((6,1), 'black', [(6, 2), (6,3)]), 0, 0, 0, 0, pawn((6,6), 'white', [(6, 4), (6,5)]), knight((6,7), 'white', [(5, 5), (7, 5)])])
    board.append([rook((7,0), 'black', []), pawn((7,1), 'black', [(7, 2), (7,3)]), 0, 0, 0, 0, pawn((7,6), 'white', [(7, 4), (7,5)]), rook((7,7), 'white', [])])
    turn = 'black'
    currentSelected = []
    validMoves = []
    whiteCap = []
    whitePCap = []
    blackCap = []
    blackPCap = []
    inPlay = True
    graveSelected = -1
    pygame.time.delay(200)
    redrawWindow()

#function called when a player wins
def endGame(winner):
    pressed = False
    winText = titleFont.render(winner + ' wins', 3, black, white)
    winTextRect = winText.get_rect()
    winTextRect.center = (240,180)
    buttonText = font.render('Play Again', 3, black, white)
    buttonTextRect = buttonText.get_rect()
    buttonTextWrapper = (145,234,191,54) 
    buttonTextRect.center = (240, 260)
    while not pressed:
        pygame.draw.rect(win, white, buttonTextWrapper)
        pygame.draw.rect(win, black, buttonTextWrapper, 3)
        win.blit(winText, winTextRect)
        win.blit(buttonText, buttonTextRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 145 <= pos[0] < 336 and 234 <= pos[1] < 288:
                    resetGame()
                    pressed = True
        pygame.time.delay(10)
                    
                
#redraw window loop for main game
def redrawWindow():
    global switchOrient
    global turn
    global whiteCap
    global blackCap
    global graveSelected
    drawColor = 0

    win.fill((248, 236, 211))
    pygame.draw.rect(win, (0,0,0), (480, 0, 8, 480))
    
    #if pawn selected from grave, highlight selected pawn
    if graveSelected != -1:
        pygame.draw.rect(win, yellow, (488+graveSelected%4*60, 240+graveSelected//4*60, 60, 60), 0)

    #draw from different perspective depending on current player    
    if not switchOrient or turn == "white":
        
        for x in range(8):
            drawColor = (drawColor + 1) % 2
            for y in range(8):
                drawColor = (drawColor + 1) % 2
                
                #draw board tile
                if drawColor == 1:
                    pygame.draw.rect(win, pale, (x*60, y*60, 60, 60), 0)
                else:
                    pygame.draw.rect(win, brown, (x*60, y*60, 60, 60), 0)
                    
                #highlight valid positions if pawn selected from captured pieces
                if graveSelected != -1:
                    if board[x][y] == 0 and y >= 4:
                        if drawColor  == 1:
                            pygame.draw.rect(win, yellow, (x*60, y*60, 60, 60), 0)
                        else:
                            pygame.draw.rect(win, darkYellow, (x*60, y*60, 60, 60), 0)

                #highlight valid moves if piece on board selected
                if (x,y) in validMoves:
                    if drawColor == 1:
                        pygame.draw.rect(win, yellow, (x*60, y*60, 60, 60), 0)
                    else:
                        pygame.draw.rect(win, darkYellow, (x*60, y*60, 60, 60), 0)

                #highlight currently selected piece
                if (x,y) == currentSelected:
                   pygame.draw.rect(win, white, (x*60, y*60, 60, 60), 0)

                #draw piece images
                if board[x][y] != 0:
                    win.blit(pygame.image.load(board[x][y].image), (x*60, y*60))
        
        #draw captured pieces
        for piece in range(len(whiteCap)):
            win.blit(pygame.image.load(whiteCap[piece]), (488+(piece%4)*60, 420-(piece // 4)*60))
        for piece in range(len(whitePCap)):
            win.blit(pygame.image.load('wPawn.png'), (488+(piece%4)*60, 240 + (piece // 4)*60))
        for piece in range(len(blackCap)):
            win.blit(pygame.image.load(blackCap[piece]), (488+(piece%4)*60, (piece // 4)*60))
        for piece in range(len(blackPCap)):
            win.blit(pygame.image.load('bPawn.png'), (488+(piece%4)*60, 180 - (piece // 4)*60))
    else:
        for x in range(8):
            drawColor = (drawColor + 1) % 2
            for y in range(8):
                drawColor = (drawColor + 1) % 2
                if drawColor == 1:
                    pygame.draw.rect(win, pale, (x*60, y*60, 60, 60), 0)
                else:
                    pygame.draw.rect(win, brown, (x*60, y*60, 60, 60), 0)
                if graveSelected != -1:
                    if board[7-x][7-y] == 0 and (7-y) < 4:
                        if drawColor  == 1:
                            pygame.draw.rect(win, yellow, (x*60, y*60, 60, 60), 0)
                        else:
                            pygame.draw.rect(win, darkYellow, (x*60, y*60, 60, 60), 0)
                if (7-x,7-y) in validMoves:
                    if drawColor == 1:
                        pygame.draw.rect(win, yellow, (x*60, y*60, 60, 60), 0)
                    else:
                        pygame.draw.rect(win, darkYellow, (x*60, y*60, 60, 60), 0)
                if (7-x,7-y) == currentSelected:
                   pygame.draw.rect(win, white, (x*60, y*60, 60, 60), 0) 
                if board[7-x][7-y] != 0:
                    win.blit(pygame.image.load(board[7-x][7-y].image), (x*60, y*60))
        for piece in range(len(blackCap)):
            win.blit(pygame.image.load(blackCap[piece]), (488+(piece%4)*60, 420-(piece // 4)*60))
        for piece in range(len(blackPCap)):
            win.blit(pygame.image.load('bPawn.png'), (488+(piece%4)*60, 240 + (piece // 4)*60))
        for piece in range(len(whiteCap)):
            win.blit(pygame.image.load(whiteCap[piece]), (488+(piece%4)*60, (piece // 4)*60))
        for piece in range(len(whitePCap)):
            win.blit(pygame.image.load('wPawn.png'), (488+(piece%4)*60, 180 - (piece // 4)*60))
                    
    
    pygame.display.update()

#check if tile is in check (only used for castling)
def inCheck(tile, color):
    global board
    for x in board:
        for y in x:
            if y != 0:
                if y.color != color:
                    if tile in y.moves:
                        return True
    return False                        
        
#function that updates all piece's valid moves
def allMoveUpdate():
    global board
    for itr in range(2):
        for x in range(8):
            for y in range(8):
                if board[x][y] != 0:
                    board[x][y].moveUpdate()

#create board
board = []
board.append([rook((0,0), 'black', []), pawn((0,1), 'black', [(0, 2), (0,3)]), 0, 0, 0, 0, pawn((0,6), 'white', [(0, 4), (0,5)]), rook((0,7), 'white', [])])
board.append([knight((1,0), 'black', [(0, 2), (2, 2)]), pawn((1,1), 'black', [(1, 2), (1,3)]), 0, 0, 0, 0, pawn((1,6), 'white', [(1, 4), (1,5)]), knight((1,7), 'white', [(0, 5), (2, 5)])])
board.append([bishop((2,0), 'black', []), pawn((2,1), 'black', [(2, 2), (2,3)]), 0, 0, 0, 0, pawn((2,6), 'white', [(2, 4), (2,5)]), bishop((2,7), 'white', [])])
board.append([king((3,0), 'black', []),  pawn((3,1), 'black', [(3, 2), (3,3)]), 0, 0, 0, 0, pawn((3,6), 'white', [(3, 4), (3,5)]), king((3,7), 'white', [])])
board.append([queen((4,0), 'black', []), pawn((4,1), 'black', [(4, 2), (4,3)]), 0, 0, 0, 0, pawn((4,6), 'white', [(4, 4), (4,5)]), queen((4,7), 'white', [])])
board.append([bishop((5,0), 'black', []), pawn((5,1), 'black', [(5, 2), (5,3)]), 0, 0, 0, 0, pawn((5,6), 'white', [(5, 4), (5,5)]), bishop((5,7), 'white', [])])
board.append([knight((6,0), 'black', [(5, 2), (7, 2)]), pawn((6,1), 'black', [(6, 2), (6,3)]), 0, 0, 0, 0, pawn((6,6), 'white', [(6, 4), (6,5)]), knight((6,7), 'white', [(5, 5), (7, 5)])])
board.append([rook((7,0), 'black', []), pawn((7,1), 'black', [(7, 2), (7,3)]), 0, 0, 0, 0, pawn((7,6), 'white', [(7, 4), (7,5)]), rook((7,7), 'white', [])])

#main game loop
while inPlay:
    #draw title, buttons and check for button press on main screen
    if currentScreen == 0:
        win.fill((248, 236, 211))
        pygame.draw.rect(win, white, buttonTextWrapper)
        pygame.draw.rect(win, black, buttonTextWrapper, 3)
        pygame.draw.rect(win, white, rulesTextWrapper)
        pygame.draw.rect(win, black, rulesTextWrapper, 3)
        win.blit(titleText, textRect)
        win.blit(buttonText, buttonTextRect)
        win.blit(rulesText, rulesTextRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                inPlay = False
                break
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 325 <= pos[0] < 475:
                    if 175 <= pos[1] < 225:
                        currentScreen = 2
                        redrawWindow()
                    elif 250 <= pos[1] < 300:
                        currentScreen = 1

    #draw rules image and back button, check for back button press
    elif currentScreen == 1:
        win.fill((248, 236, 211))
        win.blit(pygame.image.load('gameRules.png'), (0,0))
        pygame.draw.rect(win,white,backTextWrapper)
        pygame.draw.rect(win,black,backTextWrapper,3)
        win.blit(backText, backTextRect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                inPlay = False
                break
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 10 <= pos[0] < 100 and 10 <= pos[1] < 60:
                    currentScreen = 0

    #main game loop
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                inPlay = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                  redrawWindow()
                  pos = pygame.mouse.get_pos()

                  
                  if pos[0] <= 480 and pos[1] <= 480: #if clicking somewhere on board
                      #get tile pressed
                      if not switchOrient or turn == "white":
                          boardPos = (pos[0]//60,pos[1]//60)
                      else:
                          boardPos = (7-(pos[0]//60),7-(pos[1]//60))
                      
                      if graveSelected != -1 and pos[1] >= 240: #if pawn selected from captured pieces
                          #if clicked tile is empty, place pawn in that tile
                          if board[boardPos[0]][boardPos[1]] == 0:
                              if turn == 'black':
                                  board[boardPos[0]][boardPos[1]] = pawn((boardPos[0],boardPos[1]), 'black', [])
                                  board[boardPos[0]][boardPos[1]].moved = True
                                  blackPCap.pop()
                              else:
                                  board[boardPos[0]][boardPos[1]] = pawn((boardPos[0],boardPos[1]), 'white', [])
                                  board[boardPos[0]][boardPos[1]].moved = True
                                  whitePCap.pop()
                              graveSelected = -1
                              allMoveUpdate()
                              redrawWindow()
                              pygame.time.delay(200)
                              if turn == "black":
                                  turn = "white"
                              else:
                                  turn = "black"
                      
                      elif (boardPos[0],boardPos[1]) in validMoves: #if selected tile is a valid move for selected piece
                          if board[boardPos[0]][boardPos[1]] != 0: #if a piece is captured, add piece to captured pieces list
                              if turn == "white":
                                  if isinstance(board[boardPos[0]][boardPos[1]], pawn):
                                      whitePCap.append(1)
                                  else:
                                      whiteCap.append(board[boardPos[0]][boardPos[1]].image)
                              else:
                                  if isinstance(board[boardPos[0]][boardPos[1]], pawn):
                                      blackPCap.append(1)
                                  else:
                                      blackCap.append(board[boardPos[0]][boardPos[1]].image)

                          #code used for castling
                          if (currentSelected == (3,0) or currentSelected == (3,7)) and isinstance(board[currentSelected[0]][currentSelected[1]], king):
                              if boardPos in castlingMoves.keys():
                                  board[castlingMoves[boardPos][1][0]][castlingMoves[boardPos][1][1]] = board[castlingMoves[boardPos][0][0]][castlingMoves[boardPos][0][1]]
                                  board[castlingMoves[boardPos][1][0]][castlingMoves[boardPos][1][1]].pX = castlingMoves[boardPos][1][0]
                                  board[castlingMoves[boardPos][1][0]][castlingMoves[boardPos][1][1]].pY = castlingMoves[boardPos][1][1]
                                  board[castlingMoves[boardPos][0][0]][castlingMoves[boardPos][0][1]] = 0

                          #move piece to new position, update its coordinates
                          board[boardPos[0]][boardPos[1]] = board[currentSelected[0]][currentSelected[1]]
                          board[currentSelected[0]][currentSelected[1]] = 0
                          board[boardPos[0]][boardPos[1]].pX = boardPos[0]
                          board[boardPos[0]][boardPos[1]].pY = boardPos[1]

                          #change moved property to false if object has one
                          try:
                              board[boardPos[0]][boardPos[1]].moved = True
                          except:
                              pass

                          graveSelected = -1
                          currentSelected = ()
                          allMoveUpdate()
                          validMoves = []
                          redrawWindow()

                          #end game if pawn gets to other side
                          if isinstance(board[boardPos[0]][boardPos[1]], pawn):
                              if boardPos[1] == 0 and board[boardPos[0]][boardPos[1]].color == 'white':
                                  endGame('White')
                              elif boardPos[1] == 7 and board[boardPos[0]][boardPos[1]].color == 'black':
                                  endGame('Black')

                          #switch turns
                          if turn == "black":
                              turn = "white"
                          else:
                              turn = "black"
                          pygame.time.delay(200)
                          
                      #if selected tile has a piece, select it
                      elif board[boardPos[0]][boardPos[1]] != 0 and board[boardPos[0]][boardPos[1]].color == turn and (boardPos[0],boardPos[1]) != currentSelected:
                          currentSelected = (boardPos[0], boardPos[1])
                          validMoves = board[boardPos[0]][boardPos[1]].moves
                          graveSelected = -1
                      else:
                        graveSelected = -1
                        currentSelected = ()
                        validMoves = []

                  #if clicked on captured pieces section
                  elif pos[0] > 488 and 240 <= pos[1] < 360:
                      #if pawn is selected from grave
                      if turn == 'black':
                          if (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4 < len(blackPCap) and graveSelected != (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4 < len(blackPCap):
                              graveSelected = (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4
                              currentSelected = ()
                              validMoves = []
                      else:
                          if (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4 < len(whitePCap) and graveSelected != (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4 < len(whitePCap):
                              graveSelected = (pos[0] - 488) // 60 + (pos[1] - 240) // 60 * 4
                              currentSelected = ()
                              validMoves = []
                  redrawWindow()
    pygame.time.delay(50)
