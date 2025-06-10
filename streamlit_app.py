# vocab_learning_app.py

import streamlit as st
import random
from vocab_data import word_list  # 単語リストを別ファイルにしてもOK

# セッションステートの初期化
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.show_answer = False
    st.session_state.score = {"correct": 0, "incorrect": 0}

# 現在の単語
word_data = word_list[st.session_state.index]

st.title("📘 単語学習アプリ")

# 単語の表示
st.subheader(f"単語: {word_data['word']}")

# ボタンで答えを表示
if not st.session_state.show_answer:
    if st.button("答えを見る"):
        st.session_state.show_answer = True
else:
    st.markdown(f"👉 意味: **{word_data['meaning']}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("正解！"):
            st.session_state.score["correct"] += 1
            st.session_state.show_answer = False
            st.session_state.index = (st.session_state.index + 1) % len(word_list)
    with col2:
        if st.button("不正解..."):
            st.session_state.score["incorrect"] += 1
            st.session_state.show_answer = False
            st.session_state.index = (st.session_state.index + 1) % len(word_list)

# スコアの表示
st.markdown("---")
st.markdown(f"✅ 正解: {st.session_state.score['correct']}回")
st.markdown(f"❌ 不正解: {st.session_state.score['incorrect']}回")

