from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from datetime import datetime

import numpy as np
import pandas as pd
import sys
import webbrowser


class BulkPDFGen:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = self.Ui()

        self.data_file = None

        self.pdfHTMLEditText = self.window.findChild(QTextEdit, 'pdf_html_edit_text')
        self.pdfStyleEditText = self.window.findChild(QTextEdit, 'pdf_style_edit_text')

        self.pdfHTMLSaveBtn = self.window.findChild(QPushButton, 'pdf_html_save_btn')
        self.pdfStyleSaveBtn = self.window.findChild(QPushButton, 'pdf_style_save_btn')

        self.tempFilePathEditText = self.window.findChild(QLineEdit, 'template_file_path_edit_text')
        self.tempFilePathChooseBtn = self.window.findChild(QPushButton, 'template_file_path_choose_btn')

        self.styleFilePathEditText = self.window.findChild(QLineEdit, 'style_file_path_edit_text')
        self.styleFilePathChooseBtn = self.window.findChild(QPushButton, 'style_file_path_choose_btn')

        self.dataFilePathEdittext = self.window.findChild(QLineEdit, 'data_file_path_edit_text')
        self.dataFilePathChooseBtn = self.window.findChild(QPushButton, 'data_file_path_choose_btn')

        self.outputDirPathEditText = self.window.findChild(QLineEdit, 'output_dir_edit_text')
        self.outputDirPathChooseBtn = self.window.findChild(QPushButton, 'output_dir_choose_btn')

        self.outputFnameFormatEditText = self.window.findChild(QLineEdit, 'output_fname_format_edit_text')

        self.clearBtn = self.window.findChild(QPushButton, 'clear_btn')
        self.loadRefreshBtn = self.window.findChild(QPushButton, 'load_refresh_btn')
        self.generateBtn = self.window.findChild(QPushButton, 'generate_btn')

        self.progressText = self.window.findChild(QTextBrowser, 'progress_text')
        self.progressBar = self.window.findChild(QProgressBar, 'progress_bar')

        self.actionDocs = self.window.findChild(QAction, 'actionDocs')
        self.actionUpdates = self.window.findChild(QAction, 'actionUpdates')
        self.actionIssues = self.window.findChild(QAction, 'actionIssues')
        self.actionInfo = self.window.findChild(QAction, 'actionInfo')
        self.actionDeveloper = self.window.findChild(QAction, 'actionDeveloper')
        self.actionGithub = self.window.findChild(QAction, 'actionGithub')

        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self.window)

        self.state = {
            'html_template_file_text': '',
            'style_template_file_text': '',
            'html_template_path': '',
            'style_template_path': '',
            'html_template_text': '',
            'style_template_text': '',
            'data_file_path': '',
            'output_dir_path': '',
            'output_file_format': '',
            'progress_text': '',
            'progress_value': '',
            'process_ongoing': False
        }

        self.attachControls()
        sys.exit(self.app.exec_())

    class Ui(QMainWindow):
        def __init__(self):
            super(BulkPDFGen.Ui, self).__init__()
            uic.loadUi('ui.ui', self)
            self.show()

    class AboutDialogUI(QDialog):
        def __init__(self):
            super(BulkPDFGen.AboutDialogUI,self).__init__()
            uic.loadUi('about.ui',self)
            self.show()

    def updateProgressText(self, text):
        self.state['progress_text'] += '\n> {}'.format(text)
        self.progressText.setText(self.state['progress_text'])
        self.writeToLog(text)

    def updateHTMLTemplatePath(self, path):
        self.state['html_template_path'] = path
        self.tempFilePathEditText.setText(path)

    def updateHTMLTemplateFileText(self, text):
        self.state['html_template_file_text'] = text
        self.pdfHTMLEditText.setPlainText(self.state['html_template_file_text'])

    def updateStyleTemplatePath(self, path):
        self.state['style_template_path'] = path
        self.styleFilePathEditText.setText(path)

    def updateStyleTemplateFileText(self, text):
        self.state['style_template_file_text'] = text
        self.pdfStyleEditText.setText(self.state['style_template_file_text'])

    def updateDataFilePath(self, path):
        self.state['data_file_path'] = path
        self.dataFilePathEdittext.setText(self.state['data_file_path'])

    def updateOutputDirPath(self, path):
        self.state['output_dir_path'] = path
        self.outputDirPathEditText.setText(self.state['output_dir_path'])

    def attachControls(self):
        self.actionDocs.triggered.connect(lambda: webbrowser.open('https://github.com/amannirala13/BulkPDF-Gen'))
        self.actionUpdates.triggered.connect(lambda: webbrowser.open('https://github.com/amannirala13/BulkPDF-Gen'
                                                                     '/releases'))
        self.actionIssues.triggered.connect(
            lambda: webbrowser.open('https://github.com/amannirala13/BulkPDF-Gen/issues'))
        self.actionDeveloper.triggered.connect(lambda: webbrowser.open('https://github.com/amannirala13'))
        self.actionGithub.triggered.connect(lambda: webbrowser.open('https://github.com/amannirala13/BulkPDF-Gen'))
        self.actionInfo.triggered.connect(self.showAboutDialog)

        self.tempFilePathChooseBtn.clicked.connect(self.tempFilePathBtnClicked)
        self.tempFilePathEditText.returnPressed.connect(self.tempFilePathPressedReturn)

        self.styleFilePathChooseBtn.clicked.connect(self.styleFilePathBtnClicked)
        self.styleFilePathEditText.returnPressed.connect(self.styleFilePathPressedReturn)

        self.dataFilePathChooseBtn.clicked.connect(self.dataFilePathBtnClicked)
        self.dataFilePathEdittext.returnPressed.connect(self.dataFilePathPressedReturn)

        self.outputDirPathChooseBtn.clicked.connect(self.outputDirPathBtnClicked)
        self.outputDirPathEditText.returnPressed.connect(self.outputDirPathPressedReturn)

        self.pdfHTMLSaveBtn.clicked.connect(self.pdfHTMLSaveBtnClicked)
        self.pdfStyleSaveBtn.clicked.connect(self.pdfStyleSaveBtnClicked)

        self.clearBtn.clicked.connect(self.resetState)
        self.loadRefreshBtn.clicked.connect(self.loadRefreshBtnClicked)

        self.generateBtn.clicked.connect(self.generateBtnClicked)

        self.shortcut_save.activated.connect(self.shortcut_save_action)

    def tempFilePathPressedReturn(self):
        path = self.tempFilePathEditText.text()
        self.loadTempFile(path)

    def styleFilePathPressedReturn(self):
        path = self.styleFilePathEditText.text()
        self.loadStyleFile(path)

    def dataFilePathPressedReturn(self):
        path = self.dataFilePathEdittext.text()
        self.updateDataFilePath(path)

    def outputDirPathPressedReturn(self):
        path = self.outputDirPathEditText.text()
        self.updateOutputDirPath(path)

    def tempFilePathBtnClicked(self):
        if self.state['html_template_file_text'] != '' and \
                self.state['html_template_file_text'] != self.pdfHTMLEditText.toPlainText():
            if self.showDecisionDialog('Do you want to save the current changes?'):
                self.pdfHTMLSaveBtnClicked()

        path = self.openHTMLFile()
        self.loadTempFile(path)

    def styleFilePathBtnClicked(self):
        if self.state['style_template_file_text'] != self.pdfStyleEditText.toPlainText():
            if self.showDecisionDialog('Do you want to save the current changes?'):
                self.pdfStyleSaveBtnClicked()

        path = self.openStyleFile()
        self.loadStyleFile(path)

    def pdfHTMLSaveBtnClicked(self):
        try:
            text = self.pdfHTMLEditText.toPlainText()
            file = open(self.state['html_template_path'], 'w')
            file.write(text)
            file.close()
            self.updateHTMLTemplateFileText(text)
            self.updateProgressText('Saved {}'.format(self.state['html_template_path']))
        except Exception as e:
            self.updateProgressText(e)
            return

    def pdfStyleSaveBtnClicked(self):
        text = self.pdfStyleEditText.toPlainText()
        try:
            file = open(self.state['style_template_path'], 'w')
            file.write(text)
            file.close()
            self.updateStyleTemplateFileText(text)
            self.updateProgressText('Saved {}'.format(self.state['style_template_path']))
        except Exception as e:
            self.updateProgressText(e)
            return

    def dataFilePathBtnClicked(self):
        path = self.openCSVFile()
        self.updateDataFilePath(path)

    def outputDirPathBtnClicked(self):
        path = self.openOutputDir()
        self.updateOutputDirPath(path)

    def generateBtnClicked(self):
        self.initPDFGeneration()

    def loadRefreshBtnClicked(self):
        self.tempFilePathPressedReturn()
        self.styleFilePathPressedReturn()
        self.dataFilePathPressedReturn()
        self.outputDirPathPressedReturn()

    def shortcut_save_action(self):
        self.pdfHTMLSaveBtnClicked()
        self.pdfStyleSaveBtnClicked()

    def initPDFGeneration(self):
        try:
            self.updateProgressText('Initializing PDF generation...\n----------------------')
            self.state['process_ongoing'] = True
            self.disableUI()
            if not self.validateState():
                self.updateProgressText('----------------------\nAborting PDF generation...')
                self.state['process_ongoing'] = False
                return
            self.data_file = pd.read_csv(self.state['data_file_path'])

            self.updateProgressText('Loaded {} successfully\n----------------------'.format(self.state['data_file_path']))

            key_list = self.data_file.columns

            self.state['output_file_format'] = self.outputFnameFormatEditText.text()

            for index in self.data_file.index:
                value_list = []
                for key in key_list:
                    value_list.append(self.data_file[key][index])
                temp_string = self.getCustomizedHtml(self.state['html_template_file_text'], key_list, value_list)
                file_name = self.getCustomizedFileName(self.state['output_file_format'], key_list, value_list)

                self.progressBar.setValue(((index+1)/len(self.data_file.index))*100)
                self.updateProgressText('Generating {} -> {}/{}'.format(file_name,
                                                                        index+1,
                                                                        len(self.data_file.index)))
                self.generatePDF(temp_string,
                                 self.state['style_template_file_text'],
                                 '{}/{}'.format(self.state['output_dir_path'], file_name))
            self.updateProgressText('----------------------\nFinished successfully')
            self.state['process_ongoing'] = False
            self.enableUI()
        except Exception as e:
            self.updateProgressText(e)
            self.enableUI()

    '''
        md2pdf(self.state['output_dir_path'] + '/test.pdf',
                       md_file_path=self.state['html_template_path'],
                       css_file_path=self.state['style_template_path'])
    '''

    @staticmethod
    def generatePDF(template, style, file_name):
        html_template = HTML(string=template)
        style_template = None if style == '' else [
            CSS(string=style)]
        font_config = FontConfiguration()

        html_template.write_pdf(file_name, stylesheets=style_template, font_config=font_config)

    def showAboutDialog(self):
        about_dialog = self.AboutDialogUI()
        about_dialog.exec_()

    def showDecisionDialog(self, message):
        reply = QMessageBox.question(self.window, 'Attention!',
                                     message, QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        return reply == QMessageBox.Yes

    def loadTempFile(self, path):
        if path.endswith('.html'):
            try:
                self.updateHTMLTemplatePath(path)
                file = open(path, 'r')
                self.updateHTMLTemplateFileText(file.read())
                file.close()
            except Exception as e:
                self.updateProgressText('Error: {}'.format(e))
                return
        else:
            self.updateProgressText('WARNING: Invalid file path selected')

    def loadStyleFile(self, path):
        if path.endswith('.css'):
            try:
                self.updateStyleTemplatePath(path)
                file = open(path, 'r')
                self.updateStyleTemplateFileText(file.read())
                file.close()
            except Exception as e:
                self.updateProgressText('ERROR: {}'.format(e))
        else:
            self.updateProgressText('WARNING: Invalid path selected')

    def openCSVFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self.window, 'Select data file (.csv)', '', 'Data (*.csv)')
        return file_name

    def openStyleFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self.window, 'Select stylesheet file (.css)', '',
                                                   'Stylesheet (*.css)')
        return file_name

    def openHTMLFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self.window, 'Select template file (.html)', '', 'HTML (*.html)')
        return file_name

    def openOutputDir(self):
        dir_name = QFileDialog.getExistingDirectory(self.window, 'Select output directory', '')
        return dir_name

    @staticmethod
    def getCustomizedHtml(text, key_list, value_list):
        for index, key in enumerate(key_list):
            value = '' if index > len(value_list)-1 else value_list[index]
            text = text.replace('%{}%'.format(key), str(value))
        return text

    @staticmethod
    def getCustomizedFileName(name_format, key_list, value_list):
        if name_format == '':
            return '_'.join(map(str, value_list))+'.pdf'

        for index, key in enumerate(key_list):
            value = '' if index > len(value_list)-1 else value_list[index]
            name_format = name_format.replace('%{}%'.format(key), str(value))
            name_format = name_format if name_format.endswith('.pdf') else name_format+'.pdf'
        return name_format

    def validateState(self):
        if self.state['html_template_path'].endswith('.html'):
            if self.state['style_template_path'].endswith('.css') or self.state['style_template_path'] == '':
                if self.state['data_file_path'].endswith('.csv'):
                    if self.state['output_dir_path'] != '':
                        return True
                    else:
                        self.updateProgressText('ERROR: Invalid output directory selected')
                        return False
                else:
                    self.updateProgressText('ERROR: Invalid data(.csv) file path selected')
                    return False
            else:
                self.updateProgressText('ERROR: Invalid style(.css) file path selected')
                return False
        else:
            self.updateProgressText('ERROR: Invalid template(.html) file path selected')
            return False

    def resetState(self):
        if not self.state['process_ongoing']:
            self.state = {
                'html_template_file_text': '',
                'style_template_file_text': '',
                'html_template_path': '',
                'style_template_path': '',
                'html_template_text': '',
                'style_template_text': '',
                'data_file_path': '',
                'output_dir_path': '',
                'output_file_format': '',
                'progress_text': '',
                'progress_value': '',
                'process_ongoing': False}

    def disableUI(self):
        self.tempFilePathChooseBtn.setEnabled(False)
        self.tempFilePathEditText.setEnabled(False)

        self.styleFilePathChooseBtn.setEnabled(False)
        self.styleFilePathEditText.setEnabled(False)

        self.dataFilePathChooseBtn.setEnabled(False)
        self.dataFilePathEdittext.setEnabled(False)

        self.outputDirPathChooseBtn.setEnabled(False)
        self.outputDirPathEditText.setEnabled(False)

        self.pdfHTMLSaveBtn.setEnabled(False)
        self.pdfStyleSaveBtn.setEnabled(False)

        self.clearBtn.setEnabled(False)
        self.loadRefreshBtn.setEnabled(False)

        self.generateBtn.setEnabled(False)

    def enableUI(self):
        self.tempFilePathChooseBtn.setEnabled(True)
        self.tempFilePathEditText.setEnabled(True)

        self.styleFilePathChooseBtn.setEnabled(True)
        self.styleFilePathEditText.setEnabled(True)

        self.dataFilePathChooseBtn.setEnabled(True)
        self.dataFilePathEdittext.setEnabled(True)

        self.outputDirPathChooseBtn.setEnabled(True)
        self.outputDirPathEditText.setEnabled(True)

        self.pdfHTMLSaveBtn.setEnabled(True)
        self.pdfStyleSaveBtn.setEnabled(True)
        self.loadRefreshBtn.setEnabled(True)

        self.clearBtn.setEnabled(True)

        self.generateBtn.setEnabled(True)

    @staticmethod
    def writeToLog(text):
        log = '\n[{}] {}'.format(datetime.now(), text)
        try:
            file = open('log.txt', 'a')
            file.write(log)
            file.close()
        except IOError:
            file = open('log.txt', 'w')
            file.write(log)
            file.close()


BulkPDFGen()
