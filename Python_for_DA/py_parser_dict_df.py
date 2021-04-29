import pandas as pd
import csv
import ast
import numpy as np
import re

csv.field_size_limit(100000000)
vacancies = pd.read_csv('data\\parsed_vacs2.csv')
vacancies = vacancies.set_index('id')


def df_dict_cols_parser(df_pars=pd.DataFrame()):
    for df_column in df_pars.columns:
        print('-------------------------------------------------------')
        print('---------------------' + df_column + '------------------------------')
        print('-------------------------------------------------------')
        if df_column == 'skills':
            df_pars[df_column] = df_pars[df_pars[df_column].notna()][df_column].apply(
                lambda x: re.sub(r"|'name'|{|}|'|: ", "", x)).append(df_pars[df_pars[df_column].isna()][df_column])
            continue
        print(df_pars[df_column].head(5))
        df_pars[df_column] = df_pars[df_pars[df_column].notna()][df_column].apply(
            lambda x: (np.NaN if str(x)[1:-1] == '' else str(x)[1:-1]) if (
                    str(x)[0] == '[' and str(x)[-1] == ']') else str(x)).append(
            df_pars[df_pars[df_column].isna()][df_column])
        print(df_pars[df_column].head(5))
        if df_pars[df_pars[df_column].notna()].empty:
            df_pars.drop(df_column, axis=1)
            continue
        try:
            df_pars[df_pars[df_column].notna()][df_column].apply(lambda x: ast.literal_eval(x).keys())
        except ValueError:
            print('        ' + df_column + ': ValueError')
            continue
        except SyntaxError:
            print('        ' + df_column + ': SyntaxError')
            continue
        except AttributeError:
            print('        ' + df_column + ': AttributeError')
            continue
        max_count_keys = max(df_pars[~df_pars[df_column].isna()][df_column].apply(lambda x: (len(ast.literal_eval(x).
                                                                                                 keys()))).to_list())
        idx = (df_pars[~df_pars[df_column].isna()][df_pars
                                                   [~df_pars[df_column].isna()][df_column].apply(
            lambda x: (len(ast.literal_eval(x).keys()))) == max_count_keys].head(1).index.to_list()[0])
        if max_count_keys > 1:
            list_keys = (df_pars[df_column].loc[[idx]].apply(lambda x: list(ast.literal_eval(x).keys()))).to_list()[0]
            for key in list_keys:
                df_pars[df_column + '_' + key] = df_pars[~df_pars[df_column].isna()][df_column].apply(
                    lambda x: ast.literal_eval(x).get(key)).append(df_pars[df_pars[df_column].isna()][df_column])
    return df_pars


df_column = 'address_metro_stations'
x = "{'station_name': 'Безымянка', 'line_name': 'Первая', 'station_id': '54.313', 'line_id': '54', 'lat': 53.212997, 'lng': 50.248891}"
df_pars = vacancies.copy()
ls = df_pars[df_pars[df_column].notna()][df_column].to_list()
for i in range(len(ls)):
    print(str(i) + ': ' +ls[i])
    ast.literal_eval(ls[i]).keys()



