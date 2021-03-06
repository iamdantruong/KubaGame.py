#Dan Truong
#Date: 5/29/21
#Description: This code will describe classes for 

from copy import deepcopy

class KubaGame:
    """This class describes Kuba and will include methods for initializing and updating game matrix, handle player turns,
    check move legality, and check win condition."""
    def __init__(self,playerA_tuple, playerB_tuple):
        """Initializes game matrix. Sets the last matrix, player turn, winner to none. Sets up the players in a dictionary
        where the key is the player name and the value is a Player object."""
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
        """Returns whose turn it is. Is None on first turn"""
        return self._player_turn

    def set_current_turn(self, playerName):
        """Sets current turn to next player. Used in make_move to update turn."""
        self._player_turn = playerName

    def get_winner(self):
        """Returns the winner of the game."""
        return self._winner

    def set_winner(self, winner):
        """Sets the winner of the game. Used in check_win method."""
        self._winner = winner

    def get_matrix(self):
        """Returns the game matrix."""
        return self._matrix

    def print_matrix(self):
        """Prints the matrix in a more readable format."""
        for num in range (0,7):
            print(self.get_matrix()[num])

    def set_matrix(self,move):
        """Updates the game matrix. Used in make_move."""
        self._matrix= move

    def get_last_matrix(self):
        """Returns the last matrix. Used to check move legality. """
        return self._last_matrix

    def set_last_matrix(self, last):
        """Sets the last matrix. Used in make_move."""
        self._last_matrix= last

    def get_player(self, playerName):
        """Takes player name as parameter and returns the Player object."""
        return self._players[playerName]

    def get_captured(self, playerName):
        """Returns the number of red marbles the Player has captured."""
        return self.get_player(playerName).get_captured()

    def get_marble(self, coordinates):
        """Returns what is in a certain coordinate (marble/blank space)."""
        row = coordinates[0]
        column = coordinates[1]
        matrix = self.get_matrix()
        return matrix[row][column]

    def get_marble_count(self):
        """Counts each color of marble from the board."""
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

    def make_move(self, playerName, coordinates, direction):
        """If the proposed move is legal, updates the last and next matrix, changes the current turn,
         then checks for win condition. Valid moves return True. Returns False if move is not legal.
         Requires helper functions: check_move_legality and check_win."""
        if self.check_move_legality(playerName, coordinates, direction) is True and self.get_winner() is None:
            self.set_last_matrix(deepcopy(self.get_matrix()))
            self.set_matrix(self.make_move_helper(playerName, coordinates, direction, self.get_matrix(), True))
            self.set_current_turn(self.get_player(playerName).get_next_player())

            if self.check_win(playerName) is True:
                self.set_winner(playerName)
            return True
        else:
            return False

    def check_win(self, playerName):
        """Returns True for the following win conditions:
        1. player's red orbs = 7
        2. opposing player has 0 orbs
        3. opposing player has 0 legal moves
        Returns False otherwise. Takes playerName as parameter.
        """
        opponent = self.get_player(playerName).get_next_player()
        opposing_color= self.get_player(opponent).get_color()
        opponent_coordinates = []
        move_list=[]
        matrix=self.get_matrix()

        if self.get_player(playerName).get_captured()==7:
            return True

        for num1 in range (0,7):
            for num2 in range (0,7):
                if matrix[num1][num2]== opposing_color:
                    opponent_coordinates.append((num1,num2))

        if len(opponent_coordinates)== 0:
            return True

        for num in range (0, len(opponent_coordinates)):
            move_list.append(self.check_direction(opponent_coordinates[num], 'L'))
            move_list.append(self.check_direction(opponent_coordinates[num], 'R'))
            move_list.append(self.check_direction(opponent_coordinates[num], 'B'))
            move_list.append(self.check_direction(opponent_coordinates[num], 'F'))
        if True not in move_list:
            return True

        else:
            return False

    def make_move_helper(self, playerName, coordinates, direction, matrix, scoring):
        """Helper method to make_move and updates the board. Assumes that the move is already legal.
        Parameters: playerName, coordinates, direction, matrix, scoring. This helper method is used
        to test move legality so scoring is a boolean T/F and only updates score in situations
        when the move is actually made.
        Returns updated matrix. """
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
                if matrix[row][0] =='R' and scoring == True:
                    self.get_player(playerName).capture()   #increments score by 1
                matrix[row].pop(0)

        if direction == 'R':
            for num in range(index, 7):
                if matrix[row][num] == 'X':
                    index_list.append(num)
            if len(index_list)!= 0:
                matrix[row].pop(index_list[0])
            matrix[row].insert(column,'X')
            if len(matrix[row]) == 8:
                if matrix[row][7] == 'R' and scoring == True:
                    self.get_player(playerName).capture()
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
                if column_list[-1]=='R' and scoring == True:
                    self.get_player(playerName).capture()
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
                if column_list[0] == 'R' and scoring == True:
                    self.get_player(playerName).capture()
                column_list.pop(0)

            for num in range(0,7):
                matrix[num][column]= column_list[num]

        return matrix

    def check_move_legality(self, playerName, coordinates, direction):
        """Checks move legality. Passes arguments to helper methods to check if a move is legal.
        1. It must be that player's turn to play. (check_player_turn)
        2. Player must move their own marble. (check_coordinates)
        3. The space preceding the marble must be open/ outside matrix. (check_direction)
        4. The new move must not undo opponent's last move.
        Returns True for legal moves and False otherwise.
        Parameters: playerName, coordinates, and direction."""
        if self.check_player_turn(playerName) is not True:
            return self.check_player_turn(playerName)

        if self.check_coordinates(playerName, coordinates) is not True:
            return self.check_coordinates(playerName, coordinates)

        if self.check_direction(coordinates, direction) is not True:
            return self.check_direction(coordinates, direction)

        old_matrix = self.get_last_matrix()
        temp = deepcopy(self.get_matrix())
        new_matrix= self.make_move_helper(playerName, coordinates, direction, temp, False)
        if new_matrix==old_matrix:
            return False

        else:
            return True

    def check_player_turn(self, playerName):
        """Returns True if it is that player's turn and False otherwise.
        Parameter: playerName"""
        if self.get_current_turn() == playerName or self.get_current_turn() is None:
            return True
        else:
            return False

    def check_coordinates(self, playerName, coordinates):
        """Returns True if that player is trying to move their own marble and False otherwise.
        Parameters: playerName, coordinates"""
        if self.get_marble(coordinates) == self.get_player(playerName).get_color():
            return True
        else:
            return False

    def check_direction(self, coordinates, direction):
        """Returns True if the marble the player is moving can be moved in that direction and False otherwise.
        Parameters: coordinates, direction. Used in check_move_legality/check_win"""
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
    """Player class to be used with KubaGame class. Has attributes player name, color, number of red orbs captured,
    and links the opponent to the Player. """
    def __init__(self, player, color, next_player):
        """Sets player name, color, captured orbs to 0, and sets the player's opponent."""
        self._player_name= player
        self._player_color= color
        self._captured = 0
        self._next_player= next_player

    def get_color(self):
        """Returns player's color."""
        return self._player_color

    def get_next_player(self):
        """Returns player's opponent. Used to swap turns and check win conditions."""
        return self._next_player

    def get_captured(self):
        """Returns number of red marbles captured."""
        return self._captured

    def capture(self):
        """Adds 1 to number of red marbles captured. This method is used in
        make_move when a red orb has been captured."""
        self._captured+=1

def main():
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print("marble count: ", game.get_marble_count())
    print(game.get_captured('PlayerA'))


if __name__== '__main__':
    main()