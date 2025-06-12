import streamlit as st
import random

# 単語リスト（自由に追加・変更可）
word_list = ["apple", "banana", "grape", "orange", "lemon", "mango", "peach"]

st.title("🔤 単語並べ替えクイズ")

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(word_list)
    st.session_state.shuffled = ''.join(random.sample(st.session_state.current_word, len(st.session_state.current_word)))
    st.session_state.score = 0

# 表示
st.subheader("この単語を元に戻してください:")
st.write(f"🔀 `{st.session_state.shuffled}`")

user_input = st.text_input("答えを入力してください")

if st.button("答える"):
    if user_input.lower() == st.session_state.current_word:
        st.success("正解です！🎉")
        st.session_state.score += 1
    else:
        st.error(f"残念！正解は `{st.session_state.current_word}` です。")

    if st.button("次の問題へ"):
        st.session_state.current_word = random.choice(word_list)
        st.session_state.shuffled = ''.join(random.sample(st.session_state.current_word, len(st.session_state.current_word)))
        st.experimental_rerun()

st.write(f"✅ 正解数: {st.session_state.score}")









