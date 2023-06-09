# -*- coding: utf-8 -*-
"""ML Music - GTZAN CSV - Genre Classification Benchmarks

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xyidvX6CF04xNvKWjAYm8I7nnXBBbGGX

FINAL PROJECT Module 3: Fit Naive Bayes, MaxEnt, and Support Vector classifiers to your dataset identified in Module #1. 

Using your knowledge of this dataset, choose a metric to score the quality of your classifiers and justify your choice of metric in the context of a specific problem that your data would address. 

Indicate which classifier achieves the highest scores and speculate why this might be the case given your knowledge of the dataset.

Finally, provide contingency tables and plots of the ROC curve for each classifier and indicate the strengths and weaknesses of each classifier for your specific dataset.

## Setup

1. Download dataset from kaggle: 
https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification.

2. Upload to your Google Drive. Store folder as "gtzan" and reference the path. 
3. Create a shortcut to this directory in your google drive at the `DATASET_PATH`, OR update the `DATASET_PATH` below as necessary to match where you uploaded the "gtzan" folder.
"""

from google.colab import drive

drive.mount('/content/drive')

import os

# you might need to update the path below, or create a shortcut to the path below
DATASET_PATH = '/content/drive/MyDrive/Research/DS Research Shared 2023/data/gtzan'

print(DATASET_PATH)
assert os.path.isdir(DATASET_PATH)

GENRES_DIRPATH = os.path.join(DATASET_PATH, "genres_original")
print(os.listdir(GENRES_DIRPATH))

from IPython.display import Audio, display

genre = "pop" # @param ['hiphop', 'country', 'rock', 'disco', 'metal', 'reggae', 'blues', 'classical', 'pop', 'jazz']

audio_path = os.path.join(GENRES_DIRPATH, genre, f"{genre}.00038.wav")
display(Audio(filename=audio_path))

"""## Load Data

We have a file of 3 second features, and a file of 30 second features. We saw last time that the 30 second features led to better performance, so we'll stick with those here.
"""

#from pandas import read_csv
#
#CSV_FILEPATH = os.path.join(DATASET_PATH, "features_3_sec.csv")
#
#df3 = read_csv(CSV_FILEPATH)
#print(df3.shape) #> 9990 rows, 60 cols
#print(df3.columns.tolist())
#df3.to_csv("features_3_sec.csv")
#df3.head()

from pandas import read_csv

CSV_FILEPATH = os.path.join(DATASET_PATH, "features_30_sec.csv")

df30 = read_csv(CSV_FILEPATH)
print(df30.shape) #> 1000 rows, 60 cols
print(df30.columns.tolist())
df30.to_csv("features_30_sec.csv")
df30.head()

"""### Feature Analysis

Let's analyze the features and their distributions.
"""

target = 'label'
features = [
    'chroma_stft_mean', 'chroma_stft_var', 
    'rms_mean', 'rms_var', 
    'spectral_centroid_mean', 'spectral_centroid_var', 
    'spectral_bandwidth_mean', 'spectral_bandwidth_var', 
    'rolloff_mean', 'rolloff_var', 
    'zero_crossing_rate_mean', 'zero_crossing_rate_var', 
    'harmony_mean', 'harmony_var', 
    'perceptr_mean', 'perceptr_var', 
    'tempo', 
    'mfcc1_mean', 'mfcc1_var', 
    'mfcc2_mean', 'mfcc2_var', 
    'mfcc3_mean', 'mfcc3_var', 
    'mfcc4_mean', 'mfcc4_var', 
    'mfcc5_mean', 'mfcc5_var', 
    'mfcc6_mean', 'mfcc6_var', 
    'mfcc7_mean', 'mfcc7_var', 
    'mfcc8_mean', 'mfcc8_var', 
    'mfcc9_mean', 'mfcc9_var', 
    'mfcc10_mean', 'mfcc10_var', 
    'mfcc11_mean', 'mfcc11_var', 
    'mfcc12_mean', 'mfcc12_var', 
    'mfcc13_mean', 'mfcc13_var', 
    'mfcc14_mean', 'mfcc14_var', 
    'mfcc15_mean', 'mfcc15_var', 
    'mfcc16_mean', 'mfcc16_var', 
    'mfcc17_mean', 'mfcc17_var', 
    'mfcc18_mean', 'mfcc18_var', 
    'mfcc19_mean', 'mfcc19_var', 
    'mfcc20_mean', 'mfcc20_var', 
]

df30[features].describe()

import plotly.express as px

#colnames = ["length", "mfcc1_mean", "mfcc1_var"]
for colname in features:

    fig = px.histogram(df30[colname], height=400, title=f"Distribution of Tracks by {colname}")
    fig.show()

"""## Plotting Functions"""

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def plot_confusion_matrix(clf, y_test, y_pred, model_name=None):
    """Params 
        clf : an sklearn classifier 
        model_name : title for chart, like "Logistic Regression"
    """

    model_name = model_name or clf.__class__.__name__

    classes = clf.classes_

    cm = confusion_matrix(y_test, y_pred)
    # Confusion matrix whose i-th row and j-th column entry indicates the number of samples with 
    # ... true label being i-th class and predicted label being j-th class.

    # df = DataFrame(cm, columns=classes, index=classes)

    sns.set(rc = {'figure.figsize':(6,6)})

    sns.heatmap(cm, 
                square=True, annot=True, cbar=True,
                xticklabels=classes,
                yticklabels=classes,            
                cmap= "Blues" #"Blues" #"viridis_r" #"rocket_r" # r for reverse
    )

    plt.ylabel("True Genre") # cm rows are true
    plt.xlabel("Predicted Genre") # cm cols are preds
    plt.title(f"Confusion Matrix on Test Data ({model_name})")
    plt.show()

#
# AUC PLOTTING FUNCTION (DOESN'T WORK FOR MULTICLASS)
#

#import numpy as np
#import matplotlib.pyplot as plt
#from sklearn import metrics
#
#def plot_auc(fpr: np.array, tpr: np.array, title="Receiver operating characteristic"):
#    """Plots the ROC characteristic and the AUC Score
#
#        See: https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py
#        
#        Params: 
#
#            fpr: False positive rate 
#            tpr: True positive rate 
#        
#        ... like:
#
#            fpr, tpr, thresholds = metrics.roc_curve(y_true.to_numpy(), y_pred.to_numpy()) # , pos_label=2  
#    """
#
#    fig, ax = plt.subplots(figsize=(10,10))
#    roc_auc = metrics.auc(fpr, tpr)
#    lw = 2
#    ax.plot(
#        fpr,
#        tpr,
#        color="darkorange",
#        lw=lw,
#        label="ROC curve (area = %0.2f)" % roc_auc,
#    )
#    ax.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
#    ax.set_xlim([0.0, 1.0])
#    ax.set_ylim([0.0, 1.0])
#    plt.xlabel("False Positive Rate")
#    plt.ylabel("True Positive Rate")
#    plt.title(title)
#    plt.legend(loc="lower right")
#    plt.show()

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.RocCurveDisplay.html#sklearn.metrics.RocCurveDisplay.from_predictions
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#one-vs-rest-multiclass-roc
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html

from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve, auc, RocCurveDisplay #, roc_auc_score
import matplotlib.pyplot as plt

def plot_auc_multiclass(clf, x_test, y_train, y_test, model_name=None):
    model_name = model_name or clf.__class__.__name__

    y_pred_proba = clf.predict_proba(x_test)

    #
    # APPROACH A (OVERALL SCORE ONLY)
    #
    #roc_auc_result = roc_auc_score(y_test, y_pred_proba, multi_class="ovr", average="micro")
    #print("Micro-averaged One-vs-Rest ROC AUC score:")
    #print(f"{roc_auc_result:.2f}")

    #
    # APPROACH B (WITH PLOTTING CAPABILITIES)
    #
    
    lb = LabelBinarizer().fit(y_train)
    y_test_onehot = lb.transform(y_test)
    y_test_onehot.shape  # (n_samples, n_classe

    fpr, tpr, roc_auc = dict(), dict(), dict()
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_onehot.ravel(), y_pred_proba.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    print("Micro-averaged One-vs-Rest ROC AUC score:")
    print(f"{roc_auc['micro']:.2f}")

    RocCurveDisplay.from_predictions(y_test_onehot.ravel(), y_pred_proba.ravel(), name="micro-average OvR", color="darkorange")
    plt.plot([0, 1], [0, 1], "k--", label="chance level (AUC = 0.5)")
    plt.axis("square")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"Micro-averaged One-vs-Rest\nReceiver Operating Characteristic\n({model_name})")
    plt.legend()
    plt.show()

"""## Classifiers

### Logistic Regression
"""

from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from pandas import Series


def logistic_pipeline_cv(df=df30, features=features, target=target, scale=True):

    x = df[features]
    y = df[target]
    #print(x.shape, y.shape)

    if scale:
        scaler = MinMaxScaler()
        x = scaler.fit_transform(x)
        x = DataFrame(x, columns=features)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
    #print(x_train.shape, y_train.shape)
    #print(x_test.shape, y_test.shape)

    model = LogisticRegression(random_state=99, max_iter=5_000)
    gs = GridSearchCV(model, cv=10, param_grid={
        #"penalty": ["l1", "l2", "elasticnet", None] 
    })

    gs.fit(x_train, y_train)
    best_est = gs.best_estimator_
    print("BEST SCORE:", gs.best_score_)
    print("BEST PARAMS:", gs.best_params_)
    print("CLASSES:", gs.classes_)
    print("COEFS:")
    coefs = Series(best_est.coef_[0], index=features).sort_values(ascending=False)
    print(coefs.head())
    print(coefs.tail())

    y_pred = gs.predict(x_test)
    #y_probs = gs.predict_proba(x_test)

    print(classification_report(y_test, y_pred))

    plot_confusion_matrix(gs, y_test, y_pred, model_name=best_est.__class__.__name__)

    plot_auc_multiclass(best_est, x_test, y_train, y_test)

logistic_pipeline_cv()

#logistic_pipeline_cv(features=["mfcc6_mean", "mfcc3_mean", "chroma_stft_var"])

"""### Naive Bayes"""

from scipy.sparse import random
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from sklearn.model_selection import train_test_split


# https://scikit-learn.org/stable/modules/naive_bayes.html#naive-bayes
# which to choose?
# GaussianNB implements the Gaussian Naive Bayes algorithm for classification
# BernoulliNB implements the naive Bayes training and classification algorithms for data that is distributed according to multivariate Bernoulli distributions; i.e., there may be multiple features but each one is assumed to be a binary-valued (Bernoulli, boolean) variable. Therefore, this class requires samples to be represented as binary-valued feature vectors; if handed any other kind of data, a BernoulliNB instance may binarize its input (depending on the binarize parameter).
# MultinomialNB implements the naive Bayes algorithm for multinomially distributed data, and is one of the two classic naive Bayes variants used in text classification (where the data are typically represented as word vector counts, although tf-idf vectors are also known to work well in practice). 
# https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
# https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from pandas import Series


def naive_bayes_pipeline_cv(df=df30, features=features, target=target, scale=True, param_grid={}):

    x = df[features]
    y = df[target]
    #print(x.shape, y.shape)
    if scale:
        scaler = MinMaxScaler()
        x = scaler.fit_transform(x)
        x = DataFrame(x, columns=features)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
    #print(x_train.shape, y_train.shape)
    #print(x_test.shape, y_test.shape)

    model = GaussianNB() #> 0.51
    #model = MultinomialNB() #> 0.41 
    gs = GridSearchCV(model, cv=10, param_grid=param_grid)

    gs.fit(x_train, y_train)
    print(gs.best_score_)
    print(gs.best_params_)
    best_est = gs.best_estimator_

    y_pred = gs.predict(x_test)
    print(classification_report(y_test, y_pred))
    
    plot_confusion_matrix(gs, y_test, y_pred, model_name=best_est.__class__.__name__)

    plot_auc_multiclass(best_est, x_test, y_train, y_test)



naive_bayes_pipeline_cv()

#naive_bayes_pipeline_cv(features=normal_features)



"""### Support Vector Classifier"""

from scipy.sparse import random
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame
from sklearn.model_selection import train_test_split

# https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
from sklearn.svm import SVC

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from pandas import Series


def svc_pipeline_cv(df=df30, features=features, target=target, scale=True, param_grid={}):

    x = df[features]
    y = df[target]
    #print(x.shape, y.shape)

    scaler = None
    if scale:
        scaler = MinMaxScaler()
        x = scaler.fit_transform(x)
        x = DataFrame(x, columns=features)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
    #print(x_train.shape, y_train.shape)
    #print(x_test.shape, y_test.shape)

    #model = SVC(kernel=kernel, gamma=gamma, random_state=99) # gamma=gamma
    model = SVC(random_state=99, probability=True) # probability=True enables .predict_proba()
    gs = GridSearchCV(model, cv=10, param_grid=param_grid)

    gs.fit(x_train, y_train)
    print(gs.best_score_)
    print(gs.best_params_)
    best_est = gs.best_estimator_
    #if kernel == "linear":
    #    print(best_est.coef_)
    #    print(best_est.intercept_)
    #    features = x.columns.tolist()
    #    print(Series(best_est.coef_[0], index=features).sort_values(ascending=False))

    y_pred = gs.predict(x_test)
    print(classification_report(y_test, y_pred))
    
    plot_confusion_matrix(gs, y_test, y_pred, model_name=best_est.__class__.__name__)

    plot_auc_multiclass(best_est, x_test, y_train, y_test)

    return gs, scaler




svc_pipeline_cv(param_grid={"kernel": ["linear", "poly", "rbf", "sigmoid"]})

# https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
#
# degree int, default=3
# Degree of the polynomial kernel function (‘poly’). Must be non-negative. Ignored by all other kernels.
#
# gamma{‘scale’, ‘auto’} or float, default=’scale’
# Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.

best_svc_all_features, scaler_all_features = svc_pipeline_cv(param_grid={
    "kernel": ["poly"],
    "degree": [ 
        #1,
        2,3,4, 
        #5,10,
        #20
        ],
    "gamma": ["scale", "auto"]

})

"""#### MFCC Only"""

mfcc_features = [f for f in features if "mfcc" in f]
print(len(mfcc_features))
print(mfcc_features)

best_svc_mfcc_features, scaler_mfcc_features = svc_pipeline_cv(
    features=mfcc_features,
    param_grid={
        "kernel": ["poly"],
        "degree": [ 
            #1,
            2,3,4, 
            #5,10,
            #20
            ],
        "gamma": ["scale", "auto"]
    }
)

"""## Saving Best Models

Let's save one version of the model that has been trained on all features. Then we'll also save another version that has been trained on MFCCs only.
"""

# https://github.com/s2t2/tweet-analysis-2020/blob/main/app/nlp/model_storage.py#L2

import os


# you might need to update the path below, or create a shortcut to the path below
MODELS_DIRPATH = '/content/drive/MyDrive/Research/DS Research Shared 2023/users/mjr300/ML Music/models'

print(MODELS_DIRPATH)
assert os.path.isdir(MODELS_DIRPATH)

import pickle
import json

def write_model(model, filepath):
    print("WRITING MODEL TO LOCAL FILE...")
    with open(filepath, "wb") as f:
        pickle.dump(model, f)

def write_params(params, filepath):
    print("WRITING PARAMS TO LOCAL FILE...")
    with open(filepath, "w") as f:
        json.dump(params, f)

model_filepath = os.path.join(MODELS_DIRPATH, "best_svc_all_features.gpickle")
params_filepath = os.path.join(MODELS_DIRPATH, "best_svc_all_features.json")
scaler_filepath = os.path.join(MODELS_DIRPATH, "scaler_all_features.gpickle")

write_model(best_svc_all_features, model_filepath)
write_params(best_svc_all_features.best_params_, params_filepath)
write_model(scaler_all_features, scaler_filepath)

model_filepath = os.path.join(MODELS_DIRPATH, "best_svc_mfcc_features.gpickle")
params_filepath = os.path.join(MODELS_DIRPATH, "best_svc_mfcc_features.json")
scaler_filepath = os.path.join(MODELS_DIRPATH, "scaler_mfcc_features.gpickle")

write_model(best_svc_mfcc_features, model_filepath)
write_params(best_svc_mfcc_features.best_params_, params_filepath)
write_model(scaler_mfcc_features, scaler_filepath)

"""## Results Summary and Interpretation

The metric of choice is general classification accuracy. We don't really yet have a need to prefer a different score. Although we could also take a look at ROC / AUC score (in this case micro-averaged because of the multi-class problem).

A) The Logistic Regression acheives 66% accuracy (and AUC of 90%) on the test data.

B) The Gaussian Naive Bayes acheives 51% accuracy (and AUC of 95%).

> NOTE: the Multinomial Naive Bayes acheives 41% accuracy, which is lower than the Gaussian version. This could be because some of our features have a Gaussian distribution, which might make the Gaussian version an appropriate choice.

C) The best SVC, which uses a polynomial kernel (with degree of three), acheives 74% accy (and AUC of 97%).

Since we have ten classes, a guess would be 10% accuracy, so the results of all these models are pretty good so far. The SVC has the best accuracy and AUC scores, so we can consider it to be the best performing. This may be because the SVC uses a polynomial kernel function to handle non-linear decision boundaries, whereas the Logistic Regression and Naive Bayes can be considered as linear models (see references below).

References:

  + https://stats.stackexchange.com/questions/88603/why-is-logistic-regression-a-linear-model
  + https://stats.stackexchange.com/questions/142215/how-is-naive-bayes-a-linear-classifier
  + https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote05.html 


UPDATE: an SVC trained on MFCC features acheives 68% accuracy and 96% AUC. We are making this version of the model so we can use a classifier trained on the GTZAN dataset to classify other audio files that have only been converted to MFCCs (not including all the other features yet).

## Scratch Work

The section below contains some commented out code used during the development of this notebook
"""

## https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
## Test whether a sample differs from a normal distribution.
## This function tests the null hypothesis that a sample comes from a normal distribution. It is based on D’Agostino and Pearson’s [1], [2] test that combines skew and kurtosis to produce an omnibus test of normality.
#
#from scipy.stats import normaltest
#from pandas import DataFrame
#
#alpha = 1e-3
#
#normality_results = []
#
#for colname in features:
#
#    x_col = df30[colname].tolist()
#    
#    k2_score, p_val = normaltest(x_col)
#    #print("K2 SCORE:", k2_score)
#    #print(f"P_VAL: {p_val:g}")
#    #if p_val < alpha:  # null hypothesis: x comes from a normal distribution
#    #    print("The null hypothesis can be rejected")
#    #else:
#    #    print("The null hypothesis cannot be rejected")
#
#    normality_results.append({"colname": colname, "score": k2_score, "p_val": p_val})
#
#norm_df = DataFrame(normality_results)
#normal_features = norm_df[norm_df["p_val"] > alpha]["colname"].tolist()
#norm_df[norm_df["p_val"] >= alpha] # the ones that come from a normal dist

#from sklearn.preprocessing import MinMaxScaler
#from pandas import DataFrame
#
#scaler = MinMaxScaler()
#scaled30 = scaler.fit_transform(df30[features])
#
#scaled30 = DataFrame(scaled30, columns=features)
#scaled30.head()

#scaled30.mean()

#from sklearn.linear_model import LogisticRegression
#
#model = LogisticRegression(random_state=99, max_iter=10_000)
#
#model.__class__.__name__

#df=df30
#features=features
#target=target
#scale=True
#
#x = df[features]
#y = df[target]
##print(x.shape, y.shape)
#
#if scale:
#    scaler = MinMaxScaler()
#    x = scaler.fit_transform(x)
#    x = DataFrame(x, columns=features)

#x.head()

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=99)
#print(x_train.shape, y_train.shape)
#print(x_test.shape, y_test.shape)

#model = LogisticRegression(random_state=99, max_iter=10_000)
#gs = GridSearchCV(model, cv=10, param_grid={
#    #"penalty": ["l1", "l2", "elasticnet", None] 
#})
#
#gs.fit(x_train, y_train)
#best_est = gs.best_estimator_
#print("BEST SCORE:", gs.best_score_)
#print("BEST PARAMS:", gs.best_params_)
#print("CLASSES:", gs.classes_)
#
#coefs = Series(best_est.coef_[0], index=features).sort_values(ascending=False)
#print(coefs.head(3))
#
#y_pred = gs.predict(x_test)
#print(classification_report(y_test, y_pred))

#coefs = Series(best_est.coef_[0], index=features).sort_values(ascending=False)
#print(coefs.head(3))
#print(coefs.tail(3))

#from sklearn.metrics import classification_report, confusion_matrix
#
#cm = confusion_matrix(y_test, y_pred
#                      #, labels=gs.classes_, 
#                          #sample_weight=None, normalize=None
#                          )
#cm
#DataFrame(cm, columns=gs.classes_, index=gs.classes_)

#import seaborn as sns
#import matplotlib.pyplot as plt
#
#sns.set(rc = {'figure.figsize':(10,10)})
#
#sns.heatmap(cm, 
#            square=True, annot=True, cbar=True,
#            xticklabels=gs.classes_,
#            yticklabels=gs.classes_,            
#            # https://stackoverflow.com/questions/47461506/how-to-invert-color-of-seaborn-heatmap-colorbar
#            cmap= "Blues" #"Blues" #"viridis_r" #"rocket_r" # r for reverse
#)
#
## Confusion matrix whose i-th row and j-th column entry indicates the number of samples with 
## ... true label being i-th class and predicted label being j-th class.
#plt.xlabel("Predicted Genre")
#plt.ylabel("True Genre")
#plt.title("Confusion Matrix on Test Data (Logistic Regression)")
#plt.show()

## https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
#
#from sklearn.metrics import roc_auc_score
#
#y_pred_proba = gs.predict_proba(x_test)
#
#roc_auc_result = roc_auc_score(y_test, y_pred_proba, multi_class="ovr", average="micro")
#print(f"Micro-averaged One-vs-Rest ROC AUC score:\n{roc_auc_result:.2f}")

## https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#one-vs-rest-multiclass-roc
#
#from sklearn.preprocessing import LabelBinarizer
#
#label_binarizer = LabelBinarizer().fit(y_train)
#y_test_onehot = label_binarizer.transform(y_test)
#y_test_onehot.shape  # (n_samples, n_classe

#label_binarizer.transform(["rock"])

#label_binarizer.transform(["country"])

#import numpy as np
#
#print(np.flatnonzero(label_binarizer.classes_ == "rock")[0])
#print(np.flatnonzero(label_binarizer.classes_ == "country")[0])
#

#y_test_onehot.ravel()

#from sklearn.metrics import roc_curve, auc 
#
#
#fpr, tpr, roc_auc = dict(), dict(), dict()
#
#fpr["micro"], tpr["micro"], _ = roc_curve(y_test_onehot.ravel(), y_pred_proba.ravel())
#
#roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
#
#print(f"Micro-averaged One-vs-Rest ROC AUC score:\n{roc_auc['micro']:.2f}")
#

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.RocCurveDisplay.html#sklearn.metrics.RocCurveDisplay.from_predictions

#import matplotlib.pyplot as plt
#
#from sklearn.metrics import RocCurveDisplay
#
#RocCurveDisplay.from_predictions(
#    y_test_onehot.ravel(),
#    y_pred_proba.ravel(),
#    name="micro-average OvR",
#    color="darkorange",
#)
#plt.plot([0, 1], [0, 1], "k--", label="chance level (AUC = 0.5)")
#plt.axis("square")
#plt.xlabel("False Positive Rate")
#plt.ylabel("True Positive Rate")
#plt.title("Micro-averaged One-vs-Rest\nReceiver Operating Characteristic")
#plt.legend()
#plt.show()