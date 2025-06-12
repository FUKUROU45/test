import streamlit as st
import random

# タイトルと説明
st.title("うらない！")
st.write("あなたの運勢を占ってみましょう！")

# ボタンを作成
if st.button('占いを始める'):
    # 占いの結果をランダムに生成
    results = ["大吉", "中吉", "小吉", "凶"]
    result = random.choice(results)

    # 結果を表示
    st.write(f"あなたの運勢は：{result}")
