import streamlit as st
import random
import sympy as sp

st.title("📐 方程式クイズ：一次方程式 ax + b = c")

# 問題生成
def generate_equation():
    a = random.randint(1, 10)
    x = sp.Symbol('x')
    solution = random.randint(-10, 10)
    b = random.randint(-10, 10)
    c = a * solution + b
    eq = sp.Eq(a * x + b, c)
    return eq, solution

# セッション状態を初期化
if "eq" not in st.session_state:
    st.session_state.eq, st.session_state.solution = generate_equation()
    st.session_state.answered = False

# 出題
st.subheader("次の方程式を解いてください：")
st.latex(sp.latex(st.session_state.eq))

user_answer = st.text_input("x の値を半角で入力してください（例：-3）")

# 答え合わせ
if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    try:
        user_val = float(user_answer)
        if abs(user_val - st.session_state.solution) < 1e-3:
            st.success("✅ 正解！")
        else:
            st.error(f"❌ 不正解... 正解は x = {st.session_state.solution} です。")
        st.info("方程式を整理して x の値を求めましょう。")
    except:
        st.warning("⚠️ 数字を正しく入力してください。")

# 次の問題
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.eq, st.session_state.solution = generate_equation()
        st.session_state.answered = False
        st.experimental_rerun()










