import streamlit as st
import random

st.title("🧮 二進数 ⇄ 十進数 クイズ")

# 問題の生成
def generate_problem():
    mode = random.choice(["10to2", "2to10"])
    if mode == "10to2":
        decimal = random.randint(1, 31)
        binary = bin(decimal)[2:]
        return {
            "mode": mode,
            "question": decimal,
            "answer": binary,
            "display": f"{decimal}_{10}"
        }
    else:
        bits = random.randint(3, 5)
        binary = ''.join(random.choice(['0', '1']) for _ in range(bits))
        decimal = int(binary, 2)
        return {
            "mode": mode,
            "question": binary,
            "answer": str(decimal),
            "display": f"{binary}_{2}"
        }

# セッションの初期化
if "problem" not in st.session_state:
    st.session_state.problem = generate_problem()
    st.session_state.answered = False

# 出題
problem = st.session_state.problem
mode = problem["mode"]

st.subheader("次の変換を行ってください：")
if mode == "10to2":
    st.write("🔄 **10進数 → 2進数**")
else:
    st.write("🔄 **2進数 → 10進数**")

st.latex(problem["display"])
user_answer = st.text_input("あなたの答え（2進数または10進数で入力）:")

# 答え合わせ
if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    correct = problem["answer"]
    if user_answer == correct:
        st.success("✅ 正解です！")
    else:
        st.error(f"❌ 不正解... 正解は {correct} です。")
    if mode == "10to2":
        st.info(f"{problem['question']} を 2進数にすると {correct} になります。")
    else:
        st.info(f"{problem['question']} を 10進数にすると {correct} になります。")

# 次の問題へ
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.problem = generate_problem()
        st.session_state.answered = False
        st.experimental_rerun()








