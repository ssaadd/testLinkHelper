# -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

import sys
import os.path
import threading
import xlrd, xlwt
from testlink import TestlinkAPIClient, testlinkerrors
from PyQt5 import QtCore, QtWidgets, QtGui

import utils
from commons import *
from gui.ui_option import Ui_optionDialog
from gui.ui_testlinkHelper import Ui_testlinkHelper


class testLinkHelper(QtWidgets.QMainWindow):
    '''
    import test case into testlink
    '''
    _insert_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(testLinkHelper, self).__init__()

        self.main_window = Ui_testlinkHelper()
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.main_window.setupUi(self)
        self.main_window.infoTextEdit.setMaximumBlockCount(1000)

        self.server_url = ''
        self.devkey = ''
        self.login_name = ''
        self.projs_info_dict = {}
        self.init_config()

        self.main_window.actionConfig.triggered.connect(self.server_config)
        self.main_window.action_Quit.triggered.connect(self.close)
        self.main_window.actionAbout.triggered.connect(self.about)
        self.main_window.actionHelp.triggered.connect(self.get_help)

        self.main_window.case_path_Button.clicked.connect(self.get_case_path)
        self.main_window.importButton.clicked.connect(self.import_case)
        self.main_window.gen_temp_Button.clicked.connect(self.generate_template)
        self.main_window.proj_comBox.currentIndexChanged.connect(self.refresh_suit_list)

        self.main_window.clear_info_Button.clicked.connect(self.main_window.infoTextEdit.clear)
        self.main_window.close_Button.clicked.connect(self.close)
        self._insert_signal.connect(self.main_window.infoTextEdit.appendHtml)

    def init_config(self):
        '''
        Interface initialization configuration:
            1. read the testlink service configuration information from the configuration file
            2. use the configuration information to connect to testlink
            3. get test items and testsuit information
        '''
        try:
            config = utils.read_config_file(CONFIG_FILE)
        except FileNotFoundError as err:
            self.main_window.infoTextEdit.appendHtml(
                '<p>Please config <span style=\" font-weight:600;color:#be2517\">server information</span> first</p>')
            return

        self.server_url = utils.join_url(base=config['server']['server_url'], url=TL_API_PATH)
        self.devkey = config['server']['devkey']
        self.login_name = config['server']['login_name']
        try:
            self.tc = TestlinkAPIClient(self.server_url, self.devkey)
            projects = self.tc.getProjects()
        except (OSError, testlinkerrors.TLResponseError):
            self.main_window.infoTextEdit.appendHtml(
                '<p>Server config is  <span style=\" font-weight:600;color:#be2517\">incorrect</span></p>')
            return
        except testlinkerrors.TLConnectionError as err:
            self.main_window.infoTextEdit.appendHtml('Connect server failed: %s' % str(err))
            return

        self.main_window.case_path_Button.setEnabled(True)

        # Convert the list data about the test project obtained from testlink into a dictionary in the format {'project_name': {'id': 12, 'prefix': 'GS'}}
        for project in projects:
            self.projs_info_dict[project['name']] = {'id': project['id'], 'prefix': project['prefix']}

        self.main_window.proj_comBox.clear()
        for key in self.projs_info_dict:    # refresh the project combox
            self.main_window.proj_comBox.addItem(key)

        self.refresh_suit_list()

    def refresh_suit_list(self):
        '''
        Refresh the testsuit list when the currently selected test item changes
        '''
        self.main_window.target_suitComBox.clear()
        if not self.main_window.proj_comBox.currentText():  # 修复服务参数配置对话框点击确定时，程序崩溃的bug
            return
        self.main_window.target_suitComBox.addItem('/')

        proj_id = self.projs_info_dict[self.main_window.proj_comBox.currentText()]['id']
        try:
            suit_list = self.tc.getFirstLevelTestSuitesForTestProject(proj_id)
            for suit in suit_list:
                self.main_window.target_suitComBox.addItem(suit['name'])
        except testlinkerrors.TLResponseError:
            return

    def import_case(self):
        '''
        Import Test Case
        '''
        self.main_window.infoTextEdit.clear()
        self.main_window.infoTextEdit.appendPlainText(self.tc.connectionInfo())
        info_dict = self.projs_info_dict[self.main_window.proj_comBox.currentText()]

        # 启动一个子进程来处理用例导入，防止导入过程中主界面卡死
        subthread = threading.Thread(target=self._insert_case, args=(self.testcase_file, info_dict,))
        subthread.setDaemon(True)
        subthread.start()

    def _insert_case(self, testcase_file, proj_info):
        '''
        Import test cases into testlink, each sheet page of excel is imported as a testsuit.
        Parameter Description:
            testcase_file: path of the test case, only files with '.xls', '.xlsx' suffix are supported
            proj_info: test project information, formatted as {'id': proj_id, 'prefix': project_prefix}
        '''
        case_book = xlrd.open_workbook(self.testcase_file)
        sheet_list = case_book.sheet_names()
        self.main_window.importButton.setEnabled(False)
        # Each sheet is considered as testsuit
        for item in sheet_list:
            suit_info = self._get_suit_info(item, proj_info)
            sheet = case_book.sheet_by_name(item)
            for i in range(1, sheet.nrows):
                case = sheet.row_values(i)
                case_precondition = case[2]														
                # a testcase which has already existed will not be imported again
                if self.is_testcase_exist(case[0]):
                    self._insert_signal.emit(
                        '<span style=\" font-weight:600;color:#be2517\">TestCase "%s" \
                        is already exist</span>' % case[0])
                    continue
                else:
                    actions_list = case[3].split(DELIMITER)
                    expected_results_list = case[4].split(DELIMITER)
                    for i in range(len(actions_list) - 1):
                        if i == 0:
                            self.tc.initStep("<pre>" + actions_list[i][2:] + "</pre>", "<pre>" + expected_results_list[i][2:] + "</pre>", MANUAL)
                        else:
                            self.tc.appendStep("<pre>" + actions_list[i][2:] + "</pre>", "<pre>" + expected_results_list[i][2:] + "</pre>", MANUAL)
                    self.tc.createTestCase(
                        testcasename=str(case[0]), testsuiteid=suit_info[0]['id'],
                        testprojectid=proj_info['id'], authorlogin=self.login_name, summary='',
                        preconditions=case_precondition, importance=priority_dict[case[1]], executiontype=executiontype_dict[case[5]], status='7')
                    self._insert_signal.emit('Import TestCase：%s' % case[0])
        self.main_window.importButton.setEnabled(True)
        self._insert_signal.emit('\nImport TestCase from %s successed' % self.testcase_file)

    def _get_suit_info(self, suit_name, proj_info):
        '''
        Check whether a suit exist under the target suit which was specified in target_suit combox.
            if suit exsit, a information list about the suit will be returned;
            if not, a new test suit will be created and it's information list.
        suit info format:
            [{'id': 704, 'name': '', 'name_changed': False, 'status': True,
            'operation': 'createTestSuite', 'additionalInfo': '', 'message': 'ok'}]
        '''
        target_suit = self.main_window.target_suitComBox.currentText()

        try:
            test_suit = self.tc.getTestSuite(suit_name, proj_info['prefix'])
        except testlinkerrors.TLResponseError as err:
            if target_suit == '/':
                parentid = proj_info['id']
            else:
                parent_suit = self.tc.getTestSuite(target_suit, proj_info['prefix'])
                parentid = parent_suit[0]['id']
            test_suit = self.tc.createTestSuite(
                testprojectid=proj_info['id'], testsuitename=suit_name, parentid=parentid)
            self._insert_signal.emit('Create TestSuit: %s' % suit_name)
        return test_suit

    def server_config(self):
        '''
        testlink server configuration
        '''
        server_dialog = optionConfig()
        if server_dialog.exec_():
            self.init_config()

    def get_case_path(self):
        self.testcase_file, file_type = QtWidgets.QFileDialog.getOpenFileName(
            self, "Get TestCase", r"/", "Excel(*.xls *xlsx)")
        if os.path.isfile(self.testcase_file):
            self.main_window.case_path.setText(self.testcase_file)
            self.main_window.importButton.setEnabled(True)

    def generate_template(self):
        '''
        Generate test cases
        '''
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Where to save template File?", "/")
        if os.path.isdir(dir_path):
            template_path = os.path.join(dir_path, TEMPLATE_FILE)
        else:
            return
        if os.path.exists(template_path):
            ret = QtWidgets.QMessageBox.question(self, "testlink Helper", "Template exists, overwrite?")
            if ret == QtWidgets.QMessageBox.No:
                return
        else:
            w = xlwt.Workbook()
            sheet = w.add_sheet("test_suit")
            for i in range(5):
                sheet.write(0, i, template_content[i])
                col = sheet.col(i)
                col.width = 256 * 40
            w.save(template_path)
        self._insert_signal.emit("Generate template successed!<br>Path: %s" % template_path)

    def get_help(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/donglin-zhang/testLinkHelper'))

    def about(self):
        QtWidgets.QMessageBox.about(self, "testlink Helper", about_content)

    def is_testcase_exist(self, testcasename):
        '''
        Detects if a test case already exists based on the case name
        Return value.
            Returns True if it exists, False if it does not.
        '''
        try:
            self.tc.getTestCaseIDByName(testcasename)
        except testlinkerrors.TLResponseError as err:
            if 5030 == err.code:
                return False
            else:
                raise Exception("Unexpected error happened: %s" % str(err.message))
        return True


class optionConfig(QtWidgets.QDialog):
    '''
    Configure testlink API information, sever_url, key, user parameters
    '''

    def __init__(self, parent=None):
        super(optionConfig, self).__init__()
        self.ui_dialog = Ui_optionDialog()
        self.ui_dialog.setupUi(self)
        self.init_window()
        self.ui_dialog.acceptButton.clicked.connect(self.write_config)
        self.ui_dialog.cancelButton.clicked.connect(self.reject)

    def init_window(self):
        try:
            self.config = utils.read_config_file(CONFIG_FILE)
        except Exception as err:
            return

        self.ui_dialog.server_urlEdit.setText(self.config['server']['server_url'])
        self.ui_dialog.devkeyEdit.setText(self.config['server']['devkey'])
        self.ui_dialog.proxyEdit.setText(self.config['server']['proxy'])
        self.ui_dialog.login_nameEdit.setText(self.config['server']['login_name'])

    def write_config(self):
        '''
        The configuration is written to the configuration file
        '''
        para_dict = {
            'server': {'server_url': self.ui_dialog.server_urlEdit.text(),
                        'devkey': self.ui_dialog.devkeyEdit.text(),
                        'proxy': self.ui_dialog.proxyEdit.text(),
                        'login_name': self.ui_dialog.login_nameEdit.text()}, }

        utils.write_config_file(CONFIG_FILE, para_dict)
        self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t_helper = testLinkHelper()
    t_helper.show()
    sys.exit(app.exec_())
