import streamlit as st
import random

st.title("📝 英単語クイズ（英語 → 日本語）")

# 中3〜高1レベルの単語リスト（例）
word_list = [
    {"english": "advice", "japanese": "助言"},
    {"english": "solution", "japanese": "解決"},
    {"english": "decide", "japanese": "決める"},
    {"english": "environment", "japanese": "環境"},
    {"english": "comfortable", "japanese": "快適な"},
    {"english": "habit", "japanese": "習慣"},
    {"english": "prepare", "japanese": "準備する"},
    {"english": "dangerous", "japanese": "危険な"},
    {"english": "education", "japanese": "教育"},
    {"english": "borrow", "japanese": "借りる"}
]

# 問題の生成
def generate_word():
    return random.choice(word_list)

if "current_word" not in st.session_state:
    st.session_state.current_word = generate_word()
    st.session_state.answered = False

current = st.session_state.current_word

st.subheader("次の英単語の意味は？")
st.markdown(f"### 🟦 {current['english']}")

user_input = st.text_input("意味を日本語で入力してください：")

# 答え合わせ
if st.button("答え合わせ") and not st.session_state.answered:
    st.session_state.answered = True
    correct = current['japanese']
    if user_input.strip() == correct:
        st.success("✅ 正解！")
    else:
        st.error(f"❌ 不正解... 正解は「{correct}」です。")

# 次の問題
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.current_word = generate_word()
        st.session_state.answered = False
        st.experimental_rerun()











