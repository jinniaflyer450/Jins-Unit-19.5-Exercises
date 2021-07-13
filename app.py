from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def display_start():
    return render_template('start_game.html')

@app.route('/game-setup')
def setup_board():
    board = boggle_game.make_board()
    session['board'] = board
    session['guesses'] = []
    return redirect('/active-game')

@app.route('/active-game')
def display_current_game():
    return render_template('board.html', board=session['board'])

@app.route('/guess')
def submit_guess():
    guess = request.args['guess']
    if guess is not None:
        session['guesses'].append(guess)
    return redirect('/active-game')


#https://werkzeug.palletsprojects.com/en/2.0.x/exceptions/#
