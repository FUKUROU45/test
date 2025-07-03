import streamlit as st
import random

st.title("🧮 四則演算クイズ")

# 問題を生成
def generate_question():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-", "*", "/"])

    # わり算の時は割り切れるように調整
    if op == "/":
        a = a * b
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, round(answer, 2)

# セッションで保持
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question()

st.subheader("次の計算を解いてください：")
st.latex(st.session_state.question)

user_input = st.text_input("あなたの答え（小数は . を使って2桁まで）:")

if st.button("答え合わせ"):
    try:
        user_answer = float(user_input)
        correct = abs(user_answer - st.session_state.answer) < 0.01  # 誤差対策
        if correct:
            st.success("✅ 正解です！")
        else:
            st.error(f"❌ 不正解... 正解は {st.session_state.answer} です。")
        # 次の問題へ
        if st.button("次の問題へ"):
            st.session_state.question, st.session_state.answer = generate_question()
            st.experimental_rerun()
    except:
        st.warning("⚠️ 数字で答えてください。")




