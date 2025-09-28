import random
import sys
from colorama import init, Fore, Style

EMPTY = "#"
SEP = "-" * 35
BYE_MSG = f"\n{SEP}\nBye and thanks for Playing!\n{SEP}"
AI_NAMES = ["Randobot", "Winobot", "Defendobot", "Ultrabot"]


class Player:
    # human player with name and sign ("O" or "X")
    def __init__(self, name, sign):
        self._name = name
        self._sign = sign

    @property
    def name(self):
        return self._name

    @property
    def sign(self):
        return self._sign


class AI:
    # AI with difficulty level and sign
    def __init__(self, level, sign):
        self._name = AI_NAMES[level - 1]
        self._level = level
        self._sign = sign

    @property
    def name(self):
        return self._name

    @property
    def sign(self):
        return self._sign

    @property
    def level(self):
        return self._level


def main():
    # choose mode and start according game
    init(autoreset=True)
    try:
        print(
            f"{Style.BRIGHT}{Fore.YELLOW}{SEP}\nWelcome to Tic-Tac-Toe!\n{SEP}\nQuit anytime by typing Strg+D\n{SEP}"
        )
        while True:
            mode = (input(
                    "  'AI'   : to play against Bot\n'normal' : to continue normally\nMode: "
                    ).strip().lower())

            if mode in ("normal", "n", ""):
                run_multiplayer_game()
                break
            elif mode in ("ai", "a"):
                run_ai_game()
                break
            else:
                print(f"{Style.BRIGHT}{Fore.RED}{SEP}\nInvalid Mode!\n{SEP}")
    except EOFError:
        # exit on Ctrl+D
        sys.exit(f"{Style.BRIGHT}{Fore.CYAN}{BYE_MSG}")


def run_multiplayer_game():
    # human vs human
    try:
        print(f"{Style.BRIGHT}{Fore.BLUE}{SEP}\nYOU CHOSE MULTIPLAYER!\n{SEP}")
        name1 = input("Whats Player 1's Name? ").strip()
        name2 = input("Whats Player 2's Name? ").strip()

        players = [Player(name1, "O"), Player(name2, "X")]
        to_move = random.randint(0, 1)  # randomly choose start player
        board = new_board()

        while True:
            print_board(board)
            current_player = players[to_move]

            print(f"{current_player.name}'s Turn!\n{SEP}")
            board = get_move(board, current_player.sign)

            won, _ = check_won(board)
            if won:
                print_board(board)
                print(f"{Style.BRIGHT}{Fore.GREEN}{SEP}\n{current_player.name} won!\n{SEP}")
                break
            if check_tie(board):
                print(f"{Style.BRIGHT}{Fore.YELLOW}{SEP}\nTie!\n{SEP}")
                break

            to_move = 1 - to_move  # switch player

    except EOFError:
        sys.exit(f"{Style.BRIGHT}{Fore.CYAN}{BYE_MSG}")


def run_ai_game():
    # human vs AI mode
    try:
        print(f"{Style.BRIGHT}{Fore.MAGENTA}{SEP}\nYOU CHOSE TO PLAY AGAINST AI!\n{SEP}")
        name = input("Whats Your Name? ").strip()
        print(SEP)

        # Ask for AI difficulty (1–4)
        while True:
            try:
                level = int(input("What Level should your AI opponent be?\n(1-4): "))
                if level not in range(1, 5):
                    raise ValueError
                break
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.RED}{SEP}\nInvalid Level Input\n{SEP}")

        players = [Player(name, "O"), AI(level, "X")]
        print(
            f"{Style.BRIGHT}{Fore.MAGENTA}{SEP}\nYOU CHOSE AI LEVEL {level}: {players[1].name}\n{SEP}"
        )
        to_move = 1  # AI always starts
        board = new_board()

        while True:
            current_player = players[to_move]

            if current_player.name in AI_NAMES:
                # AI turn
                print(
                    f"{Style.BRIGHT}{Fore.MAGENTA}{SEP}\n{current_player.name}'s Turn!\n{SEP}"
                )
                row, col = get_ai_move(board, current_player.sign, level)
                board = make_move(board, current_player.sign, row, col)
            else:
                # Human turn
                print_board(board)
                print(f"{SEP}\nYour Turn!\n{SEP}")
                board = get_move(board, current_player.sign)

            won, _ = check_won(board)
            if won:
                print_board(board)
                if current_player.name in AI_NAMES:
                    print(
                        f"{Style.BRIGHT}{Fore.GREEN}{SEP}\n{current_player.name} won!\n{SEP}"
                    )
                else:
                    print(
                        f"{Style.BRIGHT}{Fore.GREEN}{SEP}\nCongrats {current_player.name}, you won!\n{SEP}"
                    )
                break
            if check_tie(board):
                print(f"{Style.BRIGHT}{Fore.YELLOW}{SEP}\nTie!\n{SEP}")
                break

            to_move = 1 - to_move  # Switch Players
    except EOFError:
        sys.exit(f"{Style.BRIGHT}{Fore.CYAN}{BYE_MSG}")


def new_board():
    # 3x3 board filled with #
    return [[EMPTY] * 3 for _ in range(3)]


def in_bounds(row, col):
    # Used to check if coordinates are on the board
    return 0 <= row < 3 and 0 <= col < 3


def print_board(b):
    # func to turn # into whitespace
    def conv(v):
        return " " if v == "#" else v

    print("    0   1   2")
    print("  ┌───┬───┬───┐")
    for r in range(3):
        c0, c1, c2 = conv(b[r][0]), conv(b[r][1]), conv(b[r][2])
        print(f"{r} │ {c0} │ {c1} │ {c2} │")
        if r != 2:
            print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘")


def move_isvalid(b, row, col):
    # check if inside board and cell is empty
    return in_bounds(row, col) and b[row][col] == EMPTY


def get_move(b, sign):
    # get a valid move from the user and register it
    while True:
        try:
            row = int(input("Row (0-2): "))
            col = int(input("Col (0-2): "))
        except ValueError:
            print(f"{Style.BRIGHT}{Fore.RED}{SEP}\nInvalid Move!\n{SEP}")
            continue

        if move_isvalid(b, row, col):
            b = make_move(b, sign, row, col)
            break

        print(f"{Style.BRIGHT}{Fore.RED}{SEP}\nInvalid Move!\n{SEP}")
    return b


def make_move(b, sign, row, col):
    # returns a new board with the given move applied
    new_b = [row[:] for row in b]
    new_b[row][col] = sign
    return new_b


def check_won(b):
    # checks all rows, cols and diagos for win
    lines = list()

    for row_i, row in enumerate(b):
        lines.append(row)  # rows
        lines.append([b[y][row_i] for y in range(3)])  # columns
    lines.append([b[i][i] for i in range(3)])          # main diagonal
    lines.append([b[i][2 - i] for i in range(3)])      # anti diagonal

    for line in lines:
        if line[0] != EMPTY and all(tile == line[0] for tile in line):
            return True, line[0]
    return False, None


def check_tie(b):
    # returns true if no empty cells remain
    for i in range(3):
        for j in range(3):
            if b[i][j] == EMPTY:
                return False
    return True


def get_ai_move(b, sign, level):
    # choose AI move by given difficulty level
    available = get_legal_moves(b)  # all availible moves
    winning = get_winning_moves(b, sign)      # moves to win
    not_losing = get_blocking_moves(b, sign)  # moves to stop opponent from winning

    if level == 1:
        # Random move
        row, col = random.choice(available)

    elif level == 2:
        # Take win if possible, else random
        if winning:
            row, col = winning[0]
        else:
            row, col = random.choice(available)

    elif level == 3:
        # Win > block > random
        if winning:
            row, col = winning[0]
        elif not_losing:
            row, col = not_losing[0]
        else:
            row, col = random.choice(available)

    elif level == 4:
        # Minimax with small opening tweak
        cache.clear()
        # try to force out mistake after perfect first 2 moves
        if b[0][0] == "X" and b[1][1] == "O" and b[2][2] == EMPTY:
            return 2, 2
        score, move = minimax(b, -1000, 1000, True)
        row, col = move
    return row, col


def get_legal_moves(b):
    # all empty cells as (row, col)
    available = list()
    for i in range(3):
        for j in range(3):
            if b[i][j] == EMPTY:
                available.append((i, j))
    return available


def get_winning_moves(b, sign):
    # moves that complete 3-in-a-row for given sign
    winning = list()
    for i, row in enumerate(b):
        # Check rows
        if row.count(EMPTY) == 1 and row.count(sign) == 2:
            for j in range(3):
                if b[i][j] == EMPTY:
                    winning.append((i, j))

        # Check columns
        col = [b[y][i] for y in range(3)]
        if col.count(EMPTY) == 1 and col.count(sign) == 2:
            for j in range(3):
                if b[j][i] == EMPTY:
                    winning.append((j, i))

    # Check diagonals
    diago1 = [b[i][i] for i in range(3)]
    if diago1.count(EMPTY) == 1 and diago1.count(sign) == 2:
        for i in range(3):
            if b[i][i] == EMPTY:
                winning.append((i, i))

    diago2 = [b[i][2-i] for i in range(3)]
    if diago2.count(EMPTY) == 1 and diago2.count(sign) == 2:
        for i in range(3):
            if b[i][2-i] == EMPTY:
                winning.append((i, 2-i))
    return winning


def get_blocking_moves(b, sign):
    # Moves that block opponent from winning next turn
    not_losing = list()
    for i, row in enumerate(b):
        # Check in rows
        if row.count(EMPTY) == 1 and row.count(sign) == 0:
            for j in range(3):
                if b[i][j] == EMPTY:
                    not_losing.append((i, j))

        # Check in columns
        col = [b[y][i] for y in range(3)]
        if col.count(EMPTY) == 1 and col.count(sign) == 0:
            for j in range(3):
                if b[j][i] == EMPTY:
                    not_losing.append((j, i))

    # Check in diagonals
    diago1 = [b[i][i] for i in range(3)]
    if diago1.count(EMPTY) == 1 and diago1.count(sign) == 0:
        for i in range(3):
            if b[i][i] == EMPTY:
                not_losing.append((i, i))

    diago2 = [b[i][2-i] for i in range(3)]
    if diago2.count(EMPTY) == 1 and diago2.count(sign) == 0:
        for i in range(3):
            if b[i][2-i] == EMPTY:
                not_losing.append((i, 2-i))
    return not_losing


def hash_board(b):
    # returns key for caching board states
    conversion = {"#": "12", "X": "34", "O": "01"}
    s = ""
    for row in b:
        for tile in row:
            s += conversion[tile]
    return s


# cache for minimax results = better performance
cache = {}


def minimax(b, alpha, beta, max_player):
    # check terminal states
    won, winner = check_won(b)
    if won:
        return (10, None) if winner == "X" else (-10, None)
    if check_tie(b):
        return 0, None

    # check cache
    board_cache_key = hash_board(b) + str(max_player)
    if board_cache_key in cache:
        return cache[board_cache_key]

    # get all moves
    moves = get_legal_moves(b)
    if max_player:
        # Maximize score for "X"
        best_score = -1000
        best_move = None
        for move in moves:
            row, col = move
            board_cp = make_move(b, "X", row, col)
            score, _ = minimax(board_cp, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha:
                alpha = score
            if beta <= alpha:
                break  # prune
        cache[board_cache_key] = (best_score, best_move)
        return best_score, best_move

    else:
        # Minimize score for "O"
        worst_score = 1000
        worst_move = None
        for move in moves:
            row, col = move
            board_cp = make_move(b, "O", row, col)
            score, _ = minimax(board_cp, alpha, beta, True)
            if score < worst_score:
                worst_score = score
                worst_move = move
            if score < beta:
                beta = score
            if beta <= alpha:
                break  # prune
        cache[board_cache_key] = (worst_score, worst_move)
        return worst_score, worst_move


if __name__ == "__main__":
    main()
