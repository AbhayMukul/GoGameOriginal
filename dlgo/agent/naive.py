import random
from flask import Flask,render_template,request,jsonify,json
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move,Board
from dlgo.goboard_slow import GameState
from dlgo.gotypes import Point,Player
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Creating a Random Bot
class RandomBot(Agent):

    def select_move(self, game_state):

        """Choose a random valid move that preserves our own eyes i.e. empty points."""

        candidates = []

        for r in range(1,game_state.board.num_rows + 1):

            for c in range(1, game_state.board.num_cols + 1):

                candidate = Point(row=r,col=c)

                if game_state.is_valid_move(Move.play(candidate)) and \
                    not is_point_an_eye(game_state.board,candidate,game_state.next_player):

                    candidates.append(candidate)
        
        if not candidates:
            return Move.pass_turn()

        return Move.play(random.choice(candidates))

#Defining the route for the UI

@app.route('/')
def index():
    return render_template('GUI.html')

# Define a route to handle requests from the UI to make a move
bot = RandomBot()
current_board = Board(num_rows= 9,num_cols= 9)
current_player = Player.black

@app.route('/make_move',methods = ['POST','GET'])
def make_move():

    game_state = GameState(board=current_board, next_player=current_player,previous=None,move=None)
    move = bot.select_move(game_state)
    game_state = game_state.apply_move(move)
    return jsonify(move.__dict__)

if __name__ == '__main__':
    app.run(debug=True)