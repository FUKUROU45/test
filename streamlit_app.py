import streamlit as st
import random

# タイトル
st.title("🧠 暗算トレーニング")

# 問題の種類
operation = st.selectbox("問題の種類を選んでください", ["足し算", "引き算", "かけ算"])

# 数字の範囲（設定可能）
min_val = st.number_input("最小の数", value=1)
max_val = st.number_input("最大の数", value=20)

# 問題を作成
if st.button("問題を出す"):
    num1 = random.randint(min_val, max_val)
    num2 = random.randint(min_val, max_val)
    
    if operation == "足し算":
        answer = num1 + num2
        question = f"{num1} + {num2}"
    elif operation == "引き算":
        answer = num1 - num2
        question = f"{num1} - {num2}"
    elif operation == "かけ算":
        answer = num1 * num2
        question = f"{num1} × {num2}"

    # セッションに保存
    st.session_state["question"] = question
    st.session_state["answer"] = answer
    st.session_state["show_question"] = True
    st.session_state["result"] = None

# 問題を表示
if "show_question" in st.session_state and st.session_state["show_question"]:
    st.subheader(f"問題：{st.session_state['question']}")
    user_answer = st.number_input("答えを入力", step=1, format="%d", key="user_answer")

    if st.button("答え合わせ"):
        if user_answer == st.session_state["answer"]:
            st.success("正解！🎉")
        else:
            st.error(f"不正解 😢 正解は {st.session_state['answer']} でした。")













