from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import webbrowser


class QtApp():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = self.Ui()
        
        self.pdfMdEditText = self.window.findChild(QTextEdit,'pdf_md_edit_text')
        self.pdfStyleEditText = self.window.findChild(QTextEdit,'pdf_style_edit_text')
        
        self.pdfMdSaveBtn = self.window.findChild(QPushButton,'pdf_md_save_btn')
        self.pdfStyleSaveBtn = self.window.findChild(QPushButton, 'pdf_style_save_btn')
        
        self.tempFilePathEditText = self.window.findChild(QLineEdit, 'template_file_path_edit_text')
        self.tempFilePathChooseBtn = self.window.findChild(QPushButton,'template_file_path_choose_btn')
        
        self.styleFilePathEditText = self.window.findChild(QLineEdit, 'style_file_path_edit_text')
        self.styleFilePathChooseBtn = self.window.findChild(QPushButton, 'style_file_path_choose_btn')
        
        self.dataFilePathEdittext = self.window.findChild(QLineEdit,'data_file_path_edit_text')
        self.dataFilePathChooseBtn = self.window.findChild(QPushButton,'data_file_path_choose_btn')
        
        self.outputFnameFormatEditText = self.window.findChild(QLineEdit,'output_fname_format_edit_text')
        
        self.clearBtn = self.window.findChild(QPushButton,'clear_btn')
        self.loadRefreshBtn = self.window.findChild(QPushButton,'load_refresh_btn')
        self.generateBtn = self.window.findChild(QPushButton,'generate_btn')
        
        self.progressText = self.window.findChild(QTextBrowser,'progress_text')
        self.progressBar = self.window.findChild(QProgressBar,'progress_bar')
        
        self.actionDocs = self.window.findChild(QAction,'actionDocs')
        self.actionUpdates = self.window.findChild(QAction,'actionUpdates')
        self.actionIssues = self.window.findChild(QAction,'actionIssues')
        self.actionInfo = self.window.findChild(QAction,'actionInfo')
        self.actionDeveloper = self.window.findChild(QAction,'actionDeveloper')
        self.actionGithub = self.window.findChild(QAction,'actionGithub')
        
        self.state = {
            'markdown_template_file_text': '',
            'style_template_file_text': '',
            'markdown_template_path': '',
            'style_template_path': '',
            'markdown_template_text': '',
            'style_template_text': '',
            'output_dir_path': '',
            'output_file_format': '',
            'progress_text': '',
            'progress_value': ''}
        
        self.attachControls()
        sys.exit(self.app.exec_())

    class Ui(QMainWindow):
        def __init__(self):
            super(QtApp.Ui, self).__init__()
            uic.loadUi('ui.ui', self)
            self.show()
    
    def updateProgressText(self, text):
        self.state['progress_text'] += '\n> {}'.format(text)
        self.progressText.setText(self.state['progress_text'])
    
    def updateMarkdownTemplatePath(self, path):
        self.state['markdown_template_path'] = path
        self.tempFilePathEditText.setText(path)
    
    def updateMarkdownTemplateFileText(self, text):
        self.state['markdown_template_file_text'] = text
        self.pdfMdEditText.setText(self.state['markdown_template_file_text'])
        
    
    
        
    def attachControls(self):
        self.actionDocs.triggered.connect(lambda:webbrowser.open('http://stackoverflow.com'))
        self.actionUpdates.triggered.connect(lambda:webbrowser.open('http://stackoverflow.com'))
        self.actionIssues.triggered.connect(lambda:webbrowser.open('http://stackoverflow.com'))
        self.actionDeveloper.triggered.connect(lambda:webbrowser.open('http://stackoverflow.com'))
        self.actionGithub.triggered.connect(lambda:webbrowser.open('http://stackoverflow.com'))
        
        self.tempFilePathChooseBtn.clicked.connect(self.tempFilePathBtnClick)
    
    
    
    
    
    
    def tempFilePathBtnClick(self):
        if self.state['markdown_template_file_text'] != self.pdfMdEditText.toPlainText():
            if self.showDecisionDialog('Do you want to save the file before opening a new one?'):
                text=self.pdfMdEditText.toPlainText()
                try:
                    file = open(self.state['markdown_template_path'], 'w')
                    file.write(text)
                    file.close()
                    self.updateMarkdownTemplateFileText(text)
                except IOError as e:
                    self.updateProgressText(e)
                    return
                
        path = self.openMarkdownFile()
        if(path.endswith('.md')):
            self.updateMarkdownTemplatePath(path)
            file = open(path, 'r')
            self.updateMarkdownTemplateFileText(file.read())
            file.close()
        else:
            self.updateProgressText('WARNING: Invalid path selected')
    
    
    
    
    
    
    def showDecisionDialog(self, message):
        reply = QMessageBox.question(self.window, 'Info',
        message, QMessageBox.Yes | 
        QMessageBox.No, QMessageBox.No)

        return reply == QMessageBox.Yes 
    
    def openCSVFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Select Data file (.csv)", "","Data (*.csv)")
        return fileName
    
    def openStyleFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Select stylesheet file (.css)", "","Stylesheet (*.css)")
        return fileName
    
    def openMarkdownFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window,"Select template file (.md)", "","Markdown (*.md)")
        return fileName
    

QtApp()
