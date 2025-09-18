from random import randint
from string import printable

def print_field(board):
    print("  ", *printable[10:20])
    for index, element in enumerate(board):
        if index + 1 != 10:
            print(index + 1, "",*element)
        else:
            print(index + 1, *element)

def init_board_secure():
    return [["#"] * 10 for _ in range(10)]

def init_board():
    cnter = 0
    i = 0
    board = [['.'] * 10 for _ in range(10)]
    
    while i < 4:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 1):
            i += 1
            
    i = 0
            
    while i < 3:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 2, direction):
            i += 1
            
    i = 0
            
    while i < 2:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 3, direction):
            i += 1
            
    i = 0
            
    while i < 1:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 4, direction):
            i += 1
            cnter += 1
        
    return board
        
def place_ship(board, x, y, length, direction = 'H'):
    if board[x][y] != '*' and is_place_free(board, x, y, length, direction):
        if direction == 'H':
            for i in range(length):
                board[x][y + i] = '*'
        elif direction == 'V':
            for i in range(length):
                board[x+i][y] = "*"
        return True
    return False
        
        
def is_place_free(board, x, y, length, direction = 'H'):
    n = len(board)

    cells = []
    if direction == "H":
        if y + length > n:  
            return False
        cells = [(x, y+i) for i in range(length)]
    else:  
        if x + length > n:
            return False
        cells = [(x+i, y) for i in range(length)]

    for cx, cy in cells:
        
        if board[cx][cy] == "*":
            return False
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] == "*":
                    return False
    return True
    
board_with_ships = init_board()
board_secure = init_board_secure()

print_field(board_secure)
print_field(board_with_ships)