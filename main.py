import sqlite3
import os
import main_config
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing
from utilities.record import add_path_prefix
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


@app.route('/toolkit_installer_dashboard/<name>/<year>')
def toolkit_installer_dashboard(name, year):
    model = Model(name+'_'+year+'_toolkit_installer_dashboard')
    column_list = ['installer_path', 'lv_version', 'lv_api_version', 
            'safemode', 'comment']
    records = model.select(column_list)
    records = sorted(records, key=lambda record: record['installer_path'], reverse=True)
    for record in records:
        record['installer_path'] = add_path_prefix(record['installer_path'],
                main_config.PATH_PREFIX)
    return render_template('toolkit_installer_dashboard.html', records=records, name=name, year=year)


@app.route('/bundle_installer_dashboard/<name>/<year>')
def bundle_installer_dashboard(name, year):
    model = Model(name+'_'+year+'_bundle_installer_dashboard')
    column_list = ['bundle_path', 'lv_version', 'lv_api_version', 'toolkit_path',
            'safemode', 'actual_size', 'dedupe_size', 'comment']
    records = model.select(column_list)
    records = sorted(records, key=lambda record: record['bundle_path'], reverse=True)
    for record in records:
        record['bundle_path'] = add_path_prefix(record['bundle_path'],
                main_config.PATH_PREFIX)
        record['toolkit_path'] = add_path_prefix(record['toolkit_path'],
                main_config.PATH_PREFIX)
    return render_template('bundle_installer_dashboard.html', records=records, name=name, year=year)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # model = Model('myrio_roborio_2016_stack_dashboard')
    # column_list = ['validated_stack', 'validated_stack_url', 'lv_version', 'lv_api_version', 
    #         'safemode', 'sanity_test_result', 'sanity_test_result_url', 'comment']
    # records = model.select(column_list)
    # records = sorted(records, key=lambda record: record['validated_stack'], reverse=True)
    # for record in records:
    #     print record
