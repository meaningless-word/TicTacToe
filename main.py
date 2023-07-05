human = 0  # счетчик побед человека
computer = 0  # счетчик побед компа

yes_no_list = ["y", "n"]
x_o_list = ["X", "0"]
row_list = [["1", "2", "3"], ["0", "1", "2"]]
column_list = [["a", "b", "c"], ["0", "1", "2"]]
horizon = "---+---+---+---"

# выигрышные комбинации
victories = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8],
             [0, 3, 6],
             [1, 4, 7],
             [2, 5, 8],
             [0, 4, 8],
             [2, 4, 6]]


def ask(question, answer_options, repeat="что, простите?"):
    """
    Задаёт вопрос, принимая ответ только из списка ответов.
    Если ответ не из списка, переспрашивает
    :param question: вопросительная фраза
    :param answer_options: список принимаемых ответов
    :param repeat: фраза при некорректном вводе
    :return: введённый ответ
    """
    if isinstance(answer_options, list):
        answer = input(f"{question} ---> ")
        while answer.upper() not in list(map(str.upper, answer_options)):
            answer = input(f"{repeat} ---> ")
        return answer


def get_state(b, h, c):
    """
    Оформление доски - расстановка на доске значков игроков в занятые ими клетки
    :param b: доска (список)
    :param h: знак человеческого игроком
    :param c: знак компьютерного игрока
    :return: список оформленных клеток
    """
    state = []
    for item in b:
        s = "·" if item == 0 else h if item == -1 else c if item == 1 else " "
        state.append(s)
    return state


def make_board(selected_type, state):
    """
    Отрисовка доски согласно предварительному оформлению
    :param selected_type: тип отображения доски
    :param state: подготовленное оформление
    :return: доска построчно (список)
    """
    lines = [f"   | {' | '.join(column_list[selected_type])} "]
    for i in range(0, 3):
        lines.append(horizon)
        lines.append(f' {row_list[selected_type][i]} | {"| ".join([s + " " for s in state[i * 3: i * 3 + 3]])}')
    return lines


def show_board(lines):
    """
    Выводит доску на экран
    :param lines: доска построчно (список)
    :return: ничего
    """
    print("\n".join(lines))


def stylize_position(cell):
    """
    Стилизует абсолютную позицию на доске в рамках выбранной системы координат
    :param cell: позиция от 0 до 8 включительно
    :return: координаты в стиле "a1" либо "0 0"
    """
    r = row_list[board_type][cell // 3]
    c = column_list[board_type][cell % 3]
    return f"{r} {c}" if board_type else f"{c}{r}"


def put_sign(p, m, e):
    """
    Ставит на доску указанный знак
    :param p: стилизованная позиция
    :param m: знак игрока
    :param e: список пустых позиций
    :return: ничего
    """
    if board_type:
        r, c = p.split()  # это координаты в стиле "0 0"
    else:
        c, r = list(p)  # а это координаты в стиле "a1"
    board[row_list[board_type].index(r) * 3 + column_list[board_type].index(c)] = m
    e.remove(p)  # удаляем текущую позицию из списка доступных клеток, чтобы исключить попытки её заполнить

def check_combination(mine, his):
    """
    Проверка игровой ситуации по каждой из игровых комбинаций для определения приемлемого хода компьютерного игрока
    :param mine: сколько клеток должно быть занято знаками компьютерного игрока
    :param his: сколько клеток должно быть занято знаками человеческого игрока
    :return: стилизованная позиция клетки, в которой можно разместить знак компьютерного игрока
    """
    for line in victories:  # перебираем выигрышные комбинации
        m = 0  # сюда считаем свои
        h = 0  # сюда - клетки оппонента
        for cell in line:  # перебираем каждую из трёх клеток комбинации
            m += 1 if board[cell] == 1 else 0  # если наша - считаем себе
            h += 1 if board[cell] == -1 else 0  # если не наша - оппоненту
        if m == mine and h == his:  # если подсчеты соответствуют заданию
            for cell in line:  # ищем пустую клетку перебором
                if not board[cell]:  # если нашлась
                    return stylize_position(cell)
    return ""


def human_turn(empty_cells):
    """
    Запрос очередного хода человеческого игрока с размещением его знака на доске и актуализация списка незанятых клеток
    :param empty_cells: список незанятых клеток
    :return: ничего
    """
    position = ask("укажи клетку", empty_cells, "эта клетка занята, другую давай!")
    put_sign(position, -1, empty_cells)


def computer_turn(empty_cells):
    """
    Подбор очередного хода компьютерного игрока с размещением его знака на доске и актуализация списка незанятых клеток
    :param empty_cells: список незанятых клеток
    :return: ничего
    """
    position = check_combination(2, 0)  # если ситуация выигрышная - осталось поставить свой знак - воспользуемся
    if not position:  # если не сложилась, анализируем дальше
        position = check_combination(0, 2)  # если выигрышная ситуация у противника - помешаем
        if not position:  # если не сложилась у него, дальше
            position = check_combination(1, 0)  # если в строке есть мой знак, а дальше пусто - достраиваем
            if not position:  # если таких строк нет - дальше
                position = stylize_position(4)  # попытаться занять центр
                if position not in empty_cells:  # если центр уже занят, продолжить анализ
                    for cell in [0, 2, 6, 8]:  # последняя надежда - попытка занять любой оставшийся угол
                        position = stylize_position(cell)
                        if position in empty_cells:
                            break
    print(f"мой ход: {position}")
    put_sign(position, 1, empty_cells)


def victory_check():
    """
    Проверка наличия выигрышной ситуации
    :return: знак победителя, если он есть и признак останова игры
    игра останавливается, если определен победитель или больше нет свободных клеток
    """
    for victory in victories:
        s = 0
        for v in victory:
            s += board[v]
        if s == 3:
            return 1, True
        elif s == -3:
            return -1, True
    return 0, 0 not in board


print("предлагаю выбрать стиль системы координат:")
print("        (1)                 (2)")
empty_state = get_state([0] * 9, "", "")
show_board([f"{x}     {y}" for x, y in zip(make_board(0, empty_state), make_board(1, empty_state))])
print("способ ввода координат:")
print("(1): a1 - пересечение именованной буквой колонки и порядкового номера строки")
print("(2): 0 0 - пересечением строки, номер которой указан первым в паре координат, и колонки - указанным вторым номером")
board_type = int(ask("1/2", ["1", "2"])) - 1

while True:
    print("на всякий случай... первый ход делает игрок, ставящий крестики. ")
    human_sign = ask("чем играешь? X/0", x_o_list).upper()
    computer_sign = x_o_list[(x_o_list.index(human_sign) + 1) % 2]
    print(f"Ok, тогда я беру \"{computer_sign}\"")

    # определение порядка ходов
    first_turn = human_turn if human_sign == "X" else computer_turn
    second_turn = human_turn if human_sign == "0" else computer_turn

    print("игра началась...")

    board = [0] * 9  # пустая доска
    show_board(make_board(board_type, get_state(board, human_sign, computer_sign)))
    # определим список всех вариантов координат на пустой доске
    z = []
    for row in [[i] * 3 for i in row_list[board_type]]:
        z.extend([f"{x}{y}" if board_type == 0 else f"{x} {y}" for x, y in zip(column_list[board_type], row)])

    winner, status = 0, False
    # игра идёт до тех пор, пока на доске остаются пустые клетки
    while 0 in board:
        first_turn(z)  # сначала ход игрока, который выбрал Х
        show_board(make_board(board_type, get_state(board, human_sign, computer_sign)))  # отрисовка доски
        winner, status = victory_check()
        if status:
            break

        # аналогично для игрока, который выбрал 0
        second_turn(z)
        show_board(make_board(board_type, get_state(board, human_sign, computer_sign)))
        winner, status = victory_check()
        if status:
            break

    if winner == 1:
        computer += 1
        print("моя победа")
    elif winner == -1:
        human += 1
        print("твоя победа")
    else:
        print("ничья")

    print("|    общий счет       |")
    print("| человек : компьютер |")
    print("|   {:3d}   :    {:3d}    |".format(human, computer))

    again = ask("сыграем снова? y/n", yes_no_list)
    if again.upper() == "N":
        break
