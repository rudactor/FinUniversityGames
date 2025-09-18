from string import printable

def print_board(board):
    print(" ", *printable[10:15])
    for index, elem in enumerate(board):
        print(index + 1, *elem)

def init_board():
    board = [['.'] * 5 for _ in range(4)]
    return board

board = init_board()

print_board(board)