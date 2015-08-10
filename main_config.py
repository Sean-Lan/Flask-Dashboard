# URL for the NI web RIO stack
STACK_WEB_URL = r'http://niweb.natinst.com/confluence/display/RIOSW/NI-RIO+15.0.0+Install+Instructions'

# *ONLY* the date newer than this will be updated.
NEWER_THAN_DATE = '20150301'

# Sometimes argo in shanghai isn't stable, you can switch it to r'\\us-aus-argo'
PATH_PREFIX = r'\\cn-sha-argo'

# The root folder for myRIO toolkit daily installer
MYRIO_TOOLKIT_INSTALLER_DAILY_FOLDER = r'\\us-aus-argo\NISoftwarePrerelease\myRIO\Toolkit\3.1\Daily'

# The root folder for roboRIO toolkit daily installer
ROBORIO_TOOLKIT_INSTALLER_DAILY_FOLDER = r'\\us-aus-argo\NISoftwarePrerelease\roboRIO\Toolkit\3.1\Daily'

# The root folder for myRIO bundle daily installer
MYRIO_BUNDLE_INSTALLER_DAILY_FOLDER = r'\\cn-sha-argo\NISoftwarePrerelease\myRIO\Bundle\3.1\Daily'

# The root folder for roboRIO bundle daily installer
ROBORIO_BUNDLE_INSTALLER_DAILY_FOLDER = r'\\cn-sha-argo\NISoftwarePrerelease\roboRIO\Bundle\3.1\Daily'

# The sainity test results folder
SANITY_TEST_ROOT_FOLDER = r'C:\Users\xlan\Desktop\SanityTest'

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

# The dafualt weight for calculating the pass rate
SANITY_TEST_DEFAULT_WEIGHT = 3

# The bottom line of pass rate.
# Pass rate higher than it, Pass.
# Lower than it, Failed.
SANITY_TEST_BOTTOMLINE = 0.98

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
