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

def return_number_columns(letter) -> dict:
    dict = {printable[10:20][i]: i for i in range(10)}
    return dict[letter]

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
        
def shoot(board, board_security, x, y):
    if board[x - 1][y] == '*' and check_cells(board, x, y):
        print("Убил")
        return True
    elif board[x - 1][y] == '*' and not check_cells(board, x, y):
        print("Попал")
        return True
    elif board_security[x - 1][y] == '.' or board_security[x - 1][y] == 'X':
        print("Вы уже туда стреляли")
        return shoot(board, board_security, x, y)
    elif board[x - 1][y] == '.':
        print("Мимо")
        return False
        
def check_cells(board, x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if board[x + dx - 1][y + dy] == "*":
            return False
    return True
        
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

while True:
    inp = input("Введите координаты хода: ").split()
    x, y = int(inp[0]), return_number_columns(str(inp[1]))
    
    if shoot(board_with_ships, board_secure, x, y):
        board_secure[x - 1][y] = 'X'
    elif not shoot(board_with_ships, board_secure, x, y):
        board_secure[x - 1][y] = '.'
    
    print_field(board_secure)
    print_field(board_with_ships)