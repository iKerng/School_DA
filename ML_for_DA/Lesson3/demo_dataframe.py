import streamlit as st
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

@st.cache()
def get_data():
    df_s = pd.read_csv('data/housing.csv')
    return df_s

df = get_data()

st.header('MVP предсказание стоимости жилья')

if st.checkbox('Отобразить данные'):
    st.write(df)
    st.line_chart(df)

# 1.Добавить в  demo_dataframe.py  возможность выбора (от 10 до 35% с шагом 5) размера test выборки с помощью streamlit.selectbox
size_test = st.selectbox(label='Выберите размер test выборки', options=range(10, 36, 5))

if st.button('Создать модель'):
    X_train, X_test, y_train, y_test = train_test_split(df.drop('MEDV', axis=1), df['MEDV'], test_size=size_test/100,
                                                        random_state=0)
    st.text('Размер данных-'+str(X_train.shape) + str( X_test.shape))

    st.text('Старт модели')
    model = CatBoostRegressor()
    model.fit(X_train,y_train)
    st.text('Обучили модель')
    pred = model.predict(X_test)
    st.text(str(np.sqrt(mean_squared_error(y_test,pred))))
    # st.write(pd.DataFrame(pred))
    # 2. Отобразить результат предсказания - pd. DataFrame(y_test, pred)
    if st.checkbox('Отобразить результат предсказания', value=False):
        st.write(pd.DataFrame({'real':y_test, 'predict':pred}))
    # st.w

