import streamlit as st
import random

# 歴史の出来事と年を辞書形式で定義
history_dict = {
    "アメリカ独立戦争が始まった年": 1775,
    "フランス革命が起こった年": 1789,
    "日本の明治維新が始まった年": 1868,
    "第一次世界大戦が始まった年": 1914,
    "第二次世界大戦が始まった年": 1939,
    "人類が月に初めて着陸した年": 1969,
    "ベルリンの壁が崩壊した年": 1989
}

st.title("🌍 歴史クイズ")

# スコアの管理
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total_questions = 0

# 歴史の出来事をランダムに選ぶ
current_event = random.choice(list(history_dict.keys()))
correct_year = history_dict[current_event]

# ダミー選択肢を生成（正しい年を含めた4択）
years = list(history_dict.values())
years.remove(correct_year)
options = random.sample(years, 3) + [correct_year]
random.shuffle(options)

# 出題
st.subheader(f"{current_event}は何年に起こったか？")
user_choice = st.radio("選択肢から選んでください", options)

# 回答ボタン
if st.button("答える"):
    if user_choice == correct_year:
        st.success("正解です！🎉")
        st.session_state.score += 1
    else:
        st.error(f"残念！正解は「{correct_year}年」でした。")
    
    # 問題数をカウント
    st.session_state.total_questions += 1

    # 次の問題へボタン
    if st.button("次の問題へ"):
        st.experimental_rerun()

# 現在のスコアを表示
st.write(f"✅ 正解数: {st.session_state.score} / {st.session_state.total_questions}")

