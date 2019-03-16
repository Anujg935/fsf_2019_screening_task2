from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np
import  random

ui,_ = loadUiType('main.ui')



class MainApp(QMainWindow,ui):
    
    def __init__(self):
        self.row_count=17
        self.col_count=8
        self.isSaved = False
        QMainWindow.__init__(self)


        self.setupUi(self)
        self.initial_Table()
        self.FileMenu()
        self.EditMenu()
        self.SetShortcuts()
        self.Hiding_Themes()
        self.Handel_Buttons()
        self.dark_orange_theme()
        self.tabWidget.tabBar().setVisible(False)

    def plot(self, axes):
        x = np.linspace(-10, 10)
        axes.plot(x, x ** 2)
        axes.plot(x, x ** 3)
    def initial_Table(self):
        self.tableWidget.setColumnCount(self.col_count)     
        self.tableWidget.setRowCount(self.row_count)
        
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Show_Themes)
        self.pushButton_6.clicked.connect(self.Hiding_Themes)
        self.pushButton_2.clicked.connect(self.dark_blue_theme)
        self.pushButton_3.clicked.connect(self.dark_gray_theme)
        self.pushButton_4.clicked.connect(self.dark_orange_theme)
        self.pushButton_5.clicked.connect(self.Qdark_theme)
        self.pushButton_7.clicked.connect(self.Show_Home)
        self.pushButton_8.clicked.connect(self.Show_Plotting)
        self.pushButton_9.clicked.connect(self.file_save)


    def Show_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Show_Plotting(self):
        self.tabWidget.setCurrentIndex(1)
        
    def FileMenu(self):
        #self.actionQuit.triggered.connect(qApp.quit)
        self.actionQuit.triggered.connect(self.closeEvent)
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.file_save)
        
    def EditMenu(self):
        self.actionAdd_Row.triggered.connect(self.AddRow)
        self.actionAdd_Column.triggered.connect(self.AddCol)
        self.actionRemove_Row.triggered.connect(self.removeRow)
        self.actionRemove_Column.triggered.connect(self.removeCol)
    
    def AddRow(self):
        self.row_count += 1     
        self.tableWidget.setRowCount(self.row_count)
    
    def AddCol(self):
        self.col_count += 1
        self.tableWidget.setColumnCount(self.col_count)
        
    def removeCol(self):
        self.tableWidget.removeColumn(self.tableWidget.currentColumn())
        
    def removeRow(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow()) 
        
    def SetShortcuts(self):
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionQuit.setShortcut("Ctrl+Q")
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
                                                  (QDir.homePath() + "/Documents/"), "CSV (*.csv *.tsv *.txt)")
        if fileName:
            self.loadCsv(fileName)


    def loadCsv(self,fileName):
        if fileName:
            df = pd.read_csv(fileName)
            #print()
            self.row_count = len(df.index)
            self.col_count = len(df.columns)
            self.tableWidget.setHorizontalHeaderLabels(list(df))
            self.tableWidget.setColumnCount(len(df.columns))     
            self.tableWidget.setRowCount(len(df.index))
            for i in range(len(df.index)):
                for j in range(len(df.columns)):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
                    
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            
    def file_save(self):
        name,_ = QFileDialog.getSaveFileName(self, "Save file", (QDir.homePath() + "/Documents/"), "(*.csv *.tsv *.txt)")
        if name:
            data = np.zeros((self.tableWidget.rowCount(),self.tableWidget.columnCount()))
            for i in range(self.tableWidget.rowCount()):
                for j in range(self.tableWidget.columnCount()):
                    print(self.tableWidget.item(i, j).text())
                    data[i][j] = self.tableWidget.item(i, j).text()
            
            #col = []
            #for i in range(self.tableWidget.columnCount):
                #col[i] = self.tableWidget.horizontalHeaderItem(str(i)).text()
            #print(col)

            col = self.tableWidget.horizontalHeaderLabels()
            print(col)
            df =pd.DataFrame(data)
            df.to_csv(name,sep=',',index=False)
            self.isSaved = True
    
    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        if self.isSaved == False:
            reply = QMessageBox.question(
                self, "Message",
                "Are you sure you want to quit? Any unsaved work will be lost.",
                QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
                QMessageBox.Save)

            if reply == QMessageBox.Close:
                event.accept()
            elif reply == QMessageBox.Save:
                self.file_save()
            else:
                QMessageBox.close()
        else:
            pass
            
    def Show_Themes(self):
        self.groupBox.show()

    def Hiding_Themes(self):
        self.groupBox.hide()
    
    ########################################
    ############## UI Themes ###############

    def dark_blue_theme(self):
        style = open('themes/darkblue.css','r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_gray_theme(self):
        style = open('themes/darkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange_theme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Qdark_theme(self):
        style = open('themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()