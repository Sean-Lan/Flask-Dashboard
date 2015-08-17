# Flask-Dashboard
-----------------
Flask-Dashboard is an example using flask, Bootstrap, Ajax and SQLite3.  
It collects installer and stack information from argo, niweb, and parse sanity test results in rdfs01.  
A detailed introduction is in the html version doc.

## Usage
### Environment Set-up
1. For Windows, please add paths of `python.exe` and `pip.exe` into your `Path` environment variable. 
2. Install the dependencies:  
	1. pip install flask
	2. pip install BeautifulSoup

### Configuration in `main_config.py`
1. Set the `STACK_WEB_URL` for NI web RIO stack.
2. Set the `NEWER_THAN_DATE` to skip the days you are not insterested in, or more common, the  days RIO stack has changed and a new rule is applied.
3. Set the installer root. They are `MYRIO_TOOLKIT_INSTALLER_DAILY_FOLDER`, `ROBORIO_TOOLKIT_INSTALLER_DAILY_FOLDER`, `MYRIO_BUNDLE_INSTALLER_DAILY_FOLDER` and `ROBORIO_BUNDLE_INSTALLER_DAILY_FOLDER`.
4. Set the sanity test root `SANIT_TEST_ROOT_FOLDER`.
5. Set the years you want to show in the page: `INDEX_SIDEBAR_YEARS`.
6. Set the year you want to collect information  to save into database: `CURRENT_YEAR`. 
7. For more configuration, please read the html version doc.

### Start 
1. Run `initDB.py` to create tables.
2. Run `updateDB.py` to gather the information you need. It will cost much time depending on the network status of argo.
3. Run `main.py` to Start the server.

### Python Version Concern
Currently, Flask-dashboard is using python 2.7.10. If you have python 3.X installer and don't want to 2.X to impede your daily work, install python 2.7.10 and add the path **after** the 3.X path; **copy** `python.exe` in `python27` and rename it as `python2.exe`; rename pip.exe in `python27/scripts` to `pip2.exe`. In the future, if you want to use python 2.X, run python2 and pip2 instead.