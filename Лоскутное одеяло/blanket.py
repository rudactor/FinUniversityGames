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

    if (not letter or not digit) or (letter < "a" or letter > "j") or (digit < 1 or digit > 10) or (board[digit - 1][return_number_columns(letter)] == 1):
        if board[digit - 1][return_number_columns(letter)] == 1:
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

print_board(board)

while True:
    current_name = first_name if player_number == 0 else second_name if player_number == 1 else third_name
    move = "X" if player_number == 0 else 'Y' if player_number == 1 else 'O'
    
    print(f"Ход игрока под именем {current_name}")
    x, y = ask_for_move()
    
    board[x - 1][y] = move
    
    print_board(board)
    
    player_number = change_move(player_number)
    
    