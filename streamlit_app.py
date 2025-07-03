import streamlit as st
import random
import time

TIME_LIMIT = 10  # 秒数の設定（例：10秒）

st.title("⏱️ 時間制限付き！四則演算クイズ")

# 問題の生成
def generate_question():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-", "*", "/"])
    if op == "/":
        a = a * b
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, round(answer, 2)

# 初期化
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question()
    st.session_state.start_time = time.time()
    st.session_state.result = None

# 経過時間を確認
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, TIME_LIMIT - int(elapsed_time))

st.subheader("問題：")
st.latex(st.session_state.question)
st.info(f"残り時間：{remaining_time} 秒")

if remaining_time == 0 and st.session_state.result is None:
    st.session_state.result = "timeout"

# 回答入力
if st.session_state.result is None:
    user_input = st.text_input("答えを入力してください（10秒以内）:")

    if st.button("答え合わせ"):
        elapsed_time = time.time() - st.session_state.start_time
        if elapsed_time > TIME_LIMIT:
            st.error("⌛ 時間切れ！")
            st.session_state.result = "timeout"
        else:
            try:
                user_answer = float(user_input)
                correct = abs(user_answer - st.session_state.answer) < 0.01
                if correct:
                    st.success("✅ 正解！")
                    st.session_state.result = "correct"
                else:
                    st.error(f"❌ 不正解... 正解は {st.session_state.answer} です。")
                    st.session_state.result = "wrong"
            except:
                st.warning("⚠️ 数字で答えてください。")

# タイムアウトメッセージ
if st.session_state.result == "timeout":
    st.error(f"⏰ 時間切れ！正解は {st.session_state.answer} でした。")

# 次の問題へ
if st.session_state.result:
    if st.button("次の問題へ"):
        st.session_state.question, st.session_state.answer = generate_question()
        st.session_state.start_time = time.time()
        st.session_state.result = None
        st.experimental_rerun()





