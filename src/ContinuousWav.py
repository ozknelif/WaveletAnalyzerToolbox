from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import librosa
import numpy as np
import pywt
from src import Features, Database
from matplotlib import pyplot as plt


class ContinuousWT(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("../ui/Continious.ui", self)
        self.setWindowTitle("Wavelet Transform Data Analyzer Tool")
        self.setWindowIcon(QtGui.QIcon('../icon/icon.png'))
        self.setFixedSize(1087, 642)
        Features.center(self)
        self.signals = []
        self.audio = []
        self.time = []
        self.load_check = False
        self.analyze_check = False

        self.actionClose.triggered.connect(self.close_window)
        self.cont_signal_Load.triggered.connect(self.load_signal)
        self.actionFolder.triggered.connect(self.load_folder)#load signal via menubar
        self.addToolBar(NavigationToolbar(self.widget_1DCont_Original.canvas, self))                         # embedding matplotlib to widget
        self.pushButton_1DCont_Analyze.clicked.connect(self.analyze_cont)                              #

        self.pushButton_save_db_cont.clicked.connect(self.save_to_db)

        wave_types = pywt.wavelist(kind='continuous')
        self.comboBox_1DCont_Type.addItems(wave_types)

        self.checkBox_1D_Average.setChecked(True),
        self.checkBox_1D_Entropy.setChecked(True)
        self.checkBox_1D_Kurtosis.setChecked(True)
        self.checkBox_1D_Max.setChecked(True)                           # discrete page statistic functions checks
        self.checkBox_1D_Median.setChecked(True)
        self.checkBox_1D_Min.setChecked(True)
        self.checkBox_1D_Skewness.setChecked(True)
        self.checkBox_1D_StandartDeviation.setChecked(True)

    def close_window(self):
        self.close()

    def load_folder(self):
        self.all_signals, self.load_check = Features.load_folder(self)
        if (self.load_check):
            Features.message(str(len(self.all_signals)) + " signals ready to be processed !", QMessageBox.Information)
            if (len(self.all_signals) > 1):  # Multiple file
                self.label_1DCont_DataName.setText("Multiple Signals")  # Data name
            else:
                name = self.all_signals[0].split(sep='/')
                self.label_1DCont_DataName.setText(name[-1])            # Setting data name
        else:
            Features.message("You have to load at least 1 signal !", QMessageBox.Warning)
            self.label_1DCont_DataName.setText("No signal selected")

    def load_signal(self):
        self.all_signals, self.filter, self.load_check = Features.load_signal(self)
        if (self.load_check):
            if (len(self.all_signals) > 1):  # Multiple file
                self.label_1DCont_DataName.setText("Multiple Signals")  # Data name
            else:
                name = self.all_signals[0].split(sep='/')
                self.label_1DCont_DataName.setText(name[-1])  # Setting data name
        else:
            Features.message("You have to load at least 1 signal !", QMessageBox.Warning)
            self.label_1DCont_DataName.setText("No signal selected")

    def plot_original_signal(self ):
        self.widget_1DCont_Original.canvas.axes.clear()
        self.widget_1DCont_Original.canvas.axes.plot(self.time,self.signals[0])
        self.widget_1DCont_Original.canvas.draw()

    def analyze_cont(self):

        self.average, self.entropy, self.kurtosis, self.max_v, self.median, self.min_v, self.skewness, self.standart_dev = Features.check_statistics(self)
        self.wavelet_type, self.sampling_per, self.min_scale, self.max_scale, self.scale_step = Features.cont_check_wavelet(self)
        if (self.load_check and (
                self.average or self.entropy or self.kurtosis or self.max_v or self.median or self.min_v or self.skewness or self.standart_dev)):  # işlenecek müzik olması durumu
            self.scaling = np.arange(int(self.min_scale), int(self.max_scale), int(self.scale_step))

            self.analyze_check = True
            self.wavelet_level = len(self.scaling) - 1
            col, self.header, self.db_header = Features.init_table(self, len(self.all_signals))
            self.db_matrix = np.zeros((len(self.all_signals), 8 * (self.wavelet_level + 1)), dtype=complex)

            for iter in range(0, len(self.all_signals)):
                print(self.all_signals[iter])
                self.signals.clear()
                self.audio, self.sample = librosa.load(self.all_signals[iter])
                self.signals.append(self.audio)
                self.time = np.arange(0, len(self.audio)) / self.sample
                coef, freqs = pywt.cwt(self.audio, self.scaling, self.wavelet_type, int(self.sampling_per))
                for i in range(0, self.wavelet_level + 1):
                    self.signals.append(coef[i])  # adding signals array to coeffs
                if (iter == 0):  # plotting first signal  only
                    self.plot_original_signal()
                    firstau = self.audio
                    time = self.time
                self.db_matrix[iter] = Features.insertTableComplex(self, iter, col)
            self.plot_wavelet(firstau,time)
        else:
            if not self.load_check:
                Features.message("You have to load at least 1 signal !", QMessageBox.Warning)
            else:
                Features.message("You have to pick at least 1 statistic function !", QMessageBox.Warning)

    def plot_wavelet(self,data,time):
        scales = self.scaling
        wavelet = self.wavelet_type
        dt = int(self.sampling_per)

        [coefficients, frequencies] = pywt.cwt(data, scales, wavelet, dt)
        power = (abs(coefficients)) ** 2

        period = 1 / frequencies
        levels = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.contourf(time, np.log2(period), np.log2(power), np.log2(levels),
                    extend='both')

        ax.set_title('%s Wavelet Power Spectrum (%s)' % ('Scalogram', wavelet))
        ax.set_ylabel('Period')
        yticks = 2 ** np.arange(np.ceil(np.log2(period.min())), np.ceil(np.log2(period.max())))
        ax.set_yticks(np.log2(yticks))
        ax.set_yticklabels(yticks)
        ax.invert_yaxis()

        cbar_ax = fig.add_axes([0.95, 0.5, 0.03, 0.25])
        fig.colorbar(im, cax=cbar_ax, orientation="vertical")
        cbar_ax.yaxis.set_ticks_position('left')

        plt.show()

    def save_to_db(self):
        if(self.load_check and self.analyze_check):
            w_name = str(self.wavelet_type)
            table_name = "Db_GTZAN_function_" + w_name + "_Scale_" + self.min_scale + "_to_" + self.max_scale + "_Period_" + self.sampling_per

            Database.create_table(Database.database_name, table_name, self.db_header, "")                   # creating new table with statistic function
            Database.create_table(Database.database_name, table_name, self.db_header, "Comp_")

            for index in range(0, len(self.all_signals)):
                name = self.all_signals[index].split(sep='/')
                Database.delete_row(Database.database_name, table_name, name[-1], "")
                Database.add_values_to_table(Database.database_name, table_name, name[-1], self.db_header, self.db_matrix[index], "")
                Database.delete_row(Database.database_name, table_name, name[-1], "Comp_")
                Database.add_values_to_table(Database.database_name, table_name, name[-1], self.db_header, self.db_matrix[index], "Comp_")
            Features.message("Your Data Saved Succesfully !", QMessageBox.Warning)
        else:
            if(self.load_check):
                Features.message("You have to analyze the signals first !", QMessageBox.Warning)
            else:
                Features.message("You have to load at least 1 signal !", QMessageBox.Warning)

    def run(self):

        self.average, self.entropy, self.kurtosis, self.max_v, self.median, self.min_v, self.skewness, self.standart_dev = Features.check_statistics(self)
        #self.wavelet_type, self.sampling_per, self.min_scale, self.max_scale, self.scale_step = Features.cont_check_wavelet(self)
        self.sampling_per = 1
        self.min_scale = 1
        self.max_scale = 8
        self.scale_step = 1
        wave_types = pywt.wavelist(kind='continuous')
        self.scaling = np.arange(self.min_scale, self.max_scale, self.scale_step)
        for wave_func in wave_types:
            self.wavelet_type = wave_func
            self.wavelet_level = len(self.scaling) - 1
            col, self.header, self.db_header = Features.init_table(self, len(self.all_signals))
            self.db_matrix = np.zeros((len(self.all_signals), 8 * (self.wavelet_level + 1)), dtype=complex)
            for iter in range(0, len(self.all_signals)):
                #print(self.all_signals[iter])

                self.signals.clear()
                self.audio, self.sample = librosa.load(self.all_signals[iter])
                self.signals.append(self.audio)
                self.time = np.arange(0, len(self.audio)) / self.sample
                coef, freqs = pywt.cwt(self.audio, self.scaling, self.wavelet_type, int(self.sampling_per))
                for i in range(0, self.wavelet_level + 1):
                    self.signals.append(coef[i])                                        # adding signals array to coeffs
                self.db_matrix[iter] = Features.insertTableComplex(self, iter, col)

            w_name = str(self.wavelet_type)
            table_name = "Db_GTZAN_function_" + w_name + "_Scale_1_to_8_Period_1"

            Database.create_table(Database.database_name, table_name, self.db_header,"")  # creating new table with statistic function
            Database.create_table(Database.database_name, table_name, self.db_header, "Comp_")

            for index in range(0, len(self.all_signals)):
                name = self.all_signals[index].split(sep='/')
                Database.add_values_to_table(Database.database_name, table_name, name[-1], self.db_header,self.db_matrix[index], "")
                Database.add_values_to_table(Database.database_name, table_name, name[-1], self.db_header,self.db_matrix[index], "Comp_")

            print(table_name)