import pandas as pd

import os
PATH = os.getcwd()


def handler(dataset, csv_name):
    Mean = []
    Min = []
    Max = []
    Median = []
    Mode = []
    for column in dataset.columns:
        if column in Exclude:
            Mean.append('-')
            Min.append('-')
            Max.append('-')
            Median.append('-')
            Mode.append(dataset[column].mode()[0])
        else:
            Mean.append(float(dataset[column].mean()))
            Min.append(float(dataset[column].min()))
            Max.append(float(dataset[column].max()))
            Median.append(float(dataset[column].median()))
            try:
                Mode.append(dataset[column].mode()[0])
            except:
                Mode.append('-')
    
    stat_frame = pd.DataFrame(
        {'Mean': Mean, 'Max': Max, 'Min': Min, 'Median': Median, 'Mode': Mode},
    index=dataset.columns)

    

    stat_frame.to_csv('%s/analysis/%s.csv' % (PATH, csv_name))
    print('--------------------%s-------------------\n' % csv_name)
    print(stat_frame, '\n')

    '''Для определения наиболее популярного объекта в выборке целесообразно
рассмотреть показатель "Lifetime Engaged Users/Lifetime Post Total Reach",
который говорит о том, какая доля от охвата поста кликнула его.'''

    print('Most popular object in set:\n')
    dataset.loc[:, 'Lifetime Engaged Users/Lifetime Post Total Reach'] = \
    dataset['Lifetime Engaged Users']/dataset['Lifetime Post Total Reach']
    rate = dataset.columns[-1]
    most_popular = dataset[dataset[rate] == dataset[rate].max()]
    print(most_popular)

def new_df(Type):
    global Exclude
    dataset = pd.read_csv('%s/dataset_Facebook.csv' % PATH, sep = ';')
    Exclude = dataset.columns[1:7]
    if Type != '':
        df_ = dataset[dataset['Type'] == Type]
        return df_
    else:
        return dataset
    

Main = new_df('')
Photo = new_df('Photo')
Link = new_df('Link')
Status = new_df('Status')
Video = new_df('Video')        


handler(Main, 'All_rows')
handler(Photo, 'Photo_rows')
handler(Link, 'Link_rows')
handler(Status, 'Status_rows')
handler(Video, 'Video_rows')



