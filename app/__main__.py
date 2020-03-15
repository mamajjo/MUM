 
import sys
import scipy
import numpy
import matplotlib
import pandas
import sklearn
# Load libraries
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
#Load submodules
from app.configuration.config import configuration as cfg

class App():
    def plot_show(self, plt):
        pyplot.draw()
        pyplot.pause(0.1)
        input("Press Enter to continue")

    def run(self):
        #load dataset
        #names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
        dataset = read_csv(cfg.dataSourceUrl, header=0)

        if cfg.should_describe_data:    
            print(dataset.shape)
            #peek 20 rows
            print(dataset.head(20))
            #describe each column
            print(dataset.describe())
            #get last column name
            classColumnName = dataset.columns[-1]
            #print avaiable classes
            print(dataset.groupby(classColumnName).size())

        dataset.plot(kind='box', subplots=True, sharex=False, sharey=False)
        self.plot_show(pyplot)

        scatter_matrix(dataset)
        self.plot_show(pyplot)

        array = dataset.values
        x = array[:,0:len(dataset.columns)-1]
        y = array[:,len(dataset.columns)-1]
        #na podstawie x i y otrzymujemy tablice testowe i wynikowe
        x_train, x_validation, y_train, y_validation = train_test_split(x,y, test_size=cfg.test_size, random_state=1)

        # Spot Check Algorithms
        # algorithms = {
        #     'KNN': KNeighborsClassifier,
        #     'CART': DecisionTreeClassifier,
        #     'NB': GaussianNB,
        #     'SVM': lambda: SVC(gamma='auto')
        # }
        # for
        models = []
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC(gamma='auto')))
        # evaluate each model in turn
        results = []
        names = []
        for name, model in models:
            print(f"---------------------------\nRunning classification for: {name}")
            #kfold - k cross-validation to algorytm polegający na testowaniu nauczania(sprawdzania jego wydajności). 
            #Zbiór TESTOWY jest dzielony na K podzbiorów. W każdej z k iteracji,
            # brane jest k-1 pozdbiorów, następuje ich nauczanie, następnie sprawdzenie 'jakości' nauczonego modelu.
            #Ze wszystkiego wyciągana jest średnia, w ten sposób otrzymuje się skuteczność nauczania modelu.
            #Przy pomocy danego algorytmu uczenia maszynowego!
            kfold = StratifiedKFold(n_splits=cfg.n_splits, random_state=1, shuffle=True)
            cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='accuracy')
            results.append(cv_results)
            names.append(name)
            print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
            # Make predictions on validation dataset
            model.fit(x_train, y_train)
            predictions = model.predict(x_validation)

            print(accuracy_score(y_validation, predictions))
            print(confusion_matrix(y_validation, predictions))
            print(classification_report(y_validation, predictions))


        # Compare Algorithms
        pyplot.boxplot(results, labels=names)
        pyplot.title('Algorithm Comparison')
        self.plot_show(pyplot)

if __name__ == '__main__':
    App().run()
