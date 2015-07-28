import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing
from model.DBUtilities import Model

# create application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myrio_roborio_2016_stack_dashboard')
def myrio_roborio_2016_stack_dashboard():
    model = Model('myrio_roborio_2016_stack_dashboard')
    column_list = ['validated_stack', 'validated_stack_url', 'lv_version', 'lv_api_version', 
            'safemode', 'sanity_test_result', 'sanity_test_result_url', 'comment']
    records = model.select(column_list)
    records = sorted(records, key=lambda record: record['validated_stack'], reverse=True)
    return render_template('myrio_roborio_2016_stack_dashboard.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
    # model = Model('myrio_roborio_2016_stack_dashboard')
    # column_list = ['validated_stack', 'validated_stack_url', 'lv_version', 'lv_api_version', 
    #         'safemode', 'sanity_test_result', 'sanity_test_result_url', 'comment']
    # records = model.select(column_list)
    # records = sorted(records, key=lambda record: record['validated_stack'], reverse=True)
    # for record in records:
    #     print record
