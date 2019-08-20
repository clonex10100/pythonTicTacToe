#!/usr/bin/env python3
import socket
        
#Board is [y][x] format
board=[[" "," "," "],[" "," "," "],[" "," "," "]]


#Draws the board
def render():
    global board
    print("+-0-1-2")
    print("|")
    for i in range(len(board)):
        print(str(i)+" "+board[i][0]+"|"+board[i][1]+"|"+board[i][2]) 
        if i != 2:
            print("| -|-|-")
    print("----------------")

#Puts piece p at position x-y if valid and returns 0, returns -1 otherwise
def put(p,x,y):
    try:
        if board[y][x] == " ":
            board[y][x] = p 
            return 0
        else:
            return -1
    except:
        return -1

#Detects if the game is over, calls end
def analyze():
    for i in range(3):
        if all(j[i] == localPiece for j in board) or all(board[i][j] == localPiece for j in range(3)):
            end(1)
        if all(j[i] == remotePiece for j in board) or all(board[i][j] == remotePiece for j in range(3)):
            end(-1)
    #Check diagnals
    if board[0][0] == board[1][1] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[1][1] == board[2][0]:
        if board[1][1] == localPiece:
            end(1)
        if board[1][1] == remotePiece:
            end(-1)
    #if cat, end 0
    for i in board:
        for j in i:
            if j == " ":
                return 0
    end(0)

def end(won):
    if won == 1:
        print("You won!")
    elif won == -1:
        print("You Lost!")
    elif won ==0:
        print("Cat's game!")
    elif won == -2:
        print("Bye!")
    s.close()
    quit()

def localTurn(n):
    global board
    while True:
        place  =  input("Where do you want to play (x.y): ")
        #if q quit
        if place == "q":
            n.sendall(str.encode(place))
            end(-2)
        try:
            #Parse input
            x,y = [int(i) for i in place.split(".")]
            #Attempt to place piece on board
            if put(localPiece,x,y) == 0:
                break
            else:
                render()
                print("Invalid position")
        except:
            render()
            print("Invalid input, try again")
    n.sendall(str.encode(place))
    render()
    analyze()

def remoteTurn(n):
    data=0
    #keep recieving from socket until non-blank datapacket
    while not data:
        data=n.recv(1024)
        if data:
            stri = data.decode('UTF-8')
            #if q, quit
            if stri == "q":
                end(-2)
            #Parse input
            x,y = [int(i) for i in stri.split(".")]
            #put their piece on the board
            put(remotePiece,x,y)
            render()
            analyze()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Setup the socket
    while True:
        try:
            port=int(input("What socket do you want to use? (Should be > 1024)"))
            break
        except:
            print("invalid port value")
    try:
        s.connect(("localhost",port))
        localPiece="o"
        remotePiece="x"
        n=s
        render()
        remoteTurn(n)
    except:
        s.bind(('localhost',port))
        s.listen()
        n, addr = s.accept()
        localPiece="x"
        remotePiece="o"
        render()
    #gameloop
    while True:
        #your turn
        localTurn(n)
        #their turn
        remoteTurn(n)
