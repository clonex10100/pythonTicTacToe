#!/usr/bin/env python3
import socket
import curses
from time import sleep
        
#Board is [y][x] format
board=[[" "," "," "],[" "," "," "],[" "," "," "]]

#Draws the board and refreshes
def render():
    global board
    pos = 0
    for i in range(len(board)):
        screen.addstr(pos,0,board[i][0]+"|"+board[i][1]+"|"+board[i][2]) 
        if i != 2:
            pos+=1
            screen.addstr(pos, 0,"-|-|-")
            pos+=1
    screen.refresh()

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

#ends the game, printing different messages based on the scenario
def end(won):
    if won == 1:
        screen.addstr(5,0,"You won!")
    elif won == -1:
        screen.addstr(5,0,"You Lost!")
    elif won ==0:
        screen.addstr(5,0,"Cat's game!")
    elif won == -2:
        screen.addstr(5,0,"Bye!")
    screen.refresh()
    sleep(5)
    n.close()
    quit()

#moves the cursor accross the board, returning the x y of the place selected
def choosePiece():
    #Get cursor in position, than show it.
    cur=[1,1]
    curses.curs_set(True)
    #Map of arrow key vals to directional tuples
    val={258:(1,0),259:(-1,0),260:(0,-1),261:(0,1)}
    while True:
        screen.move(cur[0]*2,cur[1]*2)
        #Grab kepress
        key = screen.getch()
        #if enter is pressed, and cursor is in a valid spot, put return the coords
        if key == 10 and board[cur[0]][cur[1]] == " ":
                curses.curs_set(False)
                return(cur[1],cur[0])
        else:
            try:
                offset=val.get(key)
                cur[0]+=offset[0]
                cur[0]%=3
                cur[1]+=offset[1]
                cur[1]%=3
                #doubles to make match with physical postition
            except:
                pass

            

#The turn for this client. Places a piece  and sends the coords to the other client in format "x.y"
def localTurn():
    global board
    x,y  = choosePiece() 
    put(localPiece,x,y)
    n.sendall(str.encode(str(x)+"."+str(y)))
    render()
    analyze()

#Recieves the other players move and adds it to the board
def remoteTurn():
    data=0
    #keep recieving from socket until non-blank datapacket
    while not data:
        data=n.recv(1024)
        if data:
            stri = data.decode('UTF-8')
            #Parse input
            x,y = [int(i) for i in stri.split(".")]
            #put their piece on the board
            put(remotePiece,x,y)
            render()
            analyze()

def main(screenPass):
    global localPiece, remotePiece, n, screen
    screen = screenPass
    curses.curs_set(False)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #Setup the socket
        curses.echo()
        #select the port
        while True:
            try:
                screen.addstr(0,0,"Enter port")
                port = int(screen.getstr(1,0,4).decode(encoding="utf-8"))
                break
            except:
                screen.clear()
                screen.addstr(2,0,"invalid port value")
        screen.clear()
        curses.noecho()
        try:
            s.connect(("localhost",port))
            localPiece="o"
            remotePiece="x"
            n=s
            render()
            remoteTurn()
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
            localTurn()
            #their turn
            remoteTurn()

curses.wrapper(main)
