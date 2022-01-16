# -*- coding:utf-8 -*-
#
# Copyright 2017, donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

from PyQt5.QtCore import PYQT_VERSION_STR
from platform import python_version

TL_HELPER_VERSION = 'V1.1'
# file names used in testLinkHelper
CONFIG_FILE = 'config.ini'
TEMPLATE_FILE = 'template.xls'

# constant variable defined for testlink
MANUAL = 1
AUTOMATED = 2
READFORREVIEW = 2
REWORK = 4
priority_dict = {
    'Low': 3,
    'Medium': 2,
    'High': 1,
}
executiontype_dict = {
    'Manual': 1,
    'Automated': 2,
}

TL_API_PATH = 'lib/api/xmlrpc/v1/xmlrpc.php'

# list used in generate_template function
template_content = ['Case Name', 'Priority', 'Pre-condition', 'Action', 'Expected Results']


# string used in about function
about_content = '''<b>TestLinkHelper {0}</b><br>\
<br>Licensed under the GPL, Version 3.0\
<br><br>Developed under:\
<ul><li>Python: {1}</li>\
<li>PyQt: {2}</li></ul>\
<br>Copyright &copy; 2017, Hangzhou, China'''.format(TL_HELPER_VERSION, python_version(), PYQT_VERSION_STR)
