import psycopg2
import pandas as pd
# import plotly
# import plotly.graph_objs as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.io as pio
import seaborn as sns
import matplotlib.pyplot as plt

# pio.renderers.default

DB_HOST = '52.157.159.24'
DB_USER = 'student10'
DB_USER_PASSWORD = 'student10_password'
DB_NAME = 'sql_ex_for_student10'

new_con = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_USER_PASSWORD, dbname=DB_NAME, port=5432)


pd_count_products_by_makers = pd.read_sql_query(sql="select * From count_products_by_makers order by maker"
                                                , con=new_con)
sns.barplot(x='maker', y='count', data=pd_count_products_by_makers)
plt.title('Количество устройств на рынке по производителям')
plt.show()


pd_sunk_ships_by_classes = pd.read_sql_query(sql="select * From sunk_ships_by_classes", con=new_con)
sns.barplot(x='ship_class', y='quantity', data=pd_sunk_ships_by_classes)
plt.title('Количество кораблей в разразе класса корабля')
plt.show()



pd_classes_count_country = pd.read_sql_query(
    '''select country, count(*) as quantity 
        from classes 
        group by country 
        order by country'''
    , con=new_con)
sns.barplot(x='country', y='quantity', data=pd_classes_count_country)
plt.title('Количество кораблей в разрезе класса корабля')
plt.show()



pd_count_ships_by_launched_year = pd.read_sql_query(
    '''select launched as year, count(*) as quantity 
        from ships 
        group by launched 
    order by launched'''
    , con=new_con)
sns.barplot(x='year', y='quantity', data=pd_count_ships_by_launched_year)
plt.title('Количество спущенных на воду кораблей по хронологии')
plt.show()
