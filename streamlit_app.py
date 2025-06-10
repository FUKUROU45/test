import streamlit as st
import random

st.title("ジャンケンゲーム")

# ジャンケンの手
hands = ["グー", "チョキ", "パー"]

# ユーザーが選択
user_choice = st.radio("あなたの手を選んでください", hands)

if st.button("勝負！"):
    # コンピューターの手をランダムに選ぶ
    comp_choice = random.choice(hands)
    st.write(f"コンピューターの手は: {comp_choice}")

    # 勝敗判定
    if user_choice == comp_choice:
        st.write("引き分けです！")
    elif (user_choice == "グー" and comp_choice == "チョキ") or \
         (user_choice == "チョキ" and comp_choice == "パー") or \
         (user_choice == "パー" and comp_choice == "グー"):
        st.write("あなたの勝ち！🎉")
    else:
        st.write("あなたの負け…😢")




