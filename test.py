import curses
from time import sleep

board=[[" "," "," "],[" "," "," "],[" "," "," "]]
def render(screen):
    global board
    for i in range(len(board)):
        screen.addstr(i,0,str(i)+" "+board[i][0]+"|"+board[i][1]+"|"+board[i][2]) 
        if i != 0:
#            screen.addstr(0,i+1,"-|-|-")
            pass
    screen.refresh()
def main(screen):
    while True:
        inp = screen.getch()
        screen.addstr(0,0,str(inp))
        screen.refresh()
    
    sleep(1)
curses.wrapper(main)
