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

def ask_for_move() -> tuple:
    move = input("Сделайте следующий ход: ")
    try:
        letter = "".join([ch for ch in move if ch.isalpha()])
        digit = int("".join([ch for ch in move if ch.isdigit()]))
        if len(letter)==1 and (len(str(digit))==1 or digit == 10):
            pass
        else:
            print("Вы ввели неправильные координаты. Попробуйте еще раз.")
            return ask_for_move()
    except:
        print("Вы ввели неправильные координаты. Попробуйте еще раз.")
        return ask_for_move()

    if (not letter or not digit) or (letter < "a" or letter > "j") or (digit < 1 or digit > 10):
        print("Вы ввели неправильные координаты. Попробуйте еще раз.")
        return ask_for_move()
    else:
        return digit, return_number_columns(letter)

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
    if board_security[x - 1][y] in ('.', 'X'):
        print("Вы уже туда стреляли")
        return "was"

    if board[x - 1][y] == '*':
        board[x - 1][y] = 'X'
        board_security[x - 1][y] = 'X'

        if check_cells(board, x, y):
            print("Корабль убит")
            return "kill"
        else:
            print("Попал")
            return "hit"

    if board[x - 1][y] == '.':
        board_security[x - 1][y] = '.'
        print("Мимо")
        return "miss"
        
def check_cells(board, x, y):
    rows, cols = len(board), len(board[0])
    stack = [(x-1, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        if 0 <= cx < rows and 0 <= cy < cols:
            if board[cx][cy] == '*':   
                return False           
            elif board[cx][cy] == 'X':
                stack.extend([
                    (cx-1, cy), (cx+1, cy),
                    (cx, cy-1), (cx, cy+1)
                ])

    return True
        
def check_win(board):
    cnter = 0
    for lst in board:
        cnter += lst.count("X")
    
    if cnter == 20:
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

while True:
    x, y = ask_for_move()
    
    result = shoot(board_with_ships, board_secure, x, y)

    if result == "was":
        continue
    
    print_field(board_secure)
    
    if check_win(board_secure):
        print("Вы победили!")
        break