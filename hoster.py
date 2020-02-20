from flask import Flask, request
import os, json

GAME_CODE = 5000

class Game():
    def __init__(self):
        self.tiles = [[0 for i in range(7)] for i in range(6)]
        self.player_1_occupied = False
        self.player_2_occupied = False
        self.game_data = {"winner":None}
        self.on_turn = 1

    def player_move(self, player, column):
        for i in range(6):
            if self.tiles[5 - i][column] == 0:
                self.tiles[5 - i][column] = player
                print(self.tiles)
                return True
        return False

    def check_winner(self):
        pass

app = Flask('app')
app.secret_key = os.urandom(24)
game = Game()

@app.route('/get/', methods=["GET"])
def get_data():
    data = {
        "tiles":game.tiles,
        "game_data":game.game_data
    }
    return json.dumps(data)

@app.route('/user_move/', methods=["POST"])
def move():
    player = int(request.form['player'])
    if player == game.on_turn:
        column = int(request.form['column'])
        if game.player_move(player, column):
            return 'true'
        return 'false'
    return 'false' 

@app.route('/join/', methods=["POST"])
def player_joines():
    if game.player_1_occupied and game.player_2_occupied:
        return 'false'
    if not game.player_1_occupied:
        game.player_1_occupied = True
        player = 1
    elif not game.player_2_occupied:
        game.player_2_occupied = True
        player = 2
    return str(player)

def host_start():
    print("** HOSTING **")
    print(f"#> URL: ") #TODO GET URL
    print(f"#> GAME PORT: {GAME_CODE}")
    app.run(host="0.0.0.0", port=GAME_CODE, debug=True)

host_start()