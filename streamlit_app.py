import streamlit as st
import random

st.title("🧮 数学クイズ - 四則演算")

# スコアの初期化
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0

# 問題の生成
operators = ["+", "-", "*", "/"]
a = random.randint(1, 20)
b = random.randint(1, 20)
op = random.choice(operators)

# わり算のゼロ除算回避
if op == "/":
    b = random.randint(1, 10)  # bをゼロ以外に

# 問題表示
st.subheader("次の計算をしてください：")
st.latex(f"{a} {op} {b}")

# 正解を計算
if op == "+":
    correct = a + b
elif op == "-":
    correct = a - b
elif op == "*":
    correct = a * b
elif op == "/":
    correct = round(a / b, 2)  # 少数第2位まで

# ユーザーの解答入力
user_answer = st.number_input("答えを入力（小数は小数第2位まで）", step=0.01)

# 答えるボタン
if st.button("答える"):
    st.sess





