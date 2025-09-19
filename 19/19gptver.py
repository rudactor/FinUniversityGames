#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Игра «19» (вариант «цифры, пары равных или в сумме 10, можно через зачёркнутые»).

Поле — три строки с 1-цифровыми клетками. Старт: выписываем подряд цифры от 1 до 19:
первая строка — 9 цифр, вторая — 9, третья — всё оставшееся (всего здесь 29 цифр).

Ход игрока: выбрать ДВЕ клетки, которые удовлетворяют:
  1) либо цифры равны, либо их сумма равна 10,
  2) клетки стоят по горизонтали (в одной строке) или вертикали (в одном столбце),
  3) между ними только зачёркнутые клетки (или они соседние).

После каждого хода поле перерисовывается.
Если ходов больше нет, оставшиеся цифры переписываются «в конец таблицы»:
  — собираем все незачёркнутые цифры по порядку чтения (строка 1 → 2 → 3),
  — снова раскладываем: по 9 в первую строку, по 9 во вторую, остаток — в третью.
Если и после «склейки» ходов нет — партия окончена (либо победа, если цифр не осталось,
либо ступор — ходов нет, но цифры остались).
"""

from __future__ import annotations
from typing import List, Tuple, Optional

# --- типы -------------------------------------------------------------

Cell    = Optional[int]        # None = зачёркнуто, иначе цифра 0..9
Row     = List[Cell]
Board   = List[Row]            # ровно 3 строки
Point   = Tuple[int, int]      # (r, c)   r: 0..2, c: 0..N-1 (по месту)

# --- генерация стартового поля ----------------------------------------

def initial_board() -> Board:
    digits = [int(ch) for n in range(1, 20) for ch in str(n)]  # «1..19» по ЦИФРАМ
    row1 = digits[:9]
    row2 = digits[9:18]
    row3 = digits[18:]
    return [row1, row2, row3]

# --- утилиты отрисовки / форматирования -------------------------------

def col_letters(n: int) -> str:
    # до 26 колонок легко; в нашей игре достаточно 11, но сделаем запас
    import string
    letters = string.ascii_lowercase
    if n <= len(letters):
        return letters[:n]
    # если когда-нибудь понадобится больше — добавим aa, ab, ...
    out = []
    q = n
    while q > 0:
        q, r = divmod(q - 1, 26)
        out.append(letters[r])
    return ''.join(out)

def draw(board: Board) -> None:
    width = max((len(r) for r in board), default=0)
    letters = [chr(ord('a') + i) for i in range(width)]
    print()
    print("    ", *letters, sep=' ')
    for i, row in enumerate(board, start=1):
        line = []
        for cell in row:
            if cell is None:
                line.append('·')  # зачёркнуто
            else:
                line.append(str(cell))
        print(f"{i:>2}  ", *line, sep=' ')
    print()

def board_is_empty(board: Board) -> bool:
    return all(cell is None for row in board for cell in row)

# --- проверка «видимости» по прямой через зачёркнутые -----------------

def clear_line_h(board: Board, p1: Point, p2: Point) -> bool:
    r, c1 = p1
    _r, c2 = p2
    if r != _r: 
        return False
    if c1 > c2: 
        c1, c2 = c2, c1
    row = board[r]
    # между c1 и c2 должны быть только None
    for c in range(c1 + 1, c2):
        if c < len(row) and row[c] is not None:
            return False
    return True

def clear_line_v(board: Board, p1: Point, p2: Point) -> bool:
    r1, c = p1
    r2, _c = p2
    if c != _c:
        return False
    # обе клетки должны существовать в своих строках
    for r in (r1, r2):
        if c >= len(board[r]):
            return False
    if r1 > r2:
        r1, r2 = r2, r1
    # между r1 и r2 в этом столбце — только None
    for r in range(r1 + 1, r2):
        if c < len(board[r]) and board[r][c] is not None:
            return False
    return True

# --- поиск доступных пар ----------------------------------------------

def iter_visible_neighbors(board: Board):
    """Итератор всех «видимых» (через зачёркнутые) соседей по горизонтали и вертикали.
       Возвращает кортежи (p1, p2, v1, v2) — позиции и значения.
       По горизонтали/вертикали мы берём соседние НЕ-None с учётом «сквозной видимости».
    """
    # Горизонтали: берём последовательности не-None по строкам.
    for r, row in enumerate(board):
        idxs = [c for c, v in enumerate(row) if v is not None]
        for a, b in zip(idxs, idxs[1:]):
            # между ними по определению нет других не-None
            v1, v2 = row[a], row[b]
            assert v1 is not None and v2 is not None
            yield ( (r, a), (r, b), v1, v2 )

    # Вертикали: по каждому столбцу берём существующие не-None сверху вниз.
    maxw = max((len(rw) for rw in board), default=0)
    for c in range(maxw):
        idxs = []
        vals = []
        for r in range(3):
            if c < len(board[r]) and board[r][c] is not None:
                idxs.append(r)
                vals.append(board[r][c])
        for i in range(len(idxs) - 1):
            r1, r2 = idxs[i], idxs[i + 1]
            v1, v2 = vals[i], vals[i + 1]
            yield ( (r1, c), (r2, c), v1, v2 )

def any_move_exists(board: Board) -> bool:
    for p1, p2, v1, v2 in iter_visible_neighbors(board):
        if v1 == v2 or (v1 + v2 == 10):
            # дополнительно проверим «чистую линию» (избыточно для наших генераторов, но надёжно)
            if (p1[0] == p2[0] and clear_line_h(board, p1, p2)) or \
               (p1[1] == p2[1] and clear_line_v(board, p1, p2)):
                return True
    return False

# --- «склейка» (переписывание остатка в конец) ------------------------

def pack_down(board: Board) -> Board:
    rest = [cell for row in board for cell in row if cell is not None]
    row1 = rest[:9]
    row2 = rest[9:18]
    row3 = rest[18:]
    return [row1, row2, row3]

# --- применение хода --------------------------------------------------

def apply_move(board: Board, p1: Point, p2: Point) -> bool:
    r1, c1 = p1
    r2, c2 = p2
    # валидность координат
    if r1 not in (0,1,2) or r2 not in (0,1,2):
        return False
    if c1 >= len(board[r1]) or c2 >= len(board[r2]):
        return False

    v1 = board[r1][c1]
    v2 = board[r2][c2]
    if v1 is None or v2 is None:
        return False
    # правило значений
    if not (v1 == v2 or (v1 + v2 == 10)):
        return False
    # правило геометрии
    if r1 == r2:
        if not clear_line_h(board, p1, p2):
            return False
    elif c1 == c2:
        if not clear_line_v(board, p1, p2):
            return False
    else:
        return False

    # зачёркиваем
    board[r1][c1] = None
    board[r2][c2] = None
    return True

# --- парсер ввода координат ------------------------------------------

def parse_cell(token: str, board: Board) -> Optional[Point]:
    t = token.strip().lower()
    if not t:
        return None
    # допускаем форматы "a1", "1a", а также через дефис/запятую и пр.
    # заберём буквы и цифры
    letters = ''.join(ch for ch in t if ch.isalpha())
    digits  = ''.join(ch for ch in t if ch.isdigit())
    if len(digits) != 1 or len(letters) != 1:
        return None
    r = int(digits) - 1
    c = ord(letters) - ord('a')
    if r not in (0,1,2) or c < 0:
        return None
    return (r, c)

def prompt_move(board: Board) -> Optional[Tuple[Point, Point]]:
    print("Введите ДВЕ клетки для пары (например: a1 c1 или 1a 3a).")
    print("Команды: 'q' — выход, 'help' — правила, 'pack' — принудительная склейка (если ходов нет).")
    raw = input("Ваш ход: ").strip()
    if raw.lower() in ("q", "quit", "exit"):
        return None
    if raw.lower() in ("help", "?"):
        print_rules()
        return prompt_move(board)
    if raw.lower() == "pack":
        return ( (-1,-1), (-1,-1) )  # специальный маркер
    # разбиваем по пробелам/знакам
    import re
    parts = re.split(r"[,\s;]+", raw)
    parts = [p for p in parts if p]
    if len(parts) != 2:
        print("Нужно указать ровно ДВЕ клетки.")
        return prompt_move(board)
    p1 = parse_cell(parts[0], board)
    p2 = parse_cell(parts[1], board)
    if p1 is None or p2 is None:
        print("Не смог распознать координаты. Пример: a1 c3")
        return prompt_move(board)
    if p1 == p2:
        print("Должны быть две РАЗНЫЕ клетки.")
        return prompt_move(board)
    return (p1, p2)

# --- правила (краткая памятка) ---------------------------------------

def print_rules() -> None:
    print("""
Правила хода:
  • Пара цифр должна стоять по горизонтали ИЛИ вертикали.
  • Между ними могут быть только зачёркнутые клетки (или ничего).
  • Пара допустима, если цифры равны ИЛИ дают в сумме 10.
Фаза «склейки»:
  • Когда ходов больше нет, все оставшиеся цифры переписываются в конец таблицы:
    заново раскладываем: 9 в строку 1, 9 в строку 2, остальное — в строку 3.
  • Если после склейки всё ещё нет ходов:
      — если цифр не осталось — победа,
      — иначе партия окончена (ходов нет).
""".strip())

# --- главный цикл -----------------------------------------------------

def main() -> None:
    board = initial_board()
    print("Игра «19». Введите 'help' для кратких правил, 'q' — чтобы выйти.")
    draw(board)

    # Автоматическая «склейка», если вдруг стартово нет ходов (на всякий случай)
    while True:
        if not any_move_exists(board):
            packed = pack_down(board)
            if packed == board:
                # больше уплотнять нечего
                if board_is_empty(board):
                    print("Идеально! Все цифры зачёркнуты. Победа.")
                else:
                    print("Ходов нет. Партия окончена.")
                return
            board = packed
            print("Склеили остаток (ходов не было).")
            draw(board)
        # есть хотя бы один ход — даём игроку походить
        ask = prompt_move(board)
        if ask is None:
            print("Выход из игры. До встречи!")
            return
        if ask == ((-1,-1), (-1,-1)):
            # принудительная склейка по просьбе пользователя — только если реально ходов нет
            if any_move_exists(board):
                print("Пока есть доступные пары — склейка недоступна.")
            else:
                board = pack_down(board)
                print("Принудительная склейка выполнена.")
                draw(board)
            continue

        p1, p2 = ask
        ok = apply_move(board, p1, p2)
        if not ok:
            print("Ход недопустим: проверьте, что клетки по прямой (гор/верт), "
                  "между ними только зачёркнутые, и цифры равны или в сумме 10.")
            continue

        # успешный ход
        draw(board)

        # после хода — если ходов не осталось, автоматом склеиваем (возможно несколько раз подряд)
        while not any_move_exists(board):
            packed = pack_down(board)
            if packed == board:
                if board_is_empty(board):
                    print("Идеально! Все цифры зачёркнуты. Победа.")
                else:
                    print("Ходов нет. Партия окончена.")
                return
            board = packed
            print("Склейка после исчерпания ходов.")
            draw(board)

if __name__ == "__main__":
    main()
