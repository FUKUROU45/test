import streamlit as st
import random
import math
import time

def generate_problem():
    problem_type = random.choice(["四則演算", "平方根", "少数計算"])

    if problem_type == "四則演算":
        op = random.choice(["+", "-", "*", "/"])
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        # 割り算は割り切れる数にする
        if op == "/":
            a = a * b
        question = f"{a} {op} {b}"
        answer = eval(question)
        if op == "/":
            answer = round(answer, 2)  # 小数第2位まで
        return question, answer

    elif problem_type == "平方根":
        # 1〜15の平方数からランダムに
        n = random.randint(1, 15)
        question = f"√{n*n}"
        answer = n
        return question, answer

    else:  # 少数計算
        op = random.choice(["+", "-", "*", "/"])
        a = round(random.uniform(1, 10), 2)
        b = round(random.uniform(1, 10), 2)
        # 割り算は割り切れるよう調整
        if op == "/":
            a = round(a * b, 2)
        question = f"{a} {op} {b}"
        answer = eval(question)
        answer = round(answer, 2)
        return question, answer

def main():
    st.title("⚡ 中学生向け高速暗算トレーニング")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "duration" not in st.session_state:
        st.session_state.duration = 60
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = None

    if st.session_state.start_time is None:
        st.subheader("ゲーム設定")
        duration = st.selectbox("制限時間(秒)", [15, 30, 60, 90], index=2)
        st.session_state.duration = duration

        if st.button("ゲーム開始"):
            st.session_state.start_time = time.time()
            q, a = generate_problem()
            st.session_state.current_question = q
            st.session_state.current_answer = a
            st.session_state.score = 0
            st.experimental_rerun()

    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.duration - elapsed

        if remaining <= 0:
            st.subheader("時間切れ！")
            st.write(f"最終スコア: {st.session_state.score}")
            if st.button("もう一度やる"):
                for key in ["start_time", "score", "current_question", "current_answer"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
            return

        st.write(f"残り時間: {int(remaining)}秒")
        st.write(f"スコア: {st.session_state.score}")
        st.subheader(f"問題: {st.session_state.current_question}")

        with st.form("answer_form"):
            user_answer = st.text_input("答えを入力してください", key="answer_input")
            submitted = st.form_submit_button("回答")

            if submitted:
                try:
                    # 答えが整数か小数か判別して比較
                    correct = False
                    if isinstance(st.session_state.current_answer, int) or (st.session_state.current_answer).is_integer():
                        if int(user_answer) == int(st.session_state.current_answer):
                            correct = True
                    else:
                        if abs(float(user_answer) - float(st.session_state.current_answer)) < 0.01:
                            correct = True

                    if correct:
                        st.success("正解！")
                        st.session_state.score += 1
                    else:
                        st.error(f"不正解。正しい答えは {st.session_state.current_answer} です。")
                except:
                    st.error("数値で答えてください。")

                q, a = generate_problem()
                st.session_state.current_question = q
                st.session_state.current_answer = a
                st.experimental_rerun()

if __name__ == "__main__":
    main('')
