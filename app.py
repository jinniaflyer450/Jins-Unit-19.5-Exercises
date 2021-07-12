from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def display_board():
    board = boggle_game.make_board()
    session['board'] = board
    session['guesses'] = []
    return render_template('board.html', board=board)

@app.route('/guess', methods=['POST'])
def submit_guess():
    guess = request.form['guess']
    return redirect('/')


#https://werkzeug.palletsprojects.com/en/2.0.x/exceptions/#
