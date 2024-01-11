import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties
import os

font = FontProperties()
font.set_family('sans-serif')
font.set_name('Helvetica')
font.set_size('18')

font1 = FontProperties()
font1.set_family('sans-serif')
font1.set_name('Helvetica')
font1.set_size('13')


def plot_feature_vs_popularity_all_years(feature_name):
    directory = 'CSV/'
    all_files = os.listdir(directory)
    df_list = []

    features_y = 'track_popularity'

    for filename in all_files:
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            df_list.append(df)

    x_values = []
    y_values = []

    for df in df_list:
        x_values.extend(df[feature_name])
        y_values.extend(df[features_y])


    plt.scatter(x_values, y_values)
    plt.xlabel(feature_name)
    plt.ylabel(features_y)
    plt.title(f"{feature_name} vs track_popularity")
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

    for i in range(num_rows):
        for j in range(num_cols):
            feature_name = list_of_features[i * num_cols + j]
            axs[i, j].scatter(df['release_date'], df[feature_name], alpha=0.5)
            axs[i, j].set_title(f"release_date vs {feature_name}")
            axs[i, j].set_xlabel("release_date")
            axs[i, j].set_ylabel(feature_name)
    plt.tight_layout()
    plt.show()

list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                        'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x', 'track_popularity', 'popularity_y']

# popularity_x - artist popularity
# popularity_y - album popularity

def plot_box(feature):
    positions = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
                 '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
                 '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'
                 ]
    data = []
    for position in positions:
        file_path = f'CSV/{position}.csv'
        df = pd.read_csv(file_path)

        box_data = df[feature]
        data.append(box_data)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    positions = [eval(i) for i in positions]
    ticks = np.arange(1, 28, 3).tolist()
    labels = [positions[i - 1] for i in ticks]
    meanpointprops = dict(marker='o', markeredgecolor='black',
                          markerfacecolor='black', markersize=4)
    medianprops = dict(linestyle='-.', linewidth=3.5, color='firebrick')
    bp = ax.boxplot(data, widths=0.65, showmeans=True, medianprops=medianprops, meanprops=meanpointprops, whis=[10, 90],
                    showfliers=False, patch_artist=True)
    plt.title(f'Track {feature} over time', fontproperties=font, fontsize=20)
    plt.xlabel('Release year', fontproperties=font, labelpad=12)
    plt.ylabel(f'Track {feature}', fontproperties=font, labelpad=13)
    plt.xticks(ticks=ticks, labels=labels, fontproperties=font1)
    plt.yticks(fontproperties=font1)
    plt.grid()
    if feature == 'duration_ms':
        for patch in bp['boxes']:
            patch.set(facecolor='pink')
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        plt.ylim(7*10**4, 3.7*10**5)

    elif feature == 'acousticness':
        for patch in bp['boxes']:
            patch.set(facecolor='darkturquoise')

    elif feature == 'danceability':
        for patch in bp['boxes']:
            patch.set(facecolor='orchid')

    elif feature == 'energy':
        for patch in bp['boxes']:
            patch.set(facecolor='skyblue')

    elif feature == 'instrumentalness':
        for patch in bp['boxes']:
            patch.set(facecolor='white')

    elif feature == 'liveness':
        for patch in bp['boxes']:
            patch.set(facecolor='moccasin')

    elif feature == 'loudness':
        for patch in bp['boxes']:
            patch.set(facecolor='mediumslateblue')
        plt.ylabel(f'Track {feature} [dB]', fontproperties=font, labelpad=13)

    elif feature == 'speechiness':
        for patch in bp['boxes']:
            patch.set(facecolor='lightsteelblue')

    elif feature == 'tempo':
        for patch in bp['boxes']:
            patch.set(facecolor='mediumspringgreen')
        plt.ylabel(f'Track {feature} [BPM]', fontproperties=font, labelpad=13)

    elif feature == 'valence':
        for patch in bp['boxes']:
            patch.set(facecolor='azure')

    elif feature == 'key':
        for patch in bp['boxes']:
            patch.set(facecolor='palegoldenrod')

    plt.show()



plot_box('key')
print('dupa')
'''
def boxplot__features_vs_time(year):     #PROBLEMATYCZNE PRZEZ FORMAT DANYCH: RRRR-MM-DD
    file_path = f'CSV/{year}.csv'
    df = pd.read_csv(file_path)

    list_of_features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                       'key', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'popularity_x']

    num_cols = 3
    num_rows = 4

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(18, 14))

    for i in range(num_rows):
        for j in range(num_cols):
            feature_name = list_of_features[i * num_cols + j]

            grouped_data = [df[df['release_date'] == year][feature_name].dropna().values for year in df['release_date'].unique()]
            axs[i, j].boxplot(grouped_data, vert=True, labels=df['release_date'].unique())

            axs[i, j].set_title(f"release_date vs {feature_name}")
            axs[i, j].set_xlabel("release_date")
            axs[i, j].set_ylabel(feature_name)
    plt.tight_layout()
    plt.show()
    
    
boxplot__features_vs_time(2022)
'''


'''                                 boxplot popularnosc albumu vs lata - wymaga R
from rpy2 import robjects
from rpy2.robjects import r
from rpy2.robjects.lib import ggplot2
from rpy2.robjects.packages import importr
from rpy2.robjects.lib.ggplot2 import ggtitle, theme_bw, aes_string

file_path = f'CSV/2022.csv'
df = pd.read_csv(file_path)

q16_boxplot = ggplot2.ggplot(df) + \
              ggplot2.aes_string(x='factor(year)', y='album_popularity') + \
              ggplot2.geom_boxplot(fill="rgb(0,0,215,100,maxColorValue=255)", lwd=0.2, color="black",
                                   outlier_color="brown", outlier_shape=20, outlier_size=1) + \
              ggplot2.stat_summary(fun_y='mean', geom="line",
                                   color="gold", size=0.9) + \
              ggplot2.stat_summary(fun_y='mean', geom="point", size=0.5, color="black") + \
              ggplot2.theme(panel_background=ggplot2.element_blank(),
                            axis_text_x=ggplot2.element_text(angle=45, hjust=1, size=4)) + \
              ggplot2.xlab('year')

print(q16_boxplot)
'''



#plot_features_vs_popularity(2022)
#plot_feature_vs_popularity_all_years('energy')
#plot_features_vs_time(2022)