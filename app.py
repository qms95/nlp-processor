from flask import Flask, render_template, redirect
from generate_poem import PoemGenerator
app = Flask(__name__)

generator = PoemGenerator(None)


@app.route("/")
def home():
    return redirect('http://git.h