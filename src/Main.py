from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from src.DiscreteWav import DiscreteWT
from src.ContinuousWav import ContinuousWT
from src.Classification import ClassificationPage
from src import Features


class MainPage(QWidget):

    def __init__(self):
        super().__init__()

        QMainWindow.__init__(self)
        loadUi("../ui/mainWindow.ui", self)
        self.setWindowTitle("Wavelet Transform Data Analyzer Tool")
        self.setWindowIcon(QtGui.QIcon('../icon/icon.png'))
        self.setFixedSize(500, 300)
        Features.center(self)

        self.pushButton_DiscreteWavelet1D.clicked.connect(self.openDiscretePage)

        self.pushButton_ContiniousWavelet1D.clicked.connect(self.openContinuousPage)

        self.pushButton_Prediction.clicked.connect(self.openClassificationPage)


    def openDiscretePage(self):
        self.discretePage = DiscreteWT()
        self.discretePage.show()

    def openContinuousPage(self):
        self.continuousPage = ContinuousWT()
        self.continuousPage.show()

    def openClassificationPage(self):
        self.classificationPage = ClassificationPage()
        self.classificationPage.show()

app = QApplication([])
window = MainPage()
window.show()
app.exec()
