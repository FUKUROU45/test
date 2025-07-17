import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
import japanize_matplotlib

# 日本語フォントの設定
plt.rcParams['font.family'] = 'DejaVu Sans'

def generate_linear_function_problem():
    """一次関数の問題を生成"""
    a = random.randint(-5, 5)
    while a == 0:
        a = random.randint(-5, 5)
    b = random.randint(-10, 10)
    
    problem_type = random.choice(['graph_to_equation', 'equation_to_value', 'two_points'])
    
    if problem_type == 'graph_to_equation':
        # グラフから式を求める問題
        x_vals = np.linspace(-5, 5, 100)
        y_vals = a * x_vals + b
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_vals, y_vals, 'b-', linewidth=2)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-15, 15)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('グラフから一次関数の式を求めなさい')
        
        # 格子点をマーク
        for x in range(-5, 6):
            y = a * x + b
            if -15 <= y <= 15:
                ax.plot(x, y, 'ro', markersize=4)
        
        problem = "上のグラフの一次関数の式を求めなさい。"
        answer = f"y = {a}x + {b}" if b >= 0 else f"y = {a}x - {abs(b)}"
        
        return problem, answer, fig
    
    elif problem_type == 'equation_to_value':
        # 式から値を求める問題
        x_val = random.randint(-5, 5)
        y_val = a * x_val + b
        
        equation = f"y = {a}x + {b}" if b >= 0 else f"y = {a}x - {abs(b)}"
        problem = f"一次関数 {equation} において、x = {x_val} のときのyの値を求めなさい。"
        answer = f"y = {y_val}"
        
        return problem, answer, None
    
    else:  # two_points
        # 2点を通る直線の式を求める問題
        x1, x2 = random.randint(-5, 5), random.randint(-5, 5)
        while x1 == x2:
            x2 = random.randint(-5, 5)
        
        y1 = a * x1 + b
        y2 = a * x2 + b
        
        problem = f"2点 ({x1}, {y1}), ({x2}, {y2}) を通る直線の式を求めなさい。"
        answer = f"y = {a}x + {b}" if b >= 0 else f"y = {a}x - {abs(b)}"
        
        return problem, answer, None

def generate_quadratic_function_problem():
    """二次関数の問題を生成"""
    a = random.randint(-3, 3)
    while a == 0:
        a = random.randint(-3, 3)
    b = random.randint(-5, 5)
    c = random.randint(-5, 5)
    
    problem_type = random.choice(['graph_to_equation', 'vertex', 'value_at_point'])
    
    if problem_type == 'graph_to_equation':
        # グラフから式を求める問題（簡単なもの）
        x_vals = np.linspace(-5, 5, 100)
        y_vals = a * x_vals**2 + b * x_vals + c
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_vals, y_vals, 'r-', linewidth=2)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-10, 10)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('グラフから二次関数の式を求めなさい')
        
        # 頂点をマーク
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        ax.plot(vertex_x, vertex_y, 'go', markersize=8, label='頂点')
        ax.legend()
        
        problem = "上のグラフの二次関数の式を求めなさい。"
        if b == 0 and c == 0:
            answer = f"y = {a}x²"
        elif b == 0:
            answer = f"y = {a}x² + {c}" if c > 0 else f"y = {a}x² - {abs(c)}"
        elif c == 0:
            answer = f"y = {a}x² + {b}x" if b > 0 else f"y = {a}x² - {abs(b)}x"
        else:
            answer = f"y = {a}x² + {b}x + {c}" if b > 0 and c > 0 else f"y = {a}x² + {b}x + {c}"
        
        return problem, answer, fig
    
    elif problem_type == 'vertex':
        # 頂点を求める問題
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        
        if b == 0 and c == 0:
            equation = f"y = {a}x²"
        elif b == 0:
            equation = f"y = {a}x² + {c}" if c > 0 else f"y = {a}x² - {abs(c)}"
        elif c == 0:
            equation = f"y = {a}x² + {b}x" if b > 0 else f"y = {a}x² - {abs(b)}x"
        else:
            equation = f"y = {a}x² + {b}x + {c}"
        
        problem = f"二次関数 {equation} の頂点の座標を求めなさい。"
        answer = f"({vertex_x}, {vertex_y})"
        
        return problem, answer, None
    
    else:  # value_at_point
        # 指定された点での値を求める問題
        x_val = random.randint(-3, 3)
        y_val = a * x_val**2 + b * x_val + c
        
        if b == 0 and c == 0:
            equation = f"y = {a}x²"
        elif b == 0:
            equation = f"y = {a}x² + {c}" if c > 0 else f"y = {a}x² - {abs(c)}"
        elif c == 0:
            equation = f"y = {a}x² + {b}x" if b > 0 else f"y = {a}x² - {abs(b)}x"
        else:
            equation = f"y = {a}x² + {b}x + {c}"
        
        problem = f"二次関数 {equation} において、x = {x_val} のときのyの値を求めなさい。"
        answer = f"y = {y_val}"
        
        return problem, answer, None

def generate_basic_function_problem():
    """基本的な関数の問題を生成"""
    problem_type = random.choice(['function_value', 'inverse_function', 'domain_range'])
    
    if problem_type == 'function_value':
        # 関数の値を求める問題
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        x_val = random.randint(1, 5)
        
        function_type = random.choice(['linear', 'quadratic', 'fraction'])
        
        if function_type == 'linear':
            y_val = a * x_val + b
            problem = f"f(x) = {a}x + {b} のとき、f({x_val}) を求めなさい。"
            answer = f"f({x_val}) = {y_val}"
        elif function_type == 'quadratic':
            y_val = a * x_val**2 + b
            problem = f"f(x) = {a}x² + {b} のとき、f({x_val}) を求めなさい。"
            answer = f"f({x_val}) = {y_val}"
        else:  # fraction
            y_val = a / x_val + b
            problem = f"f(x) = {a}/x + {b} のとき、f({x_val}) を求めなさい。"
            answer = f"f({x_val}) = {y_val}"
        
        return problem, answer, None
    
    elif problem_type == 'inverse_function':
        # 逆関数の問題（簡単なもの）
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        y_val = random.randint(5, 20)
        
        x_val = (y_val - b) / a
        problem = f"f(x) = {a}x + {b} のとき、f(x) = {y_val} となるxの値を求めなさい。"
        answer = f"x = {x_val}"
        
        return problem, answer, None
    
    else:  # domain_range
        # 定義域と値域の基本問題
        a = random.randint(1, 3)
        b = random.randint(1, 5)
        
        problem = f"関数 f(x) = {a}x + {b} において、xの定義域が 0 ≤ x ≤ 3 のとき、値域を求めなさい。"
        min_val = a * 0 + b
        max_val = a * 3 + b
        answer = f"{min_val} ≤ y ≤ {max_val}"
        
        return problem, answer, None

def main():
    st.title("📐 関数問題作成アプリ（中1〜高1）")
    st.write("中学1年生から高校1年生までの範囲で関数の問題を作成します。")
    
    # サイドバーで問題レベルを選択
    st.sidebar.header("問題設定")
    problem_level = st.sidebar.selectbox(
        "問題のレベルを選択してください",
        ["基本的な関数", "一次関数", "二次関数", "ランダム"]
    )
    
    difficulty = st.sidebar.selectbox(
        "難易度を選択してください",
        ["やさしい", "普通", "少し難しい"]
    )
    
    # 問題生成ボタン
    if st.sidebar.button("新しい問題を生成", type="primary"):
        st.session_state.generate_new = True
    
    # 問題表示
    if 'generate_new' in st.session_state or 'current_problem' not in st.session_state:
        if problem_level == "基本的な関数":
            problem, answer, fig = generate_basic_function_problem()
        elif problem_level == "一次関数":
            problem, answer, fig = generate_linear_function_problem()
        elif problem_level == "二次関数":
            problem, answer, fig = generate_quadratic_function_problem()
        else:  # ランダム
            level = random.choice(["basic", "linear", "quadratic"])
            if level == "basic":
                problem, answer, fig = generate_basic_function_problem()
            elif level == "linear":
                problem, answer, fig = generate_linear_function_problem()
            else:
                problem, answer, fig = generate_quadratic_function_problem()
        
        st.session_state.current_problem = problem
        st.session_state.current_answer = answer
        st.session_state.current_fig = fig
        st.session_state.show_answer = False
    
    # 問題の表示
    st.subheader("📝 問題")
    st.write(st.session_state.current_problem)
    
    # グラフがある場合は表示
    if st.session_state.current_fig is not None:
        st.pyplot(st.session_state.current_fig)
    
    # 答えを表示するボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.button("答えを見る"):
            st.session_state.show_answer = True
    
    with col2:
        if st.button("答えを隠す"):
            st.session_state.show_answer = False
    
    # 答えの表示
    if st.session_state.get('show_answer', False):
        st.subheader("✅ 答え")
        st.success(st.session_state.current_answer)
    
    # 学習のヒント
    st.sidebar.header("💡 学習のヒント")
    hints = {
        "基本的な関数": [
            "関数とは、xの値が決まると、yの値が一意に決まる関係のことです",
            "f(x) = 3x + 2 のとき、f(1) = 3×1 + 2 = 5 となります",
            "定義域はxの取りうる値の範囲、値域はyの取りうる値の範囲です"
        ],
        "一次関数": [
            "一次関数は y = ax + b の形で表されます",
            "aは傾き、bはy切片（y軸との交点）です",
            "傾きは「変化の割合」を表し、yの増加量/xの増加量で求められます"
        ],
        "二次関数": [
            "二次関数は y = ax² + bx + c の形で表されます",
            "放物線のグラフになります",
            "頂点の座標は (-b/2a, -D/4a) です（D = b² - 4ac）"
        ]
    }
    
    if problem_level in hints:
        for hint in hints[problem_level]:
            st.sidebar.info(hint)
    
    # 統計情報
    st.sidebar.header("📊 使用統計")
    if 'problem_count' not in st.session_state:
        st.session_state.problem_count = 0
    
    if 'generate_new' in st.session_state:
        st.session_state.problem_count += 1
    
    st.sidebar.metric("生成した問題数", st.session_state.problem_count)
    
    # フッター
    st.markdown("---")
    st.markdown("**📚 学習のコツ**")
    st.markdown("- 問題を解いた後は、必ず答えを確認しましょう")
    st.markdown("- 間違えた問題は、もう一度同じタイプの問題を解いてみましょう")
    st.markdown("- グラフ問題では、軸の目盛りや点の位置を正確に読み取ることが大切です")

if __name__ == "__main__":
    main()

