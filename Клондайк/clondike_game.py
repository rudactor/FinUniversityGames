from string import printable

def print_rules() -> str:
    return """
Игра ведётся на игровом поле размером 10 на 10 клеток. 
Игроки по очереди выставляют в любую свободную клетку по отметке, и тот игрок, 
после чьего хода получилась цепочка длиной хотя бы в три отметки, проигрывает. 
При этом в цепочке считаются как свои отметки, так и отметки соперника, у игровых 
фишек как бы нет хозяина. Цепочка — это ряд фишек, следующая фишка в котором примыкает к 
предыдущей с любого из восьми направлений.
    """

def print_matrix(matrix) -> None:
    print("  ", *printable[10:20])
    for i in range(len(matrix)):
        if i == 9:
            print(i + 1, *matrix[i])
        else:
            print(i + 1, "", *matrix[i])
        
def create_matrix() -> list:
    return [[0] * 10 for _ in range(10)]

def return_number_columns(letter) -> dict:
    dict = {printable[10:20][i]: i for i in range(10)}
    return dict[letter]

def search_needable_elements(moves, row, column, matrix) -> bool:
    for i in moves:
        if row + i[0] * 2 <= 9 and column + i[1] * 2 <= 9 and row + i[0] * 2 >= 0 and column + i[1] * 2 >= 0:
            if matrix[row + i[0]][column + i[1]] == 1:
                if matrix[row + i[0] * 2][column + i[1] * 2] == 1:
                    return True
    return False

def check_winner(matrix, row, column) -> bool:
    moves = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1],  [1, 0],  [1, 1],
    ]
    return search_needable_elements(moves, row, column, matrix)

def check_board_full(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                return False
    return True

def change_move(player) -> int:
    if player == 1:
        return 0
    else:
        return 1

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

    if (not letter or not digit) or (letter < "a" or letter > "j") or (digit < 1 or digit > 10) or (matrix[digit - 1][return_number_columns(letter)] == 1):
        if matrix[digit - 1][return_number_columns(letter)] == 1:
            print("Данная ячейка уже занята. Попробуйте еще раз")
            return ask_for_move()
        else:
            print("Вы ввели неправильные координаты. Попробуйте еще раз.")
            return ask_for_move()
    else:
        return digit, letter

matrix = create_matrix()
player = 0

print_matrix(matrix)
print(print_rules())

name_first = input("Введите имя первого игрока: ")
name_second = input("Введите имя второго игрока: ")

while True:
    current_name = name_first if player == 0 else name_second
    print(f"Ход игрока под именем {current_name}")
    
    row_number, letter = ask_for_move()
    column_number = return_number_columns(letter)
    
    matrix[row_number - 1][column_number] = 1
    
    print_matrix(matrix)
    
    if check_winner(matrix, row_number - 1, column_number):
        print(f"Игрок {current_name} выйграл")
        break
    
    if check_board_full(matrix):
        print("Ничья")
        break

    player = change_move(player)
    
    