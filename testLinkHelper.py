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
        self.main_window.save_info_Button.clicked.connect(self.save_info)
        self._insert_signal.connect(self.main_window.infoTextEdit.appendHtml)

    def init_config(self):
        '''
        get project names from testlink
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
                '<p>Server config is  <span style=\" font-weight:600;color:#be2517\">incorrect</span> first</p>')
            return
        except testlinkerrors.TLConnectionError as err:
            self.main_window.infoTextEdit.appendHtml('Connect server failed: %s' % str(err))
            return

        for project in projects:
            self.projs_info_dict[project['name']] = {'id': project['id'], 'prefix': project['prefix']}
        self.main_window.proj_comBox.clear()
        for key in self.projs_info_dict:
            self.main_window.proj_comBox.addItem(key)
        self.refresh_suit_list()

    def refresh_suit_list(self):
        self.main_window.target_suitComBox.clear()
        self.main_window.target_suitComBox.addItem('/')
        proj_id = self.projs_info_dict[self.main_window.proj_comBox.currentText()]['id']
        suit_list = self.tc.getFirstLevelTestSuitesForTestProject(proj_id)
        for suit in suit_list:
            self.main_window.target_suitComBox.addItem(suit['name'])

    def import_case(self):
        self.main_window.infoTextEdit.clear()
        self.main_window.infoTextEdit.appendPlainText(self.tc.connectionInfo())
        info_dict = self.projs_info_dict[self.main_window.proj_comBox.currentText()]

        subthread = threading.Thread(target=self._insert_case, args=(self.testcase_file, info_dict,))
        subthread.setDaemon(True)
        subthread.start()

    def _insert_case(self, testcase_file, proj_info):
        '''
        insert testcase into testlink
        parameters:
            testcase_file: file_path of testcase file, only postfix '.xls','.xlsx' supported
            proj_info: a dict include projcet informaition, such as {'id': proj_id, 'prefix': project_prefix}
        '''
        case_book = xlrd.open_workbook(self.testcase_file)
        sheet_list = case_book.sheet_names()

        for item in sheet_list:
            suit_info = self._get_suit_info(item, proj_info)
            sheet = case_book.sheet_by_name(item)
            for i in range(1, sheet.nrows):
                case = sheet.row_values(i)
                case_precondition = case[2]
                self.tc.stepsList = [{
                            'step_number': 1,
                            'actions': case[3].replace('\n', '<br>'),
                            'expected_results': case[4].replace('\n', '<br>'),
                            'execution_type': 0}, ]
                self.tc.createTestCase(
                    testcasename=str(case[0]), testsuiteid=suit_info[0]['id'],
                    testprojectid=proj_info['id'], authorlogin=self.login_name, summary='',
                    preconditions=case_precondition, importance=HIGH, status='7')
                self._insert_signal.emit('Import TestCase：%s' % case[0])
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
        '''
        server_dialog = optionConfig()
        if server_dialog.exec_():
            self.init_config()

    def get_case_path(self):
        self.testcase_file, file_type = QtWidgets.QFileDialog.getOpenFileName(
            self, "Get TestCase", r"/", "Excel(*.xls *xlsx)")
        self.main_window.case_path.setText(self.testcase_file)

    def generate_template(self):
        '''
        generate a template file about how to write testcases.
        '''
        basedir = os.path.dirname(__file__)
        if os.path.exists(TEMPLATE_FILE):
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
            w.save(TEMPLATE_FILE)
        QtWidgets.QMessageBox.information(
            self, "testlink Helper", "Generate template successed!\nPath: %s" % os.path.join(basedir, TEMPLATE_FILE))

    def get_help(self):
        QtWidgets.QMessageBox.information(self, "testlink Helper", "get_help")

    def about(self):
        QtWidgets.QMessageBox.about(self, "testlink Helper", about_content)

    def save_info(self):
        QtWidgets.QMessageBox.information(self, "testlink Helper", "save_info")


class optionConfig(QtWidgets.QDialog):
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
