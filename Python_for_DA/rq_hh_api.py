import requests as req
import pandas as pd
import math
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import ast
import numpy as np
import re
import datetime


# api_hh_vacancies_rq(site, comp, area, pg, per_pg, sort, date_to, date_from, api_df)
# https://api.hh.ru/vacancies?employer_id=3529&area=113&page=0&per_page=100
def api_hh_vacancies_rq(site='https://api.hh.ru/vacancies?', comp='3529', area='113', pg='0', per_pg='100',
                        sort='publication_time', date_to='', date_from='1970-01-02', api_df=pd.DataFrame()):
    rq_url_params = dict({'employer_id': comp, 'area': area, 'page': pg, 'per_page': per_pg, 'order_by': sort})
    if date_from != '': rq_url_params['date_from'] = date_from
    if date_to != '':
        rq_url_params['date_to'] = date_to
        rq_url_params['date_from'] = date_from
    api_rq = req.get(site, params=rq_url_params)
    api_rq_df = pd.DataFrame(api_rq.json().get('items'))
    if api_rq.status_code == 200:
        api_df = api_df.append(api_rq_df)
    else:
        print('Получена ошибка с кодом [' + str(api_rq.status_code) + ']. Описание ошибки: '
              + api_rq.json().get('description') + '.')
        print('    ' + site)

    return [api_rq.status_code, api_df, api_rq.json(), api_rq.json().get('found'), api_rq.json().get('pages'),
            api_rq.json().get('per_page')]


# response = api_hh_vacancies_rq()[0] Код ответа                 api_rq_status_code,
# response = api_hh_vacancies_rq()[1] DF массива                 api_df,
# response = api_hh_vacancies_rq()[2] JSON ответа                api_rq_json,
# response = api_hh_vacancies_rq()[3] Общее Кол. вакансий        api_rq_quantity,
# response = api_hh_vacancies_rq()[4] кол. страниц               api_rq_pages,
# response = api_hh_vacancies_rq()[5] Кол. вакансий на странице  api_rq_per_page


# append_df_hh_download(site, comp, area, pg, per_pg, sort, date_to, date_from, df_all)
def append_df_hh_download(site='https://api.hh.ru/vacancies?', comp='3529', area='113', pg='0', per_pg='100',
                          sort='publication_time', date_to='', date_from='1970-01-02', df_all=pd.DataFrame()):
    response = api_hh_vacancies_rq()
    count_set = math.ceil(response[3] / (response[4] * response[5]))
    #     df_all = pd.DataFrame()
    rq_date_to = date_to
    if response[0] == 200:
        for i in tqdm(range(count_set)):
            if i != 0 and date_to == '': rq_date_to = df_all['published_at'].iloc[-1].split('T')[0]
            for k in range(20):
                df_all = api_hh_vacancies_rq(site=site, comp=comp, area=area, pg=str(k), per_pg=per_pg, sort=sort,
                                             date_to=rq_date_to, date_from=date_from, api_df=df_all)[1]
    df_all['url_desc'] = df_all['id'].apply(lambda x: 'https://api.hh.ru/vacancies/' + str(x))
    vac_desc = pd.DataFrame(columns=['id', 'description'])
    for i in tqdm(range(len(df_all))):
        vac_desc = api_hh_vacancy_rq(df_all['url_desc'].iloc[i], vac_desc)
    # print(vac_desc.head(20))
    df_all = (df_all.set_index('id').join(vac_desc.set_index('id'))).reset_index()
    ls_id = ((df_all.groupby(by='id').idxmin()['premium']).reset_index().set_index('premium')).index.to_list()
    df_all = df_all[(df_all.reset_index())['index'].isin(ls_id)].set_index('id')
    df_all = df_dict_cols_parser(df_all)
    df_all = df_all.drop(['department', 'area', 'salary', 'type', 'address', 'sort_point_distance',
                          'insider_interview', 'relations', 'employer', 'snippet', 'contacts', 'schedule',
                          'working_days', 'working_time_intervals', 'working_time_modes', 'accept_temporary',
                          'department_id', 'area_id', 'area_url', 'type_id', 'address_description',
                          'address_lat', 'address_lng', 'address_metro_stations', 'address_id', 'employer_id',
                          'schedule_id', 'working_days_id', 'working_time_intervals_id',
                          'working_time_modes_id', 'employer_logo_urls'], axis=1)
    df_all = df_dict_cols_parser(df_all)
    df_all = df_all.drop(['address_metro', 'address_metro_station_id', 'address_metro_line_id',
                          'address_metro_lat', 'address_metro_lng'], axis=1)
    df_all['description'] = df_all['description'].apply(lambda x: re.sub(r"\<[^>]*\>", '', x))
    df_all['published'] = df_all['published_at'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z'))
    df_all['created_at'] = df_all['created_at'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z'))
    return df_all


def api_hh_vacancy_rq(site='', df_vac_rq=pd.DataFrame(columns=['id', 'description', 'skills'])):
    if len(site) > 0:
        api_hh_vac_rq = req.get(site).json()
        ks = api_hh_vac_rq.get('key_skills')
        if ks == []:
            ks = ''
        else:
            ks = str(api_hh_vac_rq.get('key_skills'))[1:-1]
        df_vac_rq = df_vac_rq.append(pd.DataFrame([[api_hh_vac_rq.get('id'), api_hh_vac_rq.get('description'), ks]],
                                                  columns=['id', 'description', 'skills']))
    else:
        print('Не передан параметр сайта')
    return df_vac_rq


def hh_plot_date_count(df=pd.DataFrame(), width=15, height=10, plt_type='', rot=0):
    if ~df.empty:
        plt.figure(figsize=(width, height))
        if plt_type == 'bar':
            plt.bar(df.x, df.y)
        else:
            plt.plot(df.set_index('x'))
            plt.yticks(range(0, 901, 50))
            plt.grid()
        plt.xticks(df.x, rotation=rot)
        plt.show()
    else:
        print('Не передан параметр ser передающий в функцию серию')


def df_dict_cols_parser(df_pars=pd.DataFrame()):
    for df_column in df_pars.columns:
        # print('------------------------------' + df_column + '------------------------------')
        if df_column == 'skills':
            # print('В колонке Skills лежит кортеж. Преобразуем в список значений.')
            df_pars[df_column] = df_pars[df_pars[df_column].notna()][df_column].apply(
                lambda x: re.sub(r"|'name'|{|}|'|: ", "", x)).append(df_pars[df_pars[df_column].isna()][df_column])
            continue
        # Если в обрабатываемой строке с типом str лежит list, в котором лежит dict, то преобразуем
        # в str в котором лежит dict, чтобы удачно прошел парсинг словаря
        df_pars[df_column] = df_pars[df_pars[df_column].notna()][df_column].apply(
            lambda x: (np.NaN if str(x)[1:-1] == '' else str(x)[1:-1]) if (
                    str(x)[0] == '[' and str(x)[-1] == ']') else str(x)).append(
            df_pars[df_pars[df_column].isna()][df_column])
        # df_column = 'salary'
        if df_pars[df_pars[df_column].notna()].empty:
            # print('Колонка пустая. Удаляем колонку DF: ' + df_column)
            df_pars.drop(df_column, axis=1)
            continue
        try:
            df_pars[df_pars[df_column].notna()][df_column].apply(lambda x: ast.literal_eval(x).keys())
        except ValueError:
            # print('        ' + df_column + ': ValueError')
            continue
        except SyntaxError:
            # print('        ' + df_column + ': SyntaxError')
            continue
        except AttributeError:
            # print('        ' + df_column + ': AttributeError')
            continue
        max_count_keys = max(df_pars[~df_pars[df_column].isna()][df_column].apply(lambda x: (len(ast.literal_eval(x).
                                                                                                 keys()))).to_list())
        # print('Ключей в словаре: ' + str(max_count_keys))
        ls_keys = (df_pars[~df_pars[df_column].isna()][df_pars
                                                       [~df_pars[df_column].isna()][df_column].apply(
            lambda x: (len(ast.literal_eval(x).keys()))) == max_count_keys].head(1).index.to_list()[0])
        if max_count_keys > 1:
            list_keys = (df_pars[df_column].loc[[ls_keys]].apply(lambda x: list(ast.literal_eval(x).keys()))).to_list()[
                0]
            # print('Список ключей: ' + str(list_keys))
            for key in list_keys:
                # print('Создаем дочернюю колонку [' + df_column + '_' + key + '] и помещаем в нее значение из ключа ['
                #       + key + ']')
                df_pars[df_column + '_' + key] = df_pars[~df_pars[df_column].isna()][df_column].apply(
                    lambda x: ast.literal_eval(x).get(key)).append(df_pars[df_pars[df_column].isna()][df_column])
    return df_pars


def best_skill(df_skill=pd.DataFrame(columns=['skill', 'count'])):
    vacs_skills = df_skill[df_skill['skills'].notna()]['skills'].str.split(', ').to_list()
    ls_skills = []
    ls_skills_unique = []
    for i in range(len(vacs_skills)):
        for k in range(len(vacs_skills[i])):
            ls_skills.append(vacs_skills[i][k])
    ser_unique_skills = pd.Series(ls_skills)
    for i in ser_unique_skills.unique():
        ls_skills_unique.append(i)
    df_skills = pd.DataFrame(columns=['skill', 'count'])
    for i in range(len(ls_skills_unique)):
        dic = {'skill': ls_skills_unique[i], 'count': ls_skills.count(ls_skills_unique[i])}
        df_skills.loc[i] = [ls_skills_unique[i], ls_skills.count(ls_skills_unique[i])]
    return print(df_skills.sort_values('count', ascending=False).iloc[0]['skill'])
