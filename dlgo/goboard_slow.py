import copy
from typing import Optional
from dlgo.gotypes import Player
from dlgo import gotypes

class Move():

    def _init_(self,point=None, is_pass=False,is_resign=False):

        #The assert statement at the beginning of the method 
        # checks that exactly one of the three arguments is not None or False.
        # This is done using the ^ operator, which is the bitwise XOR operator 
        # in Python. It returns True if exactly one of the operands is True, 
        # and False otherwise.

        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play =  (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign


    @classmethod
    def play(cls,point):
        return Move(point = point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass = True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign = True)

    def to_json(self):
        if self.is_pass:
            return Move(is_pass = True)
        
        elif self.is_resign:
            return Move(is_resign = True)

        else:
            return {'point': (self.point.row, self.point.col)}


#Tracking connected groups of stones: Strings

class GoString():

    def __init__(self,color,stones,liberties):
        self.color = color
        self.stones = stones
        self.liberties = liberties

    def remove_liberty(self,point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self,go_string):
        assert go_string.color == self.color

        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    #accessing the number of liberties at any point
    @property
    def num_liberties(self):
        return(len(self.liberties))

    def _eq__(self, other):
        return isinstance(other,GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


#Placing and capturin stones on the Go board
       
class Board():

    def __init__(self, num_rows,num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        
        #using _grid to keep track of the board state internally
        #which is a dictionary used to store strings of stones
        self._grid = {}

        #placing the stones
        def place_stone(self,player,point):

            assert self.is_on_grid(point)
            assert self._grid.get(point) is None
            adjacent_same_color = []
            adjacent_opposite_color = []
            liberties = []

            for neighbor in point.neighbors():
                if not self.is_on_grid(neighbor):
                    continue
                neighbor_string = self._grid.get(neighbor)

                if neighbor_string is None:
                    liberties.append(neighbor)

                elif neighbor_string.color == player:
                    if neighbor_string not in adjacent_same_color:
                        adjacent_same_color.append(neighbor_string)
                
                else:
                    if neighbor_string not in adjacent_opposite_color:
                        adjacent_opposite_color.append(neighbor_string)

            new_string = GoString(player,[point],liberties)

            #Merge any adjacent strings of the same color

            for same_color_string in adjacent_same_color:
                new_string = new_string.merged_with(same_color_string)


            for new_string_point in new_string.stones:
                self._grid[new_string_point] = new_string
            

            #Reduce liberties of any adjacent strings of the opposite color

            for other_color_string in adjacent_opposite_color:
                other_color_string.remove_liberty(point)


            # If any opposite-color strings now have zero liberties, remove them

            for other_color_string in adjacent_opposite_color:
                if other_color_string.num_liberties == 0:
                    self._remove_string(other_color_string)



        def is_on_grid(self, point):
            return 1 <= point.row <= self.num_rows and \
                1 <= point.col <= self.num_cols


        #Returns the content of a point on the board: a Player 
        # if a stone is on that point, or else None

        def get(self, point: gotypes.Point) -> Optional[str]:
            string = self._grid.get(point)
            if string is None:
                return None
            return string.color


        #Returns the entire string of stones at a point:
        # a GoString if a stone is on that point, or else None
        # to prevent self capture

        def get_go_string(self, point):
            string = self._grid.get(point)
            if string is None:
                return None
            return string       


        # Removing string of stones

        def remove_string(self, string):
            
            for point in string.stones:

                for neighbor in point.neighbors():

                    neighbor_string = self._grid.get(neighbor)

                    if neighbor_string is None:
                        continue

                    if neighbor_string is not string:
                        neighbor_string.add_liberty(point)

                self._grid[point] = None



# Capturing game state and checking for illegal moves

class GameState():
    
    def __init__(self,board, next_player, previous, move):

        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move
    

    def apply_move(self,move):

        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return cls(board, Player.black, None, None)

    
    # Deciding when a game of Go is over

    def is_over(self):
        
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def __str__(self):
        return f'Next Player: {self.next_player}\nBoard:\n{self.board}'
        
    # Checking for Illegal Moves: Self-Capture, Ko

    # Checking if the move is Self-Capture or not

    def is_move_self_capture(self,player,move):

        if not move.is_play:
            return False
        
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)

        return new_string.num_liberties == 0


    #Checking if current game state violates the KO rule
    
    @property
    def situation(self):
        return (self.next_player,self.board)


    def does_move_violate_ko(self,player,move):

        if not move.is_play:
            return False
        
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)

        past_state = self.previous_state

        while past_state is not None:

            if past_state.situation == next_situation:
                return True

            past_state = past_state.previous_state
        return False

    
    # Checking if the valid move or not

    def is_valid_move(self,move):

        if self.is_over():
            return False
        
        if move.is_pass or move.is_resign:
            return True

        return(
            self.board.get(move.point) is None and 
            not self.is_move_self_capture(self.next_player, move) and 
            not self.does_move_violate_ko(self.next_player, move)
        )


        