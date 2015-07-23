import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing

# create application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inner.html')
def inner():
    return render_template('inner.html')

if __name__ == '__main__':
    app.run()
