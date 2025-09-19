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
    max_len = max(len(r) for r in matrix)
    letters = printable[10:10+max_len]
    print("  ", *letters)
    for i in range(3):
        print(i + 1, "", *matrix[i])


def return_number_columns(letter) -> int:
    letters = printable[10:21]
    colmap = {letters[i]: i for i in range(len(letters))}
    return colmap[letter]


def check_move_is_full(matrix, digit, letter) -> bool:
    try:
        row_idx = digit - 1
        col_idx = return_number_columns(letter)
        if row_idx < 0 or row_idx >= len(matrix):
            return False
        if col_idx < 0 or col_idx >= len(matrix[row_idx]):
            return False
        return matrix[row_idx][col_idx] != '.'
    except:
        return False


def ask_for_move(mtrx) -> tuple:
    try:
        move = input("Введите координату (например, 1a или a1, буква a–k, строка 1–3): ")
        letter = "".join([ch for ch in move if ch.isalpha()])
        digit_str = "".join([ch for ch in move if ch.isdigit()])
        if len(letter) != 1 or len(digit_str) != 1:
            raise ValueError
        digit = int(digit_str)

        if (letter in printable[10:21]) and (digit in range(1, 4)) and check_move_is_full(mtrx, digit, letter):
            return digit, letter
        else:
            print("Вы ввели неправильные координаты (нет такой клетки/клетка пустая). Попробуйте еще раз.")
            return ask_for_move(mtrx)
    except Exception:
        print("Вы ввели неправильные координаты. Попробуйте еще раз.")
        return ask_for_move(mtrx)


def move_asker(mtrx) -> tuple:
    print("Ваш первый ход: ")
    move1 = ask_for_move(mtrx)
    print("Ваш второй ход: ")
    move2 = ask_for_move(mtrx)
    if move1 == move2:
        print("Вы ввели одинаковые координаты. Введите координаты заново: ")
        return move_asker(mtrx)
    else:
        return move1, move2


def _same_line_or_column(r1, c1, r2, c2) -> bool:
    return (r1 == r2) or (c1 == c2)


def _path_clear(mtrx, r1, c1, r2, c2) -> bool:
    if r1 == r2:
        row = mtrx[r1]
        left, right = sorted([c1, c2])
        for x in range(left + 1, right):
            if x >= len(row):
                return False
            if row[x] != '.':
                return False
        return True
    elif c1 == c2:
        top, bottom = sorted([r1, r2])
        for rr in range(top + 1, bottom):
            if c1 >= len(mtrx[rr]):
                return False
            if mtrx[rr][c1] != '.':
                return False
        return True
    else:
        return False


def check_move_is_correct(mtrx):
    moves = move_asker(mtrx)
    (r1_in, l1), (r2_in, l2) = moves
    r1 = r1_in - 1
    r2 = r2_in - 1
    c1 = return_number_columns(l1)
    c2 = return_number_columns(l2)

    def in_bounds(r, c):
        return 0 <= r < len(mtrx) and 0 <= c < len(mtrx[r])

    if not (in_bounds(r1, c1) and in_bounds(r2, c2)):
        print("Координаты вне поля. Попробуйте еще раз.")
        return check_move_is_correct(mtrx)

    if not _same_line_or_column(r1, c1, r2, c2):
        print("Клетки должны быть в одной строке или одном столбце.")
        return check_move_is_correct(mtrx)

    if not _path_clear(mtrx, r1, c1, r2, c2):
        print("Между клетками есть незачёркнутые цифры. Ход недопустим.")
        return check_move_is_correct(mtrx)

    v1 = mtrx[r1][c1]
    v2 = mtrx[r2][c2]
    if not (isinstance(v1, int) and isinstance(v2, int)):
        print("Вы выбрали уже зачёркнутую клетку. Попробуйте еще раз.")
        return check_move_is_correct(mtrx)

    if (v1 == v2) or (v1 + v2 == 10):
        mtrx[r1][c1] = '.'
        mtrx[r2][c2] = '.'
        return mtrx
    else:
        print("Цифры не равны и не дают в сумме 10. Попробуйте еще раз.")
        return check_move_is_correct(mtrx)


def check_winner() -> bool:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != '.':
                return False
    return True

matrix = create_board()
show_board(matrix)
while True:
    pass

