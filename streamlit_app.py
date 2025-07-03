import streamlit as st
import random

st.title("🔢 二進数 → 十進数 クイズ")

# 問題生成（4ビットまたは5ビット程度）
def generate_question():
    bits = random.randint(3, 5)  # ビット数をランダム化（例：3〜5ビット）
    binary = ''.join(random.choice(['0', '1']) for _ in range(bits))
    decimal = int(binary, 2)
    return binary, decimal

# セッション状態の初期化
if "binary" not in st.session_state:
    st.session_state.binary, st.session_state.decimal = generate_question()
    st.session_state.answered = False

st.subheader("次の2進数を10進数に変換してください：")
st.latex(f"{st.session_state.binary}_{2}")

user_answer = st.text_input("あなたの答え（10進数）:")

# 答え合わせ
if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    try:
        user_input = int(user_answer)
        correct = st.session_state.decimal
        if user_input == correct:
            st.success("✅ 正解！")
        else:
            st.error(f"❌ 不正解... 正解は {correct} です。")
        st.info(f"{st.session_state.binary} は 2進数で、{correct} として表せます。")
    except:
        st.warning("⚠️ 数字を半角で入力してください。")

# 次の問題
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.binary, st.session_state.decimal = generate_question()
        st.session_state.answered = False
        st.experimental_rerun()







