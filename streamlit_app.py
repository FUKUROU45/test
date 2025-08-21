import streamlit as st
import random
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import time

x = sp.symbols('x')

# --------------------
# 問題生成・整形関数
# --------------------
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
    expr = a * (x - h)**2 + k
    return expr, h, k, a

def format_expr(h, k, a):
    def fmt(num):
        return f"{num:.3f}"

    # a部分
    if abs(a - 1) < 1e-8:
        a_part = ""
    elif abs(a + 1) < 1e-8:
        a_part = "-"
    else:
        a_part = fmt(a)

    # h部分
    if abs(h) < 1e-8:
        x_part = "x^{2}"
    elif h > 0:
        x_part = f"(x - {fmt(h)})^2"
    else:
        x_part = f"(x + {fmt(-h)})^2"

    # k部分
    if abs(k) < 1e-8:
        k_part = ""
    elif k > 0:
        k_part = f" + {fmt(k)}"
    else:
        k_part = f" - {fmt(-k)}"

    return f"{a_part}{x_part}{k_part}"

def generate_choices(a, b, c):
    correct_expr, h, k, a = complete_the_square(a, b, c)
    correct_str = format_expr(h, k, a)
    choices = [correct_str]

    # 間違い選択肢を作る
    for _ in range(3):
        delta_h = random.choice([-1, 1]) * random.uniform(0.5, 2)
        delta_k = random.choice([-1, 1]) * random.uniform(0.5, 3)
        wrong_h = h + delta_h
        wrong_k = k + delta_k
        wrong_str = format_expr(wrong_h, wrong_k, a)
        if wrong_str not in choices:
            choices.append(wrong_str)

    random.shuffle(choices)
    return choices, correct_str

def plot_graph(a, b, c):
    xx = np.linspace(-10, 10, 400)
    yy = a * xx**2 + b * xx + c
    fig, ax = plt.subplots()
    ax.plot(xx, yy, label=f'f(x) = {a}x² + {b}x + {c}')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    plt.close()

# --------------------
# Streamlit アプリ開始
# --------------------
st.set_page_config("平方完成 四択トレーニング", layout="centered")
st.title("📘 平方完成トレーニング（四択）")

# 設定
with st.sidebar:
    st.header("▶ 設定")
    difficulty = st.radio("難易度", ["初級", "中級", "上級"])
    total_questions = st.number_input("問題数", 1, 20, 5)
    show_graph = st.radio("グラフを表示しますか？", ["表示する", "表示しない"]) == "表示する"

# 初期化
if "questions" not in st.session_state:
    st.session_state.questions = [generate_question(difficulty) for _ in range(total_questions)]
    st.session_state.current_index = 0
    st.session_state.user_answers = []
    st.session_state.results = []
    st.session_state.completed = False

# 終了チェック
if st.session_state.completed:
    st.header("📝 結果")
    score = sum(st.session_state.results)
    st.success(f"あなたのスコア: {score} / {int(total_questions)}")

    for i, ((a, b, c), user_ans, result) in enumerate(zip(
        st.session_state.questions,
        st.session_state.user_answers,
        st.session_state.results
    )):
        expr = format_quadratic(a, b, c)
        correct_expr, h, k, a = complete_the_square(a, b, c)
        correct_str = format_expr(h, k, a)

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
    st.stop()

# 現在の問題
index = st.session_state.current_index
a, b, c = st.session_state.questions[index]
expr = format_quadratic(a, b, c)
choices, correct = generate_choices(a, b, c)

st.markdown(f"### 問題 {index + 1} / {int(total_questions)}")
st.latex(f"f(x) = {sp.latex(expr)}")

if show_graph:
    plot_graph(a, b, c)

user_choice = st.radio("平方完成の正しい式を選んでください", choices, key=index)

col1, col2 = st.columns(2)
with col1:
    if st.button("判定", key=f"check_{index}"):
        is_correct = (user_choice == correct)
        st.session_state.user_answers.append(user_choice)
        st.session_state.results.append(is_correct)
        st.session_state.current_index += 1

        if st.session_state.current_index >= total_questions:
            st.session_state.completed = True

        st.experimental_rerun()

with col2:
    if st.button("スキップ", key=f"skip_{index}"):
        st.session_state.user_answers.append("（スキップ）")
        st.session_state.results.append(False)
        st.session_state.current_index += 1

        if st.session_state.current_index >= total_questions:
            st.session_state.completed = True

        st.experimental_rerun()
