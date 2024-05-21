from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "mysupersecretkey1302"
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/word-submit')
def word_submit():
    board = session["board"]
    word = request.args["word"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})