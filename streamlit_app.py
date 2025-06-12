import streamlit as st
import random

st.title("🧠 方程式クイズ")

# スコア記録
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0

# ランダムな係数を生成
a = random.randint(1, 9)
x_answer = random.randint(1, 10)
b = random.randint(-10, 10)
c = a * x_answer + b

# 問題を表示
st.subheader("次の方程式を解いて、x の値を答えてください：")
st.latex(f"{a}x {'+' if b >= 0 else '-'} {abs(b)} = {c}")

# 解答欄
user_input = st.number_input("x =", step=1.0, format="%.2f")

# 回答処理
if st.button("答える"):
    st.session_state.total += 1
    if abs(user_input - x_answer) < 0.001:
        st.success("正解です！🎉")
        st.session_state.score += 1
    else:
        st.error(f"不正解です。正解は x = {x_answer} です。")

    if st.button("次の問題へ"):
        st.experimental_rerun()

# スコア表示
st.write(f"✅ 正解数: {st.session_state.score} / {st.session_state.total}"）

