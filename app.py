from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session

app=Flask(__name__)
app.config['SECRET_KEY']='catdog'


boggle_game = Boggle()
