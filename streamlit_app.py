import streamlit as st
import random

st.title("🧪 16進数 ⇄ 10進数 クイズ")

# 問題生成関数
def generate_problem():
    mode = random.choice(["10to16", "16to10"])
    if mode == "10to16":
        decimal = random.randint(0, 255)
        hex_str = hex(decimal)[2:].upper()
        return {
            "mode": mode,
            "question": decimal,
            "answer": hex_str,
            "display": f"{decimal}_{10}"
        }
    else:
        decimal = random.randint(0, 255)
        hex_str = hex(decimal)[2:].upper()
        return {
            "mode": mode,
            "question": hex_str,
            "answer": str(decimal),
            "display": f"{hex_str}_{16}"
        }

# 初期化
if "hex_problem" not in st.session_state:
    st.session_state.hex_problem = generate_problem()
    st.session_state.answered = False

problem = st.session_state.hex_problem
mode = problem["mode"]

# 出題表示
st.subheader("次の変換を行ってください：")
if mode == "10to16":
    st.write("🔄 **10進数 → 16進数**（大文字で入力）")
else:
    st.write("🔄 **16進数 → 10進数**")

st.latex(problem["display"])

user_answer = st.text_input("あなたの答え（例：1A、255 など）")

# 答え合わせ
if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    correct = problem["answer"]
    if user_answer.strip().upper() == correct:
        st.success("✅ 正解！")
    else:
        st.error(f"❌ 不正解... 正解は {correct} です。")
    
    # 解説
    if mode == "10to16":
        st.info(f"{problem['question']} を 16進数にすると {correct} です。")
    else:
        st.info(f"{problem['question']} を 10進数にすると {correct} です。")

# 次の問題
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.hex_problem = generate_problem()
        st.session_state.answered = False
        st.experimental_rerun()









