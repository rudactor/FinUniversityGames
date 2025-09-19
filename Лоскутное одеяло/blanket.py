from string import printable

def print_board(board):
    print(" ", *printable[10:15])
    for index, elem in enumerate(board):
        print(index + 1, *elem)

def init_board():
    board = [['.'] * 5 for _ in range(4)]
    return board

def change_move(player) -> int:
    if player == 0:
        return 1
    elif player == 1:
        return 2
    elif player == 2:
        return 0
    
def return_number_columns(letter) -> dict:
    dict = {printable[10:15][i]: i for i in range(5)}
    return dict[letter]

def check_cells(board, x, y, cell):
    cnter = 0
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (-1, 1)]
    for i in moves:
        if x + i[0] - 1 <= 3 and x + i[0] - 1 >= 0 and y + i[1] >= 0 and y + i[1] <= 4:
            if board[x - 1 + i[0]][y + i[1]] == cell:
                cnter += 1
    return cnter
            

def check_full_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '.':
                return False
    return True

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

    if (not letter or not digit) or (letter < "a" or letter > "j") or (digit < 1 or digit > 10) or (board[digit - 1][return_number_columns(letter)] != '.'):
        if board[digit - 1][return_number_columns(letter)] == '.':
            print("Данная ячейка уже занята. Попробуйте еще раз")
            return ask_for_move()
        else:
            print("Вы ввели неправильные координаты. Попробуйте еще раз.")
            return ask_for_move()
    else:
        return digit, return_number_columns(letter)

board = init_board()

first_name = str(input("Введите имя первого игрока: "))
second_name = str(input("Введите имя второго игрока: "))
third_name = str(input("Введите имя третьего игрока: "))

player_number = 0

cnter_moves = [0, 0, 0]

print_board(board)

while True:
    current_name = first_name if player_number == 0 else second_name if player_number == 1 else third_name
    move = "X" if player_number == 0 else 'Y' if player_number == 1 else 'Z'
    
    print(f"Ход игрока под именем {current_name}")
    x, y = ask_for_move()
    
    board[x - 1][y] = move
    
    print_board(board)
    
    cnter_moves[player_number] += check_cells(board, x, y, move)
    
    if check_full_board(board):
        number_lose = cnter_moves.index(max(cnter_moves))
        current_name = first_name if number_lose == 0 else second_name if number_lose == 1 else third_name
        print(f"Игрок {current_name} проиграл")
        break
        
    player_number = change_move(player_number)
    
    