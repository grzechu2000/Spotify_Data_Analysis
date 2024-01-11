import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cluster import KMeans
from sklearn import linear_model, preprocessing, model_selection, pipeline, ensemble, tree, datasets, cluster
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM, Dropout, BatchNormalization
from sklearn.model_selection import cross_val_score
from tensorflow.keras.optimizers import Adam
from sklearn.ensemble import  RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBClassifier, XGBRegressor
import optuna

scaler = MinMaxScaler()

positions = ['2019', '2020', '2021', '2022']
genres = ['pop', 'rock', 'country', 'metal', 'hip', 'rap', 'latin', 'indie', 'christian', 'punk', 'folk', 'jazz',
          'mexican', 'house', 'trap', 'soul', 'alt', 'r&b']
interested_columns = ['track_popularity', 'duration_ms', 'energy', 'loudness', 'speechiness', 'valence', 'genres_x']

scaled_columns = [ 'duration_ms', 'energy', 'loudness', 'speechiness', 'valence']


def data_preprocessing(years):
    crucial_data = pd.DataFrame()
    for position in years:
        file_path = f'CSV/{position}.csv'
        df0 = pd.read_csv(file_path)
        df1 = df0[interested_columns]
        crucial_data = crucial_data.append(df1, ignore_index=True)

    empty_1 = []
    for i in range(len(crucial_data['genres_x'])):
        crucial_data['genres_x'][i] = eval(crucial_data['genres_x'][i])
        if len(crucial_data['genres_x'][i]) == 0:
            empty_1.append(i)
    crucial_data = crucial_data.drop(empty_1)
    crucial_data = crucial_data.reset_index(drop=True)
    temp_dict = {}
    empty_2 = []
    sum_genres = []
    for i in range(len(crucial_data['genres_x'])):
        for genre in genres:
            sum_genres.append(sum(1 for s in crucial_data['genres_x'][i] if genre in s))
        temp_dict = dict(zip(genres, sum_genres))
        if temp_dict[max(temp_dict, key=temp_dict.get)] == 0:
            empty_2.append(i)
        else:
            crucial_data['genres_x'][i] = max(temp_dict, key=temp_dict.get)
        temp_dict = {}
        sum_genres = []
    crucial_data = crucial_data.drop(empty_2)
    crucial_data = crucial_data.reset_index(drop=True)
    temp_dicter = dict(zip(Counter(crucial_data['genres_x']).keys(), Counter(crucial_data['genres_x']).values()))
    empty_3 = []
    for i in range(len(crucial_data['genres_x'])):
        if crucial_data['genres_x'][i] != 'pop':
            empty_3.append(i)

    crucial_data = crucial_data.drop(empty_3)
    crucial_data = crucial_data.reset_index(drop=True)
    crucial_data = crucial_data.drop('genres_x', axis=1)
    Y = pd.DataFrame(crucial_data['track_popularity'])
    X = crucial_data.drop('track_popularity', axis=1)
    return Y, X, temp_dicter

Y_data, X_data_unscaled, dict_appearence = data_preprocessing(positions)
X_data = scaler.fit_transform(X_data_unscaled[scaled_columns])
z = Y_data['track_popularity'].quantile(0.8)
for i in range(len( Y_data['track_popularity'])):
    if Y_data['track_popularity'][i] >= z:
        Y_data['track_popularity'][i] = 1
    else:
        Y_data['track_popularity'][i] = 0


song_popularity_stats = dict(zip(Counter(Y_data['track_popularity']).keys(), Counter(Y_data['track_popularity']).values()))

X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.2, random_state=1)
# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=1)
X_train = pd.DataFrame(X_train, columns=scaled_columns)
X_test = pd.DataFrame(X_test, columns=scaled_columns)


clf = XGBClassifier(
        eval_metric = 'rmse',
        learning_rate = 0.1,
        n_estimators = 100,
        max_depth = 3,
        subsample = 0.9,
        colsample_bytree = 0.9,
        silent = False
)

clf.fit(X_train, y_train)

import shap
features = scaled_columns
explainer = shap.Explainer(clf, X_train)
shap_values = explainer(X_train)

path = 'save_path_here.png'
shap.summary_plot(shap_values, X_train, max_display=6)
plt.savefig(path, bbox_inches='tight', dpi=300)


importance = clf.feature_importances_

dfi = pd.DataFrame(importance, index=scaled_columns, columns=["Importance"])
dfi = dfi.sort_values(['Importance'], ascending=False)
# dfi.plot(kind='bar',color='Purple')
fig, ax = plt.subplots(figsize=(14, 9))
plt.rcParams.update({'font.size': 18})
plot=plt.barh(dfi["Importance"].keys(), (dfi["Importance"].values*100), color='maroon')
ax.bar_label(plot)
ax.set_title('Feature importance',  fontsize=20)
ax.set_ylabel('Features',  fontsize=20)
ax.set_xlabel('Importance [%]',  fontsize=20)
plt.show()

Ascores_Train = cross_val_score(clf, X_train, y_train, cv=5)
Ascores_Test = clf.score(X_test,y_test)


print('lala')
print(Ascores_Train.mean())
print(Ascores_Train.std())
print(Ascores_Test)
print('end')




