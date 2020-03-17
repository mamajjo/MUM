 
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
from sklearn.metrics import plot_confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
#Load submodules
from app.configuration.config import json_config as cfg

class App():
    def plot_show(self):
        pyplot.draw()
        pyplot.pause(0.1)

    def run(self):
        #load dataset
        dataset = read_csv(cfg.dataSourceUrl, header=0)

        if cfg.should_describe_data:    
            print(dataset.shape)
            print(dataset.head(20))
            #describe each column
            print(dataset.describe())
            #get last column name
            classColumnName = dataset.columns[-1]
            #print avaiable classes
            print(dataset.groupby(classColumnName).size())
        
        # dataset.plot(kind='box', subplots=True, sharex=False, sharey=False)
        # self.plot_show()

        # scatter_matrix(dataset)
        # self.plot_show()

        array = dataset.values
        x = array[:,0:len(dataset.columns)-1]
        y = array[:,len(dataset.columns)-1]
        #na podstawie x i y otrzymujemy tablice testowe i wynikowe
        x_train, x_validation, y_train, y_validation = train_test_split(x,y, test_size=cfg.test_size, random_state=1)

        models = []
        models.extend([
            ('KNN', KNeighborsClassifier(), 0),
            ('CART', DecisionTreeClassifier(), 1),
            ('NB', GaussianNB(), 2),
            ('SVM', SVC(gamma='auto'), 3)
        ])
        results = []
        names = []
        fig, axes = pyplot.subplots(4, 2, sharex=True, sharey=True, figsize=(20,5), gridspec_kw={'hspace': 1, 'wspace': 1})
        fig.suptitle("Confusion matrices")
        fig.tight_layout()
        for name, model, subplot_row in models:
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
            titles_options = [(f"{name}: CF", None, 0), (f"{name}: normalized CF", 'true', 1)]
            for title, normalize, subplot_num in titles_options:
                disp = plot_confusion_matrix(model, x_validation, y_validation,
                                            cmap=pyplot.cm.Blues,
                                            ax=axes[subplot_row, subplot_num],
                                            normalize=normalize)
                disp.ax_.set_title(title)
                self.plot_show()
            print(classification_report(y_validation, predictions))


        # Compare Algorithms
        fig = pyplot.figure()
        fig.suptitle("Algorithm Comparison")
        ax = fig.add_subplot(1,1,1)
        ax.set_title("Algorithm Comparison")
        ax.boxplot(results, labels=names)
        self.plot_show()
        input("Press Enter to continue")

if __name__ == '__main__':
    App().run()