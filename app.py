from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True)