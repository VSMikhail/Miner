from random import randint
import string


class MinerGame:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.alphabet = string.ascii_uppercase

    def create_field(self):
        mines_cells = set()
        empty_cells = {}
        while len(mines_cells) < self.mines:
            mines_cells.add(str(randint(1, self.height)) + self.alphabet[randint(0, self.width - 1)])
        for line in range(1, self.height + 1):
            for row in self.alphabet[0:self.width]:
                cell = str(line) + row
                if cell in mines_cells:
                    pass
                else:
                    empty_cells[cell] = len(self.round_check(self.translate_cell(cell), mines_cells)[0])

        return mines_cells, empty_cells

    def translate_cell(self, cell):
        return [int(cell[:-1]), self.alphabet.index(cell[-1].upper())]

    def retranslate_cell(self, cell):
        return f'{cell[:-1]}{self.alphabet[-1]}'

    def print_field(self, empty, found_mines, marks):
        print(''.join(' ' + letter + ' ' for letter in self.alphabet[0:self.width]))
        for line in range(1, self.height + 1):
            for row in self.alphabet[0:self.width]:
                if str(line) + row in found_mines:
                    print(' 💣', end='')
                elif str(line) + row in empty:
                    print(f' {empty[str(line) + row]} ', end='')
                elif str(line) + row in marks:
                    print(' 🚩', end='')
                else:
                    print(' 🌱', end='')
            print(f' {line}')

    def check_mine(self, cell, mines):
        if cell in mines:
            return None
        else:
            return cell

    def round_check(self, cell, mines):
        mine_cells = set()
        empty_cells = set()
        for line in range(cell[0] - 1, cell[0] + 2):
            for row in range(cell[1] - 1, cell[1] + 2):
                if row < len(self.alphabet):
                    if str(line) + self.alphabet[row] in mines:
                        mine_cells.add(str(line) + self.alphabet[row])
                    else:
                        empty_cells.add(str(line) + self.alphabet[row])
        return [mine_cells, empty_cells]


new_game = MinerGame(4, 4, 1)
field = new_game.create_field()
opened_mines_cells = set()
opened_empty_cells = {}
marks = set()
new_game.print_field(opened_empty_cells, opened_mines_cells, marks)
while not opened_mines_cells and marks != field[0]:
    cur_hit = input('Поставить флаг - x \nСтреляй! ').upper()
    if cur_hit in field[1].keys():
        opened_empty_cells[cur_hit] = field[1][cur_hit]
        for _ in new_game.round_check(new_game.translate_cell(cur_hit), field[0])[1]:
            opened_empty_cells[_] = field[1].get(_)
    elif cur_hit == 'X':
        mark = input('На какую клетку? ').upper()
        marks.add(mark)
    else:
        opened_mines_cells.add(cur_hit)
    new_game.print_field(opened_empty_cells, opened_mines_cells, marks)
if marks == field[0]:
    print('Победа!')
else:
    print('Проиграл!')
