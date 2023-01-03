#using enum to represent the different colored stones

import enum
from collections import namedtuple

class Player(enum.Enum):
    black = 1  
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


#to represent coordinates on the board, we use tuples
#'namedtuple is a useful tool for defining simple classes 
# when you don't need to add any additional behavior beyond 
# storing and accessing the attributes of the class.'

class Point(namedtuple('Point','row col')):
    def neighbors(self):
        return[
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]


    