from random import randint

def print_field(board):
    for i in board:
        print(*i)

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
            i+=1
            cnter += 1
            
    i = 0
            
    while i < 3:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 2, direction):
            i+=1
            cnter += 1
            
    i = 0
            
    while i < 2:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 3, direction):
            i+=1
            cnter += 1
            
    i = 0
            
    while i < 1:
        index = randint(0, 99)
        row = index // 10
        column = index % 10
        direction = "H" if randint(0, 1) == 0 else "V"
        if place_ship(board, column, row, 4, direction):
            i+=1
            cnter += 1
        
    print_field(board)
        
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
    
init_board()