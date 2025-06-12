import streamlit as st
import random

# 単語と意味の辞書（自由に追加可能）
word_dict = {
    "apple": "りんご",
    "dog": "犬",
    "car": "車",
    "book": "本",
    "house": "家",
    "water": "水",
    "computer": "コンピュータ",
    "music": "音楽",
    "teacher": "先生",
    "friend": "友達"
}

st.title("📚 英単語の意味はなんぞや")

# 単語の選出
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(word_dict.keys()))
    st.session_state.correct_meaning = word_dict[st.session_state.current_word]

    # ダミー選択肢をランダムに選ぶ
    meanings = list(word_dict.values())
    meanings.remove(st.session_state.correct_meaning)
    st.session_state.options = random.sample(meanings, 3) + [st.session_state.correct_meaning]
    random.shuffle(st.session_state.options)

# 出題
st.subheader(f"「{st.session_state.current_word}」の意味は？")

# 選択肢表示
user_choice = st.radio("選択肢から選んでください", st.session_state.options)

# 回答ボタン
if st.button("答える"):
    if user_choice == st.session_state.correct_meaning:
        st.success("正解です！🎉")
    else:
        st.error(f"残念！正解は「{st.session_state.correct_meaning}」でした。")

    # 次の問題ボタン
    if st.button("次の問題へ"):
        st.session_state.current_word = random.choice(list(word_dict.keys()))
        st.session_state.correct_meaning = word_dict[st.session_state.current_word]
        meanings = list(word_dict.values())
        meanings.remove(st.session_state.correct_meaning)
        st.session_state.options = random.sample(meanings, 3) + [st.session_state.correct_meaning]
        random.shuffle(st.session_state.options)
        st.experimental_rerun()










