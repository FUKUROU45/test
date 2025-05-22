import streamlit as st

st.title('あいうえお')

st.write('aaaaaaaaa')

user_name = st.text_imput('名前を入力してください')

st.header('あなたの名前は' + str(user_name) + 'です')
h = st.text_imput