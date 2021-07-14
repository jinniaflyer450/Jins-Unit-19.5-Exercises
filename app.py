from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'


boggle_game = Boggle()
final_score = None

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

@app.route('/stop-timer')
def stop_timer():
    global final_score
    final_score = int(request.args['finalScore'])
    return jsonify(redirect='/post-game')

@app.route('/post-game')
def end_game():
    return render_template('post_game.html', finalScore = final_score)
    
#Got some help with jsonify here: https://www.kite.com/python/docs/flask.jsonify
#Figured out how to get my page to redirect properly here. 
#https://stackoverflow.com/questions/56932954/flask-redirect-not-working-but-i-dont-get-any-errors