from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'


boggle_game = Boggle()
final_score = None

@app.route('/')
def display_start():
    """Initializes the game-count and high-score values, then returns the HTML page that gives instructions and allows
    starting the game."""
    session['game-count'] = 0
    session['high-score'] = 0
    return render_template('start_game.html')

@app.route('/setup-game')
def setup_board():
    """Initializes a new board and includes it in the session. Covers for if game-count and high-score were not initialized in session
    and redirects to the /show-board route."""
    board = boggle_game.make_board()
    session['board'] = board
    if session.get('game-count', None) == None:
        session['game-count'] = 0
    if session.get('high-score', None) == None:
        session['high-score'] = 0
    return redirect('/show-board')

@app.route('/show-board')
def show_board():
    """If board is not initialized in session, redirects to /setup-game so that board can be initialized. Otherwise,
    returns the template that shows the board and allows you to play the game."""
    if session.get('board', None) == None:
        return redirect('/setup-game')
    return render_template('board.html', board=session['board'])

@app.route('/guess')
def submit_guess():
    """If board is not initialized in session, redirects to /setup-game so that board can be initialized. If no guess was sent,
    redirects to /show-board to allow a guess. If game-count and high-score are not initialized in session, initializes them.
    Otherwise, retrieves guess from the query string, checks if the guess is valid and if it is if it is on the board, then returns
    the results of checking as JSON."""
    if session.get('board', None) == None:
        return redirect('/setup-game')
    elif request.args.get('guess', None) == None:
        return redirect('/show-board')
    else:
        if session.get('game-count', None) == None:
            session['game-count'] = 0
        if session.get('high-score', None) == None:
            session['high-score'] = 0
        guess = request.args['guess']
        is_valid_and_on_board = boggle_game.check_valid_word(session['board'], guess)
        return jsonify(result=is_valid_and_on_board)

@app.route('/stop-timer')
def stop_timer():
    """After the time for the game has run out, updates game-count in session (adding 1) and final_score as a global variable 
    from the query string. If game-count or high-score do not exist in session, redirects to '/setup-game'.
    If final_score is the new high score, updates high-score in session. Then, sends data in JSON that allows for automatic redirection 
    to the /post-game route."""
    global final_score
    if session.get('game-count', None) == None or session.get('high-score', None) == None or request.args.get('finalScore', None) == None:
        return redirect('/setup-game')
    session['game-count'] += 1
    final_score = int(request.args['finalScore'])
    if session['high-score'] == None or session['high-score'] <= final_score:
        session['high-score'] = final_score
    return jsonify(redirect='/post-game')

@app.route('/post-game')
def end_game():
    """Returns the HTML page that displays that the game has ended, the number of times played, the high score, and the
    final score. If final_score is not initialized, sets it to 0."""
    global final_score
    if final_score == None:
        final_score = 0
    if session.get('game-count', None) == None or session.get('high-score', None) == None:
        return redirect('/setup-game')
    return render_template('post_game.html', finalScore = final_score)

#Got some help with jsonify here: https://www.kite.com/python/docs/flask.jsonify
#Figured out how to get my page to redirect properly here. 
#https://stackoverflow.com/questions/56932954/flask-redirect-not-working-but-i-dont-get-any-errors