import streamlit as st
import random
import math

# タイトル
st.title("📐 面積を求める問題")

# スコア管理
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0

# ランダムな図形とパラメータの生成
shapes = ["円", "三角形", "長方形"]

# ランダムで図形を選択
shape = random.choice(shapes)

# 問題と解答の計算
if shape == "円":
    radius = random.randint(1, 10)  # 半径（1から10までのランダム）
    correct_answer = math.pi * (radius ** 2)  # 円の面積の公式: πr²
    question = f"半径 {radius} の円の面積は？"

elif shape == "三角形":
    base = random.randint(1, 10)  # 底辺（1から10までのランダム）
    height = random.randint(1, 10)  # 高さ（1から10までのランダム）
    correct_answer = 0.5 * base * height  # 三角形の面積の公式: 1/2 * 底辺 * 高さ
    question = f"底辺 {base} 高さ {height} の三角形の面積は？"

elif shape == "長方形":
    length = random.randint(1, 10)  # 長さ（1から10までのランダム）
    width = random.randint(1, 10)  # 幅（1から10までのランダム）
    correct_answer = length * width  # 長方形の面積の公式: 長さ * 幅
    question = f"長さ {length} 幅 {width} の長方形の面積は？"

# 問題を表示
st.subheader(question)

# ユーザーの解答入力
user_answer = st.number_input("面積を入力してください", step=0.01)

# 回答ボタン
if st.button("答える"):
    st.session_state.total += 1
    # 正解判定（誤差範囲で比較）
    if abs(user_answer - correct_answer) < 0.01:
        st.success("正解です！🎉")
        st.session_state.score += 1
    else:
        st.error(f"残念！正解は {correct_answer:.2f} です。")

    # 次の問題へボタン
    if st.button("次の問題へ"):
        st.experimental_rerun()

# スコア表示
st.write(f"✅ 正解数: {st.session_state.score} / {st.session_state.total}")



