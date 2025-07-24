import streamlit as st
import random

st.title("平方完成の練習アプリ（似た問題を出題）")

# 間違えた問題リストをセッション状態で保持
if "wrong_problems" not in st.session_state:
    st.session_state.wrong_problems = []

def generate_problem():
    # まず間違え問題があれば確率でそちらを優先
    if st.session_state.wrong_problems and random.random() < 0.7:
        # 間違え問題からランダムに選択
        return random.choice(st.session_state.wrong_problems)
    else:
        # 新規問題生成
        a = random.choice([1, -1, 2, -2])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        return (a, b, c)

def is_correct_answer(a, b, c, user_str):
    try:
        half_b_over_a = b / (2 * a)
        expected_term1 = f"(x + {round(half_b_over_a, 2)})"
        expected_term2 = f"(x - {round(-half_b_over_a, 2)})"
        delta = b**2 - 4*a*c
        const_term = -delta / (4 * a)
        if (expected_term1 in user_str or expected_term2 in user_str) and str(round(const_term, 2)) in user_str:
            return True
        else:
            return False
    except:
        return False

# 問題を生成・取得
if "current_problem" not in st.session_state:
    st.session_state.current_problem = generate_problem()

a, b, c = st.session_state.current_problem

st.markdown(f"次の式を平方完成してください。")
st.latex(f"{a}x^2 + {b}x + {c}")

user_input = st.text_input("平方完成した式を入力してください（例：2*(x + 3)**2 - 5）")

if user_input:
    correct = is_correct_answer(a, b, c, user_input)
    if correct:
        st.success("正解です！🎉")
        # 正解したら間違え問題リストから削除（あれば）
        if (a,b,c) in st.session_state.wrong_problems:
            st.session_state.wrong_problems.remove((a,b,c))
        # 新しい問題へ
        st.session_state.current_problem = generate_problem()
        st.experimental_rerun()  # ページを更新して新問題を表示
    else:
        st.error("残念、不正解です。")
        if (a,b,c) not in st.session_state.wrong_problems:
            st.session_state.wrong_problems.append((a,b,c))

        # 解答と解説を表示
        delta = b**2 - 4*a*c
        half = b / (2 * a)
        const = -delta / (4 * a)
        st.markdown("### 解答")
        st.markdown(f"平方完成の形は：\n\n{a}*(x + {round(half, 2)})^2 + {round(const, 2)} です。")
        st.markdown("### 解説")
        st.markdown(f"""
平方完成の公式：
\[
ax^2 + bx + c = a\left(x + \frac{{b}}{{2a}}\right)^2 - \frac{{b^2 - 4ac}}{{4a}}
\]

ここで、

- \( a = {a} \)
- \( b = {b} \)
- \( c = {c} \)
- 判別式 \( \Delta = b^2 - 4ac = {delta} \)

を代入して計算しています。
        """)

