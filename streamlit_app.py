import streamlit as st
import numpy as np
import random
from fractions import Fraction
import plotly.graph_objects as go

def generate_quadratic_problem(difficulty="basic"):
    """難易度に応じて二次関数の問題を生成"""
    if difficulty == "basic":
        # 基本: a=1, 整数係数
        a = 1
        b = random.randint(-10, 10)
        c = random.randint(-20, 20)
    elif difficulty == "intermediate":
        # 中級: a≠1, 整数係数
        a = random.choice([2, 3, 4, -1, -2, -3])
        b = random.randint(-12, 12)
        c = random.randint(-25, 25)
    else:  # advanced
        # 上級: 分数係数も含む
        a = random.choice([1, 2, 3, -1, -2, Fraction(1,2), Fraction(3,2), Fraction(-1,2)])
        b = random.randint(-15, 15)
        c = random.randint(-30, 30)
    
    return a, b, c

def solve_completion_of_square(a, b, c):
    """平方完成の解を計算"""
    # ax² + bx + c = a(x + p)² + q の形に変形
    # p = b/(2a), q = c - b²/(4a)
    
    if isinstance(a, Fraction) or isinstance(b, Fraction) or isinstance(c, Fraction):
        a = Fraction(a)
        b = Fraction(b)
        c = Fraction(c)
    
    p = b / (2 * a)
    q = c - (b * b) / (4 * a)
    
    return a, p, q

def format_fraction(value):
    """分数を見やすい形で表示"""
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        else:
            return f"{value.numerator}/{value.denominator}"
    elif isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        else:
            frac = Fraction(value).limit_denominator()
            if frac.denominator == 1:
                return str(frac.numerator)
            else:
                return f"{frac.numerator}/{frac.denominator}"
    else:
        return str(value)

def format_quadratic(a, b, c):
    """二次関数を見やすい形で表示"""
    result = "y = "
    
    # aの項
    if a == 1:
        result += "x²"
    elif a == -1:
        result += "-x²"
    else:
        result += f"{format_fraction(a)}x²"
    
    # bの項
    if b > 0:
        if b == 1:
            result += " + x"
        else:
            result += f" + {format_fraction(b)}x"
    elif b < 0:
        if b == -1:
            result += " - x"
        else:
            result += f" - {format_fraction(abs(b))}x"
    
    # cの項
    if c > 0:
        result += f" + {format_fraction(c)}"
    elif c < 0:
        result += f" - {format_fraction(abs(c))}"
    
    return result

def format_completed_square(a, p, q):
    """平方完成の形を表示"""
    result = "y = "
    
    # aの係数
    if a == 1:
        result += "("
    elif a == -1:
        result += "-("
    else:
        result += f"{format_fraction(a)}("
    
    # x + p の部分
    if p > 0:
        result += f"x + {format_fraction(p)}"
    elif p < 0:
        result += f"x - {format_fraction(abs(p))}"
    else:
        result += "x"
    
    result += ")²"
    
    # qの項
    if q > 0:
        result += f" + {format_fraction(q)}"
    elif q < 0:
        result += f" - {format_fraction(abs(q))}"
    
    return result

def plot_quadratic(a, b, c):
    """二次関数のグラフを描画"""
    x = np.linspace(-10, 10, 400)
    y = float(a) * x**2 + float(b) * x + float(c)
    
    # 頂点の座標
    vertex_x = -float(b) / (2 * float(a))
    vertex_y = float(a) * vertex_x**2 + float(b) * vertex_x + float(c)
    
    fig = go.Figure()
    
    # 二次関数のグラフ
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=f'y = {format_fraction(a)}x² + {format_fraction(b)}x + {format_fraction(c)}',
        line=dict(color='blue', width=3)
    ))
    
    # 頂点をマーク
    fig.add_trace(go.Scatter(
        x=[vertex_x], y=[vertex_y],
        mode='markers',
        name=f'頂点 ({format_fraction(vertex_x)}, {format_fraction(vertex_y)})',
        marker=dict(color='red', size=10, symbol='circle')
    ))
    
    fig.update_layout(
        title="二次関数のグラフ",
        xaxis_title="x",
        yaxis_title="y",
        grid=True,
        showlegend=True,
        height=400
    )
    
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray')
    
    return fig

def check_answer(user_a, user_p, user_q, correct_a, correct_p, correct_q):
    """解答をチェック"""
    try:
        # 入力値を数値に変換
        if '/' in str(user_a):
            user_a = Fraction(user_a)
        else:
            user_a = float(user_a)
            
        if '/' in str(user_p):
            user_p = Fraction(user_p)
        else:
            user_p = float(user_p)
            
        if '/' in str(user_q):
            user_q = Fraction(user_q)
        else:
            user_q = float(user_q)
        
        # 許容誤差
        tolerance = 1e-10
        
        def is_close(a, b):
            return abs(float(a) - float(b)) < tolerance
        
        return (is_close(user_a, correct_a) and 
                is_close(user_p, correct_p) and 
                is_close(user_q, correct_q))
    except:
        return False

def main():
    st.set_page_config(page_title="平方完成問題", page_icon="📐", layout="wide")
    
    st.title("📐 平方完成問題練習")
    st.write("二次関数を平方完成の形に変形する練習をしましょう！")
    
    # サイドバーで設定
    st.sidebar.title("問題設定")
    difficulty = st.sidebar.selectbox(
        "難易度を選択:",
        ["basic", "intermediate", "advanced"],
        format_func=lambda x: {"basic": "基本 (a=1)", "intermediate": "中級 (a≠1)", "advanced": "上級 (分数含む)"}[x]
    )
    
    # セッション状態の初期化
    if 'problem_data' not in st.session_state:
        st.session_state.problem_data = None
        st.session_state.show_solution = False
        st.session_state.score = 0
        st.session_state.total_problems = 0
    
    # 新しい問題を生成
    if st.sidebar.button("新しい問題を生成") or st.session_state.problem_data is None:
        a, b, c = generate_quadratic_problem(difficulty)
        correct_a, correct_p, correct_q = solve_completion_of_square(a, b, c)
        st.session_state.problem_data = {
            'original': (a, b, c),
            'solution': (correct_a, correct_p, correct_q)
        }
        st.session_state.show_solution = False
    
    # 現在の問題データ
    if st.session_state.problem_data:
        a, b, c = st.session_state.problem_data['original']
        correct_a, correct_p, correct_q = st.session_state.problem_data['solution']
        
        # 問題表示
        st.markdown("## 📝 問題")
        st.markdown(f"### 次の二次関数を平方完成してください:")
        st.markdown(f"## {format_quadratic(a, b, c)}")
        
        # 2列レイアウト
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 解答入力")
            st.write("平方完成の形: y = a(x + p)² + q")
            
            # 解答入力フィールド
            user_a = st.text_input("a の値:", placeholder="例: 2, -1, 1/2")
            user_p = st.text_input("p の値:", placeholder="例: 3, -2, 1/4")
            user_q = st.text_input("q の値:", placeholder="例: 5, -7, 3/2")
            
            # ボタン
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                check_btn = st.button("解答チェック", type="primary")
            with col_btn2:
                show_solution_btn = st.button("解答を見る")
            
            # 解答チェック
            if check_btn and user_a and user_p and user_q:
                if check_answer(user_a, user_p, user_q, correct_a, correct_p, correct_q):
                    st.success("🎉 正解です！")
                    st.balloons()
                    st.session_state.score += 1
                    st.session_state.total_problems += 1
                else:
                    st.error("❌ 不正解です。もう一度確認してください。")
                    st.session_state.total_problems += 1
            
            # 解答表示
            if show_solution_btn:
                st.session_state.show_solution = True
            
            if st.session_state.show_solution:
                st.markdown("### 💡 正解")
                st.info(format_completed_square(correct_a, correct_p, correct_q))
                
                # 解法の説明
                with st.expander("📖 解法の手順"):
                    st.write("**平方完成の手順:**")
                    st.write(f"1. 元の式: {format_quadratic(a, b, c)}")
                    
                    if a != 1:
                        st.write(f"2. aで括り出す: {format_fraction(a)}(x² + {format_fraction(Fraction(b)/Fraction(a))}x) + {format_fraction(c)}")
                    
                    p_val = Fraction(b) / (2 * Fraction(a))
                    st.write(f"3. x²の係数の半分: {format_fraction(b)}/(2×{format_fraction(a)}) = {format_fraction(p_val)}")
                    
                    st.write(f"4. 平方を作る: (x + {format_fraction(p_val)})² = x² + {format_fraction(2*p_val)}x + {format_fraction(p_val**2)}")
                    
                    adjustment = Fraction(c) - Fraction(a) * (p_val**2)
                    st.write(f"5. 定数項を調整: {format_fraction(c)} - {format_fraction(a)} × {format_fraction(p_val**2)} = {format_fraction(adjustment)}")
                    
                    st.write(f"6. 最終形: {format_completed_square(correct_a, correct_p, correct_q)}")
        
        with col2:
            # グラフ表示
            st.markdown("### 📈 グラフ")
            fig = plot_quadratic(a, b, c)
            st.plotly_chart(fig, use_container_width=True)
            
            # 頂点の情報
            vertex_x = -float(b) / (2 * float(a))
            vertex_y = float(a) * vertex_x**2 + float(b) * vertex_x + float(c)
            
            st.markdown("### 📊 頂点の情報")
            st.write(f"**x座標**: {format_fraction(vertex_x)}")
            st.write(f"**y座標**: {format_fraction(vertex_y)}")
            st.write(f"**頂点**: ({format_fraction(vertex_x)}, {format_fraction(vertex_y)})")
        
        # スコア表示
        if st.session_state.total_problems > 0:
            accuracy = st.session_state.score / st.session_state.total_problems * 100
            st.sidebar.markdown("### 📊 成績")
            st.sidebar.write(f"正解数: {st.session_state.score}/{st.session_state.total_problems}")
            st.sidebar.write(f"正解率: {accuracy:.1f}%")
            
            if st.sidebar.button("成績をリセット"):
                st.session_state.score = 0
                st.session_state.total_problems = 0
    
    # 平方完成の説明
    with st.expander("📚 平方完成とは？"):
        st.markdown("""
        **平方完成（Completing the Square）**とは、二次関数を標準形から頂点形に変形する方法です。
        
        **変形の目的:**
        - ax² + bx + c → a(x + p)² + q
        - 頂点の座標(-p, q)が簡単に読み取れる
        - グラフの性質（最大値・最小値）が分かりやすい
        
        **基本的な手順:**
        1. x²の係数aが1でない場合は、aで括り出す
        2. x²とxの項から完全平方式を作る
        3. 定数項を調整する
        
        **例:** x² + 6x + 5
        1. x² + 6x + 5
        2. (x + 3)² - 9 + 5  ← (6÷2)² = 9を加えて引く
        3. (x + 3)² - 4
        
        **頂点:** (-3, -4)
        """)
    
    # 練習のヒント
    with st.expander("💡 解き方のコツ"):
        st.markdown("""
        **平方完成のコツ:**
        
        1. **係数に注意**: aが1でない時は最初にaで括り出す
        2. **半分の計算**: xの係数を2で割った値がpになる
        3. **符号に注意**: (x + p)²の形では、頂点のx座標は-p
        4. **定数項の調整**: 元の定数項から調整値を引く
        5. **検算**: 展開して元の式になるか確認
        
        **分数の扱い:**
        - 分数は「分子/分母」の形で入力
        - 例: 1/2, -3/4, 5/3
        - 整数は普通に入力（例: 2, -5）
        """)

if __name__ == "__main__":
    main()