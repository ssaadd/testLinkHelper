# -*- coding:utf-8 -*-
#
# Copyright 2017, donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

from PyQt5.QtCore import PYQT_VERSION_STR
from platform import python_version

# file names used in testLinkHelper
CONFIG_FILE = 'config.ini'
TEMPLATE_FILE = 'template.xls'

# constant variable defined for testlink
MANUAL = 1
AUTOMATED = 2
READFORREVIEW = 2
REWORK = 4
HIGH = 3
MEDIUM = 2
LOW = 1

TL_API_PATH = 'lib/api/xmlrpc/v1/xmlrpc.php'

# list used in generate_template function
template_content = ['Case Name', 'Priority', 'Pre-condition', 'Action', 'Expected Results']


# string used in about function
about_content = '''<b>TestLinkHelper V1.0</b><br>\
<br>Licensed under the GPL, Version 3.0\
<br><br>Developed under:\
<ul><li>Python: {0}</li>\
<li>PyQt: {1}</li></ul>\
<br>Copyright &copy; 2017, Hangzhou, China'''.format(python_version(), PYQT_VERSION_STR)
