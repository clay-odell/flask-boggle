from flask import Flask, render_template, request, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysupersecretkey1302"

boggle_game = Boggle()


@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)