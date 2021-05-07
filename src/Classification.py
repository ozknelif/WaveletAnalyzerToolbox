from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from src import ClassifyMusic, Features, Database
from tabulate import tabulate

class ClassificationPage(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("../ui/Prediction.ui", self)
        self.setWindowTitle("Wavelet Transform Data Analyzer Tool")
        self.setWindowIcon(QtGui.QIcon('../icon/icon.png'))
        Features.center(self)
        list_tables = Database.get_table_names(Database.database_name)
        Features.list_db_tables(self, list_tables)
        for i in range(2, 21):
            self.comboBox_kfold.addItem(str(i), i)

        self.selected_table_name = ""
        self.checkBox_knn.setChecked(True)
        self.checkBox_randomForest.setChecked(True)
        self.checkBox_svcLinear.setChecked(True)
        self.checkBox_svcPoly.setChecked(True)  # prediction page checks
        self.checkBox_gaussianNB.setChecked(True)
        self.checkBox_svcRBF.setChecked(True)

        self.pushButton.clicked.connect(self.analyze_signal)

        self.dbTables_listWidget.itemSelectionChanged.connect(self.selectionChanged)

    def selectionChanged(self):
        self.selected_table_name = self.dbTables_listWidget.currentItem().text()

    def analyze_signal(self):
        if(self.selected_table_name != ""):
            table_name = self.selected_table_name
            if(table_name.find('Comp_') != -1) :
                table_name = table_name.replace('Comp_','')
            matrix = ClassifyMusic.run(table_name, int(self.comboBox_kfold.currentText()), Features.checked_functions(self), self.checkBox_printConf.isChecked())
            Features.init_results_table(self)
            Features.fill_result_table(self, matrix)
        else :
            Features.message("You have to choose a table", QMessageBox.Warning)


    def analyze_all_continuous(self):
        list_tables = Database.get_table_names(Database.database_name)

        iter = 0
        func_names = {}
        for table in list_tables:
            if (table.split('_')[0] != 'Comp'):
                func_name = table.split('_')[3]
                if (func_names.get(func_name, -1) == -1):
                    func_names[str(func_name)] = iter
                    iter += 1

        acc_matrix = [['' for x in range(7)] for x in range(iter)]
        rec_matrix = [['' for x in range(7)] for x in range(iter)]
        prec_matrix = [['' for x in range(7)] for x in range(iter)]

        iter = -1
        x = 0
        for table in list_tables:
            print(table)
            if (table.split('_')[0] != 'Comp'):
                func_name = table.split('_')[3]

                result = ClassifyMusic.run(table, 5, [1, 2, 3, 4, 5, 6], False)

                string = acc_matrix[func_names.get(func_name)]
                array = [func_name, result[0][2], result[1][2], result[2][2], result[3][2], result[4][2], result[5][2]]
                if (string[0] == ''):
                    acc_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    acc_matrix[func_names.get(func_name)] = arr

                array = [func_name, result[0][3], result[1][3], result[2][3], result[3][3], result[4][3], result[5][3]]
                if (string[0] == ''):
                    prec_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    prec_matrix[func_names.get(func_name)] = arr

                array = [func_name, result[0][4], result[1][4], result[2][4], result[3][4], result[4][4], result[5][4]]
                if (string[0] == ''):
                    rec_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    rec_matrix[func_names.get(func_name)] = arr

        avg_acc_matrix = cont_create_tables(acc_matrix)
        avg_rec_matrix = cont_create_tables(rec_matrix)
        avg_prec_matrix = cont_create_tables(prec_matrix)

        print('-------------------------------------------------------------------')
        print('------------------------------------acc matrix---------------------')

        print(tabulate(avg_acc_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print(
            '----------------------------------------------------------------------------')
        print(
            '-----------------------------------acc matrix--------------------------------')

        print(
            '-------------------------------------------------------------------------------')
        print(
            '----------------------------------------rec matrix-----------------------------')


        print(tabulate(avg_rec_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print(
            '-----------------------------------------------------------------------------------')
        print(
            '-----------------------------rec matrix--------------------------------------------')

        print(
            '----------------------------------------------------------------')
        print(
            '-------------------------prec matrix-----------------------------')

        print(tabulate(avg_prec_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print(
            '-------------------------------------------------------------------------------')
        print(
            '-----------------------------------------prec matrix---------------------------')

    def analyze_all_discrete(self):

        list_tables = Database.get_table_names(Database.database_name)

        iter = 0
        func_names = {}
        for table in list_tables:
            if (table.split('_')[0] != 'Comp'):
                func_name = table.split('_')[3]
                level = table.split('_')[5]
                if( func_names.get(func_name, -1) == -1):
                    func_names[str(func_name)] = iter
                    iter += 1

        acc_matrix = [['' for x in range(7)] for x in range(iter)]
        rec_matrix = [['' for x in range(7)] for x in range(iter)]
        prec_matrix = [['' for x in range(7)] for x in range(iter)]

        iter = -1
        x = 0
        for table in list_tables:
            print(table)
            if (table.split('_')[0] != 'Comp'):
                func_name = table.split('_')[3]
                level = table.split('_')[5]

                result = ClassifyMusic.run(table, 5, [1, 2, 3, 4, 5, 6], False)

                string = acc_matrix[func_names.get(func_name)]
                array = [func_name, result[0][2], result[1][2], result[2][2], result[3][2], result[4][2], result[5][2]]
                if(string[0] == ''):
                    acc_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    acc_matrix[func_names.get(func_name)] = arr

                array = [func_name, result[0][3], result[1][3], result[2][3], result[3][3], result[4][3], result[5][3]]
                if (string[0] == ''):
                    prec_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    prec_matrix[func_names.get(func_name)] = arr

                array = [func_name, result[0][4], result[1][4], result[2][4], result[3][4], result[4][4], result[5][4]]
                if (string[0] == ''):
                    rec_matrix[func_names.get(func_name)] = array
                else:
                    arr = [a + '-' + b for a, b in zip(string, array)]
                    rec_matrix[func_names.get(func_name)] = arr


        avg_acc_matrix = create_tables(acc_matrix)
        avg_rec_matrix = create_tables(rec_matrix)
        avg_prec_matrix = create_tables(prec_matrix)

        print(avg_acc_matrix)
        print(avg_rec_matrix)
        print(avg_prec_matrix)

        print('-------------------------------------------------------------------')
        print('------------------------------------acc matrix---------------------')

        print(tabulate(avg_acc_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print('----------------------------------------------------------------------------')
        print('-----------------------------------acc matrix--------------------------------')

        print('-------------------------------------------------------------------------------')
        print('----------------------------------------rec matrix-----------------------------')

        print(tabulate(avg_rec_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print('-----------------------------------------------------------------------------------')
        print('-----------------------------rec matrix--------------------------------------------')

        print('----------------------------------------------------------------')
        print('-------------------------prec matrix-----------------------------')

        print(tabulate(avg_prec_matrix, tablefmt="latex_raw",
                       headers=['Type', 'Random Forest', 'KNN', 'SVC Poly', 'GaussianNB', 'SVC Linear', 'SVC RBF']))

        print('-------------------------------------------------------------------------------')
        print('-----------------------------------------prec matrix---------------------------')

def create_tables(matrix):

        funcs = ['sym', 'bior', 'coif', 'db', 'dmey', 'haar', 'rbio']

        arraySym = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        symiter = 0

        arrayCoif = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        coifiter = 0

        arrayDb = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        dbiter = 0

        arrayBior = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        bioriter = 0

        arrayRbio = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rbioiter = 0

        arrayHaar = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        haariter = 0

        arrayDmey = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        dmeyiter = 0


        for row in matrix:          #sym4 ,52-56-45, 60-8-65,
            result = ''.join([i for i in row[0].split('-')[0] if i.isalpha()])
            index = next((i for i, e in enumerate(funcs) if result in e), len(funcs) - 1)

            for i in range(1,7):
                stracc = row[i]
                acc1 = float(stracc.split('-')[0])
                acc2 = float(stracc.split('-')[1])
                acc3 = float(stracc.split('-')[2])
                if (index == 0):
                    fill(arraySym, acc1, acc2, acc3, i)
                    symiter += 1
                if (index == 1):
                    fill(arrayBior, acc1, acc2, acc3, i)
                    bioriter += 1
                if (index == 2):
                    fill(arrayCoif, acc1, acc2, acc3, i)
                    coifiter += 1
                if (index == 3):
                    fill(arrayDb, acc1, acc2, acc3, i)
                    dbiter += 1
                if (index == 4):
                    fill(arrayDmey, acc1, acc2, acc3, i)
                    dmeyiter += 1
                if (index == 5):
                    fill(arrayHaar, acc1, acc2, acc3, i)
                    haariter += 1
                if (index == 6):
                    fill(arrayRbio, acc1, acc2, acc3, i)
                    rbioiter += 1

        avg_acc_matrix = [['' for x in range(7)] for x in range(len(funcs))]

        if (symiter != 0):
            avgSym = [x / (symiter / 6) for x in arraySym]
            avg_acc_matrix[0] = create_avg(avgSym, 'sym')
        if (haariter != 0):
            avgHaar = [x / (haariter / 6) for x in arrayHaar]
            avg_acc_matrix[1] = create_avg(avgHaar, 'haar')
        if (coifiter != 0):
            avgCoif = [x / (coifiter / 6) for x in arrayCoif]
            avg_acc_matrix[2] = create_avg(avgCoif, 'coif')
        if (dbiter != 0):
            avgDb = [x / (dbiter / 6) for x in arrayDb]
            avg_acc_matrix[3] = create_avg(avgDb, 'db')
        if (rbioiter != 0):
            avgRbio = [x / (rbioiter / 6) for x in arrayRbio]
            avg_acc_matrix[4] = create_avg(avgRbio, 'rbio')
        if (bioriter != 0):
            avgBior = [x / (bioriter / 6) for x in arrayBior]
            avg_acc_matrix[5] = create_avg(avgBior, 'bior')
        if (dmeyiter != 0):
            avgDmey = [x / (dmeyiter / 6) for x in arrayDmey]
            avg_acc_matrix[6] = create_avg(avgDmey, 'dmey')

        return avg_acc_matrix

def create_avg(result, func_name):
    i= 0
    array = [func_name, str("%.2f" % result[0]) + '- ' + str("%.2f" % result[1]) + '- ' + str("%.2f" % result[2]) ,
                        str("%.2f" % result[3]) + '- ' + str("%.2f" % result[4]) + '- ' + str("%.2f" % result[5]) ,
                        str("%.2f" % result[6]) + '- ' + str("%.2f" % result[7]) + '- ' + str("%.2f" % result[8]) ,
                        str("%.2f" % result[9]) + '- ' + str("%.2f" % result[10]) + '- ' + str("%.2f" % result[11]) ,
                        str("%.2f" % result[12]) + '- ' + str("%.2f" % result[13]) + '- ' + str("%.2f" % result[14]) ,
                        str("%.2f" % result[15]) + '- ' + str("%.2f" % result[16]) + '- ' + str("%.2f" % result[17])]
    return array

def fill(array, val1, val2, val3, index):
    array[index * 3 - 3] += val1                    #0 , 3 , 6 , 9
    array[index * 3 - 2] += val2
    array[index * 3 - 1] += val3

def cont_create_tables(matrix):

    funcs = ['cgau', 'cmor', 'fbsp', 'gaus', 'mexh', 'morl', 'shan']

    arrayCgau = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    cgauiter = 0

    arrayCmor = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    cmoriter = 0

    arrayFbsp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    fbspiter = 0

    arrayGaus = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    gausiter = 0

    arrayMexh = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    mexhiter = 0

    arrayMorl = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    morliter = 0

    arrayShan = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,]
    shaniter = 0

    for row in matrix:  # sym4 ,52-56-45, 60-8-65,
        result = ''.join([i for i in row[0].split('-')[0] if i.isalpha()])
        index = next((i for i, e in enumerate(funcs) if result in e), len(funcs) - 1 )

        for i in range(1, 7):
            stracc = row[i]
            acc1 = float(stracc.split('-')[0])

            if (index == 0):
                arrayCgau[i - 1] += acc1
                cgauiter += 1
            if (index == 3):
                arrayGaus[i - 1] += acc1
                gausiter += 1
            if (index == 1):
                arrayCmor[i - 1] += acc1
                cmoriter += 1
            if (index == 2):
                arrayFbsp[i - 1] += acc1
                fbspiter += 1
            if (index == 6):
                arrayShan[i - 1] += acc1
                shaniter += 1
            if (index == 5):
                arrayMorl[i - 1] += acc1
                morliter += 1
            if (index == 4):
                arrayMexh[i - 1] += acc1
                mexhiter += 1

    avg_acc_matrix = [['' for x in range(7)] for x in range(len(funcs))]

    if (cgauiter != 0):
        avgCgau = [x / (cgauiter / 6) for x in arrayCgau]
        avg_acc_matrix[0] = create_avg_comp(avgCgau, 'cgau')
    if (morliter != 0):
        avgMorl = [x / (morliter / 6) for x in arrayMorl]
        avg_acc_matrix[1] = create_avg_comp(avgMorl, 'morl')
    if (cmoriter != 0):
        avgCmor = [x / (cmoriter / 6) for x in arrayCmor]
        avg_acc_matrix[2] = create_avg_comp(avgCmor, 'cmor')
    if (fbspiter != 0):
        avgFbsp = [x / (fbspiter / 6) for x in arrayFbsp]
        avg_acc_matrix[3] = create_avg_comp(avgFbsp, 'fbsp')
    if (mexhiter != 0):
        avgMexh = [x / (mexhiter / 6) for x in arrayMexh]
        avg_acc_matrix[4] = create_avg_comp(avgMexh, 'mexh')
    if (gausiter != 0):
        avgGaus = [x / (gausiter / 6) for x in arrayGaus]
        avg_acc_matrix[5] = create_avg_comp(avgGaus, 'gaus')
    if (shaniter != 0):
        avgShan = [x / (shaniter / 6) for x in arrayShan]
        avg_acc_matrix[6] = create_avg_comp(avgShan, 'shan')

    return avg_acc_matrix

def create_avg_comp(result, func_name):
    i= 0
    array = [func_name, str("%.2f" % result[0]) , str("%.2f" % result[1]) , str("%.2f" % result[2]) ,
                        str("%.2f" % result[3]) , str("%.2f" % result[4]) , str("%.2f" % result[5])]
    return array
