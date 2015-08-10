import sqlite3
import os
import main_config
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash, jsonify
from contextlib import closing
from utilities import add_path_prefix, get_date, get_stack_date
from model.DBUtilities import Model

# create application
app = Flask(__name__)

def get_sanity_test_result(stack_name, bottom_line=1.0):
    model = Model('stack_test_result')
    column_list = ['pass_rate']
    condition_dict = { 'validated_stack': stack_name }
    records = model.select(column_list, condition_dict)
    pass_rates = [record['pass_rate'] for record in records]
    average_pass_rates = float(sum(pass_rates))/len(pass_rates) \
                if len(pass_rates) > 0 else -1
    if average_pass_rates == -1:
        return 'Not Tested'
    elif average_pass_rates >= bottom_line:
        return 'Pass'
    else:
        return 'Failed'

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] != main_config.DASHBOARD_USER_NAME:
        flash('Invalid username')
    elif request.form['password'] != main_config.DASHBOARD_PASSWORD:
        flash('Invalid password')
    else:
        session['logged_in'] = True
        session['username'] = 'admin'
        return redirect(url_for('index'))
    return redirect(url_for('welcome')) 
        
@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('username')
    flash('You were logged out')
    return redirect(url_for('welcome')) 
    

@app.route('/')
def index():
    if not session.get('logged_in'):
        flash('Please login.')
        return redirect(url_for('welcome'))
    return render_template('index.html', username=session['username'],
            years=main_config.INDEX_SIDEBAR_YEARS)


@app.route('/myrio_roborio_stack_dashboard/<year>')
def myrio_roborio_stack_dashboard(year):
    if not session.get('logged_in'):
        flash('Please login.')
        return redirect(url_for('welcome'))
    table_name = 'myrio_roborio_' + year + '_stack_dashboard'
    key_name = 'validated_stack'
    model = Model(table_name)
    column_list = ['validated_stack', 'validated_stack_url', 'lv_version', 
            'lv_api_version', 'safemode', 'comment']
    records = model.select(column_list)
    records = sorted(records, key=lambda record: record['validated_stack'], 
            reverse=True)
    for record in records:
        stack_date = get_stack_date(record['validated_stack'])
        sanity_test_result = get_sanity_test_result(stack_date, 
                main_config.SANITY_TEST_BOTTOMLINE)
        record['sanity_test_result'] = sanity_test_result

    return render_template('myrio_roborio_stack_dashboard.html', records=records, 
            year=year, table_name=table_name, key_name = key_name)


@app.route('/toolkit_installer_dashboard/<name>/<year>')
def toolkit_installer_dashboard(name, year):
    if not session.get('logged_in'):
        flash('Please login.')
        return redirect(url_for('welcome'))
    table_name = name+'_'+year+'_toolkit_installer_dashboard'
    key_name = 'installer_path'
    model = Model(table_name)
    column_list = ['installer_path', 'lv_version', 'lv_api_version', 
            'safemode', 'comment']
    records = model.select(column_list)
    records = sorted(records, 
                     key=lambda record: record['installer_path'], 
                     reverse=True)
    for record in records:
        record['installer_date'] = get_date(record['installer_path'])
        record['installer_path'] = add_path_prefix(record['installer_path'],
                main_config.PATH_PREFIX).rstrip('\\')
    return render_template('toolkit_installer_dashboard.html', records=records, 
                           name=name, year=year, table_name = table_name, 
                           key_name = key_name)


@app.route('/bundle_installer_dashboard/<name>/<year>')
def bundle_installer_dashboard(name, year):
    if not session.get('logged_in'):
        flash('Please login.')
        return redirect(url_for('welcome'))
    table_name = name+'_'+year+'_bundle_installer_dashboard'
    key_name = 'bundle_path'
    model = Model(table_name)
    column_list = ['bundle_path', 'lv_version', 'lv_api_version', 'toolkit_path',
            'safemode', 'actual_size', 'dedupe_size', 'comment']
    records = model.select(column_list)
    records = sorted(records, 
                     key=lambda record: record['bundle_path'], 
                     reverse=True)
    for record in records:
        record['bundle_date'] = get_date(record['bundle_path'])
        record['bundle_path'] = add_path_prefix(record['bundle_path'],
                main_config.PATH_PREFIX).rstrip('\\')
        record['toolkit_date'] = get_date(record['toolkit_path'])
        record['toolkit_path'] = add_path_prefix(record['toolkit_path'],
                main_config.PATH_PREFIX).rstrip('\\')
    return render_template('bundle_installer_dashboard.html', records=records, 
            name=name, year=year, table_name = table_name, key_name = key_name)


@app.route('/_update_table', methods=['POST'])
def update_table():
    if not session.get('logged_in'):
        abort(401) 
    table_name = request.form['table_name']
    key_name = request.form['key_name']
    primary_key = request.form['primary_key']
    comments = request.form['comments']
    print table_name, primary_key, comments
    print key_name
    model = Model(table_name)
    condition_dict = {key_name: primary_key}
    column_dict = {'comment': comments}
    model.update(column_dict, condition_dict, like=True)
    return jsonify(status='success')


@app.route('/detailed_sainity_test_result')
def detailed_sainity_test_result():
    stack_date = request.args.get('stack_date')
    model = Model('stack_test_result')
    column_list = ['daily_folder', 'pass_rate', 'validated_stack',
            'os_name', 'target_name']
    condition_dict = { 'validated_stack': stack_date }
    test_records = model.select(column_list, condition_dict)
    for record in test_records:
        record['test_date'] = record['daily_folder'].split('\\')[-1]
        record['os_folder_path'] = os.path.join(
                record['daily_folder'],
                record['os_name']
                )
    return render_template('detailed_sainity_test_result.html', 
            records = test_records, 
            stack_date = stack_date,
            bottom_line = main_config.SANITY_TEST_BOTTOMLINE)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    # Flask needs a secret_key to encrypt session
    app.secret_key = "Academic Software Group"
    app.run(host='0.0.0.0', debug=True)
