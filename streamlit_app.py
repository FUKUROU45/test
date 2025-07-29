import streamlit as st
import random
import time
from fractions import Fraction

def generate_problem(level):
    if level == "初級":
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8])
        return 1, b, 0
    elif level == "中級":
        b = random.choice([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
        c = random.randint(-5, 5)
        return 1, b, c
    else:
        a = random.choice([-3, -2, 2, 3])
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8])
        c = random.randint(-10, 10)
        return a, b, c

def format_quadratic(a, b, c):
    terms = []
    if a == 1:
        terms.append("x^2")
    elif a == -1:
        terms.append("-x^2")
    else:
        terms.append(f"{a}x^2")
    if b > 0:
        terms.append(f"+ {b}x" if b != 1 else "+ x")
    elif b < 0:
        terms.append(f"- {abs(b)}x" if abs(b) != 1 else "- x")
    if c > 0:
        terms.append(f"+ {c}")
    elif c < 0:
        terms.append(f"- {abs(c)}")
    return " ".join(terms) if terms else "0"

def calculate_completion(a, b, c):
    if a == 1:
        h = -b / 2
        k = c - (b**2) / 4
    else:
        h = -b / (2 * a)
        k = c - (b**2) / (4 * a)
    return a, h, k

def format_completion_answer(a, h, k):
    h_frac = Fraction(h).limit_denominator()
    k_frac = Fraction(k).limit_denominator()
    a_str = "" if a == 1 else str(a)
    if h_frac == 0:
        x_part = "x^2"
    elif h_frac > 0:
        x_part = f"(x + {h_frac})^2"
    else:
        x_part = f"(x - {abs(h_frac)})^2"
    if k_frac == 0:
        k_part = ""
    elif k_frac > 0:
        k_part = f" + {k_frac}"
    else:
        k_part = f" - {abs(k_frac)}"
    return f"{a_str}{x_part}{k_part}"

def normalize_answer(answer):
    if not answer:
        return ""
    normal = answer.replace(" ", "").replace("²", "^2").replace("**2", "^2")
    normal = normal.replace("X", "x").replace("（", "(").replace("）", ")")
    import re
    for dec in re.findall(r'\d*\.\d+', normal):
        try:
            frac = Fraction(float(dec)).limit_denominator()
            normal = normal.replace(dec, f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator))
        except:
            pass
    return normal.lower()

def parse_quadratic_completion(expr):
    expr = normalize_answer(expr)
    import re
    # 簡易版: (x±h)^2±k 形式のみ対応
    pattern = r'(\d*(?:/\d+)?|\-?\d*(?:/\d+)?)*(?:\()x([+-])(\d+(?:/\d+)?)\)\^2([+-]\d+(?:/\d+)?)?'
    m = re.search(pattern, expr)
    if not m:
        return None
    a_str, sign, h_str, k_str = m.groups()
    a = float(Fraction(a_str)) if a_str not in (None, "", "-") else ( -1.0 if expr.startswith('-') else 1.0 )
    h = float(Fraction(h_str))
    if sign == '+':
        h = -h
    k = float(Fraction(k_str)) if k_str else 0.0
    return a, h, k

def is_equivalent_completion(user, a, h, k):
    parsed = parse_quadratic_completion(user)
    if not parsed:
        return False
    ua, uh, uk = parsed
    return abs(ua - a) < 1e-8 and abs(uh - h) < 1e-8 and abs(uk - k) < 1e-8

def explain_solution_simple(a, b, c):
    a_ans, h_ans, k_ans = calculate_completion(a, b, c)
    ans = format_completion_answer(a_ans, h_ans, k_ans)
    return f"### 答え: {ans}\n（詳細説明は割愛）"

# ==== Streamlit UI ====

st.title("平方完成 チャレンジ")

# 初期化
for key in ["quiz_started", "current_problem", "correct_answers", "problems", "wrong_problems", "quiz_finished", "time_up", "start_time"]:
    if key not in st.session_state:
        default = 0 if "problem" in key else False
        st.session_state[key] = default
if "level" not in st.session_state:
    st.session_state.level = "中級"
if "time_limit" not in st.session_state:
    st.session_state.time_limit = 120
if "problem_count" not in st.session_state:
    st.session_state.problem_count = 5

if not st.session_state.quiz_started:
    st.header("クイズ設定")
    level = st.selectbox("難易度", ["初級","中級","上級"], index=["初級","中級","上級"].index(st.session_state.level))
    count = st.selectbox("問題数", [5,10,15], index=1)
    time_limit = st.selectbox("制限時間", [60,120,180], index=1, format_func=lambda x: f"{x//60}分")
    if st.button("スタート"):
        st.session_state.level = level
        st.session_state.problem_count = count
        st.session_state.time_limit = time_limit
        st.session_state.problems = [generate_problem(level) for _ in range(count)]
        st.session_state.quiz_started = True
        st.session_state.start_time = time.time()
        st.session_state.correct_answers = 0
        st.session_state.current_problem = 0
        st.session_state.wrong_problems = []
        st.rerun()

elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    elapsed = time.time() - st.session_state.start_time
    if elapsed >= st.session_state.time_limit:
        st.session_state.quiz_finished = True
        st.session_state.time_up = True
        st.rerun()

    a,b,c = st.session_state.problems[st.session_state.current_problem]
    st.header(f"問題 {st.session_state.current_problem+1}")
    st.write(format_quadratic(a,b,c))
    correct_a, correct_h, correct_k = calculate_completion(a,b,c)
    correct_ans = format_completion_answer(correct_a, correct_h, correct_k)

    user = st.text_input("平方完成の答えを入力してください", key=f"ans_{st.session_state.current_problem}")
    answered_key = f"answered_{st.session_state.current_problem}"

    if answered_key not in st.session_state:
        if st.button("回答を送信", key=f"btn_{st.session_state.current_problem}"):
            st.session_state[answered_key] = True
            if is_equivalent_completion(user, correct_a, correct_h, correct_k):
                st.session_state.correct_answers += 1
                st.session_state[f"result_{st.session_state.current_problem}"] = "correct"
                st.success("正解！")
            else:
                st.session_state[f"result_{st.session_state.current_problem}"] = "incorrect"
                st.error(f"不正解　正解: {correct_ans}")
    else:
        # ✔️ ここが構文的に正しい else ブロック
        result_key = f"result_{st.session_state.current_problem}"
        if result_key in st.session_state:
            if st.session_state[result_key] == "correct":
                st.success("🎉 正解！")
            else:
                st.error(f"❌ 不正解　正解: {correct_ans}")
        if st.button("解説を見る"):
            st.write(explain_solution_simple(a,b,c))
        if st.button("次へ"):
            st.session_state.current_problem += 1
            if st.session_state.current_problem >= st.session_state.problem_count:
                st.session_state.quiz_finished = True
            st.rerun()

elif st.session_state.quiz_finished:
    st.header("クイズ終了")
    total = st.session_state.correct_answers
    cnt = st.session_state.problem_count
    rate = total / cnt * 100
    st.write(f"正答率: {rate:.1f}% ({total}/{cnt})")
    if st.session_state.time_up:
        st.write("⏰ 時間切れです")
    if st.session_state.wrong_problems:
        st.write("間違えた問題：")
        for idx,(a,b,c,user_ans) in enumerate(st.session_state.wrong_problems):
            st.write(f"{idx+1}: {format_quadratic(a,b,c)} → あなたの答え: {user_ans}")

with st.sidebar:
    st.header("平方完成のコツ")
    st.write("✅ xの係数の半分を求めて、それを2乗して足し引きすることで平方完成を作ります。引く定数項も忘れずに。")
