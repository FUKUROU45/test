import streamlit as st
import random

def generate_problem():
    # b と c は偶数にすることで平方完成の結果pが整数になるよう調整
    b = random.choice([i for i in range(-20, 21) if i % 2 == 0 and i != 0])
    c = random.randint(-50, 50)

    # 平方完成のpとqを整数で求める
    p = -b // 2
    q = c - (b**2) // 4

    question = f"次の二次関数を平方完成しなさい:\n\n y = x^2 + {b}x + {c} \n\n整数で答えてください。\n(p, q)の順で入力してください。"
    return question, (p, q)

def main():
    st.title("平方完成トレーニング（整数のみ）")

    if "question" not in st.session_state or st.button("新しい問題を生成"):
        q, ans = generate_problem()
        st.session_state.question = q
        st.session_state.answer = ans
        st.session_state.answered = False

    st.write("### 問題")
    st.write(st.session_state.question)

    with st.form("answer_form"):
        p_input = st.text_input("pの値", key="p_input")
        q_input = st.text_input("qの値", key="q_input")
        submitted = st.form_submit_button("答え合わせ")

        if submitted:
            try:
                p_user = int(p_input)
                q_user = int(q_input)
                p_correct, q_correct = st.session_state.answer

                if p_user == p_correct and q_user == q_correct:
                    st.success("正解です！")
                else:
                    st.error(f"不正解です。正しい答えは p = {p_correct}, q = {q_correct} です。")
            except:
                st.error("整数で入力してください。")

if __name__ == "__main__":
    main()


