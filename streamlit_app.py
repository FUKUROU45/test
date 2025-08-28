import streamlit as st
import random
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import time

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
    h_int = int(round(h))
    k_int = int(round(k))
    return a, h_int, k_int

def format_expr(h, k, a):
    if abs(a - 1) < 1e-8:
        a_part = ""
    elif abs(a + 1) < 1e-8:
        a_part = "-"
    else:
        a_part = str(a)

    if h == 0:
        x_part = "x²"
    elif h > 0:
        x_part = f"(x - {h})²"
    else:
        x_part = f"(x + {-h})²"

    if k == 0:
        k_part = ""
    elif k > 0:
        k_part = f" + {k}"
    else:
        k_part = f" - {-k}"

    return f"{a_part}{x_part}{k_part}"

def generate_choices(a, b, c):
    a_c, h, k = complete_the_square(a, b, c)
    correct_str = format_expr(h, k, a_c)
    choices = [correct_str]

    attempts = 0
    while len(choices) < 4 and attempts < 30:
        delta_h = random.choice([-3, -2, -1, 1, 2, 3])
        delta_k = random.choice([-3, -2, -1, 1, 2, 3])
        wrong_h = h + delta_h
        wrong_k = k + delta_k
        wrong_str = format_expr(wrong_h, wrong_k, a_c)
        if wrong_str not in choices:
            choices.append(wrong_str)
        attempts += 1

    random.shuffle(choices)
    return choices, correct_str

def plot_graph(a, b, c):
    xx = np.linspace(-10, 10, 400)
    yy = a * xx**2 + b * xx + c
    fig, ax = plt.subplots()
    ax.plot(xx, yy, label=f'f(x) = {a}x² + {b}x + {c}', color='b')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_xlabel("x軸")
    ax.set_ylabel("f(x)軸")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    plt.close()

# --------------------
# Streamlit UI開始
# --------------------

st.set_page_config(page_title="平方完成 四択トレーニング", layout="centered")
st.title("📘 平方完成トレーニング（四択・整数）")

# 初期設定画面
if "initialized" not in st.session_state:
    with st.sidebar:
        st.header("▶ 設定")
        st.session_state.difficulty = st.radio("難易度を選択", ["初級", "中級", "上級"])
        st.session_state.total_questions = st.number_input("問題数", min_value=1, max_value=20, value=5)
        st.session_state.show_graph = st.radio("グラフを表示しますか？", ["表示する", "表示しない"]) == "表示する"
        st.session_state.time_limit = st.selectbox("制限時間（秒）", [0, 15, 30, 60], index=2)
        if st.button("問題を開始"):
            st.session_state.questions = [generate_question(st.session_state.difficulty) for _ in range(st.session_state.total_questions)]
            st.session_state.current_index = 0
            st.session_state.user_answers = []
            st.session_state.results = []
            st.session_state.completed = False
            st.session_state.start_time = time.time()
            st.session_state.initialized = True
            st.experimental_rerun()
    st.stop()

# 終了画面
if st.session_state.completed:
    st.header("📝 結果")
    score = sum(st.session_state.results)
    st.success(f"あなたのスコア: {score} / {st.session_state.total_questions}")

    for i, ((a, b, c), user_ans, result) in enumerate(zip(
        st.session_state.questions,
        st.session_state.user_answers,
        st.session_state.results
    )):
        expr = format_quadratic(a, b, c)
        a_c, h, k = complete_the_square(a, b, c)
        correct_str = format_expr(h, k, a_c)

        st.markdown(f"### 第 {i+1} 問")
        st.latex(f"f(x) = {sp.latex(expr)}")
        st.write(f"あなたの答え: `{user_ans}`")
        st.write("判定:", "✅ 正解" if result else "❌ 不正解")
        if not result:
            st.write(f"正しい平方完成: `{correct_str}`")
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

st.markdown(f"### 問題 {index + 1} / {st.session_state.total_questions}")
st.latex(f"f(x) = {sp.latex(expr)}")

if st.session_state.show_graph:
    plot_graph(a, b, c)

# 制限時間処理
time_limit = st.session_state.time_limit
if time_limit > 0:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(time_limit - elapsed)
    st.info(f"⏱ 残り時間: {remaining} 秒")
    if remaining <= 0:
        st.warning("時間切れです！この問題はスキップされました。")
        st.session_state.user_answers.append("（時間切れ）")
        st.session_state.results.append(False)
        st.session_state.current_index += 1
        if st.session_state.current_index >= st.session_state.total_questions:
            st.session_state.completed = True
        else:
            st.session_state.start_time = time.time()
        st.experimental_rerun()

# 四択の選択肢をラジオボタンで表示
user_choice = st.radio("平方完成の正しい式を選んでください", choices, key=f"choice_{index}")

def check_answer():
    is_correct = (st.session_state[f"choice_{index}"] == correct)
    st.session_state.user_answers.append(st.session_state[f"choice_{index}"])
    st.session_state.results.append(is_correct)
    st.session_state.current_index += 1
    if st.session_state.current_index >= st.session_state.total_questions:
        st.session_state.completed = True
    else:
        st.session_state.start_time = time.time()
    st.experimental_rerun()

def skip_question():
    st.session_state.user_answers.append("（スキップ）")
    st.session_state.results.append(False)
    st.session_state.current_index += 1
    if st.session_state.current_index >= st.session_state.total_questions:
        st.session_state.completed = True
    else:
        st.session_state.start_time = time.time()
    st.experimental_rerun()

col1, col2 = st.columns(2)
with col1:
    st.button("判定", on_click=check_answer)
with col2:
    st.button("スキップ", on_click=skip_question)
