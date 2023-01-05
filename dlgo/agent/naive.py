import random
from flask import Flask,render_template,jsonify,request
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import GameState, Move
from dlgo.gotypes import Point
import json

app = Flask(__name__)

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

@app.route('/make_move',methods = ['POST'])

def make_move():
    game_state = GameState.from_json(request.json)
    move = bot.select_move(game_state)
    return json.dumps(move.to_json())

if __name__ == '__main__':
    app.run()