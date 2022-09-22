# Connect Four (Four in a Row) game inspired by project #30 from
# the book 'The Big Book of Small Python Projects' by Al Sweigart

import sys

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

EMPTY_SYMBOL = chr(183)
EMPTY_CHAR = ' '
UP_DOWN_CHAR = chr(9474)
LEFT_RIGHT_CHAR = chr(9472)
DOWN_RIGHT_CHAR = chr(9484)
DOWN_LEFT_CHAR = chr(9488)
UP_RIGHT_CHAR = chr(9492)
UP_LEFT_CHAR = chr(9496)


class Player:
    symbols = []
    bext.clear()
    print('''Enter symbols for all available players.

The number of symbols entered determines the
maximum number of players that can play a game.

Symbols must be unique single characters,
and different to '{}'.

Press ENTER when done, or type QUIT to exit.\n'''.format(EMPTY_SYMBOL))

    while True:
        try:
            symbol = input('Symbol #{:,}: '.format(len(symbols) + 1))
            if symbol.upper() == 'QUIT':
                bext.clear()
                print('Thanks for playing!')
                sys.exit()
            elif symbol == '' and len(symbols) > 0:
                print('\nNumber of symbols registered: {:,}'.format(len(symbols)))
                print('Symbols registered: ' + ', '.join(symbols))
                input('\nPress ENTER to continue...')
                break
            elif len(symbol) != 1 or symbol == EMPTY_SYMBOL or symbol in symbols:
                print('Invalid symbol.')
            else:
                print('Symbol registered.')
                symbols.append(symbol)
                continue
        except KeyboardInterrupt:
            bext.clear()
            print('Thanks for playing!')
            sys.exit()

    available_players = len(symbols)
    symbol_index = 0

    def __init__(self):
        self.symbol = Player.symbols[Player.symbol_index]
        self.name = 'Player {}'.format(self.symbol)
        self.won = False
        Player.symbol_index += 1

    @classmethod
    def reset_index(cls):
        Player.symbol_index = 0


class ConnectFour:
    def __init__(self):
        bext.title('Connect Four')
        self.players = []
        self.board = {}
        self.board_is_full = False
        self.board_width = 7
        self.board_height = 6
        self.num_in_row = 4
        self.playing = True
        self.initialise_game()
        self.winner = None

    def initialise_game(self):
        bext.clear()
        bext.goto(0, 0)
        num_players = self.get_num_players()
        for i in range(num_players):
            self.players.append(Player())
        self.board_width = self.get_board_width()
        self.board_height = self.get_board_height()
        self.num_in_row = self.get_num_in_row()

    def get_num_players(self):
        while True:
            try:
                num_players = input('Number of players (1-{}), or (Q)UIT: '.format(Player.available_players))
                if num_players.upper().startswith('Q'):
                    self.stop_playing(clear=True)
                else:
                    num_players = int(num_players)
            except KeyboardInterrupt:
                self.stop_playing(clear=True)
            except ValueError:
                print('Invalid input.')
            else:
                if 1 <= num_players <= Player.available_players:
                    break
                else:
                    print('Invalid number.')
        return num_players

    def get_board_width(self):
        while True:
            try:
                board_width = input('Board width (1-9), or (Q)UIT: ')
                if board_width.upper().startswith('Q'):
                    self.stop_playing(clear=True)
                else:
                    board_width = int(board_width)
            except KeyboardInterrupt:
                self.stop_playing(clear=True)
            except ValueError:
                print('Invalid input.')
            else:
                if 1 <= board_width <= 9:
                    break
                else:
                    print('Invalid number.')
        return board_width

    def get_board_height(self):
        while True:
            try:
                board_height = input('Board height (1-9), or (Q)UIT: ')
                if board_height.upper().startswith('Q'):
                    self.stop_playing(clear=True)
                else:
                    board_height = int(board_height)
            except KeyboardInterrupt:
                self.stop_playing(clear=True)
            except ValueError:
                print('Invalid input.')
            else:
                if 1 <= board_height <= 9:
                    break
                else:
                    print('Invalid number.')
        return board_height

    def get_num_in_row(self):
        while True:
            try:
                num_in_row = input('Number to get in a row (1-9), or (Q)UIT: ')
                if num_in_row.upper().startswith('Q'):
                    self.stop_playing(clear=True)
                else:
                    num_in_row = int(num_in_row)
            except KeyboardInterrupt:
                self.stop_playing(clear=True)
            except ValueError:
                print('Invalid input.')
            else:
                if 1 <= num_in_row <= 9:
                    break
                else:
                    print('Invalid number.')
        return num_in_row

    def create_board(self):
        bext.clear()
        for y in range(0, self.board_height + 3):
            for x in range(0, self.board_width + 3):
                char = EMPTY_SYMBOL
                if y == 0:
                    if 2 <= x <= self.board_width + 1:
                        char = str(x - 1)
                    else:
                        char = EMPTY_CHAR
                elif x == 0:
                    if 2 <= y <= self.board_height + 1:
                        char = str(y - 1)
                    else:
                        char = EMPTY_CHAR
                elif y in [1, self.board_height + 2]:
                    if x in [1, self.board_width + 2]:
                        if (x, y) == (1, 1):
                            char = DOWN_RIGHT_CHAR
                        elif (x, y) == (1, self.board_height + 2):
                            char = UP_RIGHT_CHAR
                        elif (x, y) == (self.board_width + 2, 1):
                            char = DOWN_LEFT_CHAR
                        elif (x, y) == (self.board_width + 2, self.board_height + 2):
                            char = UP_LEFT_CHAR
                    else:
                        char = LEFT_RIGHT_CHAR
                elif 2 <= y <= self.board_height + 1:
                    if x in [1, self.board_width + 2]:
                        char = UP_DOWN_CHAR
                self.board[(x, y)] = char

    def display_board(self, move=None):
        bext.goto(0, 2)
        for y in range(0, self.board_height + 3):
            for x in range(0, self.board_width + 3):
                if move:
                    if (x, y) in move:
                        bext.fg('red')
                    else:
                        bext.fg('reset')
                print(self.board[(x, y)], sep='', end='')
            print()
        print()

    def display_message(self, msg, line=0):
        bext.goto(0, line)
        print(msg)

    def check_for_full_board(self):
        for y in range(2, self.board_height + 2):
            for x in range(2, self.board_width + 2):
                if self.board[(x, y)] == EMPTY_SYMBOL:
                    self.board_is_full = False
                    return
        self.board_is_full = True

    def move_is_valid(self, col, row):
        if self.board[(col, row)] == EMPTY_SYMBOL:
            return True
        return False

    def attempt_move(self, player, col):
        if not self.board_is_full:
            row = self.board_height + 1
            while not self.move_is_valid(col, row):
                row -= 1
                if row == 0:
                    return False, 'Invalid move; enter a different column.', None
            self.board[(col, row)] = player.symbol
            self.check_for_full_board()
            winning_move = self.check_for_winner()
            bext.goto(0, 0)
            if self.winner:
                move = winning_move
            else:
                move = [(col, row)]
            return True, '{} placed at col: {}, row: {}.'.format(player.symbol, col - 1, row - 1), move
        else:
            return False, 'Board is full.', None

    def get_move(self, player):
        while True:
            try:
                col = input('{}, enter a column, or (Q)UIT: '.format(player.name))
                if col.upper().startswith('Q'):
                    self.stop_playing()
                else:
                    col = int(col) + 1
            except ValueError:
                print('Invalid input.')
            else:
                if 2 <= col <= self.board_width + 1:
                    break
                else:
                    print('Invalid column.')
        bext.clear()
        return col

    def execute_move(self, player):
        col = self.get_move(player)
        success, msg, move = self.attempt_move(player, col)
        while not success:
            self.display_board()
            self.display_message(msg, self.board_height + 5)
            col = self.get_move(player)
            success, msg, move = self.attempt_move(player, col)
        self.display_message(msg)
        return move

    def check_for_winner(self):
        if self.board_width >= self.num_in_row or self.board_height >= self.num_in_row:
            for y in range(2, self.board_height + 2):
                for x in range(2, self.board_width + 3 - self.num_in_row):
                    try:
                        chars = set()
                        positions = []
                        for i in range(0, self.num_in_row):
                            chars.add(self.board[(x + i, y)])
                            positions.append((x + i, y))
                    except KeyError:
                        continue
                    else:
                        if len(chars) == 1 and chars != {EMPTY_SYMBOL}:
                            self.assign_winner(chars)
                            return positions
            for x in range(2, self.board_width + 2):
                for y in range(2, self.board_height + 3 - self.num_in_row):
                    try:
                        chars = set()
                        positions = []
                        for i in range(0, self.num_in_row):
                            chars.add(self.board[(x, y + i)])
                            positions.append((x, y + i))
                    except KeyError:
                        continue
                    else:
                        if len(chars) == 1 and chars != {EMPTY_SYMBOL}:
                            self.assign_winner(chars)
                            return positions
            for y in range(2, self.board_height + 2):
                for x in range(2, self.board_width + 1):
                    try:
                        chars = set()
                        positions = []
                        for i in range(0, self.num_in_row):
                            chars.add(self.board[(x + i, y + i)])
                            positions.append((x + i, y + i))
                    except KeyError:
                        continue
                    else:
                        if len(chars) == 1 and chars != {EMPTY_SYMBOL}:
                            self.assign_winner(chars)
                            return positions
            for y in range(2, self.board_height + 2):
                for x in range(self.board_width + 2, 1, -1):
                    try:
                        chars = set()
                        positions = []
                        for i in range(0, self.num_in_row):
                            chars.add(self.board[(x - i, y + i)])
                            positions.append((x - i, y + i))
                    except KeyError:
                        continue
                    else:
                        if len(chars) == 1 and chars != {EMPTY_SYMBOL}:
                            self.assign_winner(chars)
                            return positions

    def assign_winner(self, symbols):
        for player in self.players:
            if player.symbol in symbols:
                player.won = True
                self.winner = player.symbol

    def cycle_through_players(self):
        while True:
            for player in self.players:
                move = self.execute_move(player)
                self.display_board(move)
                if self.board_is_full or player.won:
                    return

    def resolve_game(self):
        if self.board_is_full:
            self.display_message('Board is full. Game ends in a draw.', self.board_height + 5)
        else:
            self.display_message('Player {} wins!'.format(self.winner), self.board_height + 5)

    def decide_to_continue(self):
        bext.goto(0, self.board_height + 7)
        response = input('Press Y to continue playing, or any other key to exit...\n').upper()
        if response.startswith('Y'):
            self.reset_game()
            self.initialise_game()
        else:
            self.stop_playing()

    def stop_playing(self, clear=False):
        if clear:
            bext.clear()
            line = 0
        else:
            line = self.board_height + 9
        self.playing = False
        self.display_message('Thanks for playing!', line)
        sys.exit()

    def reset_game(self):
        bext.clear()
        Player.reset_index()
        self.players = []
        self.board = {}
        self.board_is_full = False
        self.winner = None
        self.playing = True

    def play(self):
        try:
            while self.playing:
                self.create_board()
                self.display_board()
                self.cycle_through_players()
                self.resolve_game()
                self.decide_to_continue()
        except KeyboardInterrupt:
            self.stop_playing()


g = ConnectFour()
g.play()
