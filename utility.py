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
        self.isChanged =False
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initial_Table()
        self.FileMenu()
        self.EditMenu()
        self.TabsMenu()
        self.SettingsMenu()
        self.SetShortcuts()
        self.Hiding_Themes()
        self.Handel_Buttons()
        self.setButtonToolTip()
        self.dark_orange_theme()
        self.tabWidget.tabBar().setVisible(False)
        self.plot(type="scatter")
        self.saveButtonText()

    def plot(self,Xdata=None,Ydata=None,type="scatter",x_label="x_label",y_label="y_label",color=None):
        """
        This is the function that performs all the things to plot the graph
        it takes many parameters like labels,type and colour,data
        based on these parameters data is plotted .
        :param Xdata: 
        :param Ydata: 
        :param type: 
        :param x_label: 
        :param y_label: 
        :param color: 
        :return: 
        """
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
        ax1f1.yaxis.grid(True )
        ax1f1.xaxis.grid(True)
        self.canvas = FigureCanvas(fig)
        self.canvas.setParent(self.mpl_widget)
        self.toolbar = NavigationToolbar(self.canvas,self.mpl_tab, coordinates=True)
        self.canvas.draw()
        self.canvas.show()


    def initial_Table(self):
        self.tableWidget.setColumnCount(self.col_count)
        self.tableWidget.setRowCount(self.row_count)

    def Handel_Buttons(self):
        '''
            This function handles all the Push buttons in 
            the application and call their respective functions 
            when the button is clicked .
        '''
        self.pushButton.clicked.connect(self.Show_Themes)
        self.pushButton_6.clicked.connect(self.Hiding_Themes)
        self.pushButton_2.clicked.connect(self.dark_blue_theme)
        self.pushButton_3.clicked.connect(self.dark_gray_theme)
        self.pushButton_4.clicked.connect(self.dark_orange_theme)
        self.pushButton_5.clicked.connect(self.Qdark_theme)
        self.pushButton_7.clicked.connect(self.Show_Home)
        self.pushButton_8.clicked.connect(self.Show_Plotting)
        self.pushButton_9.clicked.connect(self.save)
        self.pushButton_10.clicked.connect(self.scatterPlot)
        self.pushButton_11.clicked.connect(self.linePlot)
        self.pushButton_12.clicked.connect(self.smoothCurve)
        self.pushButton_13.clicked.connect(self.loadCsv)
        self.pushButton_14.clicked.connect(self.printCsv)
        self.pushButton_15.clicked.connect(self.handlePreview)

    def setButtonToolTip(self):
        '''
            This functions sets tooltip to required buttons. 
        '''
        self.pushButton.setToolTip("Change Theme")
        self.pushButton_7.setToolTip("Home View CSV ")
        self.pushButton_8.setToolTip("Plot Data")
        self.pushButton_14.setToolTip("Print CSV")
        self.pushButton_15.setToolTip("Print Preview")
        self.pushButton_13.setToolTip("Open CSV File")

    def Show_Home(self):
        '''
            This function is called to move the tabWidget to
            index 0 that contains the contains csv file 
        '''
        self.tabWidget.setCurrentIndex(0)
        self.saveButtonText()

    def Show_Plotting(self):
        '''
            This function is called to move the tabWidget to
            index 1 that contains the contains plotting  
        '''
        self.tabWidget.setCurrentIndex(1)
        self.saveButtonText()

    def plotColorSelecter(self):
        '''
            This function is used to select the colour of the
            line or points in the line or scatter plot          
        '''
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
        '''
            This function is used to plot line plot
            to the canvas figure  
        '''
        x_axis = self.comboBox_X.currentText()
        y_axis = self.comboBox_Y.currentText()

        if (x_axis == y_axis):
            QMessageBox.about(self, 'Important', "X and Y axis can't be same to plot !!!!")
        else:
            xData = np.array(self.df[x_axis]).reshape(-1)
            yData = np.array(self.df[y_axis]).reshape(-1)
            self.plot(xData, yData,type="line",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())

    def scatterPlot(self):
        '''
            This function is used to plot scatter plot
            to the canvas figure  
        '''
        x_axis = self.comboBox_X.currentText()
        y_axis = self.comboBox_Y.currentText()

        if(x_axis == y_axis):
            QMessageBox.about(self, 'Important', "X and Y axis can't be same to plot !!!!")
        else:
            xData = np.array(self.df[x_axis]).reshape(-1)
            yData = np.array(self.df[y_axis]).reshape(-1)
            self.plot(xData,yData,type="scatter",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())

    def smoothCurve(self):
        '''
            This function is used to plot smooth line
            to the canvas figure  
        '''
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
            self.plot(xSmooth, ySmooth, type="scatter",x_label=x_axis,y_label=y_axis,color=self.plotColorSelecter())

    def FileMenu(self):
        """
            This function is used to handle all the the events
            under the "File" menu
        """
        self.actionQuit.triggered.connect(self.closeEvent)
        self.actionOpen.triggered.connect(self.loadCsv)
        self.actionSave.triggered.connect(self.save)
        self.actionPrint.triggered.connect(self.printCsv)
        self.actionPrint_Preview.triggered.connect(self.handlePreview)
        self.actionSave_as_Png.triggered.connect(self.saveAsPng)
        self.actionExport_To_Excel.triggered.connect(self.writeXlsx)
        self.actionRetain_Selected_Row_Columns.triggered.connect(self.retain)
    def EditMenu(self):
        """
            This function is used to handle all the the events
            under the "Edit" menu
        """
        self.actionEdit.triggered.connect(self.edit)
        self.actionAdd_Row.triggered.connect(self.AddRow)
        self.actionAdd_Column.triggered.connect(self.AddCol)
        self.actionRemove_Row.triggered.connect(self.removeRow)
        self.actionRemove_Column.triggered.connect(self.removeCol)
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionCut.triggered.connect(self.cut)

    def TabsMenu(self):
        """
            This function is used to handle all the the events
            under the "Tabs" menu
        """
        self.actionHome.triggered.connect(self.Show_Home)
        self.actionPlotting.triggered.connect(self.Show_Plotting)

    def SettingsMenu(self):
        self.actionChange_Theme.triggered.connect(self.Show_Themes)

    def edit(self):
        data = np.zeros((self.tableWidget.rowCount(), self.tableWidget.columnCount()))
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                data[i][j] = self.tableWidget.item(i, j).text()

        col = []
        for i in range(self.col_count):
            col.append(self.tableWidget.horizontalHeaderItem(i).text())
        d = pd.DataFrame(data, columns=col)
        self.df  = d

    def AddRow(self):
        """
            This function is used to add row
        """
        self.row_count += 1     
        self.tableWidget.setRowCount(self.row_count)
        self.isChanged = True
    
    def AddCol(self):
        """
            This function is used to add column
        """
        self.col_count += 1
        self.tableWidget.setColumnCount(self.col_count)
        self.isChanged = True
        
    def removeCol(self):
        """
            This function is used to remove selected column
        """
        self.tableWidget.removeColumn(self.tableWidget.currentColumn())
        self.row_count -= 1
        self.isChanged = True
        
    def removeRow(self):
        """
            This function is used to remove selected row
        """
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.row_count += 1
        self.isChanged = True

    def copy(self):
        """
            Copies the content of the selected cell
        
        """
        if self.tabWidget.currentIndex() == 0:
            clip = QApplication.clipboard()
            for content in self.tableWidget.selectedItems():
                if content.text() is not None:
                    clip.setText(content.text())
        else:
            pass

    def cut(self):
        """
            Cuts the content of the selected cell
        """
        if self.tabWidget.currentIndex() == 0:
            clip = QApplication.clipboard()
            for content in self.tableWidget.selectedItems():
                row = content.row()
                col = content.column()
                if content.text() is not None:
                    clip.setText(content.text())
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str()))
            self.isChanged = True
        else:
            pass

    def paste(self):
        """
            Paste the content to all selected cells
        """
        if self.tabWidget.currentIndex() == 0:
            clip = QApplication.clipboard()
            for content in self.tableWidget.selectedItems():
                row = content.row()
                col = content.column()
                if content.text() is not None:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(clip.text())))
            self.isChanged = True
        else:
            pass

    def retain(self):
        if self.tabWidget.currentIndex() == 0:
            i=0
            #range = self.tableWidget.selectedRanges()
            #print(range.row(),range.column())
            rows =[]
            cols =[]
            for content in self.tableWidget.selectedItems():
                #index.append(content.row(),content.column())
                print(content.row(),content.column())
                rows.append(content.row())
                cols.append(content.column())
                #if content.text() is not None:
                    #self.tableWidget.setItem(row, col, QTableWidgetItem(str(clip.text())))
                    #self.tableWidget.setItem(row, col, QTableWidgetItem(str(clip.text())))

            row_max = max(rows)
            row_min = min(rows)
            col_max = max(cols)
            col_min = min(cols)
            print("removing")
            print(len(rows),len(cols))
            for i in range(-1,row_min):
                self.tableWidget.removeRow(i)
                print("row",i)
            for i in range(row_max+1,self.row_count):
                self.tableWidget.removeRow(i)
                print("row", i)
            for i in range(-1,col_min):
                self.tableWidget.removeColumn(i)
                print("col", i)
            for i in range(col_max+1,self.col_count):
                self.tableWidget.removeColumn(i)
                print("col", i)
            self.isChanged = True
        else:
            pass
    def SetShortcuts(self):
        """
            This function is used to set keyboard shortcuts to
            important operations
        """
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionQuit.setShortcut("Ctrl+Q")
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCut.setShortcut("Ctrl+X")
        self.actionPaste.setShortcut("Ctrl+V")
        self.actionPrint.setShortcut("Ctrl+P")

    def handlePreview(self, printer):
        """
            This function handles the printPreview Functionality 
            of the csv file in the GUI app an opens print preview window
        :param printer: 
        :return: 
        """
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def printCsv(self):
        """
            This is used open the print diaglog to select the printer and
            other properties to print the csv file currently viewed
            or edited in the application
        :return: 
        """
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer,self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePaintRequest(self,printer):
        """
            This is the backbone main function that handles all the 
            print functions PrintPreview and PrintCsv .
            This handles all the required operations like bolding the header labels
            and all the other things like moving the cursor for each cell 
            row and column wise and finally printing to document.
        :param printer: 
        :return: 
        """
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
        """
            This is a additional function which is used bu y the print functions
            this is used to get and return text from the widget 
        :param w: 
        :return: 
        """
        t = ""
        if isinstance(w):
            t = w.currentText()
        return t

    def writeXlsx(self):
        """
            This function is used to export the csv file as Xslx
            file.
        :return: 
        """
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Xlsx",
                                                  (QDir.homePath() + "/Documents/"), "Excel (*.xlsx)")
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        self.df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()


    def fillComboBox(self):
        """
            This is te function that fills the combobox to select the columns
            to select plots it fills both the cobobox with the header labels
        :return: 
        """
        col = []
        for i in range(self.tableWidget.columnCount()):
            col.append(self.tableWidget.horizontalHeaderItem(i).text())

        self.comboBox_X.insertItems(0,col)
        self.comboBox_Y.insertItems(0,col)

    def fillRowComboBox(self):

        for i in range(self.row_count):
            self.comboBox_X_2.insertItems(i,QString(i+1))
            self.comboBox_X_3.insertItems(i,i+1)

    def loadCsv(self):
        """
            This is the function that opens the filedialog to open csv file
            it opens the csv file and view it as qtablewidget in the GUI app
        :return: 
        """
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
                                                  (QDir.homePath() + "/Documents/"), "CSV (*.csv *.tsv *.txt)")
        if fileName:
            self.df = pd.read_csv(fileName)
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
            #self.fillRowComboBox()
    def saveButtonText(self):
        """
            This is the function which handles the text of the save button
            If current tab is for csv reding than the text on the button is to " Save Csv"
            and if the current tab is plotting than the text is to "Save as Png"
        :return: 
        """
        if self.tabWidget.currentIndex() == 0:
            self.pushButton_9.setText("Save Csv File")
            self.pushButton_9.setToolTip("Save CSV File")
        elif self.tabWidget.currentIndex() == 1:
            self.pushButton_9.setText("Save Plot \n as png")
            self.pushButton_9.setToolTip("Save Graph Plot")

    def saveCsv(self):
        """
            This function is used to save the csv file 
        :return: 
        """
        name,_ = QFileDialog.getSaveFileName(self, "Save file", (QDir.homePath() + "/Documents/"), "(*.csv *.tsv *.txt)")
        if name:
            self.df.to_csv(name,sep=',',index=False)
            self.isSaved = True
            self.isChanged = False

    def saveAsPng(self):
        """
            This function is used to save the plot image as png
        :return: 
        """
        name, _ = QFileDialog.getSaveFileName(self, "Save file", (QDir.homePath() + "/Documents/"), "(*.png)")
        if name:
            self.canvas.print_figure(name)

    def save(self):
        """
            This function calls the saveaspng or savecsv function
            based on the current active tab on the gui app
        :return: 
        """
        if self.tabWidget.currentIndex() == 0:
            self.saveCsv()
        elif self.tabWidget.currentIndex() == 1:
            self.saveAsPng()



    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        if self.isChanged == True:
            reply = QMessageBox.question(
                self, "Message",
                "Are you sure you want to quit? Any unsaved work will be lost.",
                QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
                QMessageBox.Save)

            if reply == QMessageBox.Close:
                qApp.quit
            elif reply == QMessageBox.Save:
                self.save()
            else:
                QMessageBox.close()
        else:
            pass
            
    def Show_Themes(self):
        """
            when change themes button is clicked this function is called and
            it will show groupbox to change the theme
        :return: 
        """
        self.groupBox.show()

    def Hiding_Themes(self):
        """
            It will hide the groupbox 
        :return: 
        """
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