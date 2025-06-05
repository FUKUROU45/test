
import streamlit as st

def load_kanji_list(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        kanji_list = [line.strip() for line in f if line.strip()]
    return kanji_list

st.title("漢字リストの読み込み")

filepath = 'kanji_list.txt'  # 漢字リストのファイルパス
kanji_list = load_kanji_list(filepath)

st.write("読み込んだ漢字リスト:")
for kanji in kanji_list:
    st.write(kanji)
