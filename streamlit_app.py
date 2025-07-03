import streamlit as st
import random

st.title("💡 二進数クイズ（10進 → 2進）")

# 問題を出す（ランダムな10進数を2進数に変換）
def generate_question():
    number = random.randint(1, 31)  # 5ビット範囲内
    return number, bin(number)[2:]  # bin()の接頭辞「0b」を除去

if "decimal" not in st.session_state:
    st.session_state.decimal, st.session_state.binary = generate_question()
    st.session_state.answered = False

st.subheader("次の10進数を2進数に変換してください：")
st.latex(f"{st.session_state.decimal}_{10}")

user_answer = st.text_input("あなたの答え（例：1010）:")

if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    correct = st.session_state.binary
    if user_answer == correct:
        st.success("✅ 正解です！")
    else:
        st.error(f"❌ 不正解... 正解は {correct} です。")
        st.info(f"ヒント：2で割りながら余りを記録する方法で変換できます。")

# 次の問題へ
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.decimal, st.session_state.binary = generate_question()
        st.session_state.answered = False
        st.experimental_rerun()






