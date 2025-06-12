import streamlit as st
import random

# タイトル
st.title("🧮 計算問題にチャレンジ！")

# 問題の種類を選択
operation = st.selectbox("問題の種類を選んでください", ["足し算", "引き算", "掛け算", "割り算"])

# 数値をランダムに生成
num1 = random.randint(1, 10)
num2 = random.randint(1, 10)

# 問題の作成
if operation == "足し算":
    correct_answer = num1 + num2
    question = f"{num1} + {num2} = ?"
elif operation == "引き算":
    correct_answer = num1 - num2
    question = f"{num1} - {num2} = ?"
elif operation == "掛け算":
    correct_answer = num1 * num2
    question = f"{num1} × {num2} = ?"
else:  # 割り算
    # 割り切れるようにする
    correct_answer = num1
    num1 = num1 * num2
    question = f"{num1} ÷ {num2} = ?"

# 問題を表示
st.subheader("問題:")
st.write(question)

# ユーザーの解答を入力
user_answer = st.number_input("あなたの答えを入力してください", step=1, format="%d")

# 回答ボタン
if st.button("答える"):
    if user_answer == correct_answer:
        st.success("正解です！🎉")
    else:
        st.error(f"不正解です。正しい答えは {correct_answer} です。")







