from random import randint

#functions
def print_board (board):
    """printing the board in user mode"""
    for row in board:
        print " ".join(row)

def random_row (board):
    """defines randomly the row ship location"""
    return randint(0,len(board)-1)

def random_col (board):
    """defines randomly the col ship location"""
    return randint(0,len(board[0])-1)

#setting up the game board
board = []
for i in range(5):
    board.append(5*['O'])
    
#locating the ship into the board
ship_row = random_row(board)
ship_col = random_col(board)
#print ship_row
#print ship_col

#presentation
print "Let's play Battleship!"
print_board(board)

#playing
for turn in range(4):
    guess_row = input("Guess Row:")
    guess_col = input("Guess Col:")

    if guess_row == ship_row and guess_col == ship_col:
        print "Congratulations! You sunk my battleship!"
        break
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            print "Oops, that's not even in the ocean."
        elif(board[guess_row][guess_col] == "X"):
            print "You guessed that one already."
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "X"
        print str(turn+1)
        print_board(board)
        if turn == 3:
            print "Game Over"
