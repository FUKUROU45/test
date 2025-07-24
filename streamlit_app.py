import streamlit as st
import random
import sympy as sp

st.title("🧠 平方完成 練習アプリ")

# ランダムな係数で2次式を生成（a ≠ 0）
a = random.choice([1, -1, 2, -2])
b = random.randint(-10, 10)
c = random.randint(-10, 10)

x = sp.Symbol('x')
expr = a * x**2 + b * x + c

st.latex(f"平方完成しなさい: \\quad {sp.latex(expr)}")

# ユーザーに入力を求める
user_input = st.text_input("平方完成した式を入力してください（例：2*(x + 3)**2 - 5）")

# 正誤判定
if user_input:
    try:
        user_expr = sp.sympify(user_input)
        # 式が同値か判定（左右の差が 0 になるか）
        if sp.simplify(user_expr - expr) == 0:
            st.success("🎉 正解です！")
        else:
            st.error("❌ 不正解です。もう一度考えてみましょう。")
    except Exception as e:
        st.error(f"⚠️ 入力エラー：{e}")

# 解答表示
if st.button("模範解答を表示"):
    completed, _ = sp.complete_square(expr, x)
    st.latex(f"{sp.latex(expr)} = {sp.latex(completed)}")
