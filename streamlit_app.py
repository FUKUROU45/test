import streamlit as st
import random
import math

# アプリのタイトル
st.title("平方完成練習アプリ")
st.write("二次関数の平方完成を練習しましょう！")

# セッション状態の初期化
if 'problem_generated' not in st.session_state:
    st.session_state.problem_generated = False
if 'show_steps' not in st.session_state:
    st.session_state.show_steps = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

def generate_problem():
    """新しい問題を生成する"""
    # 係数をランダムに選択（計算しやすい値に限定）
    a = random.choice([1, 2, 3, -1, -2])
    b = random.choice([-6, -4, -2, 2, 4, 6, 8])
    c = random.choice([-5, -3, -1, 1, 3, 5, 7])
    
    return a, b, c

def solve_square_completion(a, b, c):
    """平方完成の解答を計算する"""
    # ax² + bx + c = a(x + p)² + q の形に変形
    p = b / (2 * a)
    q = c - (b * b) / (4 * a)
    
    return p, q

def format_expression(a, b, c):
    """二次式を見やすい形で表示する"""
    expr = f"{a}x²"
    
    if b > 0:
        expr += f" + {b}x"
    elif b < 0:
        expr += f" - {abs(b)}x"
    
    if c > 0:
        expr += f" + {c}"
    elif c < 0:
        expr += f" - {abs(c)}"
    
    return expr

def format_answer(a, p, q):
    """平方完成の答えを見やすい形で表示する"""
    # a(x + p)² + q の形で表示
    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "-"
    else:
        a_str = f"{a}"
    
    if p > 0:
        p_str = f"x + {p}"
    elif p < 0:
        p_str = f"x - {abs(p)}"
    else:
        p_str = "x"
    
    if q > 0:
        q_str = f" + {q}"
    elif q < 0:
        q_str = f" - {abs(q)}"
    else:
        q_str = ""
    
    return f"{a_str}({p_str})²{q_str}"

# 新しい問題を生成するボタン
if st.button("新しい問題を生成"):
    st.session_state.a, st.session_state.b, st.session_state.c = generate_problem()
    st.session_state.problem_generated = True
    st.session_state.show_steps = False
    st.session_state.current_step = 0
    st.rerun()

# 問題が生成されている場合の表示
if st.session_state.problem_generated:
    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    
    st.subheader("問題")
    st.write(f"次の二次式を平方完成してください：")
    st.latex(f"y = {format_expression(a, b, c)}")
    
    # 解答の計算
    p, q = solve_square_completion(a, b, c)
    
    # ヒント表示ボタン
    if st.button("解き方を段階的に見る"):
        st.session_state.show_steps = True
        st.session_state.current_step = 1
        st.rerun()
    
    # 解答表示ボタン
    if st.button("答えを見る"):
        st.session_state.show_steps = True
        st.session_state.current_step = 5
        st.rerun()
    
    # 段階的な解答表示
    if st.session_state.show_steps:
        st.subheader("解答手順")
        
        if st.session_state.current_step >= 1:
            st.write("**ステップ1: 係数を確認**")
            st.write(f"a = {a}, b = {b}, c = {c}")
            
            if st.session_state.current_step == 1:
                if st.button("次のステップ"):
                    st.session_state.current_step = 2
                    st.rerun()
        
        if st.session_state.current_step >= 2:
            st.write("**ステップ2: x²の係数でくくり出す**")
            if a == 1:
                st.latex(f"y = x^2 + {b}x + {c}")
            else:
                inner_b = b // a if b % a == 0 else f"\\frac{{{b}}}{{{a}}}"
                inner_c = c
                st.latex(f"y = {a}(x^2 + {inner_b}x) + {inner_c}")
            
            if st.session_state.current_step == 2:
                if st.button("次のステップ", key="step2"):
                    st.session_state.current_step = 3
                    st.rerun()
        
        if st.session_state.current_step >= 3:
            st.write("**ステップ3: 平方完成の公式を適用**")
            st.write("x² + px の形を (x + p/2)² - (p/2)² に変形")
            p_half = b / (2 * a)
            p_half_squared = (b * b) / (4 * a * a)
            
            if a == 1:
                st.latex(f"y = (x + {p_half})^2 - {p_half_squared} + {c}")
            else:
                st.latex(f"y = {a}[(x + {p_half})^2 - {p_half_squared}] + {c}")
            
            if st.session_state.current_step == 3:
                if st.button("次のステップ", key="step3"):
                    st.session_state.current_step = 4
                    st.rerun()
        
        if st.session_state.current_step >= 4:
            st.write("**ステップ4: 定数項を整理**")
            if a == 1:
                final_q = c - (b * b) / (4 * a)
                st.latex(f"y = (x + {p})^2 + {final_q}")
            else:
                final_q = c - (b * b) / (4 * a)
                st.latex(f"y = {a}(x + {p})^2 + {final_q}")
            
            if st.session_state.current_step == 4:
                if st.button("最終答え", key="step4"):
                    st.session_state.current_step = 5
                    st.rerun()
        
        if st.session_state.current_step >= 5:
            st.write("**最終答え**")
            final_answer = format_answer(a, p, q)
            st.latex(f"y = {final_answer}")
            
            # 検証
            st.write("**検証**")
            st.write("元の式と展開した式が同じか確認してみましょう：")
            
            # 展開計算
            expanded_a = a
            expanded_b = 2 * a * p
            expanded_c = a * (p * p) + q
            
            st.write(f"展開: {a}(x + {p})² + {q}")
            st.write(f"= {expanded_a}x² + {expanded_b}x + {expanded_c}")
            st.write(f"元の式: {format_expression(a, b, c)}")
            
            if abs(expanded_b - b) < 0.0001 and abs(expanded_c - c) < 0.0001:
                st.success("✅ 正解です！")
            else:
                st.error("❌ 計算を確認してください")

# 使い方の説明
st.sidebar.header("使い方")
st.sidebar.write("1. 「新しい問題を生成」ボタンを押して問題を作成")
st.sidebar.write("2. 自分で解いてみる")
st.sidebar.write("3. 「解き方を段階的に見る」で手順を確認")
st.sidebar.write("4. 「答えを見る」で最終答えを確認")

st.sidebar.header("平方完成の公式")
st.sidebar.latex(r"ax^2 + bx + c = a(x + \frac{b}{2a})^2 + c - \frac{b^2}{4a}")

st.sidebar.header("ポイント")
st.sidebar.write("• x²の係数でくくり出す")
st.sidebar.write("• (x + p/2)² - (p/2)² の形を作る")
st.sidebar.write("• 定数項を正しく計算する")
st.sidebar.write("• 最後に検証する")