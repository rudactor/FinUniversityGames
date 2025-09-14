from random import randint
from string import printable

def print_rules() -> None:
    print("На шахматной доске в некоторых клетках случайно разбросаны фишки или пуговицы. Игроки ходят по очереди. За один ход можно снять все фишки с какой-либо горизонтали или вертикали, на которой они есть. Выигрывает тот, кто заберет последние фишки.")
    return None

def create_matrix() -> list:
    matrix = [[0] * 8 for _ in range(8)]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = randint(0,1)
    return(matrix)


def print_matrix(mtrx) -> None:
    print("  ", *printable[10:18])
    for i in range(len(mtrx)):
        print(i + 1, "", *mtrx[i])

def ask_for_move():
    letters = printable[10:18]
    digits = [str(i) for i in range(1, 9)]
    move = input("Введите координату (буква a–h или число 1–8): ")
    if move in digits or move in letters:
        return move
    else:
        print("Неверный ввод. Попробуйте еще раз.")
        return ask_for_move()

def edit_matrix_after_move(mv, mtrx) -> list:
    if mv.isdigit():
        for i in range(len(mtrx)):
            mtrx[int(mv)-1][i] = 0
    else:
        for i in range(len(mtrx)):
            mtrx[i][ord(mv)-ord("a")] = 0
    return mtrx


def check_winner(mtrx):
    sum = 0
    for i in range(len(mtrx)):
        for j in range(len(mtrx)):
            sum += mtrx[i][j]
    if sum < 1:
        return True
    else:
        return False


movenumber = 0

print_rules()
user1 = input("1ый игрок. Введите ваш никнейм: ")
user2 = input("2ой игрок. Введите ваш никнейм: ")
matrix = create_matrix()
print_matrix(matrix)

while True:
    if movenumber % 2 == 0:
        print(f"Ход игрока {user1}")
    else:
        print(f"Ход игрока {user2}")
    move = ask_for_move()
    movenumber += 1
    edit_matrix_after_move(move, matrix)
    print_matrix(matrix)
    if check_winner(matrix):
        break

if movenumber % 2 == 0:
    winner = user1
else:
    winner = user2
print(f"Игрок {winner} победил!")
print(f"Партия длилась {movenumber} ходов")