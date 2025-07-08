import streamlit as st
import random

# タイトル
st.title("1次方程式クイズ")

# 問題の係数をランダムに生成
a = random.randint(1, 10)
b = random.randint(-10, 10)
x = random.randint(-10, 10)
c = a * x + b  # 方程式を成り立たせるcを計算

# 問題文の表示
st.latex(f"{a}x + ({b}) = {c}")

# ユーザーの回答を入力
user_answer = st.number_input("x の値を入力してください", step=1)

# 判定ボタン
if st.button("答え合わせ"):
    if user_answer == x:
        st.success("正解です！🎉")
    else:
        st.error(f"不正解です。正しい答えは x = {x} です。")
