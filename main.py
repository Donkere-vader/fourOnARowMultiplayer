from tkinter import Tk, Button, Entry, Frame, Label, messagebox
import requests, os, json

def clear_screen():
    for i in root.winfo_children():
        i.destroy()


class Game():
    def __init__(self):
        self.load_menu()
        self.tiles = [[0 for i in range(7)] for i in range(6)]
        self.url = "http://127.0.0.1"
        self.my_turn = False
        self.player_num = None
        self.game_data = {
            "winner":None
        }
    
    def load_menu(self):
        clear_screen()
        Label(
            text="Menu",
            font="arial 20"
        ).grid()
        selection_frame = Frame()
        selection_frame.grid()

        Button(
            master=selection_frame,
            text="Join",
            width=15,
            height=3,
            font='arial 20',
            command= lambda: self.join_game_menu()
        ).grid(row=0, column=0)

        Button(
            master=selection_frame,
            text="Host",
            width=15,
            height=3,
            font='arial 20',
            command= lambda: self.host_game()
        ).grid(row=0, column=1)

    def join_game_menu(self):
        clear_screen()
        Label(
            text="Join game",
            font="arial 18",
            width=20
        ).grid()

        url_entry = Entry(
            font='arial 18',
            width=20,
        )
        url_entry.insert(0, self.url)
        url_entry.grid()

        port_entry = Entry(
            font='arial 18',
            width=20,
        )
        port_entry.insert(0, "Enter game port ...")
        port_entry.grid()

        Button(
            text="Join",
            font='arial 18',
            width=20,
            command= lambda port_entry=port_entry, url_entry=url_entry: self.join_game(port_entry, url_entry) 
        ).grid()

    def join_game(self, port_entry, url_entry):
        self.url = url_entry.get()
        try:
            port = port_entry.get()
            if len(port) != 4:
                messagebox.showerror('ERROR','Invalid game code')
                return
            self.port = int(port)
            self.url += ":" + str(self.port)
        except ValueError:
            messagebox.showerror('ERROR','Invalid game code')
            return
        try:
            req = requests.post(f'{self.url}/join/')
        except:
            messagebox.showerror('Error', "Game not found")
            return
        if req.text != 'false':
            self.player_num = int(req.text)
            if self.player_num == 1:
                self.my_turn = True 
            self.draw()
            self.update()
        else:
            messagebox.showerror('Game full','Game already full')

    def update(self):
        req = requests.get(f'{self.url}/get/')
        if json.loads(req.text)['tiles'] != self.tiles:
            self.tiles = json.loads(req.text)['tiles']
            self.game_data = json.loads(req.text)['game_data']
            if self.game_data['winner']:
                self.draw()
                messagebox.showinfo('Winner', 'You won!!' if self.game_data['winner'] == self.player_num else 'You lost..')
            if self.game_data['on_turn'] == self.player_num:
                self.my_turn = True
            self.draw()
        root.after(1000, self.update)

    def draw(self):
        clear_screen()

        if self.my_turn:
            Label(
                text="Your turn",
                bg='green',
                fg='white',
                font='arial 15'
            ).grid()
        else:
            Label(
                text="Wait for your turn",
                bg='red',
                fg='white',
                font='arial 15'
            ).grid()

        player_symbol = "X" if self.player_num == 1 else "O"

        Label(
            text=f"Playing as: {player_symbol}",
            font='arial 15'
        ).grid()

        field_frame = Frame()
        field_frame.grid()
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                btn_text = ""
                btn_color = "white" 
                if tile == 1:
                    btn_text = 'X'
                    btn_color = "red"
                if tile == 2:
                    btn_text = 'O'
                    btn_color = "blue"
                Button(
                    master=field_frame,
                    text=btn_text,
                    fg='white',
                    bg=btn_color,
                    width=3,
                    font='arial 15',
                    border=1
                ).grid(row=y, column=x)
        
        btn_frame = Frame()
        btn_frame.grid()

        for x in range(len(self.tiles)+1):
            Button(
                master=btn_frame,
                text="\\/",
                font='arial 15',
                width=3,
                border=1,
                bg='black',
                fg='white',
                command= lambda column=x: self.do_turn(column)
            ).grid(row=0, column=x)

        #Button(
        #    text="refresh",
        #    command= lambda: self.update()
        #).grid()


    def do_turn(self, column):
        if game.my_turn:
                data = {"player":self.player_num,"column":column}
                req = requests.post(f'{self.url}/user_move/', data=data)
                if req.text != 'false':
                    self.my_turn = False
                    self.update()

    def host_game(self):
        messagebox.showinfo("Hosting a game","To host a game run the hoster script")

root = Tk()
root.title("Four in a row")

game = Game()
root.mainloop()