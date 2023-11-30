import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import os

def plot_feature_vs_popularity_all_years():
    directory = 'CSV/'
    all_files = os.listdir(directory)
    df_list = []

    features_y = 'track_popularity'

    cmap = cm.get_cmap('viridis')
    years = range(1995, 2023)
    colors = [cmap((year - 1995) / (2022 - 1995)) for year in years]

    num_cols = 3
    num_rows = 4

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 14))

    list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                        'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x']

    for filename, color in zip(all_files, colors):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            df['release_date'] = pd.to_datetime(df['release_date'])
            df_list.append((df, color))

    for i in range(num_rows):
        for j in range(num_cols):
            feature_name = list_of_features[i * num_cols + j]
            ax = axs[i, j]

            for df, color in df_list:
                ax.scatter(df[feature_name], df[features_y], label=str(df['release_date'].iloc[0].year), color=color)

            ax.set_xlabel(feature_name)
            ax.set_ylabel(features_y)
            ax.set_title(f"{feature_name} vs track_popularity")

    plt.tight_layout()
    plt.show()


def plot_features_vs_popularity(year):

    file_path = f'CSV/{year}.csv'
    df = pd.read_csv(file_path)

    list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                       'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x']

    num_cols = 3
    num_rows = 4

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 14))

    for i in range(num_rows):
        for j in range(num_cols):
            feature = list_of_features[i * num_cols + j]
            axs[i, j].scatter(df[feature], df['track_popularity'], alpha=0.5)
            axs[i, j].set_title(f"{feature} vs track_popularity")
            axs[i, j].set_xlabel(feature)
            axs[i, j].set_ylabel('track_popularity')
    plt.tight_layout()
    plt.show()

def plot_features_vs_time(year):
    file_path = f'CSV/{year}.csv'
    df = pd.read_csv(file_path)

    list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                       'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x']

    num_cols = 3
    num_rows = 4

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 14))
    df['release_date'] = pd.to_datetime(df['release_date'])
    for i in range(num_rows):
        for j in range(num_cols):
            feature_name = list_of_features[i * num_cols + j]
            axs[i, j].scatter(df['release_date'], df[feature_name], alpha=0.5)
            axs[i, j].set_title(f"release_date vs {feature_name}")
            axs[i, j].set_xlabel("release_date")
            axs[i, j].set_ylabel(feature_name)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.show()





def features_vs_time():
    directory = 'CSV/'
    all_files = os.listdir(directory)
    df_list = []

    list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                       'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x']

    num_cols = 3
    num_rows = 4

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 14))

    for filename in all_files:
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            df['release_date'] = pd.to_datetime(df['release_date'])
            df_list.append(df)

    for i in range(num_rows):
        for j in range(num_cols):
            feature_name = list_of_features[i * num_cols + j]
            ax = axs[i, j]

            cmap = cm.get_cmap('viridis')
            years = range(1995, 2023)
            colors = [cmap((year - 1995) / (2022 - 1995)) for year in years]

            for year, color in zip(years, colors):
                subset = df_list[year - 1995]  # Assuming the list is ordered by year
                ax.scatter(subset['release_date'], subset[feature_name], label=str(year), color=color)

            ax.set_title(f"release_date vs {feature_name}")
            ax.set_xlabel("release_date")
            ax.set_ylabel(feature_name)

    plt.tight_layout()
    plt.show()

    

#plot_features_vs_popularity(2022) # w konkretnym roku jaki wpływ na popualrnosc ma dana cecha
#plot_feature_vs_popularity_all_years() # jaki wpływ na popularność ma dana cecha na przestrzeni lat
#plot_features_vs_time(2022) # jak sie zmielao wykrozystanie cech w danym roku
features_vs_time() # jak sie zmienialo wykorzystanie cech na przestrzeni lat