import streamlit as st

# 質問と答え
questions = {
    "織田信長が本能寺で討たれた年は？": "1582",
    "第二次世界大戦が終わった年は？": "1945",
    "アメリカ合衆国の独立宣言は何年？": "1776",
}

# ユーザーのスコアを初期化
score = 0
total_questions = len(questions)

# ユーザーに問題を出題
for question, correct_answer in questions.items():
    user_answer = st.text_input(question, "")

    # ユーザーが答えた後に確認する
    if user_answer:
        if user_answer == correct_answer:
            score += 1
            st.write("正解!")
        else:
            st.write("不正解。正しい答えは：", correct_answer)

# 最終的なスコアを表示
st.write(f"あなたのスコアは {score} / {total_questions} です。")
