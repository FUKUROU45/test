import streamlit as st
import random

st.title("平方完成の練習アプリ")

# ランダムに2次式の係数を生成 (a != 0)
a = random.choice([1, -1, 2, -2])
b = random.randint(-10, 10)
c = random.randint(-10, 10)

st.markdown(f"次の式を平方完成してください。")

# 2次式を文字列で表示
st.latex(f"{a}x^2 + {b}x + {c}")

# 平方完成の計算 (a(x + b/(2a))^2 - Δ/(4a))
# 判別式 Δ = b^2 - 4ac
delta = b**2 - 4*a*c

# ユーザーの入力を受け取る
user_input = st.text_input("平方完成した式を入力してください（例：2*(x + 3)**2 - 5）")

def is_correct(user_str):
    # 安全のためevalは使わずに簡単な判定のみ（整数値が含まれているかなど）
    # ここでは簡易的に入力の文字列に係数aやb/(2a)を含むかチェック
    # 実用的には高度な数式処理が必要なので、ここは参考程度にしてください
    try:
        # たとえば "(x + 3)" や "-5" が含まれているかどうかでざっくり判定
        from math import isclose
        half_b_over_a = b / (2 * a)
        expected_term = f"(x + {half_b_over_a})"
        # 正確には b/(2a) は符号に注意
        expected_term_alt = f"(x - {-half_b_over_a})"

        # 判別式を計算して平方完成の定数項も計算
        const_term = -delta / (4 * a)

        # 判定はユーザー入力文字列に expected_term または expected_term_alt と
        # const_term の値が入っているか簡易チェック
        if (expected_term in user_str or expected_term_alt in user_str) and str(round(const_term, 2)) in user_str:
            return True
        else:
            return False
    except:
        return False

if user_input:
    if is_correct(user_input):
        st.success("正解です！🎉")
    else:
        st.error("残念、不正解です。もう一度試してみてください。")

if st.button("模範解答を表示"):
    half = b / (2 * a)
    const = -delta / (4 * a)
    st.markdown(f"模範解答:  {a}*(x + ({round(half, 2)}))^2 + ({round(const, 2)})")
