board = list(range(1, 10))


def draw_board(board):
    print("-" * 13)
    for i in range(3):
        print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
        print("-" * 13)

def take_input(player_token, player_name):
    valid = False
    while not valid:
        player_answer = input(f"ход делает {player_name} \nКуда поставим {player_token}? ")
        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if 1 <= player_answer <= 9:
            if str(board[player_answer - 1]) not in "XO":
                board[player_answer - 1] = player_token
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число от 1 до 9.")

def check_win(board):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False

def main(board):
    print("""Добро пожаловать в игру Крестики нолики!
В этой игре опоненты делают поочерёдные ходы крестиком или ноликом,
пока один из них не соберёт три одинаковых знака по вертикали, горизонтали или вертикали.
Первым ход делает крестик.""")
    player1 = input("Кто будет играть за X? ")
    player2 = input("Кто будет играть за 0? ")
    counter = 0
    win = False
    while not win:
        draw_board(board)
        if counter % 2 == 0:
            take_input("X", player1)
        else:
            take_input("O", player2)
        counter += 1

        tmp = check_win(board)
        if tmp == 'X':
            print(player1, "выиграл!")
            win = True
            break
        if tmp == '0':
            print(player2, "выиграл!")
            win = True
            break

        if counter == 9:
            print("Ничья!")
            break
    draw_board(board)
main(board)