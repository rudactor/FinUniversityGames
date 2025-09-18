from string import printable


def create_board() -> tuple:
    all_numbers = [i for i in range(1, 20)]
    str_all_numbers = ""
    for i in all_numbers:
        str_all_numbers += str(i)
    firstrow = [int(i) for i in str_all_numbers[:9]]
    secondrow = [int(i) for i in str_all_numbers[9:18]]
    thirdrow = [int(i) for i in str_all_numbers[18:]]
    return firstrow, secondrow, thirdrow


def show_board(matrix) -> None:
    print("  ", *printable[10:21])
    for i in range(3):
        print(i + 1, "", *matrix[i])


def ask_for_move() -> tuple:
    try:
        move = input("Введите координату (буква a–k или число 1–3): ")
        letter = "".join([ch for ch in move if ch.isalpha()])
        digit = int("".join([ch for ch in move if ch.isdigit()]))
        if (len(letter)==1 and len(str(digit))==1) and (letter in printable[10:21] and digit in range(1, 4)):
            return digit, letter
        else:
            print("Вы ввели неправильные координаты. Попробуйте еще раз.")
        return ask_for_move()
    except:
        print("Вы ввели неправильные координаты. Попробуйте еще раз.")
        return ask_for_move()


def move_asker() -> tuple:
    print("Ваш первый ход: ")
    move1 = ask_for_move()
    print("Ваш второй ход: ")
    move2 = ask_for_move()
    if move1 == move2:
        print("Вы ввели одинаковые координаты. Введите координаты заново: ")
        return move_asker()
    else:
        return move1, move2




matrix = create_board()
show_board(matrix)
