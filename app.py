from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def display_start():
    return render_template('start_game.html')

@app.route('/setup-game')
def setup_board():
    board = boggle_game.make_board()
    session['board'] = board
    return redirect('/show-board')

@app.route('/show-board')
def show_board():
    return render_template('board.html', board=session['board'])

@app.route('/guess')
def submit_guess():
    guess = request.args['guess']
    is_valid_and_on_board = boggle_game.check_valid_word(session['board'], guess)
    return jsonify(result=is_valid_and_on_board)


#Got some help with jsonify here: https://www.kite.com/python/docs/flask.jsonify
