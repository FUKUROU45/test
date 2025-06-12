import streamlit as st
import random

# 単語とその意味を辞書で定義
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

st.title("📚 英単語の意味当てクイズ")

# スコアの管理
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total_questions = 0

# 問題をランダムに選ぶ
current_word = random.choice(list(word_dict.keys()))
correct_meaning = word_dict[current_word]

# ダミー選択肢を生成
meanings = list(word_dict.values())
meanings.remove(correct_meaning)
options = random.sample(meanings, 3) + [correct_meaning]
random.shuffle(options)

# 出題
st.subheader(f"「{current_word}」の意味は？")
user_choice = st.radio("選択肢から選んでください", options)

# 回答ボタン
if st.button("答える"):
    if user_choice == correct_meaning:
        st.success("正解です！🎉")
        st.session_state.score += 1
    else:
        st.error(f"残念！正解は「{correct_meaning}」でした。")
    
    # 問題数をカウント
    st.session_state.total_questions += 1

    # 次の問題へボタン
    if st.button("次の問題へ"):
        st.experimental_rerun()

# 現在のスコアを表示
st.write(f"✅ 正解数: {st.session_state.score} / {st.session_state.total_questions}")
