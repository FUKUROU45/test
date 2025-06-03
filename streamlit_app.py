import streamlit as st
import random

# 漢字とその読み
kanji_dict = {
    "日": "にち",
    "月": "つき",
    "火": "ひ",
    "水": "みず",
    "木": "き",
    "金": "きん",
    "土": "ど",
    "山": "やま",
    "川": "かわ",
    "鳥": "とり"
}

# 漢字のリスト
kanji_list = list(kanji_dict.keys())

# タイトル
st.title("漢字でGO！ 🚀")

# クイズ
st.subheader("この漢字の読みを当ててください！")

# ランダムに漢字を選ぶ
current_kanji = random.choice(kanji_list)

# ユーザー入力
user_answer = st.text_input(f"漢字: {current_kanji}", "")

# 正解判定
if user_answer:
    if user_answer == kanji_dict[current_kanji]:
        st.success("正解！🎉")
    else:
        st.error(f"間違い！正しい読みは「{kanji_dict[current_kanji]}」です。")

# 次の問題
if st.button("次の問題"):
    current_kanji = random.choice(kanji_list)
    st.experimental_rerun()
