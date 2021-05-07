import numpy as np
from sklearn import model_selection, preprocessing, metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from src import Database
import warnings

def print_conf_matrix(label_test, label_pred):

    array = []
    j = 0
    for j in range(len(label_test)):
        iter = 0
        flag = True
        while (iter < len(array) and flag):
            if (label_test[j] == array[iter]):
                flag = False
            iter += 1
        if (flag):
            array.append(label_test[j][0])

    cnf_matrix = confusion_matrix(label_test, label_pred)

    plt.matshow(cnf_matrix)
    plt.colorbar()
    plt.ylabel('Expected label')
    plt.xlabel('Predicted label')
    plt.xticks(np.arange(0, len(array)), array, rotation='vertical')
    plt.yticks(np.arange(0, len(array)), array, rotation='horizontal')
    plt.show()


def classification_compare(data, label, selection, kfold, bool_conf):

    scaler = preprocessing.MinMaxScaler((-1,1))
    cv = model_selection.KFold(n_splits=kfold, shuffle=True)
    total_acc = 0
    total_prec = 0
    total_recall = 0
    trainer="null"

    if selection == 1: trainer, model = "Random Forest", RandomForestClassifier(n_estimators=100,criterion='entropy')
    if selection == 2: trainer, model = "KNN", KNeighborsClassifier(n_neighbors=1, weights='distance')
    if selection == 3: trainer, model = "SVC POLY", SVC(kernel='poly',degree=2,C=100, gamma='auto')
    if selection == 4: trainer, model = "GaussianNB", GaussianNB()
    if selection == 5: trainer, model = "SVC Linear",LinearSVC(penalty='l1',dual=False,multi_class='crammer_singer',max_iter=1000000)
    if selection == 6: trainer, model = "SVC RBF", SVC(kernel='rbf', random_state=0, gamma=.01, C=100000)

    scaler.fit(data)
    i= 0
    for train_index, test_index in cv.split(data):
        data_train, data_test = data[train_index], data[test_index]
        label_train, label_test = label[train_index], label[test_index]
        data_train = scaler.transform(data_train)
        data_test  = scaler.transform(data_test)
        model.fit(data_train, label_train)
        label_pred = model.predict(data_test)
        acc = metrics.accuracy_score(label_test, label_pred)*100
        prec = metrics.precision_score(label_test, label_pred, average='weighted') * 100
        recall = metrics.recall_score(label_test, label_pred, average='weighted') * 100

        total_acc += acc
        total_prec += prec
        total_recall += recall
        i += 1

    avg_acc = total_acc / i
    avg_prec = total_prec / i
    avg_recall = total_recall / i

    if(bool_conf):
        print_conf_matrix(label_test, label_pred)

    print('acc = ' + str("%.2f" % avg_acc), 'prec = ' + str(("%.2f" % avg_prec)), 'recall = ' + str(("%.2f" % avg_recall)))

    return [str(kfold), trainer, str("%.2f" % avg_acc), str(("%.2f" % avg_prec)), str(("%.2f" % avg_recall))]

def start(data, label, kfold, functions, bool_conf):

    table = []
    for i in range(len(functions)):
        table.append(classification_compare(data, label, functions[i], kfold, bool_conf))
    return table


def get_data_label(features):
    data = np.array(features)

    label = data[:, [0]]
    label = np.array(label)
    i = 0
    for i in range(len(label)):
        label[i][0] = np.char.split(label, '.')[i][0][0]

    data = np.delete(data, 0, 1)
    return data, label

def run(table_name, kFold, functions, bool_conf):
    warnings.filterwarnings("ignore")
    data = Database.read_from_table(Database.database_name, table_name)
    data, label = get_data_label(data)
    return start(data, label, kFold, functions, bool_conf)

