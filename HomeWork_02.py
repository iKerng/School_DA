import pandas as pd
import rq_hh_api
import os.path
import csv
import numpy as np

csv.field_size_limit(100000000)

# + Задание вытащить все вакансии СБЕРа с ХХ (у апи есть ограничение в 2000, подумайте как его обойти)
# + Вытащите все описания этих вакансий
# + Создайте аналогичный vacancy DataFrame только добавьте поле skills
if os.path.isfile('data\\vacancies.csv'):
    print('Выгруженный файл вакансий существует.', end=' ')
    if os.path.getsize('data\\vacancies.csv') == 0:
        print('Файл оказался пустой. Выгружаем данные с HH.ru')
        vacancies = rq_hh_api.append_df_hh_download()
        vacancies.to_csv('data\\vacancies.csv')
    else:
        print('Загрузили данные в DF.')
        vacancies = pd.read_csv('data\\vacancies.csv')

else:
    print('Выгруженный файл Отсутствует. Выгружаем данные с HH.ru.')
    vacancies = rq_hh_api.append_df_hh_download()
    vacancies.to_csv('data\\vacancies.csv')

# + Переведите даты публикаций в datetime
vacancies.published_at = pd.to_datetime(vacancies.published_at)

# + Переведите даты в дни недели, и определите день недели, в который больше всего публикуют вакансий
vacancies[['week_day']] = vacancies.published_at.dt.dayofweek+1
df_for_bar = (vacancies.groupby(by='week_day').count()['id'].reset_index()).rename(columns={'id': 'y', 'week_day': 'x'})
rq_hh_api.hh_plot_date_count(df=df_for_bar, plt_type='bar')

# + Постройте график опубликованных вакансий по датам
df_for_plt = pd.DataFrame(vacancies.groupby(by=vacancies['published_at'].dt.date)['premium'].count())
df_for_plt = df_for_plt.reset_index().rename(columns={'published_at': 'x', 'premium': 'y'})
rq_hh_api.hh_plot_date_count(df_for_plt)

# - Найдите те вакансии с использованием python, которые вам интересны


# - Определите по полю skills какие навыки больше всего востребованы для этих вакансий, и


# - Постройте график наиболее востребованных вакансий