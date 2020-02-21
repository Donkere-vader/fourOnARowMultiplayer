from flask import Flask, request
import os, json, socket

GAME_CODE = int(input('Game port: '))

class Game():
    def __init__(self):
        self.tiles = [[0 for i in range(7)] for i in range(6)]
        self.player_1_occupied = False
        self.player_2_occupied = False
        self.winner = None
        self.on_turn = 1

    def reset(self):
        self.tiles = [[0 for i in range(7)] for i in range(6)]
        self.winner = None
        print('reset')

    def player_move(self, player, column):
        for i in range(6):
            if self.tiles[5 - i][column] == 0:
                self.tiles[5 - i][column] = player
                self.on_turn = 2 if self.on_turn == 1 else 1
                return True
        return False

    def check_winner(self):
        winner = False
        for player in [1, 2]:
            for y in range(len(self.tiles)):
                for x in range(len(self.tiles[0])-3):
                    if self.tiles[y][x] == player and self.tiles[y][x+1] == player and self.tiles[y][x+2] == player and self.tiles[y][x+3] == player:
                        winner = player
            
            for x in range(len(self.tiles[0])):
                for y in range(len(self.tiles)-3):
                    if self.tiles[y][x] == player and self.tiles[y+1][x] == player and self.tiles[y+2][x] == player and self.tiles[y+3][x] == player:
                        winner = player

            for y in range(len(self.tiles)-3):
                for x in range(len(self.tiles[0])-3):
                    if self.tiles[y][x] == player and self.tiles[y+1][x+1] == player and self.tiles[y+2][x+2] == player and self.tiles[y+3][x+3] == player:
                        winner = player
            
            for y in range(len(self.tiles)-3):
                for x in range(3, len(self.tiles[0])):
                    if self.tiles[y][x] == player and self.tiles[y+1][x-1] == player and self.tiles[y+2][x-2] == player and self.tiles[y+3][x-3] == player:
                        winner = player

        if winner:
            self.winner = winner

app = Flask('app')
app.secret_key = os.urandom(24)
game = Game()

@app.route('/get/', methods=["GET"])
def get_data():
    data = {
        "tiles":game.tiles,
        "game_data":{
            "winner":game.winner,
            "on_turn":game.on_turn
        }
    }
    return json.dumps(data)

@app.route('/user_move/', methods=["POST"])
def move():
    if game.winner:
        game.reset()
    player = int(request.form['player'])
    if player == game.on_turn:
        column = int(request.form['column'])
        if game.player_move(player, column):
            game.check_winner()
            return 'true'
        return 'false'
    return 'false' 

@app.route('/join/', methods=["POST"])
def player_joines():
    if game.winner:
        game.__init__()
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
    print("\n\n** HOSTING **")
    print(f"[+] URL: {socket.gethostbyname(socket.gethostname())}") #TODO GET URL
    print(f"[+] GAME PORT: {GAME_CODE}\n\n\n")
    app.run(host="0.0.0.0", port=GAME_CODE)

host_start()