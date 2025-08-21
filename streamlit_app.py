import streamlit as st
import random
import sympy as sp
import time
import numpy as np
import matplotlib.pyplot as plt

# シンボル定義
x = sp.symbols('x')

def generate_question(difficulty):
    if difficulty == "初級":
        a = random.choice([1, -1])
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
    elif difficulty == "中級":
        a = random.choice([-2, -1, 1, 2])
        b = random.randint(-8, 8)
        c = random.randint(-8, 8)
    else:  # 上級
        a = random.randint(-5, 5)
        while a == 0:
            a = random.randint(-5, 5)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
    return a, b, c

def format_quadratic(a, b, c):
    return sp.expand(a * x**2 + b * x + c)

def complete_the_square(a, b, c):
    h = -b / (2 * a)
    k = a * h**2 + b * h + c
    return a * (x - h)**2 + k, h, k

def compare_expressions(user_input, correct_expr):
    try:
        # "^"を"**"に置換してsympyで評価
        user_expr = sp.sympify(user_input.replace("^", "**"))
        return sp.simplify(user_expr - correct_expr) == 0
    except Exception:
        return False

def plot_graph(a, b, c):
    fig, ax = plt.subplots()
    xx = np.linspace(-10, 10, 400)
    yy = a * xx**2 + b * xx + c
    ax.plot(xx, yy, label=f'f(x) = {a}x² + {b}x + {c}')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("f(x) のグラフ")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    plt.close()

# --- Streamlit UI ---
st.set_page_config(page_title="平方完成トレーニング", layout="centered")
st.title("📘 平方完成トレーニング")

with st.sidebar:
    st.header("設定")
    difficulty = st.radio("難易度", ["初級", "中級", "上級"])
    time_limit = st.selectbox("制限時間（秒）", [0, 30, 60])
    show_graph = st.checkbox("グラフを表示する", value=True)
    total_questions = st.number_input("問題数", 1, 20, 5)

if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.user_answers = []
    st.session_state.results = []
    st.session_state.start_time = None
    st.session_state.completed = False

if not st.session_state.questions:
    for _ in range(total_questions):
        st.session_state.questions.append(generate_question(difficulty))
    st.session_state.start_time = time.time()

index = st.session_state.current_index
a, b, c = st.session_state.questions[index]
question_expr = format_quadratic(a, b, c)
correct_expr, h, k = complete_the_square(a, b, c)

st.markdown(f"### 問題 {index + 1} / {int(total_questions)}")
st.latex(f"f(x) = {sp.latex(question_expr)}")

if show_graph:
    plot_graph(a, b, c)

if time_limit > 0:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = time_limit - elapsed
    st.info(f"⏱ 残り時間: {remaining} 秒")
    if remaining <= 0:
        st.warning("時間切れ！スキップします。")
        st.session_state.user_answers.append("（時間切れ）")
        st.session_state.results.append(False)
        st.session_state.current_index += 1
        if st.session_state.current_index >= total_questions:
            st.session_state.completed = True
        else:
            st.session_state.start_time = time.time()
        st.experimental_rerun()

answer = st.text_input("平方完成の形を入力（例: 2*(x + 1)**2 - 3）", key=index)

col1, col2 = st.columns(2)
with col1:
    if st.button("判定", key=f"check_{index}"):
        is_correct = compare_expressions(answer, correct_expr)
        st.session_state.user_answers.append(answer)
        st.session_state.results.append(is_correct)
        if is_correct:
            st.success("正解です！")
        else:
            st.error("不正解です。")
            st.markdown(f"正解は: $f(x) = {sp.latex(correct_expr)}$")
        st.session_state.current_index += 1
        if st.session_state.current_index >= total_questions:
            st.session_state.completed = True
        else:
            st.session_state.start_time = time.time()
        st.experimental_rerun()

with col2:
    if st.button("スキップ", key=f"skip_{index}"):
        st.session_state.user_answers.append("（スキップ）")
        st.session_state.results.append(False)
        st.session_state.current_index += 1
        if st.session_state.current_index >= total_questions:
            st.session_state.completed = True
        else:
            st.session_state.start_time = time.time()
        st.experimental_rerun()

if st.session_state.completed:
    st.header("📝 結果")
    score = sum(st.session_state.results)
    st.success(f"スコア: {score} / {int(total_questions)}")

    for i, ((a, b, c), user_ans, result) in enumerate(zip(
        st.session_state.questions,
        st.session_state.user_answers,
        st.session_state.results
    )):
        expr = format_quadratic(a, b, c)
        correct_expr, _, _ = complete_the_square(a, b, c)
        st.markdown(f"### 第 {i+1} 問")
        st.latex(f"f(x) = {sp.latex(expr)}")
        st.write(f"あなたの答え: `{user_ans}`")
        st.write("判定:", "✅ 正解" if result else "❌ 不正解")
        if not result:
            st.latex(f"正しい平方完成: f(x) = {sp.latex(correct_expr)}")
        st.markdown("---")

    if st.button("もう一度やる"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
