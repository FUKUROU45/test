import streamlit as st

st.title('自己紹介')

st.write('あなたの名前は')

user_name = st.text_imput('名前を入力してください')

st.header('あなたの名前は' + str(user_name) + 'です')

h = st.text_imput('身長を入力してください(m',value=1.67)
w = st.number_input('体重を入力してください(kg)',value=60)

bmi = w/h(h**2)

dbmi = round(bmi,2)

st.header('あなたのBMIは'+str(dbmi)+'です')