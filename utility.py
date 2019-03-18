import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QTextDocument ,QTextCursor ,QTextCharFormat ,QFont
from PyQt5.uic import loadUiType
from PyQt5.QtPrintSupport import QPrinter ,QPrintDialog,QPrintPreviewDialog
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from scipy.interpolate import interp1d

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
        self.plot(type="scatter")
        #self.p = plotting(self)
        #self.p.plot()

    def plot(self,Xdata=None,Ydata=None,type="scatter",x_label="x_label",y_label="y_label",color=None):
        box = dict(facecolor='yellow', pad=5, alpha=0.2)
        fig = Figure(figsize=(4, 4), dpi=100,tight_layout=True)
        ax1f1 = fig.add_subplot(111)
        if type == "scatter":
            ax1f1.scatter(Xdata, Ydata,c=color)
        elif type =="line":
            ax1f1.plot(Xdata,Ydata,c=color)
        else:
            pass
        ax1f1.set_xlabel(x_label,bbox=box)
        ax1f1.set_ylabel(y_label,bbox=box)
        ax1f1.set_title("Plot ( "+x_label+" V/S "+y_label+" )")
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(self.mpl_widget)
        self.toolbar = NavigationToolbar(self.canvas,self.mpl_tab, coordinates=True)
        self.canvas.draw()
        self.canvas.show()


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
        self.pushButton_10.clicked.connect(self.scatterPlot)
        self.pushButton_11.clicked.connect(self.linePlot)
        self.pushButton_12.clicked.connect(self.smoothCurve)

    def Show_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Show_Plotting(self):
        self.tabWidget.setCurrentIndex(1)

    def plotColorSelecter(self):
        color = self.comboBox_color.currentText()
        if(color=="Blue"):
            return "b"
        elif (color == "Green"):
            return "g"
        elif(color=="Red"):
            return "r"
        elif(color=="Yellow"):
            return "y"
        elif(color=="Black"):
            return "k"
        elif(color=="Magenta"):
            return "m"
        elif(color=="Cyan"):
            return "c"
        elif(color=="White"):
            return "w"
        else:
            return None

    def linePlot(self):
        x_axis = self.comboBox_X.currentText()
        y_axis = self.comboBox_Y.currentText()

        if (x_axis == y_axis):
            QMessageBox.about(self, 'Important', "X and Y axis can't be same to plot !!!!")
        else:
            xData = np.array(self.df[x_axis]).reshape(-1)
            yData = np.array(self.df[y_axis]).reshape(-1)
            self.plot(xData, yData,type="line",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())

    def scatterPlot(self):
        x_axis = self.comboBox_X.currentText()
        y_axis = self.comboBox_Y.currentText()

        if(x_axis == y_axis):
            QMessageBox.about(self, 'Important', "X and Y axis can't be same to plot !!!!")
        else:
            xData = np.array(self.df[x_axis]).reshape(-1)
            yData = np.array(self.df[y_axis]).reshape(-1)
            self.plot(xData,yData,type="scatter",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())

    def smoothCurve(self):
        x_axis = self.comboBox_X.currentText()
        y_axis = self.comboBox_Y.currentText()

        if (x_axis == y_axis):
            QMessageBox.about(self, 'Important', "X and Y axis can't be same to plot !!!!")
        else:
            xData = np.array(self.df[x_axis]).reshape(-1)
            yData = np.array(self.df[y_axis]).reshape(-1)
            xSmooth = np.linspace(xData.min(),xData.max(),300)
            f = interp1d(xData, yData, kind='quadratic')
            ySmooth=f(xSmooth)
            self.plot(xData, yData, type="scatter", x_label=x_axis, y_label=y_axis)
            self.plot(xSmooth, ySmooth, type="line",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())
    def FileMenu(self):
        #self.actionQuit.triggered.connect(qApp.quit)
        self.actionQuit.triggered.connect(self.closeEvent)
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.file_save)
        self.actionPrint.triggered.connect(self.printCsv)
        self.actionPrint_Preview.triggered.connect(self.handlePreview)
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

    def handlePreview(self, printer):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    def printCsv(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer,self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePaintRequest(self,printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        table = cursor.insertTable(self.tableWidget.rowCount(), self.tableWidget.columnCount())
        fm = QTextCharFormat()
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        fm.setFont(font)
        for i in range(self.tableWidget.columnCount()):
            col = self.tableWidget.horizontalHeaderItem(i).text()
            if col is not None:
                cursor.insertText(col,fm)
            cursor.movePosition(QTextCursor.NextCell)
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                w = self.tableWidget.cellWidget(row, col)
                it = self.tableWidget.item(row, col)
                if w is not None:
                    cursor.insertText(self.get_text_from_widget(w))
                elif it is not None:
                    cursor.insertText(it.text())
                cursor.movePosition(QTextCursor.NextCell)

        document.print_(printer)

    def get_text_from_widget(self,w):
        t = ""
        if isinstance(w):
            t = w.currentText()
        return t
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
                                                  (QDir.homePath() + "/Documents/"), "CSV (*.csv *.tsv *.txt)")
        if fileName:
            self.loadCsv(fileName)

    def fillComboBox(self):
        col = []
        for i in range(self.tableWidget.columnCount()):
            col.append(self.tableWidget.horizontalHeaderItem(i).text())

        self.comboBox_X.insertItems(0,col)
        self.comboBox_Y.insertItems(0,col)
    def loadCsv(self,fileName):
        if fileName:
            self.df = pd.read_csv(fileName)
            #print()
            self.row_count = len(self.df.index)
            self.col_count = len(self.df.columns)
            self.tableWidget.setHorizontalHeaderLabels(list(self.df))
            self.tableWidget.setColumnCount(self.col_count)
            self.tableWidget.setRowCount(self.row_count)
            for i in range(self.row_count):
                for j in range(self.col_count):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
            self.comboBox_X.clear()
            self.comboBox_Y.clear()
            self.fillComboBox()

    def file_save(self):
        if self.tabWidget.currentIndex() == 0:
            name,_ = QFileDialog.getSaveFileName(self, "Save file", (QDir.homePath() + "/Documents/"), "(*.csv *.tsv *.txt)")
            if name:
                self.df.to_csv(name,sep=',',index=False)
                self.isSaved = True
        elif self.tabWidget.currentIndex() == 1:
            name, _ = QFileDialog.getSaveFileName(self, "Save file", (QDir.homePath() + "/Documents/"), "(*.png)")
            if name:
                self.canvas.print_figure(name)
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

class plotting(QMainWindow,ui):
    def __init__(self,MainApp):
        self.plot()
    def plot(self, Xdata=None, Ydata=None, type="scatter", x_label="x_label", y_label="y_label"):
        fig = Figure(figsize=(4, 4), dpi=100)
        ax1f1 = fig.add_subplot(111)
        if type == "scatter":
            ax1f1.scatter(Xdata, Ydata)
        elif type == "line":
            ax1f1.plot(Xdata, Ydata)
        else:
            pass
        ax1f1.set_xlabel(x_label)
        ax1f1.set_ylabel(y_label)
        ax1f1.set_title("Plot")
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(MainApp.mpl_widget)
        self.toolbar = NavigationToolbar(self.canvas, self.mpl_tab, coordinates=True)
        self.canvas.draw()
        self.canvas.show()
def main():

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()