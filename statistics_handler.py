import pandas as pd
import os
PATH = os.getcwd()


def handler(dataset, csv_name): #функция-обработчик таблицы
    #создаются списки для статистик по каждому показателю в таблице
    Mean = []
    Min = []
    Max = []
    Median = []
    Mode = []
    #обрабатывается каждое поле в таблице
    for column in dataset.columns:
        if column in Exclude: #для полей с качественными показателями расчитывается только мода
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
            try: #по сути мода в количественных данных не имеет такого значения, из-за низкой частоты элементов
                Mode.append(dataset[column].mode()[0])
            except:
                Mode.append('-')
    #для удобства создается сводная таблица статистики...
    stat_frame = pd.DataFrame(
        {'Mean': Mean, 'Max': Max, 'Min': Min, 'Median': Median, 'Mode': Mode},
    index=dataset.columns)

    
    #... которая сохраняется в формате csv в analysis/
    stat_frame.to_csv('%s/analysis/%s.csv' % (PATH, csv_name))
    print('--------------------%s-------------------\n' % csv_name)
    print(stat_frame, '\n')

    '''Для определения наиболее популярного объекта в выборке целесообразно
рассмотреть показатель "Lifetime Engaged Users/Lifetime Post Total Reach",
который говорит о том, какая доля от охвата поста кликнула его,
или "Total Interactions/Lifetime Post Total Reach", который говорит о доле пользователей взаимодействующих с контентом от охвата поста.
Простой охват не отражает эффективности поста, поскольку он мог и не привлечь внимания. И напротив, количество кликнувших и взаимодействующих с контентом
бесполезны, если охват принимает куда большие масштабы'''

    #функция определена ниже
    most_popular_by('Lifetime Engaged Users', dataset, csv_name)
    most_popular_by('Total Interactions', dataset, csv_name)

    
def most_popular_by(by, dataset, csv_name):    
    print('Most popular object in set by %s:\n' % by)
    dataset.loc[:, '%s/Lifetime Post Total Reach' % by] = \
    dataset[by]/dataset['Lifetime Post Total Reach']
    #во избежание ошибочной интерпретации показателя, необходимо, чтобы охват объекта был на высоком уровне (выше среднего)
    dataset_ = dataset[dataset['Lifetime Post Total Reach'] > dataset['Lifetime Post Total Reach'].mean()]
    rate = dataset_.columns[-1]
    most_popular = dataset_[dataset_[rate] == dataset_[rate].max()]
    print(most_popular)
    most_popular.to_csv('%s/analysis/%s_most_popular_by_%s.csv' % (PATH, csv_name, by))

#во избежание конфликтов копирования таблиц нужна функция, создающая нужную выборку по полю Type
def new_df(Type):
    global Exclude
    dataset = pd.read_csv('%s/dataset_Facebook.csv' % PATH, sep = ';')
    Exclude = dataset.columns[1:7]
    if Type != '':
        df_ = dataset[dataset['Type'] == Type]
        return df_
    else:
        return dataset
    
#создаем все необходимые таблицы и
#производим все необходимые расчеты
handler(new_df(''), 'All_rows')
handler(new_df('Photo'), 'Photo_rows')
handler(new_df('Link'), 'Link_rows')
handler(new_df('Status'), 'Status_rows')
handler(new_df('Video'), 'Video_rows')
