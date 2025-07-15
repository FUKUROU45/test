import streamlit as st
import random

def generate_linear_problem():
    # y = ax + b の形の一次関数
    a = random.randint(-10, 10)
    while a == 0:
        a = random.randint(-10, 10)
    b = random.randint(-20, 20)
    question = f"一次関数 y = {a}x + {b} のグラフの傾きを答えなさい。"
    answer = a
    return question, answer

def generate_quadratic_problem():
    # 二次関数を平方完成する問題
    # 形：x^2 + bx + c
    b = random.randint(-10, 10)
    c = random.randint(-20, 20)
    # 答えは (x + p)^2 + q の p,q
    p = -b / 2
    q = c - (b**2) / 4
    question = f"二次関数 y = x^2 + {b}x + {c} の平方完成を行い、(x + p)^2 + q の形で表しなさい。p と q を小数第2位まで答えてください。"
    return question, (round(p, 2), round(q, 2))

def main():
    st.title("関数問題トレーニング")

    problem_type = st.selectbox("問題の種類を選択してください", ["一次関数の傾き", "二次関数の平方完成"])

    if st.button("問題を生成"):
        if problem_type == "一次関数の傾き":
            q, a = generate_linear_problem()
            st.session_state.question = q
            st.session_state.answer = a
        else:
            q, a = generate_quadratic_problem()
            st.session_state.question = q
            st.session_state.answer = a
        st.session_state.answered = False

    if "question" in st.session_state:
        st.write("### 問題")
        st.write(st.session_state.question)

        if problem_type == "一次関数の傾き":
            user_answer = st.text_input("傾きの値を入力してください", key="linear_answer")
            if st.button("答え合わせ") and user_answer:
                try:
                    if int(user_answer) == st.session_state.answer:
                        st.success("正解です！")
                    else:
                        st.error(f"不正解です。正しい答えは {st.session_state.answer} です。")
                except:
                    st.error("整数で入力してください。")

        else:  # 二次関数の平方完成
            col1, col2 = st.columns(2)
            with col1:
                p_input = st.text_input("pの値を入力してください", key="p_answer")
            with col2:
                q_input = st.text_input("qの値を入力してください", key="q_answer")

            if st.button("答え合わせ") and p_input and q_input:
                try:
                    p_user = round(float(p_input), 2)
                    q_user = round(float(q_input), 2)
                    p_correct, q_correct = st.session_state.answer
                    if abs(p_user - p_correct) < 0.01 and abs(q_user - q_correct) < 0.01:
                        st.success("正解です！")
                    else:
                        st.error(f"不正解です。正しい答えは p={p_correct}, q={q_correct} です。")
                except:
                    st.error("小数点以下2桁までの数字で入力してください。")

if __name__ == "__main__":
    main()

