import streamlit as st
import random

def generate_question():
    # bは偶数にして平方完成しやすくする
    b = random.choice(range(-10, 11, 2))
    q = random.randint(-10, 10)
    c = (b / 2) ** 2 + q
    p = -b / 2
    return b, c, p, q

def main():
    st.title("平方完成の問題")

    if "b" not in st.session_state or st.button("新しい問題を出す"):
        b, c, p, q = generate_question()
        st.session_state.b = b
        st.session_state.c = c
        st.session_state.p = p
        st.session_state.q = q
        st.session_state.solved = False

    st.write(f"次の式を平方完成してください：")
    st.latex(f"x^2 + {st.session_state.b} x + {round(st.session_state.c, 2)}")

    if not st.session_state.get("solved", False):
        with st.form("answer_form"):
            p_input = st.text_input("pの値 (例: 3.5)")
            q_input = st.text_input("qの値 (例: -2)")
            submitted = st.form_submit_button("答え合わせ")

            if submitted:
                try:
                    p_user = float(p_input)
                    q_user = float(q_input)
                    if abs(p_user - st.session_state.p) < 0.01 and abs(q_user - st.session_state.q) < 0.01:
                        st.success("正解です！")
                        st.session_state.solved = True
                    else:
                        st.error(f"不正解です。正しい答えは p={round(st.session_state.p,2)}, q={round(st.session_state.q,2)} です。")
                except ValueError:
                    st.error("数値を入力してください。")

if __name__ == "__main__":
    main()

