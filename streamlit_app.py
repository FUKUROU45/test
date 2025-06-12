import streamlit as st
import random
import time

st.title("🧠 記憶力トレーニング")

# ステップ1: ランダムな数字列を生成
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.numbers = []

if st.session_state.step == 1:
    if st.button("数字を表示"):
        st.session_state.numbers = [random.randint(0, 9) for _ in range(5)]
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.write("覚えてください：")
    st.write(" ".join(str(n) for n in st.session_state.numbers))
    time.sleep(3)  # 表示時間
    st.session_state.step = 3
    st.experimental_rerun()

elif st.session_state.step == 3:
    st.write("入力してください：")
    user_input = st.text_input("スペースで区切って入力（例: 1 3 5 7 9）")

    if st.button("答える"):
        try:
            user_numbers = list(map(int, user_input.strip().split()))
            if user_numbers == st.session_state.numbers:
                st.success("正解です！👏")
            else:
                st.error(f"残念、不正解。正解は {' '.join(map(str, st.session_state.numbers))} でした。")
        except:
            st.error("入力形式が正しくありません。")
        # 再挑戦
        if st.button("もう一度挑戦"):
            st.session_state.step = 1
            st.experimental_rerun()








