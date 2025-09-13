from random import randint

def print_rules():
    return ''

def create_random_str() -> str:
    l = []
    while len(l) < 4:
        a = randint(0, 9)
        if a not in l:
            l.append(a)
    return "".join(list(map(str, l)))

def check_right_str() -> bool:
    player_str = input("Введите строку, чтобы угадать загаданную: ")
    l = [int(i) for i in player_str if i.isdigit()]
    if len(set(l)) == len(player_str):
        return player_str
    else:
        print('Введите корректные данные')
        return check_right_str()

def check_positions(main_str: str, check_str: str) -> tuple:
    bulls, cows = 0, 0
    for i in range(len(main_str)):
        if check_str[i] == main_str[i]:
            bulls += 1
        elif check_str[i] != main_str[i] and check_str[i] in main_str:
            cows += 1
    return bulls, cows

def swap_move(player) -> int:
    if player == 1:
        return 0
    else:
        return 1
        
player = 0

print(print_rules())

name_first = input("Введите имя первого игрока: ")
name_second = input("Введите имя второго игрока: ")

random_str = create_random_str()
        
while True:
    current_name = name_first if player == 0 else name_second
    print(f"Ход игрока под именем {current_name}")
    
    player_str = check_right_str()
    bulls, cows = check_positions(random_str, player_str)
    
    if bulls == 4:
        print(f"Игрок {current_name} выйграл")
        break
    
    print(f"Быки: {bulls}, Коровы: {cows}")