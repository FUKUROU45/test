import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import font_manager

# 日本語フォント設定
plt.rcParams['font.family'] = 'DejaVu Sans'

st.set_page_config(page_title="関数問題生成アプリ", layout="wide")

st.title("📊 関数問題生成アプリ")
st.markdown("一次関数と二次関数の問題をランダムに生成し、グラフを表示します")

# サイドバーで設定
st.sidebar.header("⚙️ 設定")
function_type = st.sidebar.selectbox(
    "関数の種類",
    ["一次関数", "二次関数", "両方"]
)

difficulty = st.sidebar.selectbox(
    "難易度",
    ["初級", "中級", "上級"]
)

# 問題数
num_problems = st.sidebar.slider("問題数", 1, 10, 5)

# 問題生成ボタン
if st.sidebar.button("🎲 新しい問題を生成", type="primary"):
    st.session_state.problems_generated = True
    st.session_state.current_problem_index = 0
    st.session_state.problems = []
    st.session_state.user_answers = {}
    st.session_state.show_answers = False
    
    # 問題生成
    for i in range(num_problems):
        if function_type == "両方":
            prob_type = random.choice(["一次関数", "二次関数"])
        else:
            prob_type = function_type
            
        problem = generate_problem(prob_type, difficulty)
        st.session_state.problems.append(problem)

def generate_problem(func_type, difficulty):
    """問題を生成する関数"""
    if func_type == "一次関数":
        return generate_linear_problem(difficulty)
    else:
        return generate_quadratic_problem(difficulty)

def generate_linear_problem(difficulty):
    """一次関数の問題を生成"""
    if difficulty == "初級":
        a = random.choice([1, 2, 3, -1, -2, -3])
        b = random.randint(-5, 5)
    elif difficulty == "中級":
        a = random.choice([0.5, 1.5, 2.5, -0.5, -1.5, -2.5])
        b = random.randint(-10, 10)
    else:  # 上級
        a = round(random.uniform(-3, 3), 1)
        if a == 0:
            a = 1
        b = round(random.uniform(-15, 15), 1)
    
    # 問題の種類をランダムに選択
    problem_types = [
        "傾きと切片を求める",
        "特定の点での値を求める",
        "x切片を求める",
        "y切片を求める",
        "グラフの特徴を説明"
    ]
    
    problem_type = random.choice(problem_types)
    
    return {
        "type": "一次関数",
        "a": a,
        "b": b,
        "problem_type": problem_type,
        "equation": f"y = {a}x + {b}" if b >= 0 else f"y = {a}x - {abs(b)}"
    }

def generate_quadratic_problem(difficulty):
    """二次関数の問題を生成"""
    if difficulty == "初級":
        a = random.choice([1, 2, -1, -2])
        b = random.randint(-4, 4)
        c = random.randint(-5, 5)
    elif difficulty == "中級":
        a = random.choice([0.5, 1.5, 2.5, -0.5, -1.5, -2.5])
        b = random.randint(-8, 8)
        c = random.randint(-10, 10)
    else:  # 上級
        a = round(random.uniform(-3, 3), 1)
        if a == 0:
            a = 1
        b = round(random.uniform(-10, 10), 1)
        c = round(random.uniform(-15, 15), 1)
    
    problem_types = [
        "頂点を求める",
        "軸の方程式を求める",
        "x切片を求める",
        "y切片を求める",
        "最大値または最小値を求める"
    ]
    
    problem_type = random.choice(problem_types)
    
    return {
        "type": "二次関数",
        "a": a,
        "b": b,
        "c": c,
        "problem_type": problem_type,
        "equation": format_quadratic_equation(a, b, c)
    }

def format_quadratic_equation(a, b, c):
    """二次関数の式を整形"""
    equation = f"y = {a}x²"
    
    if b > 0:
        equation += f" + {b}x"
    elif b < 0:
        equation += f" - {abs(b)}x"
    
    if c > 0:
        equation += f" + {c}"
    elif c < 0:
        equation += f" - {abs(c)}"
    
    return equation

def plot_function(problem):
    """関数のグラフを描画"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if problem["type"] == "一次関数":
        x = np.linspace(-10, 10, 100)
        y = problem["a"] * x + problem["b"]
        ax.plot(x, y, 'b-', linewidth=2, label=problem["equation"])
        ax.set_title(f"一次関数: {problem['equation']}")
        
    else:  # 二次関数
        x = np.linspace(-10, 10, 100)
        y = problem["a"] * x**2 + problem["b"] * x + problem["c"]
        ax.plot(x, y, 'r-', linewidth=2, label=problem["equation"])
        ax.set_title(f"二次関数: {problem['equation']}")
        
        # 頂点を表示
        vertex_x = -problem["b"] / (2 * problem["a"])
        vertex_y = problem["a"] * vertex_x**2 + problem["b"] * vertex_x + problem["c"]
        ax.plot(vertex_x, vertex_y, 'ro', markersize=8, label=f"頂点({vertex_x:.1f}, {vertex_y:.1f})")
    
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-20, 20)
    
    return fig

def get_correct_answer(problem):
    """正解を計算"""
    if problem["type"] == "一次関数":
        if problem["problem_type"] == "傾きと切片を求める":
            return f"傾き: {problem['a']}, y切片: {problem['b']}"
        elif problem["problem_type"] == "特定の点での値を求める":
            x_val = 2  # 例としてx=2での値
            y_val = problem["a"] * x_val + problem["b"]
            return f"x = {x_val}のとき、y = {y_val}"
        elif problem["problem_type"] == "x切片を求める":
            if problem["a"] != 0:
                x_intercept = -problem["b"] / problem["a"]
                return f"x切片: {x_intercept:.2f}"
            else:
                return "x切片は存在しません"
        elif problem["problem_type"] == "y切片を求める":
            return f"y切片: {problem['b']}"
        else:
            return f"傾き{problem['a']}の直線"
    
    else:  # 二次関数
        if problem["problem_type"] == "頂点を求める":
            vertex_x = -problem["b"] / (2 * problem["a"])
            vertex_y = problem["a"] * vertex_x**2 + problem["b"] * vertex_x + problem["c"]
            return f"頂点: ({vertex_x:.2f}, {vertex_y:.2f})"
        elif problem["problem_type"] == "軸の方程式を求める":
            axis_x = -problem["b"] / (2 * problem["a"])
            return f"軸の方程式: x = {axis_x:.2f}"
        elif problem["problem_type"] == "y切片を求める":
            return f"y切片: {problem['c']}"
        elif problem["problem_type"] == "最大値または最小値を求める":
            vertex_x = -problem["b"] / (2 * problem["a"])
            vertex_y = problem["a"] * vertex_x**2 + problem["b"] * vertex_x + problem["c"]
            if problem["a"] > 0:
                return f"最小値: {vertex_y:.2f} (x = {vertex_x:.2f})"
            else:
                return f"最大値: {vertex_y:.2f} (x = {vertex_x:.2f})"
        else:
            # x切片の場合
            discriminant = problem["b"]**2 - 4*problem["a"]*problem["c"]
            if discriminant > 0:
                x1 = (-problem["b"] + np.sqrt(discriminant)) / (2*problem["a"])
                x2 = (-problem["b"] - np.sqrt(discriminant)) / (2*problem["a"])
                return f"x切片: {x1:.2f}, {x2:.2f}"
            elif discriminant == 0:
                x = -problem["b"] / (2*problem["a"])
                return f"x切片: {x:.2f} (重解)"
            else:
                return "x切片は存在しません（実数解なし）"

# メイン表示部分
if hasattr(st.session_state, 'problems_generated') and st.session_state.problems_generated:
    st.header("📝 生成された問題")
    
    if st.session_state.problems:
        # 問題選択
        col1, col2 = st.columns([3, 1])
        with col1:
            problem_index = st.selectbox(
                "問題を選択",
                range(len(st.session_state.problems)),
                format_func=lambda x: f"問題 {x+1}"
            )
        
        with col2:
            if st.button("📋 解答を表示"):
                st.session_state.show_answers = True
        
        current_problem = st.session_state.problems[problem_index]
        
        # 問題表示
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"問題 {problem_index + 1}")
            st.markdown(f"**関数:** {current_problem['equation']}")
            st.markdown(f"**問題:** {current_problem['problem_type']}")
            
            # 解答入力
            user_answer = st.text_area(
                "あなたの解答:",
                key=f"answer_{problem_index}",
                height=100
            )
            
            if st.session_state.show_answers:
                correct_answer = get_correct_answer(current_problem)
                st.success(f"**正解:** {correct_answer}")
        
        with col2:
            st.subheader("グラフ")
            fig = plot_function(current_problem)
            st.pyplot(fig)
        
        # 問題一覧
        st.subheader("📋 問題一覧")
        for i, prob in enumerate(st.session_state.problems):
            with st.expander(f"問題 {i+1}: {prob['type']} - {prob['problem_type']}"):
                st.write(f"**式:** {prob['equation']}")
                if st.session_state.show_answers:
                    st.write(f"**解答:** {get_correct_answer(prob)}")

else:
    st.info("👈 サイドバーから設定を選択し、「新しい問題を生成」ボタンを押してください")
    
    # サンプル表示
    st.subheader("🎯 アプリの機能")
    st.markdown("""
    - **一次関数・二次関数の問題生成**: ランダムに問題を作成
    - **グラフ表示**: 関数のグラフを視覚的に表示
    - **難易度設定**: 初級・中級・上級から選択
    - **多様な問題タイプ**: 
        - 一次関数: 傾き・切片、特定点での値、x切片・y切片
        - 二次関数: 頂点、軸の方程式、切片、最大値・最小値
    - **解答確認**: 正解を表示して学習をサポート
    """)

# フッター
st.markdown("---")
st.markdown("💡 **使い方:** サイドバーで設定を選んで問題を生成し、解答を入力して学習しましょう！")

