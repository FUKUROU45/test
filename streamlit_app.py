import streamlit as st
import random

st.title("平方完成の練習アプリ（難易度選択＆解答表示）")

# 難易度選択
level = st.selectbox("難易度を選んでください", ["初級", "中級", "上級"])

def generate_problem(level):
    if level == "初級":
        a = 1
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
    elif level == "中級":
        a = random.choice([1, -1, 2, -2])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
    else:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-20, 20)
        c = random.randint(-20, 20)
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

if "wrong_problems" not in st.session_state:
    st.session_state.wrong_problems = []

def pick_problem(level):
    candidates = [p for p in st.session_state.wrong_problems if problem_level(p) == level]
    if candidates and random.random() < 0.7:
        return random.choice(candidates)
    else:
        return generate_problem(level)

def problem_level(problem):
    a, b, c = problem
    if a == 1 and -5 <= b <=5 and -5 <= c <= 5:
        return "初級"
    elif a in [1, -1, 2, -2] and -10 <= b <= 10 and -10 <= c <= 10:
        return "中級"
    else:
        return "上級"

if "current_problem" not in st.session_state:
    st.session_state.current_problem = pick_problem(level)

if st.session_state.get("last_level", None) != level:
    st.session_state.current_problem = pick_problem(level)
    st.session_state.last_level = level

a, b, c = st.session_state.current_problem

st.markdown(f"次の式を平方完成してください。")
st.latex(f"{a}x^2 + {b}x + {c}")

user_input = st.text_input("平方完成した式を入力してください（例：2*(x + 3)**2 - 5）")

if user_input:
    correct = is_correct_answer(a, b, c, user_input)
    if correct:
        st.success("正解です！🎉")
        if (a,b,c) in st.session_state.wrong_problems:
            st.session_state.wrong_problems.remove((a,b,c))
        st.session_state.current_problem = pick_problem(level)
        st.experimental_rerun()
    else:
        st.error("残念、不正解です。")
        if (a,b,c) not in st.session_state.wrong_problems:
            st.session_state.wrong_problems.append((a,b,c))
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

# ここで解答表示ボタンを追加
if st.button("模範解答を表示"):
    delta = b**2 - 4*a*c
    half = b / (2 * a)
    const = -delta / (4 * a)
    st.markdown("### 模範解答")
    st.markdown(f"{a}*(x + {round(half, 2)})^2 + {round(const, 2)}")


