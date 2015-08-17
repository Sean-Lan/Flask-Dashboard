title: Introduction to Stack Dashboard
speaker: Sean
url: https://github.com/Sean-Lan
transition: move
files: /css/arch.css, /js/zoom.js, /css/all.css
theme: dark

[slide]
# Introduction to Stack Dashboard
<small>Sean</small>

[slide]
## Agenda
---------
* Background
    * RIO Stack
    * Sanity Test
    * Needed Information
* Architecture of Stack Dashboard
* Implementation Details
    * Website
    * Data Collection
    * Sanity Test Parse
* Dependency Issues

[slide]
## Background

[slide]
## RIO Stack
------------
* Sevaral softwares related to RIO
    * LabVIEW
    * RT
    * FPGA
    * cRIO
    * ...
* [NI-RIO 15.0.0 Install Instructions](http://niweb.natinst.com/confluence/display/RIOSW/NI-RIO+15.0.0+Install+Instructions)
* Validated Stack

[slide]
## Sanity Test
--------------
* Test_Install Software.vi
* test_upgrading_firmware target.vi
* test_renaming target.vi
* test_format target.vi

[slide]
## Information We Need
----------------------
* Installer location
* lvVersion
* lvAPIVersion
* Safemode (firmware version)

[slide]
## Architecture of Stack Dashboard

[slide]
<div id="arch">
<div id="desktop">
<img src="/img/desktop.svg"/>
    Browser
</div>
<div id="dsk-svr-line">
    <img src="/img/horizonal_line.svg"/>
</div>
<div id="server">
    <img src="/img/server_main.svg"/>
    Flask Server
</div>
<div id="svr-db-line">
    <img src="/img/horizonal_line.svg"/>
</div>
<div id="database">
    <img src="/img/database.svg"/>
    SQLite3
</div>
<div class="clear"></div>
<div id="db-ps-line">
    <img src="/img/vertical_line.svg"/>
</div>
<div id="db-dc-line">
    <img src="/img/vertical_line2.svg"/>
</div>
<div class="clear"></div>
<div id="rdfs01">
    <img src="/img/server.svg"/>
    rdfs01
</div>
<div id="rdfs-ps-line">
    <img src="/img/horizonal_line.svg"/>
</div>
<div id="parser">
    <img src="/img/parser.svg"/>
    Test Parser
</div>
<div id="updatedb">
    <img src="/img/updatedb.svg"/>
    Data Collection
</div>
<div class="clear"></div>
<div id="dc-niweb-line">
    <img src="/img/vertical_line.svg"/>
</div>
<div id="dc-argo-line">
    <img src="/img/vertical_line2.svg"/>
</div>
<div class="clear"></div>
<div id="niweb">
    <img src="/img/server.svg"/>
    niweb 
</div>
<div id="argo">
    <img src="/img/server.svg"/>
    argo
</div>
</div>

[slide]
## Implementation Details

[slide]
### Website
----------
* [myRIO/robRIO Stack Dashboard](http://sh-rd-myrio04:5000/)
* jQuery
* Bootstrap
* Flask Framework
* SQLite3
[slide]
### Web Basics
-------------
* ["What happens when you type google.com into your browser's address box and press enter?"](https://github.com/alex/what-happens-when)
* Cookie
	* Saved in client's browser
	* Authentication, site preferences, and session id
	* Browser adds related cookies into the request header
* Session
	* Saved in the server
	* Related to one certain client
	* Across multiple requests
	* Internally, a server saves sessions using a dict structure
[note]
What is a `Cookie`?
-------------------
A `cookie` is a small piece of text stored on a user's computer by their browser. Common uses for cookies are authentication, storing of site preferences, and server session identification.  
Each time the users' web browser interacts with a web server it will pass the cookie information to the web server. Only the cookies stored by the browser that relate to the domain in the requested URL will be sent to the server.   
What is a `Session`?
--------------------
A `session` can be defined as a server-side storage of information that is desired to persist throughout the user's interaction with the web site or web application. 
Instead of storing large and constantly changing information via cookies in the user's browser, only a unique identifier is stored on the client side (called a "session id"). This session id is passed to the web server every time the browser makes an HTTP request (i.e. a page link or AJAX request). The web application pairs this session id with it's internal database and retrieves the stored variables for use by the requested page.
[/note]
[slide]
### Brief Introduction to [Flask](http://flask.pocoo.org/)
---------------------------------------------------------
* Server side **micro**framework
* RESTful request dispatching
* Use [Jinja2](http://jinja.pocoo.org/docs/dev/templates/) templating  
![Flask](/img/flask.png)
[slide]
### Template Engine: [Jinja2](http://jinja.pocoo.org/docs/dev/templates/)
------------------------------------------------------------------------
	<pre><code class="django">
{% extends "layout.html" %}
{% block body %}
  &lt;ul&gt;
  {% for user in users %}
    &lt;li&gt;&lt;a href="{{ user.url }}">{{ user.username }}&lt;/a&gt;&lt;/li&gt;
  {% endfor %}
  &lt;/ul&gt;
{% endblock %}
    </code></pre>
![Jinja2](/img/jinja-logo.png)
[slide]
### Template Inheritance
* layout.html
	* index.html
	* welcome.html
	* dashboard_common.html
		* stack_dashboard.html
		* toolkit_installer_dashboard.html
		* bundle_installer_dashbaord.html
		* detailed_sanity_test_result.html
[slide]
#### Define basic page information in `layout.html`:
-----------------------------------------------
* Meta data
* common css and javascript files
	<pre><code class="django">
&lt;!DOCTYPE html&gt;
&lt;html lang="zh-CN"&gt;
        {% block head %}
        &lt;meta http-equiv="Content-Type" content="text/html; charset=UTF-8"&gt;

        &lt;meta charset="utf-8"&gt;
        &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
        &lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;
        &lt;meta name="description" 
			content="A site for demonstrating myRIO/roboRIO stack and installer information"&gt;
        &lt;meta name="author" content="Sean"&gt;
        &lt;title&gt;{% block title %}{% endblock %}&lt;/title&gt;
        &lt;link rel="shortcut icon" href="{{ url_for('static', filename='images/myRIO.png') }}"/&gt;
        &lt;link rel="bookmark" href="{{ url_for('static', filename='images/myRIO.png') }}"/&gt;
        &lt;!-- Bootstrap core CSS --&gt;
        &lt;link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet"&gt;
        &lt;script src="{{ url_for('static', filename='js/jquery.min.js') }}"&gt;&lt;/script&gt;
        &lt;script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"&gt;&lt;/script&gt;
    &lt;body&gt;
        {% endblock %}
        {% block content %}{% endblock%}
    &lt;/body&gt;
&lt;/html&gt;
    </code></pre>

[slide]
#### Define the main layout in the `index.html`:
-------------------------------------------
	<pre><code class="django">
{% extends "layout.html" %}
{% extends "layout.html" %}
{% block title %}myRIO/roboRIO Stack Dashboard{% endblock %}
{% block head %}
{{ super() }}
&lt;link href="{{ url_for('static', filename='css/index.css') }}" rel="stylesheet"&gt;
{% endblock %}
{% block content %}
&lt;nav class="navbar navbar-inverse navbar-fixed-top"&gt;
......
&lt;/nav&gt;
&lt;div class="container-fluid"&gt;
    &lt;div class="row"&gt;
        &lt;div class="col-sm-3 col-md-2 sidebar"&gt;
            &lt;ul class="nav nav-sidebar"&gt;
                ......
            &lt;/ul&gt;
        &lt;/div&gt;
        &lt;div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main"&gt;
            &lt;iframe name="main-frame" src="myrio_roborio_stack_dashboard/2016" 
				marginHeight=0 marginWidth=0 frameborder="0" id="main-frame"&gt;
            &lt;/iframe&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/div&gt;
{% endblock %}
    </code></pre>

[slide]
#### Define the common modal in the `dashboard_common.html`:
-------------------------------------------------------
	<pre><code class="django">
{% extends "layout.html" %}
{% block head %}
{{ super() }}
&lt;script src="{{ url_for('static', filename='kindeditor-all-min.js') }}"&gt;&lt;/script&gt;
&lt;script src="{{ url_for('static', filename='js/ZeroClipboard.min.js') }}"&gt;&lt;/script&gt;
......
{% endblock %}
{% block content %}
{{ super() }}
&lt;div class="modal fade" id="comments-modal" role="dialog" aria-hidden="true"&gt;
    &lt;div class="modal-dialog"&gt;
        &lt;div class="modal-content"&gt;
            &lt;div class="modal-header"&gt;
                &lt;button type="button" class="close" data-dismiss="modal" 
				 aria-hidden="true"&gt;&times;&lt;/button&gt;
                &lt;h4 class="modal-title" id="myModalLabel"&gt;Edit Comments&lt;/h4&gt;
            &lt;/div&gt;
        &lt;textarea name='comments' class="modal-body"&gt;&lt;/textarea&gt;
            &lt;div class="modal-footer"&gt;
                &lt;button type="button" class="btn btn-default" 
						data-dismiss="modal"&gt;close&lt;/button&gt;
                &lt;button type="button" id="btn-submit" class="btn btn-primary"&gt;
					submit&lt;/button&gt;
            &lt;/div&gt;
        &lt;/div&gt;&lt;!-- /.modal-content --&gt;
    &lt;/div&gt;&lt;!-- /.modal --&gt;
&lt;/div&gt;
{% endblock %}
    </code></pre>

[slide]
#### Define information table in sub-templates:  
----------------------------------------------
#### As with `myrio_roborio_stack_dashboard.html`:
	<pre><code class="django">
{% extends "dashboard_common.html" %}
......
{% block content %}
{{ super() }}
&lt;div id="main" style="margin: 0; padding: 0;"&gt;
    &lt;h1&gt;myRIO/roboRIO {{ year }} Stack Dashboard&lt;/h1&gt;
    &lt;div class="table-responsive"&gt;
        &lt;table class="table table-striped main-table" table_name={{ table_name }}&gt;
            &lt;thead&gt;
				&lt;tr&gt;&lt;th&gt;Validated Stack&lt;/th&gt;
					......
                    &lt;th&gt;Comments&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;
            &lt;tbody&gt;
                {% for record in records %}
                &lt;tr&gt;
                    &lt;td&gt;&lt;a href="{{ record['validated_stack_url'] }}"&gt;
						&lt;span class="primary-key"&gt;{{ record['validated_stack'] }}
						&lt;/span&gt;&lt;/a&gt;&lt;/td&gt;
                    ......
                    &lt;td class="comments" onselectstart="return false"&gt;
                    {% if record['comment'] %}
                        {{ record['comment'] | safe }}
                    {% endif %}
                    &lt;/td&gt;&lt;/tr&gt;
                {% endfor %}
            &lt;/tbody&gt;&lt;/table&gt;&lt;/div&gt;&lt;/div&gt;
{% endblock %}
    </code></pre>

[slide]
### Sanity Test Parser

[slide]
### Sanity Test Parser
----------------------
* Directory Structure:
	* SanityTestROOT 
		* 20160102_151351
			* BuildInfo.xml
			* Windows 7 (32-bit SP1 English)
				* *.csv
			* Windows 8 (32-bit SP1 English) 
			* ......
		* ......
[slide]
### Sanity Test Parser
* The target stack is retrieved from `BuildInfo.xml`
	<pre><code class="xml">
	&lt;BuildInfo&gt;
		&lt;Sequence IsTemp="True" SeqID="111131950"&gt;
            ...
			&lt;Step6 Path="...\NI CompactRIO\15.0.0\daily\20150529_0345b64\NICRIO" 
                      StepName="SWStack NI CompactRIO 15.0 20150228_0317"/&gt;
            ...
		&lt;/Sequence&gt;
	&lt;/BuildInfo&gt;
    </code></pre>
* Use `re` module to retrieve the date.
	<pre><code class="python">
def get_stack_date(stack_name):
    date_pattern = re.compile(r'\d{8}_\d+[dabf]\d+')
    match = date_pattern.search(stack_name)
    return match.group()
</code></pre>
[slide]
### Sanity Test Parser
----------------------
* Get date and os name
* Get target model, test name and test result from .csv files
<pre><code class="python">
{'results':
        {'Windows 7 (32-bit SP1 English)': 
                {'roboRIO': 
                    {'Test_Install Software.vi': 'Passed', 
                     'test_upgrading_firmware target.vi': 'Passed',
                     'test_renaming target.vi': 'Passed', 
                     'test_format target.vi': 'Passed'}, 
                 'myRIO-1950': 
                    {'Test_Install Software.vi': 'Passed',
                     'test_upgrading_firmware target.vi': 'Passed', 
                     'test_renaming target.vi': 'Passed',
                     'test_format target.vi': 'Passed'}, 
                 'myRIO-1900': 
                    {'Test_Install Software.vi': 'Avoided', 
                     'test_upgrading_firmware target.vi': 'Passed', 
                     'test_renaming target.vi': 'Passed', 
                     'test_format target.vi': 'Failed'}
                }
        ...
        }, 
     'crio_date': '20150624_1715f3'
}
</pre></code>
[slide]
### Sanity Test Parser
----------------------
* Calculate pass rate according to rating dict in `main_config` module
<pre><code class="python">
# The rating dict
# The weight is 0~5(inclusive)
# The higher the weight is, the more important the test case is.
# If some test case with weight 5 is failed, the whole test's passrate will be zero
# and thus will get failed.
SANITY_TEST_RATING_DICT = {
    'Test_Install Software.vi': 5, 
    'test_upgrading_firmware target.vi': 4, 
    'test_renaming target.vi': 3, 
    'test_format target.vi':  2,
    # add the test cases you want to change the default weight
}
# The default weight for calculating the pass rate
SANITY_TEST_DEFAULT_WEIGHT = 3
</code></pre>
* After the calculation:
<pre><code class="python">
{'results':
    {'Windows 7 (32-bit SP1 English)': 
            {'roboRIO': 1.0, 
             'myRIO-1950': 1.0, 
             'myRIO-1900': 0.77},
     ...
    },
 'crio_date': '20150624_1715f3'
}
</pre></code>
[slide]
### Data Collection

[slide]
#### Get each validated stack from [NI-RIO 15.0.0 Install Instructions](http://niweb.natinst.com/confluence/display/RIOSW/NI-RIO+15.0.0+Install+Instructions)
-------------------------------------------------------------------------------------------------------------------------------------------------------------  
* In `niweb` module:
	<pre><code class="python">
def extract_valid_stack_urls(url):
    urls = []
    try:
        htmlsource = urllib2.urlopen(url).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        sw = soup.findAll('h4', text='Software Stacks')[-1]
        swtable = sw.findNext('table', { 'class': 'confluenceTable' })
        for tr in swtable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) >= 3 and ('dat validated' in tds[2].text.lower() 
                    or 'passed' in tds[2].text.lower()):
                urls.append(NIWEB_URL + tds[1].find('a')['href'])
    except:
        pass
    return urls
	</code></pre>
* More at [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

[slide]
#### Retrieve the installer location of each component
------------------------------------------------------
    [20150624_1715f3 Stack](http://niweb.natinst.com/confluence/display/RIOSW/RIO+Build+20150624_1715f3+with+06-18+LV+Stack)
	<pre><code class="python">
def extract_installer_locations(stackUrl):
    installerLocationDict = {}
    try:
        htmlsource = urllib2.urlopen(stackUrl).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        installerHeader = soup.findAll('h1', text='Installers')[0]
        installerInfoTable = installerHeader.findNext('table',  { 'class': 'confluenceTable' })
        for tr in installerInfoTable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) == 0:                    # skip the table header
                continue
            softwareName = tds[0].find('strong').string
            installerLocation = tds[1]
            if installerLocation.find('p'):      # means the field in the table is empty
                installerLocation = ''
            else:
                installerLocation = installerLocation.string
            installerLocationDict[softwareName] = installerLocation.\
                                replace('\setup.exe','')
    except:
        pass
    return installerLocationDict
    </code></pre>

[slide]
#### Get `lvVersion/lvAPIVersion` from `buildInfo.txt`
------------------------------------------------------
* `buildInfo.txt`:
	<pre><code class="ini">
[Build Information]
perforceSyncTime=2015/06/17:10:26:49
Perforce Changelist=4250056
lvVersion=15.0
lvAPIVersion=15.0.0r0
ATS_testInstance=...
    </code></pre>
* In `record` module:	
<pre><code class="python">
def get_lv_info(config_file_path):
    lvInfo = {}
    lvCfgParser = ConfigParser.ConfigParser()
    lvCfgParser.read(config_file_path)
    if lvCfgParser.has_section('Build Information'):
        section_name = 'Build Information'
    else:
        section_name = 'LabVIEW Build Information'

    lvInfo['lvVersion'] = lvCfgParser.get(section_name, 'lvVersion')
    lvInfo['lvAPIVersion'] = lvCfgParser.get(section_name, 'lvAPIVersion')
    return lvInfo
</code></pre>

[slide]
#### Get `safemode` from `cRIO_Firmware.msi`
--------------------------------------------
<pre><code class="python">
def get_versions_from_msi(msiPath,productNames):
    """
    Get product versions from the File of designated msi file.
    The FileName field in the File table must end with '.cfg'
    (e.g. kcsbvqgs.cfg|myRIO-1900_3.0.0a10.cfg)
    """
    db = msilib.OpenDatabase(msiPath,msilib.MSIDBOPEN_READONLY)
    viewSql = "SELECT FileName FROM File "       
    fileView = db.OpenView(viewSql)
    fileView.Execute(None)
    fileNameList = []
    try:
        while True:
            result = fileView.Fetch()
            fileNameList.append(result.GetString(1))
    except:
        pass
    versionDict = {}
    for fileName in fileNameList:
        for productName in productNames:
            index = fileName.find(productName)
            if index != -1:
                version = fileName[index+len(productName)+1:-4]
                versionDict[productName] = version
    return versionDict
</code></pre>

[slide]
#### Dedupe process in `bundle` module
--------------------------------------
1. Find the folder contains `.msi` files.
2. Sort the `.msi` files and retrieve first of them as a **representative**.
3. Get the `UpgradeCode` and `ProductVersion` from the **representative**.
4. Only keep the installer with the newest `ProductVersion` if the `UpgradeCode` is the same. 

[slide]
#### Dedupe process in `bundle` module
--------------------------------------
<pre><code class="python">
def get_deduped_size(dirname):
    product_dict = {}
    deduped_size = 0L
    for root, dirs, files in os.walk(dirname):  
        if len(dirs) != 0:
            continue
        files = filter( lambda filename: os.path.splitext(filename)[1] == '.msi',
                    files
                    )
        if len(files) == 0:
            continue
        # Get the first msi as a representative
        msi = sorted(files)[0]
        fullpath = os.path.join(root, msi)
        UpgradeCode, ProductVersion = get_installer_info_from_msi(fullpath)

        size = reduce(lambda size, name: size + os.path.getsize(
                                            os.path.join(root, name)),
                      files, 0)
        if UpgradeCode in product_dict:
            if product_dict[UpgradeCode]['version'] > ProductVersion:
                deduped_size += size
            else:
                deduped_size += product_dict[UpgradeCode]['size']
                product_dict[UpgradeCode] = {'version': ProductVersion,
                                             'size': size}
        else:
            product_dict[UpgradeCode] = {'version': ProductVersion,
                                         'size': size}
    return deduped_size
</code></pre>

[slide]
#### Dedupe process in `bundle` module
--------------------------------------
* The `actual size` is the bundle size without dedupe.
* The `ideal size` equals `actual size` - `deduped_size`
<pre><code class="python">
def getdirsize(dir):    # actual size 
    size = 0L  
    for root, dirs, files in os.walk(dir):  
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
    return size
</code></pre>
<pre><code class="python">
ideal_size = getdirsize(bundle_path) - get_deduped_size(bundle_path)
</code></pre>

[slide]
#### ORM Class: `model.DBUtilities.Model`
------------------------------------------
* Define the `Model` class:
<pre><code class="python">
class Model:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = connect_db()
    def __del__(self):
        self.conn.close()
    def insert(self, column_dict): pass
    def update(self, column_dict, condition_dict={}, like=False): pass
    def delete(self, condition_dict={}, like=False): pass
    def select(self, columns_list, condition_dict = {}, like=False): pass
</code></pre>
* Then we could operate like:
<pre><code class="python">
model = Model('stack_test_result')  # 'stack_test_result' is the table name
column_list = ['daily_folder',]     # 'daily_folder' is the column name
parsed_folders = [record['daily_folder'] for record in model.select(column_list)]
for target_model, pass_rate in pass_rates.items():
    table_record = {
            'daily_folder': daily_folder,   # column name and value pair
            'validated_stack': crio_date,
            'os_name': os_name,
            'target_name': target_model,
            'pass_rate': pass_rate
            }
    model.insert(table_record)
</code></pre>
[slide]
## Dependency Consideration

[slide]
### General Dependencies
* `niweb` module relates to RIO stack website
* `record` and `bundle` modules relate to installers in **argo**
* `testing` module relates to test results in **rdfs01**

[slide]
### RIO Stack Website Related
-----------------------------
* Set the right web page url
* Set the `NEWER_THAN_DATE` in `main_config` module
	<pre><code class="python">
# URL for the NI web RIO stack
STACK_WEB_URL = r'http://niweb.natinst.com/confluence/display/RIOSW/NI-RIO+15.0.0+Install+Instructions'
# *ONLY* the date newer than this will be updated.
NEWER_THAN_DATE = '20150301'
	</code></pre>

[slide]
### RIO Stack Website Related
-----------------------------
* If structure of web page changes, the `extract_valid_stack_urls(url)` in `niweb` module needed to be modified
<pre><code class="python">
def extract_valid_stack_urls(url):
    urls = []
    try:
        htmlsource = urllib2.urlopen(url).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        sw = soup.findAll('h4', text='Software Stacks')[-1]
        swtable = sw.findNext('table', { 'class': 'confluenceTable' })
        for tr in swtable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) >= 3 and ('dat validated' in tds[2].text.lower() 
                    or 'passed' in tds[2].text.lower()):
                urls.append(NIWEB_URL + tds[1].find('a')['href'])
    except:
        pass
    return urls
</code></pre>

[slide]
### RIO Stack Website Related
-----------------------------
* If structure of daily stack page changes, the `extract_installer_locations(stackUrl)` in `niweb` module needed to be modified
<pre><code class="python">
def extract_installer_locations(stackUrl):
    installerLocationDict = {}
    try:
        htmlsource = urllib2.urlopen(stackUrl).read()
        soup = BeautifulSoup(htmlsource, 'lxml')
        installerHeader = soup.findAll('h1', text='Installers')[0]
        installerInfoTable = installerHeader.findNext('table',  { 'class': 'confluenceTable' })
        for tr in installerInfoTable.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) == 0:                    # skip the table header
                continue
            softwareName = tds[0].find('strong').string
            installerLocation = tds[1]
            if installerLocation.find('p'):      # means the field in the table is empty
                installerLocation = ''
            else:
                installerLocation = installerLocation.string
            installerLocationDict[softwareName] = installerLocation.\
                                replace('\setup.exe','')
    except:
        pass
    return installerLocationDict
</code></pre>


[slide]
### Installer Related
---------------------
* Sometimes argo in Shanghai is **NOT** happy
* You need to change the `main_config` module to use us-aus-argo:
<pre><code class="python">
# Sometimes argo in shanghai isn't stable, you can switch it to r'\\us-aus-argo'
PATH_PREFIX = r'\\cn-sha-argo'
</code></pre>

[slide]
### Installer Related
---------------------
* For bundle installer, we need traverse the directory to dedupe, Shanghai argo is much more faster.
* For toolkit installer, use Austin argo is more stable.
* Please the correct root folder for each Installer in`main_config` module:
<pre><code class="python">
# The root folder for myRIO toolkit daily installer
MYRIO_TOOLKIT_INSTALLER_DAILY_FOLDER = r'\\us-aus-argo\NISoftwarePrerelease\myRIO\Toolkit\3.1\Daily'
# The root folder for roboRIO toolkit daily installer
ROBORIO_TOOLKIT_INSTALLER_DAILY_FOLDER = r'\\us-aus-argo\NISoftwarePrerelease\roboRIO\Toolkit\3.1\Daily'
# The root folder for myRIO bundle daily installer
MYRIO_BUNDLE_INSTALLER_DAILY_FOLDER = r'\\cn-sha-argo\NISoftwarePrerelease\myRIO\Bundle\3.1\Daily'
# The root folder for roboRIO bundle daily installer
ROBORIO_BUNDLE_INSTALLER_DAILY_FOLDER = r'\\cn-sha-argo\NISoftwarePrerelease\roboRIO\Bundle\3.1\Daily'
</code></pre>

[slide]
### Sanity Test Related
-----------------------
* Sanity tests will **NOT** always pass r.w.t the same stack.
* If possible, please delete the useless test results at rdfs01
<pre><code class="python">
# The sainity test results folder
SANITY_TEST_ROOT_FOLDER = r'\\cn-sha-rdfs01\AutoTestData\Report\myRIO\2015\RT\All_SanityTest'
# The rating dict
# The weight is 0~5(inclusive)
# The higher the weight is, the more important the test case is.
# If some test case with weight 5 is failed, the whole test's passrate will be zero
# and thus will get failed.
SANITY_TEST_RATING_DICT = {
    'Test_Install Software.vi': 5, 
    'test_upgrading_firmware target.vi': 4, 
    'test_renaming target.vi': 3, 
    'test_format target.vi':  2,
    # add the test cases you want to change the default weight
}
# The default weight for calculating the pass rate
SANITY_TEST_DEFAULT_WEIGHT = 3
# The bottom line of pass rate.
# Pass rate higher than it, Pass.
# Lower than it, Failed.
SANITY_TEST_BOTTOMLINE = 0.98
</code></pre>

[slide]
Dashboard Website Related
-------------------------
* Define the current you want to collect the information
* Run `initDB` module and `updateDB` module
* `initDB` will create the tables according to the predefined schema:
<pre><code class="sql">
CREATE TABLE IF NOT EXISTS [myrio_roborio_{year}_stack_dashboard] (
  [validated_stack] VARCHAR(100) NOT NULL, 
  [validated_stack_url] VARCHAR(200) NOT NULL, 
  [lv_version] VARCHAR(20) NOT NULL, 
  [lv_api_version] VARCHAR(20) NOT NULL, 
  [safemode] VARCHAR(20) NOT NULL, 
  [comment] TEXT(1000), 
  CONSTRAINT [sqlite_autoindex_myrio_roborio_{year}_stack_dashboard_1] PRIMARY KEY ([validated_stack]));
</code></pre>
* `updateDB` will invoke `testing`, `bundle`, `installer`, `record` to collect data

[slide]
Dashboard Website Related
-------------------------
* Define the years you want to show
<pre><code class="python">
# The data of the year you want to show in the index page.
INDEX_SIDEBAR_YEARS = [
        2015,
        2016
        ]
# The year for update database.
CURRENT_YEAR = 2016
# The username and password to login the dashboard
DASHBOARD_USER_NAME = "admin"
DASHBOARD_PASSWORD = "admin"
</code></pre>

[slide]
## Thank You
