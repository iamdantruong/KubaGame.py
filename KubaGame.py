#Dan Truong
#Date:
#Description:

from copy import deepcopy
class KubaGame:
    def __init__(self,playerA_tuple, playerB_tuple):
        self._matrix= [ ['W','W','X','X','X','B','B'],
                        ['W','W','X','R','X','B','B'],
                        ['X','X','R','R','R','X','X'],
                        ['X','R','R','R','R','R','X'],
                        ['X','X','R','R','R','X','X'],
                        ['B','B','X','R','X','W','W'],
                        ['B','B','X','X','X','W','W']  ]
        self._last_matrix = None
        self._player_turn = None
        self._winner = None
        self._players = {playerA_tuple[0]: Player(playerA_tuple[0], playerA_tuple[1], playerB_tuple[0]),
                         playerB_tuple[0]: Player(playerB_tuple[0], playerB_tuple[1], playerA_tuple[0])}

    def get_current_turn(self):
        return self._player_turn

    def set_current_turn(self, playername):
        self._player_turn = playername

    def get_winner(self):
        return self._winner

    def set_winner(self, winner):
        self._winner = winner

    def get_matrix(self):
        return self._matrix

    def print_matrix(self):
        for num in range (0,7):
            print(self.get_matrix()[num])

    def set_matrix(self,move):
        self._matrix= move

    def get_last_matrix(self):
        return self._last_matrix

    def set_last_matrix(self, last):
        self._last_matrix= last

    def get_player(self, playername):
        return self._players[playername]

    def get_captured(self, player):
        return self.get_player(player).get_captured()

    def get_marble(self, coordinates):
        row = coordinates[0]
        column = coordinates[1]
        matrix = self.get_matrix()
        return matrix[row][column]

    def get_marble_count(self):
        matrix= self.get_matrix()
        white= 0
        black= 0
        red = 0
        for num in range(0,7):
            for index in range (0,7):
                if matrix[num][index]== 'R':
                    red+=1
                if matrix[num][index]== 'W':
                    white+=1
                if matrix[num][index]== 'B':
                    black+=1
        return (white, black, red)

    def make_move(self, playername, coordinates, direction):
        if self.check_move_legality(playername, coordinates, direction) is True:
            self.set_last_matrix(deepcopy(self.get_matrix()))
            self.set_matrix(self.make_move_helper(playername, coordinates, direction, self.get_matrix()))
            self.set_current_turn(self.get_player(playername).get_next_player())

            if self.check_win(playername) is True:
                self.set_winner(playername)
            return True
        else:
            return self.check_move_legality(playername, coordinates, direction)

    def check_win(self, playername):
        opponent = self.get_player(playername).get_next_player()
        opposing_color= self.get_player(opponent).get_color()
        matrix=self.get_matrix()
        color_count=0

        if self.get_player(playername).get_captured()==7:
            return True
        for num in range(0,7):
            for index in range(0,7):
                if matrix[num][index]==opposing_color:
                    color_count+=1
        if color_count==0:
            return True
        else:
            return False

    def make_move_helper(self, playername, coordinates, direction, matrix):
        """Helper function to make_move and updates the board. Assumes that the move is already legal.
        Takes coordinates, direction, and matrix as a parameter. Returns updated matrix."""
        row = coordinates[0]
        column = coordinates[1]
        index_list= []
        index = coordinates[1]
        column_list = []

        if direction == 'L':
            for num in range(0, index):
                if matrix[row][num] == 'X':
                    index_list.append(num)
            if len(index_list)!=0:
                matrix[row].pop(index_list[-1])
            matrix[row].insert(column+1,'X')          #inserts at position
            if len(matrix[row])==8:             #if no blank space, then position 7 is a marble and taken off board
                if matrix[row][0] =='R':
                    self.get_player(playername).capture()   #increments score by 1
                matrix[row].pop(0)

        if direction == 'R':
            for num in range(index, 7):
                if matrix[row][num] == 'X':
                    index_list.append(num)
            if len(index_list)!= 0:
                matrix[row].pop(index_list[0])
            matrix[row].insert(column,'X')
            if len(matrix[row]) == 8:
                if matrix[row][7] == 'R':
                    self.get_player(playername).capture()
                matrix[row].pop(7)

        if direction == 'B':
            for num in range(0,7):
                column_list.append(matrix[num][column])

            for num in range(row, len(column_list)):
                if column_list[num]== 'X':
                    index_list.append(num)

            if len(index_list) != 0:
                column_list.pop(index_list[0])

            column_list.insert(row,'X')

            if len(column_list) == 8:
                if column_list[-1]=='R':
                    self.get_player(playername).capture()
                column_list.pop(-1)

            for num in range (0,7):
                matrix[num][column] = column_list[num]

        if direction =='F':
            column_list = []
            for num in range(0, 7):
                column_list.append(matrix[num][column])

            for num in range(0, row):
                if column_list[num] == 'X':
                    index_list.append(num)

            if len(index_list) != 0:
                column_list.pop(index_list[-1])

            column_list.insert(row+1,'X')

            if len(column_list)==8:
                if column_list[0] == 'R':
                    self.get_player(playername).capture()
                column_list.pop(0)

            for num in range(0,7):
                matrix[num][column]= column_list[num]

        return matrix

    def check_move_legality(self, playername, coordinates, direction):
        if self.check_player_turn(playername) is not True:
            return self.check_player_turn(playername)

        if self.check_coordinates(playername, coordinates) is not True:
            return self.check_coordinates(playername, coordinates)

        if self.check_direction(coordinates, direction) is not True:
            return self.check_direction(coordinates, direction)

        old_matrix = self.get_last_matrix()
        temp = deepcopy(self.get_matrix())
        new_matrix= self.make_move_helper(playername, coordinates, direction, temp)
        if new_matrix==old_matrix:
            return False

        else:
            return True

    def check_player_turn(self, playername):
        if self.get_current_turn() == playername or self.get_current_turn() is None:
            return True
        else:
            return False

    def check_coordinates(self, playername, coordinates):
        if self.get_marble(coordinates) == self.get_player(playername).get_color():
            return True
        else:
            return False

    def check_direction(self, coordinates, direction):
        row = coordinates[0]
        column = coordinates[1]
        matrix = self.get_matrix()

        if direction == 'L':
            if column+1 == len(matrix[column]):
                return True
            elif matrix[row][column+1] == 'X':
                return True
            else:
                return False

        if direction == 'R':
            if column-1 < 0:
                return True
            elif matrix[row][column-1] == 'X':
                return True
            else:
                return False

        if direction == 'F':
            if row+1 == len(matrix[row]):
                return True
            elif matrix[row+1][column] == 'X':
                return True
            else:
                return False

        if direction == 'B':
            if row-1 < 0:
                return True
            elif matrix[row-1][column] == 'X':
                return True
            else:
                return False

class Player:
    def __init__(self, player, color, next_player):
        self._player_name= player
        self._player_color= color
        self._captured = 0
        self._next_player= next_player

    def get_color(self):
        return self._player_color

    def get_next_player(self):
        return self._next_player

    def get_captured(self):
        return self._captured

    def capture(self):
        self._captured+=1

def main():
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print("marble count: ", game.get_marble_count())
    print(game.get_captured('PlayerA'))
    print(game.make_move('PlayerA', (6, 5) , 'F'))
    print(game.make_move('PlayerB', (0,5), 'B'))
    print(game.make_move('PlayerA', (5, 5), 'F'))
    game.print_matrix()
    print(game.make_move('PlayerB', (0, 6), 'B'))
    game.make_move('PlayerA',(4,5),'F')
    game.make_move('PlayerB', (1, 6), 'B')
    print("marble count: ", game.get_marble_count())
    game.make_move('PlayerA', (3, 5), 'F')
    print(game.get_player('PlayerA').get_captured())
    game.print_matrix()
    print("marble count: ", game.get_marble_count())
    game.make_move('PlayerB',(2,6),'L')
    game.print_matrix()
    game.make_move('PlayerA',(1,0),'R')
    print('space')
    print(game.make_move('PlayerB',(5,0),'R'))
    game.print_matrix()
    print(game.get_player('PlayerA').get_captured())




if __name__== '__main__':
    main()