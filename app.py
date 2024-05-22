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
    """Shows the Boggle Game Board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    attempts = session.get('attempts', 0)
    return render_template('index.html', board=board, highscore=highscore, attempts=attempts)

@app.route('/word-submit')
def word_submit():
    """Checks to see if word is in dict"""
    board = session["board"]
    word = request.args["word"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """Receives score, updates highscore and number of attempts as necessary"""
    score = request.json["score"]
    highscore = int(session.get("highscore", 0))
    attempts = session.get("attempts", 0)
    session['highscore'] = max(score, highscore)
    session['attempts'] = attempts + 1
    return jsonify(newRecord=score > highscore)

