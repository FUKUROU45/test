import streamlit as st
import random
import sympy as sp

# 問題生成関数
def generate_problem():
    problem_type = random.choice(["basic", "equation", "sqrt", "factor"])
    
    if problem_type == "basic":
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        op = random.choice(["+", "-", "*", "/"])
        question = f"{a} {op} {b}"
        answer = eval(question)
    
    elif problem_type == "equation":
        x = sp.Symbol('x')
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 20)
        expr = sp.Eq(a*x + b, c)
        solution = sp.solve(expr, x)
        question = f"{sp.pretty(expr)} を解け"
        answer = float(solution[0])
    
    elif problem_type == "sqrt":
        a = random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100])
        question = f"√{a} を計算せよ"
        answer = a ** 0.5

    elif problem_type == "factor":
        x = sp.Symbol('x')
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        expr = (x + a)*(x + b)
        expanded = sp.expand(expr)
        question = f"{sp.pretty(expanded)} を因数分解せよ"
        answer = expr
    
    return question, answer, problem_type

# セッションステートでスコア管理
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer, st.session_state.type = generate_problem()

st.title("🧠 中学レベル 計算ゲーム")

st.markdown("以下の問題を解いてください：")
st.latex(st.session_state.question)

user_input = st.text_input("答えを入力してください（数値は少数で、因数分解は (x+a)(x+b) 形式）：")

if st.button("答え合わせ"):
    correct = False
    try:
        if st.session_state.type == "factor":
            # 入力を式として解釈して比較
            x = sp.Symbol('x')
            user_expr = sp.sympify(user_input)
            correct = sp.expand(user_expr) == sp.expand(st.session_state.answer)
        else:
            user_val = float(user_input)
            correct = abs(user_val - st.session_state.answer) < 0.01
    except:
        st.error("入力形式に誤りがあります。")

    if correct:
        st.success("正解です！ 🎉")
        st.session_state.score += 1
    else:
        st.error(f"不正解です。正しい答えは {st.session_state.answer} です。")
    
    # 次の問題を出す
    st.session_state.question, st.session_state.answer, st.session_state.type = generate_problem()

st.markdown(f"**スコア：{st.session_state.score}**")

