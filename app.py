from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'


boggle_game = Boggle()

@app.route('/display_board')
def display_board():
    board = boggle_game.make_board()
    return render_template('board.html', board=board)
