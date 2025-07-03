import streamlit as st
import random
import time

st.title("🧠 暗算トレーニング")

# 設定（範囲・演算子）
operators = ["＋", "－", "×", "÷"]

def generate_problem():
    op = random.choice(operators)
    if op == "＋":
        a, b = random.randint(10, 99), random.randint(10, 99)
        ans = a + b
    elif op == "－":
        a, b = random.randint(50, 99), random.randint(10, 49)
        ans = a - b
    elif op == "×":
        a, b = random.randint(2, 12), random.randint(2, 12)
        ans = a * b
    elif op == "÷":
        b = random.randint(2, 12)
        ans = random.randint(2, 12)
        a = b * ans  # 整数になるように調整
    return f"{a} {op} {b}", ans

# 初期化
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_problem()
    st.session_state.answered = False
    st.session_state.start_time = time.time()

# 出題
st.sub













