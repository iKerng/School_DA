import pandas as pd
from Python_for_DA import rq_hh_api
import os.path
import csv

csv.field_size_limit(100000000)

# + Задание вытащить все вакансии СБЕРа с ХХ (у апи есть ограничение в 2000, подумайте как его обойти)
# + Вытащите все описания этих вакансий
# + Создайте аналогичный vacancy DataFrame только добавьте поле skills
if os.path.isfile('../data/vacancies.csv'):
    print('Выгруженный файл вакансий существует.', end=' ')
    if os.path.getsize('../data/vacancies.csv') == 0:
        print('Файл оказался пустой. Выгружаем данные с HH.ru')
        vacancies = rq_hh_api.append_df_hh_download()
        vacancies.to_csv('data\\vacancies.csv')
    else:
        print('Загрузили данные в DF.')
        vacancies = pd.read_csv('../data/vacancies.csv')
        vacancies = vacancies.set_index('id')

else:
    print('Выгруженный файл Отсутствует. Выгружаем данные с HH.ru.')
    vacancies = rq_hh_api.append_df_hh_download()
    vacancies.to_csv('data\\vacancies.csv')

# + Переведите даты публикаций в datetime
vacancies.published_at = pd.to_datetime(vacancies.published_at)

# + Переведите даты в дни недели, и определите день недели, в который больше всего публикуют вакансий
vacancies[['week_day']] = vacancies.published_at.dt.dayofweek + 1
# Строим график количества публикаций по дням недели
df_for_bar = (vacancies.groupby(by='week_day').count()['premium']).reset_index().rename(
    columns={'premium': 'y', 'week_day': 'x'})
print('Максимальное число публикаций совершается в ' +
      str(df_for_bar[df_for_bar['y'] == max(df_for_bar['y'].to_list())]['x'].to_list()[0]) +
      '-й день недели.')
print('Строим столбчатую диаграмму публикаций вакансий по дням недели.')
rq_hh_api.hh_plot_date_count(df=df_for_bar, plt_type='bar')

# + Постройте график опубликованных вакансий по датам
df_for_plt = pd.DataFrame(vacancies.groupby(by=vacancies['published_at'].dt.date)['premium'].count())
df_for_plt = df_for_plt.reset_index().rename(columns={'published_at': 'x', 'premium': 'y'})
print('Строим график количества публикаций вакансий по датам')
rq_hh_api.hh_plot_date_count(df=df_for_plt, rot=90)

# - Найдите те вакансии с использованием python, которые вам интересны
like_vac = vacancies[['area_name', 'name', 'description', 'skills', 'address_metro_station_name', 'published_at',
                      'archived', 'salary_from', 'salary_to']].copy()
like_vac = like_vac[like_vac['area_name'].str.lower() == 'москва']
like_vac = like_vac[like_vac['description'].str.contains('DA|data analytic|Data analytic|Data Analytic')]
like_vac = like_vac[like_vac['description'].str.lower().str.contains('python')]
# print(like_vac)

# - Определите по полю skills какие навыки больше всего востребованы для этих вакансий, и
print('Список навыков требуемых для данных вакансий: ' +
      str(like_vac[like_vac['skills'].notna()]['skills'].to_list()[:])[1:-1].replace("'", ""))
rq_hh_api.best_skill(like_vac)

# - Постройте график наиболее востребованных вакансий
df_vostr = pd.DataFrame((vacancies.groupby('name').name.count().sort_values(ascending=False))).rename(
    columns={'name': 'count'}).reset_index()
df_vostr = df_vostr.rename(columns={'name': 'x', 'count': 'y'}).head(20)
rq_hh_api.hh_plot_date_count(df=df_vostr, plt_type='bar', rot=90)
