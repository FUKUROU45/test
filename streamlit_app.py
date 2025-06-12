import streamlit as st
import random
import sympy as sp

# シンボル定義
x = sp.Symbol('x')

# 問題生成関数（因数分解）
def generate_factor_problem():
    # 例：(x + a)(x + b) の形
    a = random.randint(-10, 10)
    b = random.randint(-10, 10)
    factored = (x + a) * (x + b)
    expanded = sp.expand(factored)
    question = expanded
    answer = factored
    return question, answer

# 初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    q, a = generate_factor_problem()
    st.session_state.question = q
    st.session_state.answer = a

# タイトル
st.title("🧩 因数分解クイズ")
st.markdown("次の式を**因数分解**せよ：")
st.latex(sp.latex(st.session_state.question))

# ユーザー入力
user_input = st.text_input("因数分解した形を (x + a)(x + b) のように入力してください：")

if st.button("答え合わせ"):
    try:
        # 入力をsympy式に変換
        user_expr = sp.sympify(user_input)
        
        # 展開して比較（同値ならOKとする）
        correct = sp.expand(user_expr) == sp.expand(st.session_state.answer)

        if correct:
            st.success("🎉 正解です！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解です。正しい答えは `{sp.pretty(st.session_state.answer)}`")
        
        # 次の問題へ
        q, a = generate_factor_problem()
        st.session_state.question = q
        st.session_state.answer = a

    except Exception as e:
        st.error(f"⚠️ 入力エラー: {e}")

# スコア表示
st.markdown(f"**現在のスコア：{st.session_state.score}**")





