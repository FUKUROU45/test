import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# ページ設定
st.set_page_config(
    page_title="平方完成練習アプリ",
    page_icon="📐",
    layout="wide"
)

# アプリのタイトル
st.title("📐 平方完成練習アプリ")
st.markdown("**二次関数の平方完成をマスターしよう！**")

# セッション状態の初期化
if 'problem_generated' not in st.session_state:
    st.session_state.problem_generated = False
if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "初級"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

def generate_problem(difficulty):
    """難易度に応じて問題を生成"""
    if difficulty == "初級":
        a = random.choice([1, 2, -1, -2])
        b = random.choice([-6, -4, -2, 2, 4, 6])
        c = random.choice([-3, -1, 0, 1, 3, 5])
    elif difficulty == "中級":
        a = random.choice([1, 2, 3, -1, -2, -3])
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8])
        c = random.choice([-5, -3, -1, 1, 3, 5, 7])
    else:  # 上級
        a = random.choice([1, 2, 3, 4, -1, -2, -3])
        b = random.choice([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
        c = random.choice([-7, -5, -3, -1, 1, 3, 5, 7, 9])
    
    return a, b, c

def solve_square_completion(a, b, c):
    """平方完成の解を計算"""
    # ax² + bx + c = a(x + p)² + q の形
    p = b / (2 * a)
    q = c - (b * b) / (4 * a)
    return p, q

def format_quadratic(a, b, c):
    """二次式を美しく表示"""
    terms = []
    
    # x²の項
    if a == 1:
        terms.append("x²")
    elif a == -1:
        terms.append("-x²")
    else:
        terms.append(f"{a}x²")
    
    # xの項
    if b > 0:
        terms.append(f"+ {b}x" if len(terms) > 0 else f"{b}x")
    elif b < 0:
        terms.append(f"- {abs(b)}x")
    
    # 定数項
    if c > 0:
        terms.append(f"+ {c}" if len(terms) > 0 else f"{c}")
    elif c < 0:
        terms.append(f"- {abs(c)}")
    
    return " ".join(terms)

def format_completed_square(a, p, q):
    """平方完成の形を美しく表示"""
    # a(x + p)² + q の形
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

def plot_quadratic(a, b, c, p, q):
    """二次関数のグラフを描画"""
    x = np.linspace(-10, 10, 1000)
    y = a * x**2 + b * x + c
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'b-', linewidth=2, label=f'y = {format_quadratic(a, b, c)}')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    # 頂点をマーク
    vertex_x = -p
    vertex_y = q
    ax.plot(vertex_x, vertex_y, 'ro', markersize=8, label=f'頂点 ({vertex_x:.1f}, {vertex_y:.1f})')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'二次関数のグラフ')
    ax.legend()
    ax.set_xlim(-8, 8)
    ax.set_ylim(-10, 10)
    
    return fig

# サイドバーの設定
st.sidebar.header("⚙️ 設定")
difficulty = st.sidebar.selectbox("難易度を選択", ["初級", "中級", "上級"])
st.session_state.difficulty = difficulty

st.sidebar.header("📊 成績")
if st.session_state.attempts > 0:
    accuracy = (st.session_state.score / st.session_state.attempts) * 100
    st.sidebar.metric("正答率", f"{accuracy:.1f}%")
    st.sidebar.metric("正解数", st.session_state.score)
    st.sidebar.metric("挑戦回数", st.session_state.attempts)

st.sidebar.header("📚 平方完成の公式")
st.sidebar.latex(r"ax^2 + bx + c = a\left(x + \frac{b}{2a}\right)^2 + c - \frac{b^2}{4a}")

st.sidebar.header("💡 解き方のコツ")
st.sidebar.markdown("""
1. **x²の係数でくくる**
2. **xの係数の半分を計算**
3. **完全平方式を作る**
4. **定数項を調整**
5. **答えを確認**
""")

# メインコンテンツ
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 問題")
    
    # 問題生成ボタン
    if st.button("🎲 新しい問題を生成", type="primary"):
        st.session_state.a, st.session_state.b, st.session_state.c = generate_problem(difficulty)
        st.session_state.problem_generated = True
        st.session_state.show_solution = False
        st.rerun()
    
    # 問題表示
    if st.session_state.problem_generated:
        a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
        
        st.subheader("次の二次式を平方完成してください：")
        st.latex(f"y = {format_quadratic(a, b, c)}")
        
        # 解答の計算
        p, q = solve_square_completion(a, b, c)
        
        # 答え入力フォーム
        st.subheader("📝 あなたの答え")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if a == 1:
                user_p = st.number_input("pの値 (x + p)²", value=0.0, step=0.5, key="user_p")
            else:
                user_p = st.number_input(f"pの値 {a}(x + p)²", value=0.0, step=0.5, key="user_p")
        
        with col_b:
            user_q = st.number_input("qの値 (定数項)", value=0.0, step=0.5, key="user_q")
        
        # 答えをチェック
        if st.button("✅ 答えをチェック"):
            st.session_state.attempts += 1
            if abs(user_p - p) < 0.01 and abs(user_q - q) < 0.01:
                st.success("🎉 正解です！素晴らしい！")
                st.session_state.score += 1
                st.balloons()
            else:
                st.error("❌ 残念！もう一度チャレンジしてみてください。")
        
        # 解答表示
        if st.button("💡 解答を見る"):
            st.session_state.show_solution = True
            st.rerun()
        
        if st.session_state.show_solution:
            st.subheader("📋 詳細な解答")
            
            with st.expander("ステップ1: 係数の確認", expanded=True):
                st.write(f"a = {a}, b = {b}, c = {c}")
            
            with st.expander("ステップ2: 公式の適用", expanded=True):
                st.write(f"p = b/(2a) = {b}/(2×{a}) = {p}")
                st.write(f"q = c - b²/(4a) = {c} - {b}²/(4×{a}) = {q}")
            
            with st.expander("ステップ3: 最終答え", expanded=True):
                answer = format_completed_square(a, p, q)
                st.latex(f"y = {answer}")
                st.success(f"答え: y = {answer}")
            
            with st.expander("ステップ4: 検証", expanded=True):
                # 展開して元の式と比較
                expanded_a = a
                expanded_b = 2 * a * p
                expanded_c = a * (p * p) + q
                
                st.write("展開による検証:")
                st.write(f"展開: {format_quadratic(expanded_a, expanded_b, expanded_c)}")
                st.write(f"元の式: {format_quadratic(a, b, c)}")
                
                if abs(expanded_b - b) < 0.0001 and abs(expanded_c - c) < 0.0001:
                    st.success("✅ 検証完了！正しく平方完成されています。")

with col2:
    st.header("📈 グラフ")
    
    if st.session_state.problem_generated:
        a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
        p, q = solve_square_completion(a, b, c)
        
        fig = plot_quadratic(a, b, c, p, q)
        st.pyplot(fig)
        
        st.subheader("🎯 頂点の情報")
        vertex_x = -p
        vertex_y = q
        st.write(f"頂点: ({vertex_x:.1f}, {vertex_y:.1f})")
        
        if a > 0:
            st.write("📈 上に凸（最小値を持つ）")
        else:
            st.write("📉 下に凸（最大値を持つ）")

# フッター
st.markdown("---")
st.markdown("**💪 頑張って練習しましょう！平方完成は二次関数の重要な技術です。**")