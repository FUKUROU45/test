import streamlit as st
import random

st.title("📐 数学公式 暗記＆クイズ")

# 数学の公式データ（拡張可能）
formulas = {
    "円の面積": "πr²",
    "三角形の面積": "1/2 × 底辺 × 高さ",
    "長方形の面積": "縦 × 横",
    "円周の長さ": "2πr",
    "二次方程式の解の公式": "x = (-b ± √(b² - 4ac)) / 2a"
}

# モード選択
mode = st.selectbox("モードを選んでください", ["📖 公式を見る", "🧠 クイズに挑戦"])

# 📖 モード1: 公式一覧を見る
if mode == "📖 公式を見る":
    st.subheader("数学の基本公式一覧")
    for name, formula in formulas.items():
        st.markdown(f"**{name}**: ${formula}$")

# 🧠 モード2: クイズに挑戦
elif mode == "🧠 クイズに挑戦":
    st.subheader("これは何の公式？")

    # ランダムに正解の公式を1つ選ぶ
    correct_key = random.choice(list(formulas.keys()))
    correct_formula = formulas[correct_key]

    # 他の選択肢を作る
    other_keys = list(formulas.keys())
    other_keys.remove(correct_key)
    choices = random.sample(other_keys, 3) + [correc]()_


