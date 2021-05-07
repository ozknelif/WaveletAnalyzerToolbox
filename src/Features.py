import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import numpy as np
import statistics
import pandas as pd
import scipy.stats
from os import walk

def ent(data):
    pd_data = pd.Series(data)
    p_data = pd_data.value_counts()  # counts occurrence of each value
    entropy = scipy.stats.entropy(p_data)  # get entropy from counts
    return entropy

def average(list):
    return sum(list) / len(list)

def message(info, type):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon('icon/icon.png'))
    msg.setWindowTitle('Wavelet Toolbox')
    msg.setIcon(type)
    msg.setText(info)
    msg.exec_()

def center(self):
    frameGm = self.frameGeometry()
    screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
        PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())

def load_signal(self):
    filename, filter = QFileDialog.getOpenFileNames(self, "Music" ,r"", "(*.au *.waw *.mp3)")
    if filename:
        return filename , filter , True
    else:
        return '', '', False

def load_folder(self):
    file = str(QFileDialog.getExistingDirectory(self, "Select Directory",""))
    if (file):
        file = file + '/'
        filepath = []
        for (root, dirs, files) in walk(file):
            if(dirs == []):
                for cur_file in files:
                    string = cur_file.split('.')
                    if(string[-1] == "waw" or string[-1] == "au" or string[-1] == "mp3"):
                        if(root[-1] == '/'):
                            filepath.append(root + cur_file)
                        else:
                            filepath.append(root + '/' + cur_file)
        return filepath, True
    else:
        return [], False

def checked_functions(self):
    functions = []
    if self.checkBox_randomForest.isChecked():
        functions.append(1)
    if self.checkBox_knn.isChecked():
        functions.append(2)
    if self.checkBox_svcPoly.isChecked():  # prediction page checks
        functions.append(3)
    if self.checkBox_gaussianNB.isChecked():
        functions.append(4)
    if self.checkBox_svcLinear.isChecked():
        functions.append(5)
    if self.checkBox_svcRBF.isChecked():
        functions.append(6)
    return functions

def  check_statistics(self):
    return (self.checkBox_1D_Average.isChecked(),
           self.checkBox_1D_Entropy.isChecked(),
           self.checkBox_1D_Kurtosis.isChecked(),
           self.checkBox_1D_Max.isChecked(),                       #discrete page statistic functions checks
           self.checkBox_1D_Median.isChecked() ,
           self.checkBox_1D_Min.isChecked(),
           self.checkBox_1D_Skewness.isChecked(),
           self.checkBox_1D_StandartDeviation.isChecked())

def discrete_check_wavelet(self):
    return self.comboBox_1D_Type.currentText(),self.comboBox_1D_Level.currentData()         # check wavelet type and wavelet level

def cont_check_wavelet(self):
    return self.comboBox_1DCont_Type.currentText(), self.edit_sampling_period.text(), self.edit_min_scale.text(), self.edit_max_scale.text(), self.edit_scale_step.text()

def discrete_clear_canvas(self):
    for i in range(0, self.clear_count):
        self.MplWidget.canvas.axes = self.MplWidget.canvas.figure.add_subplot(self.clear_count * 100 + 11 + i)
        self.MplWidget.canvas.axes.remove()
        self.MplWidget.canvas.draw()
    self.clear_count = 0

def discrete_plot_signal(self):
    if (self.clear_count > 0):                                                    #eğer ekranda oluşturulmuş sinyal sayısı 0 dan büyükse ekran temizlenmelidir
        discrete_clear_canvas(self)
    for i in range (0, len(self.signals)):
        self.MplWidget.canvas.axes = self.MplWidget.canvas.figure.add_subplot((len(self.signals)) * 100 + 11 + i)
        self.MplWidget.canvas.axes.plot(np.arange(0, len(self.signals[i])) / self.sample, self.signals[i])                                #wavelet sinyalleri
        self.MplWidget.canvas.draw()

    self.clear_count = len(self.signals)

def list_db_tables(self, table_names):
    print(table_names)
    self.dbTables_listWidget.setStyleSheet("QListWidget::item { height: 25px; border-bottom: 1px solid black; } QListWidget::item:selected {border: 1px solid blue; background-color: white; color: black}" )
    for i in range (0,len(table_names)):
        self.dbTables_listWidget.addItem(str(table_names[i]))


def init_table(self, row):
    col, header, db_header = addHeader(self)  # header kısmını ekleme
    self.tableWidget_1D_matrix.setRowCount(row)
    self.tableWidget_1D_matrix.setColumnCount(col * (self.wavelet_level + 1))
    self.tableWidget_1D_matrix.setHorizontalHeaderLabels(header)
    return col, header, db_header

def addHeader(self):
    col = 0                                                                     #kaç kolon olacağını tutan değişken
    header = []                                                                 #header stringinin tutulacağı dizi
    db_header = ["A" + str(self.wavelet_level) + "_Average",
                 "A" + str(self.wavelet_level) + "_Entropy",
                 "A" + str(self.wavelet_level) + "_Kurtosis",
                 "A" + str(self.wavelet_level) + "_Max",
                 "A" + str(self.wavelet_level) + "_Min",
                 "A" + str(self.wavelet_level) + "_Median",
                 "A" + str(self.wavelet_level) + "_Skewness",
                 "A" + str(self.wavelet_level) + "_Standart"]

    if (self.average):
        col += 1
        header.append("A"+str(self.wavelet_level)+"_Average")
    if (self.entropy):
        col += 1
        header.append("A"+str(self.wavelet_level)+"_Entropy")
    if (self.kurtosis):
        col += 1
        header.append("A"+str(self.wavelet_level)+"_Kurtosis")
    if (self.max_v):
        col += 1
        header.append("A"+str(self.wavelet_level)+ "_Max")
    if (self.min_v):
        col += 1
        header.append("A"+str(self.wavelet_level)+ "_Min")
    if (self.median):
        col += 1
        header.append("A" + str(self.wavelet_level) + "_Median")
    if (self.skewness):
        col += 1
        header.append("A"+str(self.wavelet_level)+ "_Skewness")
    if (self.standart_dev):
        col += 1
        header.append("A"+str(self.wavelet_level)+  "_Standart")

    for i in range(0 , self.wavelet_level):
        db_header.append("D" + str(self.wavelet_level - i) + "_Average")
        db_header.append("D" + str(self.wavelet_level - i) + "_Entropy")
        db_header.append("D" + str(self.wavelet_level - i) + "_Kurtosis")
        db_header.append("D" + str(self.wavelet_level - i) + "_Max")
        db_header.append("D" + str(self.wavelet_level - i) + "_Min")
        db_header.append("D" + str(self.wavelet_level - i) + "_Median")
        db_header.append("D" + str(self.wavelet_level - i) + "_Skewness")
        db_header.append("D" + str(self.wavelet_level - i) + "_Standart")

        if (self.average):
            header.append("D" + str(self.wavelet_level - i) + "_Average")
        if (self.entropy):
            header.append("D" + str(self.wavelet_level - i) + "_Entropy")
        if (self.kurtosis):
            header.append("D" + str(self.wavelet_level - i) + "_Kurtosis")
        if (self.max_v):
            header.append("D" + str(self.wavelet_level - i) + "_Max")
        if (self.min_v):
            header.append("D" + str(self.wavelet_level - i) + "_Min")
        if (self.median):
            header.append("D" + str(self.wavelet_level - i) +"_Median")
        if (self.skewness):
            header.append("D" + str(self.wavelet_level - i) + "_Skewness")
        if (self.standart_dev):
            header.append("D" + str(self.wavelet_level - i) + "_Standart")

    return col , header, db_header

def insertTable(self, row, col):
    default_float = 0.0
    avg_results = []
    entropy_results = []
    kurtosis_results = []
    max_v_results = []
    min_v_results = []
    median_results = []
    skewness_results = []
    standartDev_results = []
    row_array = []
    db_row_array = []

    for i in range(1, self.wavelet_level + 2):                      # ilk sinyal source onu dahil etmiyoruz
        if (self.average):
            avg_results.append(average(self.signals[i]))
        if (self.entropy):
            entropy_results.append(ent(self.signals[i]))
        if (self.kurtosis):
            kurtosis_results.append(np.float64(scipy.stats.kurtosis(self.signals[i])))
        if (self.max_v):
            max_v_results.append(np.float64(max(self.signals[i])))
        if (self.min_v):
            min_v_results.append(np.float64(min(self.signals[i])))
        if (self.median):
            median_results.append(np.float64(statistics.median(self.signals[i])))
        if (self.skewness):
            skewness_results.append(np.float64(scipy.stats.skew(self.signals[i])))
        if (self.standart_dev):
            standartDev_results.append(np.float64(np.std(self.signals[i])))

    for i in range(0, col * (self.wavelet_level + 1), col):
        iter = 0

        if (self.average):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(avg_results[int(i / col)])))             #tablewidget üzerine değerleri yazma
            row_array.append(avg_results[int(i / col)])
            iter += 1
        if (not self.average):
            row_array.append(default_float)

        if (self.entropy):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(entropy_results[int(i / col)])))
            row_array.append(entropy_results[int(i / col)])
            iter += 1
        if (not self.entropy):
            row_array.append(default_float)


        if (self.kurtosis):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(kurtosis_results[int(i / col)])))
            row_array.append(kurtosis_results[int(i / col)])
            iter += 1
        if (not self.kurtosis):
            row_array.append(default_float)


        if (self.max_v):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(max_v_results[int(i / col)])))
            row_array.append(max_v_results[int(i / col)])
            iter += 1
        if (not self.max_v):
            row_array.append(default_float)

        if (self.min_v):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(min_v_results[int(i / col)])))
            row_array.append(min_v_results[int(i / col)])
            iter += 1
        if (not self.min_v):
            row_array.append(default_float)

        if (self.median):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(median_results[int(i / col)])))
            row_array.append(median_results[int(i / col)])
            iter += 1
        if (not self.median):
            row_array.append(default_float)

        if (self.skewness):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(skewness_results[int(i / col)])))
            row_array.append(skewness_results[int(i / col)])
            iter += 1
        if (not self.skewness):
            row_array.append(default_float)

        if (self.standart_dev):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(standartDev_results[int(i / col)])))
            row_array.append(standartDev_results[int(i / col)])
            iter += 1
        if (not self.standart_dev):
            row_array.append(default_float)

    return row_array


def insertTableComplex(self, row, col):
    default_value = np.complex(0)
    avg_results = []
    entropy_results = []
    kurtosis_results = []
    max_v_results = []
    min_v_results = []
    median_results = []
    skewness_results = []
    standartDev_results = []
    row_array = []

    for i in range(1, self.wavelet_level + 2):                      # ilk sinyal source onu dahil etmiyoruz
        if (self.average):
            avg_results.append(average(self.signals[i]))
        if (self.entropy):
            entropy_results.append(ent(self.signals[i]))
        if (self.kurtosis):
            kurtosis_results.append(np.complex(scipy.stats.kurtosis(self.signals[i])))
        if (self.max_v):
            max_v_results.append(np.complex(max(self.signals[i])))
        if (self.min_v):
            min_v_results.append(np.complex(min(self.signals[i])))
        if (self.median):
            median_results.append(np.complex(statistics.median(self.signals[i])))
        if (self.skewness):
            skewness_results.append(np.complex(scipy.stats.skew(self.signals[i])))
        if (self.standart_dev):
            standartDev_results.append(np.complex(np.std(self.signals[i])))

    for i in range(0, col * (self.wavelet_level + 1), col):
        iter = 0

        if (self.average):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(avg_results[int(i / col)])))             #tablewidget üzerine değerleri yazma
            row_array.append(avg_results[int(i / col)])
            iter += 1
        if (not self.average):
            row_array.append(default_value)

        if (self.entropy):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(entropy_results[int(i / col)])))
            row_array.append(entropy_results[int(i / col)])
            iter += 1
        if (not self.entropy):
            row_array.append(default_value)


        if (self.kurtosis):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(kurtosis_results[int(i / col)])))
            row_array.append(kurtosis_results[int(i / col)])
            iter += 1
        if (not self.kurtosis):
            row_array.append(default_value)

        if (self.max_v):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(max_v_results[int(i / col)])))
            row_array.append(max_v_results[int(i / col)])
            iter += 1
        if (not self.max_v):
            row_array.append(default_value)

        if (self.min_v):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(min_v_results[int(i / col)])))
            row_array.append(min_v_results[int(i / col)])
            iter += 1
        if (not self.min_v):
            row_array.append(default_value)

        if (self.median):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(median_results[int(i / col)])))
            row_array.append(median_results[int(i / col)])
            iter += 1
        if (not self.median):
            row_array.append(default_value)

        if (self.skewness):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(skewness_results[int(i / col)])))
            row_array.append(skewness_results[int(i / col)])
            iter += 1
        if (not self.skewness):
            row_array.append(default_value)

        if (self.standart_dev):
            self.tableWidget_1D_matrix.setItem(row, i + iter, QTableWidgetItem(str(standartDev_results[int(i / col)])))
            row_array.append(standartDev_results[int(i / col)])
            iter += 1
        if (not self.standart_dev):
            row_array.append(default_value)

    return row_array

def init_results_table(self):
    self.results_tableWidget.setRowCount(len(checked_functions(self)))
    self.results_tableWidget.setColumnCount(5)
    self.results_tableWidget.horizontalHeader().setStretchLastSection(True)
    self.results_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.results_tableWidget.setHorizontalHeaderLabels(['KFOLD', 'Trainer', 'Average Accuracy', 'Average Precision', 'Average Recall'])

def fill_result_table(self, matrix):

    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            self.results_tableWidget.setItem(i, j, QTableWidgetItem(str(val)))