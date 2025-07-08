import streamlit as st
import random

st.title("📝 英検4〜3級 英単語クイズ")

# 問題データ（必要に応じて拡張可能）
questions = [
    {
        "question": "次の単語の意味は？ 'apple'",
        "choices": ["りんご", "バナナ", "ぶどう", "オレンジ"],
        "answer": "りんご"
    },
    {
        "question": "次の単語の意味は？ 'library'",
        "choices": ["図書館", "病院", "学校", "駅"],
        "answer": "図書館"
    },
    {
        "question": "'I go to school ___ bus.' 空欄に入るのは？",
        "choices": ["by", "on", "at", "in"],
        "answer": "by"
    },
    {
        "question": "次の単語の意味は？ 'beautiful'",
        "choices": ["きれいな", "にぎやかな", "静かな", "暗い"],
        "answer": "きれいな"
    }
]

# 問題をランダムに1つ選択
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)
    st.session_state.answered = False

question_data = st.session_state.current_question

st.write("### 問題：")
st.write(question_data["question"])

user_choice = st.radio("選択肢：", question_data["choices"])

if st.button("答え合わせ"):
    st.session_state.answered = True
    if user_choice == question_data["answer"]:
        st.success("正解！ 🎉")
    else:
        st.error(f"不正解。正解は「{question_data['answer']}」でした。")

# 次の問題へ
if st.session_state.answered:
    if st.button("次の問題"):
        st.session_state.current_question = random.choice(questions)
        st.session_state.answered = False














