import requests as req
import pandas as pd
import math
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


# api_hh_vacancies_rq(site, comp, area, pg, per_pg, sort, date_to, date_from, api_df)
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
    df_all = (df_all.set_index('id').join(vac_desc.set_index('id'))).reset_index()
    ls_id = ((df_all.groupby(by='id').idxmin()['premium']).reset_index().set_index('premium')).index.to_list()
    df_all = df_all[(df_all.reset_index())['index'].isin(ls_id)].set_index('id')
    return df_all


def api_hh_vacancy_rq(site='', df_vac_rq=pd.DataFrame(columns=['id', 'description','skills'])):
    if len(site) > 0:
        api_hh_vac_rq = req.get(site).json()
        df_vac_rq = df_vac_rq.append(pd.DataFrame([[api_hh_vac_rq.get('id'), api_hh_vac_rq.get('description'),
                                                    api_hh_vac_rq.get('key_skills')]],
                                                  columns=['id', 'description', 'skills']))
    else:
        print('Не передан параметр сайта')
    return df_vac_rq


def hh_plot_date_count(df=pd.DataFrame(), width=15, height=10, plt_type=''):
    if ~df.empty:
        plt.figure(figsize=(width, height))
        if plt_type == 'bar':
            plt.bar(df.x, df.y)
        else:
            plt.plot(df.set_index('x'))
            plt.yticks(range(0, 901, 50))
            plt.xticks(df.x, rotation=90)
            plt.grid()
        plt.show()
    else:
        print('Не передан параметр ser передающий в функцию серию')


# a = pd.DataFrame(columns=['id', 'url'])
# b = pd.DataFrame(columns=['id', 'description'])
# # print(a)
# a = a.append(pd.DataFrame([[42975821, 'https://api.hh.ru/vacancies/42975821']], columns=['id', 'url']))
# b = b.append(pd.DataFrame([[42975821, 'dgpughafpuyp3w']], columns=['id', 'description']))
# print(a)
# print(b)
# print('-----------------------------------------------------')
# # print(a[['description']].iloc[0])
# a = a.set_index('id').join(b.set_index('id'))
# print(a)