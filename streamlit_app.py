import streamlit as st

# 漢字リストをPythonのリストで定義
kanji_list = [
    "漢", "字", "学", "習", "日", "本", "語", "書", "読", "写"
]

st.title("漢字リスト表示アプリ")

st.write("漢字リスト:")
for kanji in kanji_list:
    st.write(kanji)

