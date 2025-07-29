import streamlit as st
import random
import math
from fractions import Fraction

def generate_problem(level):
    """レベルに応じて問題を生成"""
    if level == "初級":
        # x^2 + bx 形式（b は偶数）
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8])
        a = 1
        c = 0
    elif level == "中級":
        # x^2 + bx + c 形式
        a = 1
        b = random.choice([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
        c = random.randint(-5, 5)
    else:  # 上級
        # ax^2 + bx + c 形式（a ≠ 1）
        a = random.choice([-3, -2, 2, 3])
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8])
        c = random.randint(-10, 10)
    
    return a, b, c

def format_quadratic(a, b, c):
    """二次式を文字列で表示"""
    terms = []
    
    # x^2の項
    if a == 1:
        terms.append("x²")
    elif a == -1:
        terms.append("-x²")
    else:
        terms.append(f"{a}x²")
    
    # xの項
    if b > 0:
        if b == 1:
            terms.append("+ x")
        else:
            terms.append(f"+ {b}x")
    elif b < 0:
        if b == -1:
            terms.append("- x")
        else:
            terms.append(f"- {abs(b)}x")
    
    # 定数項
    if c > 0:
        terms.append(f"+ {c}")
    elif c < 0:
        terms.append(f"- {abs(c)}")
    
    return " ".join(terms) if terms else "0"

def calculate_completion(a, b, c):
    """平方完成の答えを計算"""
    if a == 1:
        # x^2 + bx + c = (x + b/2)^2 + (c - b^2/4)
        h = -b / 2
        k = c - (b**2) / 4
        return 1, h, k
    else:
        # ax^2 + bx + c = a(x + b/(2a))^2 + (c - b^2/(4a))
        h = -b / (2 * a)
        k = c - (b**2) / (4 * a)
        return a, h, k

def format_completion_answer(a, h, k):
    """平方完成の答えを文字列で表示"""
    # h を分数で表示
    h_frac = Fraction(h).limit_denominator()
    k_frac = Fraction(k).limit_denominator()
    
    # a の係数
    a_str = "" if a == 1 else f"{a}"
    
    # (x + h) の部分
    if h_frac == 0:
        x_part = "x²"
    elif h_frac > 0:
        if h_frac.denominator == 1:
            x_part = f"(x + {h_frac.numerator})²"
        else:
            x_part = f"(x + {h_frac})²"
    else:
        if h_frac.denominator == 1:
            x_part = f"(x - {abs(h_frac.numerator)})²"
        else:
            x_part = f"(x - {abs(h_frac)})²"
    
    # k の部分
    if k_frac == 0:
        k_part = ""
    elif k_frac > 0:
        if k_frac.denominator == 1:
            k_part = f" + {k_frac.numerator}"
        else:
            k_part = f" + {k_frac}"
    else:
        if k_frac.denominator == 1:
            k_part = f" - {abs(k_frac.numerator)}"
        else:
            k_part = f" - {abs(k_frac)}"
    
    return f"{a_str}{x_part}{k_part}"

def explain_solution(a, b, c):
    """解法の解説を生成"""
    explanation = f"**解法の手順：**\n\n"
    explanation += f"元の式：{format_quadratic(a, b, c)}\n\n"
    
    if a != 1:
        explanation += f"**ステップ1：** 最高次の係数 {a} でくくり出す\n"
        explanation += f"{a}(x² + {Fraction(b, a)}x) + {c}\n\n"
        
        explanation += f"**ステップ2：** x の係数の半分を求める\n"
        explanation += f"x の係数：{Fraction(b, a)}\n"
        explanation += f"その半分：{Fraction(b, a)} ÷ 2 = {Fraction(b, 2*a)}\n\n"
        
        explanation += f"**ステップ3：** 平方完成する\n"
        explanation += f"{a}(x² + {Fraction(b, a)}x + ({Fraction(b, 2*a)})² - ({Fraction(b, 2*a)})²) + {c}\n"
        explanation += f"= {a}((x + {Fraction(b, 2*a)})² - {Fraction(b**2, 4*a**2)}) + {c}\n"
        explanation += f"= {a}(x + {Fraction(b, 2*a)})² - {Fraction(b**2, 4*a)} + {c}\n"
        explanation += f"= {a}(x + {Fraction(b, 2*a)})² + {Fraction(4*a*c - b**2, 4*a)}\n\n"
    else:
        explanation += f"**ステップ1：** x の係数の半分を求める\n"
        explanation += f"x の係数：{b}\n"
        explanation += f"その半分：{b} ÷ 2 = {Fraction(b, 2)}\n\n"
        
        explanation += f"**ステップ2：** 平方完成する\n"
        explanation += f"x² + {b}x + {c}\n"
        explanation += f"= x² + {b}x + ({Fraction(b, 2)})² - ({Fraction(b, 2)})² + {c}\n"
        explanation += f"= (x + {Fraction(b, 2)})² - {Fraction(b**2, 4)} + {c}\n"
        explanation += f"= (x + {Fraction(b, 2)})² + {Fraction(4*c - b**2, 4)}\n\n"
    
    a_ans, h_ans, k_ans = calculate_completion(a, b, c)
    explanation += f"**答え：** {format_completion_answer(a_ans, h_ans, k_ans)}"
    
    return explanation

# Streamlit アプリのメイン部分
st.title("🧮 平方完成 練習アプリ")
st.write("二次式を平方完成する練習をしましょう！")

# セッション状態の初期化
if 'problem_generated' not in st.session_state:
    st.session_state.problem_generated = False
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'total_answers' not in st.session_state:
    st.session_state.total_answers = 0
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

# レベル選択
level = st.selectbox(
    "難易度を選択してください：",
    ["初級", "中級", "上級"],
    help="初級：x² + bx、中級：x² + bx + c、上級：ax² + bx + c"
)

# 問題生成ボタン
if st.button("新しい問題を生成"):
    st.session_state.a, st.session_state.b, st.session_state.c = generate_problem(level)
    st.session_state.problem_generated = True
    st.session_state.show_explanation = False

# 問題表示
if st.session_state.problem_generated:
    st.subheader("問題")
    problem_text = format_quadratic(st.session_state.a, st.session_state.b, st.session_state.c)
    st.write(f"次の二次式を平方完成してください：")
    st.markdown(f"### {problem_text}")
    
    # 正解を計算
    correct_a, correct_h, correct_k = calculate_completion(
        st.session_state.a, st.session_state.b, st.session_state.c
    )
    correct_answer = format_completion_answer(correct_a, correct_h, correct_k)
    
    # ユーザーの回答入力
    user_answer = st.text_input(
        "答えを入力してください（例：2(x - 3)² + 1）：",
        help="分数は「1/2」のように入力してください"
    )
    
    # 答え合わせボタン
    if st.button("答え合わせ"):
        if user_answer.strip():
            st.session_state.total_answers += 1
            
            # 簡単な答え合わせ（完全ではないが、基本的なケースに対応）
            user_clean = user_answer.replace(" ", "").replace("²", "^2")
            correct_clean = correct_answer.replace(" ", "").replace("²", "^2")
            
            if user_clean.lower() == correct_clean.lower():
                st.success("🎉 正解です！")
                st.session_state.correct_answers += 1
                st.balloons()
            else:
                st.error("❌ 不正解です。解説を確認してください。")
                st.session_state.show_explanation = True
            
            st.write(f"**正解：** {correct_answer}")
        else:
            st.warning("答えを入力してください。")
    
    # 解説表示
    if st.session_state.show_explanation or st.button("解説を見る"):
        with st.expander("📖 詳しい解説", expanded=True):
            explanation = explain_solution(st.session_state.a, st.session_state.b, st.session_state.c)
            st.markdown(explanation)

# 統計表示
if st.session_state.total_answers > 0:
    accuracy = (st.session_state.correct_answers / st.session_state.total_answers) * 100
    st.sidebar.write("## 📊 成績")
    st.sidebar.write(f"正解数: {st.session_state.correct_answers}")
    st.sidebar.write(f"総問題数: {st.session_state.total_answers}")
    st.sidebar.write(f"正答率: {accuracy:.1f}%")
    
    if st.sidebar.button("成績をリセット"):
        st.session_state.correct_answers = 0
        st.session_state.total_answers = 0

# 使い方の説明
with st.expander("📋 使い方とレベル説明"):
    st.markdown("""
    **使い方：**
    1. 難易度を選択してください
    2. 「新しい問題を生成」ボタンを押してください
    3. 表示された問題を平方完成してください
    4. 答えを入力して「答え合わせ」ボタンを押してください
    
    **レベル説明：**
    - **初級**：x² + bx の形（定数項なし、最高次係数1）
    - **中級**：x² + bx + c の形（最高次係数1）
    - **上級**：ax² + bx + c の形（最高次係数が1以外）
    
    **入力例：**
    - (x + 2)² + 3
    - 2(x - 1/2)² - 4
    - -3(x + 1)² + 5
    """)