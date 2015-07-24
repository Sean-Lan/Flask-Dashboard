import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing

# create application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myrio_roborio_2016_stack_dashboard')
def myrio_roborio_2016_stack_dashboard():
    return render_template('myrio_roborio_2016_stack_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
