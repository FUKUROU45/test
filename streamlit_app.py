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
        c = random.randint(-import streamlit as st
import numpy as np
import random
from fractions import Fraction

def generate_similar_problem(original_a, original_b, original_c, difficulty="basic"):
    """間違えた問題に似た問題を生成"""
    # 元の問題の特徴を分析
    original_pattern = analyze_problem_pattern(original_a, original_b, original_c)
    
    # 似た特徴を持つ問題を生成
    attempts = 0
    while attempts < 10:  # 無限ループ防止
        if difficulty == "basic":
            a = 1
            # 元の問題のbの符号と大きさを参考に
            if original_b > 0:
                b = random.randint(2, 8) if original_b > 0 else random.randint(-8, -2)
            else:
                b = random.randint(-8, -2) if original_b < 0 else random.randint(2, 8)
            # 似た範囲のc値
            c_range = abs(original_c)
            c = random.randint(-c_range-5, c_range+5)
            
        elif difficulty == "intermediate":
            # 元の問題のaの符号を保持
            a_choices = [2, 3, 4] if original_a > 0 else [-2, -3, -4]
            a = random.choice(a_choices)
            
            # 似た係数パターン
            b_range = abs(original_b)
            b = random.randint(-b_range-3, b_range+3)
            if b == 0:
                b = random.choice([-2, 2])
            
            c_range = abs(original_c)
            c = random.randint(-c_range-5, c_range+5)
            
        else:  # advanced
            # 分数係数を含む類似問題
            if isinstance(original_a, Fraction) or abs(original_a) < 1:
                a = random.choice([Fraction(1,2), Fraction(3,2), Fraction(-1,2), Fraction(-3,2)])
            else:
                a = random.choice([2, 3, -1, -2])
            
            b_range = abs(original_b)
            b = random.randint(-b_range-4, b_range+4)
            c_range = abs(original_c)
            c = random.randint(-c_range-8, c_range+8)
        
        # 元の問題と全く同じにならないようにチェック
        if not (a == original_a and b == original_b and c == original_c):
            break
        attempts += 1
    
    return a, b, c

def analyze_problem_pattern(a, b, c):
    """問題のパターンを分析"""
    pattern = {
        'a_positive': float(a) > 0,
        'b_positive': float(b) > 0,
        'c_positive': float(c) > 0,
        'a_magnitude': abs(float(a)),
        'b_magnitude': abs(float(b)),
        'c_magnitude': abs(float(c)),
        'has_fractions': isinstance(a, Fraction) or isinstance(b, Fraction) or isinstance(c, Fraction)
    }
    return pattern
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
    """二次関数のグラフをStreamlitのline_chartで描画"""
    x = np.linspace(-10, 10, 200)
    y = float(a) * x**2 + float(b) * x + float(c)
    
    # 頂点の座標
    vertex_x = -float(b) / (2 * float(a))
    vertex_y = float(a) * vertex_x**2 + float(b) * vertex_x + float(c)
    
    return x, y, vertex_x, vertex_y

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
        ["初級", "中級", "上級"],
        help="初級: a=1の基本問題、中級: a≠1の問題、上級: 分数係数を含む問題"
    )
    
    # 難易度を内部的な値に変換
    difficulty_map = {"初級": "basic", "中級": "intermediate", "上級": "advanced"}
    internal_difficulty = difficulty_map[difficulty]
    
    # セッション状態の初期化
    if 'problem_data' not in st.session_state:
        st.session_state.problem_data = None
        st.session_state.show_solution = False
        st.session_state.score = 0
        st.session_state.total_problems = 0
        st.session_state.wrong_problems = []  # 間違えた問題を記録
        st.session_state.practice_mode = False  # 類似問題練習モード
    
    # 新しい問題を生成
    if st.sidebar.button("新しい問題を生成") or st.session_state.problem_data is None:
        a, b, c = generate_quadratic_problem(internal_difficulty)
        correct_a, correct_p, correct_q = solve_completion_of_square(a, b, c)
        st.session_state.problem_data = {
            'original': (a, b, c),
            'solution': (correct_a, correct_p, correct_q),
            'difficulty': difficulty
        }
        st.session_state.show_solution = False
    
    # 現在の問題データ
    if st.session_state.problem_data:
        a, b, c = st.session_state.problem_data['original']
        correct_a, correct_p, correct_q = st.session_state.problem_data['solution']
        
        # 問題表示
        st.markdown("## 📝 問題")
        problem_difficulty = st.session_state.problem_data.get('difficulty', '初級')
        st.markdown(f"**難易度: {problem_difficulty}**")
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
                    st.error("❌ 不正解です。正解と解説を確認してください。")
                    st.session_state.total_problems += 1
                    st.session_state.show_solution = True  # 間違えた時に自動で解答表示
            
            # 解答表示
            if show_solution_btn:
                st.session_state.show_solution = True
            
            if st.session_state.show_solution:
                st.markdown("### 💡 正解")
                st.info(format_completed_square(correct_a, correct_p, correct_q))
                
                # 入力値との比較（間違えた場合）
                if check_btn and user_a and user_p and user_q:
                    try:
                        # 入力値を数値に変換して表示
                        if '/' in str(user_a):
                            input_a = Fraction(user_a)
                        else:
                            input_a = float(user_a)
                            
                        if '/' in str(user_p):
                            input_p = Fraction(user_p)
                        else:
                            input_p = float(user_p)
                            
                        if '/' in str(user_q):
                            input_q = Fraction(user_q)
                        else:
                            input_q = float(user_q)
                        
                        st.markdown("### 🔍 あなたの解答との比較")
                        col_compare1, col_compare2 = st.columns(2)
                        
                        with col_compare1:
                            st.write("**あなたの解答:**")
                            user_format = format_completed_square(input_a, input_p, input_q)
                            st.write(user_format)
                        
                        with col_compare2:
                            st.write("**正解:**")
                            correct_format = format_completed_square(correct_a, correct_p, correct_q)
                            st.write(correct_format)
                        
                        # 各項目の正誤チェック
                        st.markdown("### ✅ 項目別チェック")
                        
                        def is_close(a, b):
                            return abs(float(a) - float(b)) < 1e-10
                        
                        a_correct = is_close(input_a, correct_a)
                        p_correct = is_close(input_p, correct_p)
                        q_correct = is_close(input_q, correct_q)
                        
                        st.write(f"**a の値**: {format_fraction(input_a)} {'✅' if a_correct else '❌'} (正解: {format_fraction(correct_a)})")
                        st.write(f"**p の値**: {format_fraction(input_p)} {'✅' if p_correct else '❌'} (正解: {format_fraction(correct_p)})")
                        st.write(f"**q の値**: {format_fraction(input_q)} {'✅' if q_correct else '❌'} (正解: {format_fraction(correct_q)})")
                        
                    except:
                        st.warning("入力値の形式を確認してください。")
                
                # 解法の説明
                with st.expander("📖 詳しい解法の手順", expanded=True):
                    st.markdown("### 🎯 平方完成の基本的な考え方")
                    st.info("**目標**: ax² + bx + c を a(x + p)² + q の形に変形する")
                    
                    st.markdown("---")
                    st.markdown("### 📝 ステップ・バイ・ステップ解説")
                    
                    # 元の式を強調表示
                    st.markdown("#### 🔵 与えられた式")
                    st.markdown(f"##### {format_quadratic(a, b, c)}")
                    
                    step_num = 1
                    
                    # Step 1: a≠1の場合の処理
                    if a != 1:
                        st.markdown(f"#### 🔸 Step {step_num}: aで括り出す")
                        st.markdown("**なぜ？** → a≠1の時は、まずaを前に出して計算しやすくします")
                        
                        inside_b = Fraction(b) / Fraction(a)
                        st.markdown(f"**計算:**")
                        st.code(f"""
元の式: {format_quadratic(a, b, c)}
     ↓ aで括り出す
= {format_fraction(a)}(x² + {format_fraction(inside_b)}x) + {format_fraction(c)}
                        """)
                        step_num += 1
                    else:
                        st.markdown(f"#### 🔸 Step {step_num}: 係数の確認")
                        st.markdown("**確認:** a = 1なので、そのまま平方完成を進めます")
                        step_num += 1
                    
                    # Step 2: pの値を計算
                    st.markdown(f"#### 🔸 Step {step_num}: 平方を作るためのp値を計算")
                    st.markdown("**公式:** p = b/(2a)")
                    
                    p_val = Fraction(b) / (2 * Fraction(a))
                    st.markdown("**計算過程:**")
                    st.code(f"""
p = b/(2a) = {format_fraction(b)}/(2 × {format_fraction(a)})
  = {format_fraction(b)}/{format_fraction(2 * Fraction(a))}
  = {format_fraction(p_val)}
                    """)
                    
                    st.markdown("**意味:** (x + p)²を作るために必要な値です")
                    step_num += 1
                    
                    # Step 3: 完全平方式の説明
                    st.markdown(f"#### 🔸 Step {step_num}: 完全平方式を理解する")
                    st.markdown("**完全平方式の形:** (x + p)² = x² + 2px + p²")
                    
                    square_term = p_val ** 2
                    st.markdown("**具体的に展開すると:**")
                    st.code(f"""
(x + {format_fraction(p_val)})² = x² + 2×{format_fraction(p_val)}×x + ({format_fraction(p_val)})²
                    = x² + {format_fraction(2*p_val)}x + {format_fraction(square_term)}
                    """)
                    
                    # 元の式のxの係数と比較
                    original_x_coeff = Fraction(b) / Fraction(a) if a != 1 else Fraction(b)
                    st.markdown(f"**確認:** 元の式のxの係数 {format_fraction(original_x_coeff)} と一致！ ✅")
                    step_num += 1
                    
                    # Step 4: 定数項の調整（最も重要）
                    st.markdown(f"#### 🔸 Step {step_num}: 定数項を調整する（重要！）")
                    st.markdown("**問題:** 完全平方式を作ると、余分な定数項が生まれます")
                    
                    if a != 1:
                        st.markdown("**元の式の構造:**")
                        st.code(f"""
{format_fraction(a)}(x² + {format_fraction(Fraction(b)/Fraction(a))}x) + {format_fraction(c)}
                        """)
                        
                        st.markdown("**完全平方式に置き換えると:**")
                        st.code(f"""
{format_fraction(a)}[(x + {format_fraction(p_val)})² - {format_fraction(square_term)}] + {format_fraction(c)}
= {format_fraction(a)}(x + {format_fraction(p_val)})² - {format_fraction(Fraction(a) * square_term)} + {format_fraction(c)}
= {format_fraction(a)}(x + {format_fraction(p_val)})² + [{format_fraction(c)} - {format_fraction(Fraction(a) * square_term)}]
                        """)
                        
                        adjustment = Fraction(c) - Fraction(a) * square_term
                        st.markdown(f"**定数項の計算:**")
                        st.code(f"""
q = {format_fraction(c)} - {format_fraction(a)} × {format_fraction(square_term)}
  = {format_fraction(c)} - {format_fraction(Fraction(a) * square_term)}
  = {format_fraction(adjustment)}
                        """)
                    else:
                        st.markdown("**元の式:**")
                        st.code(f"x² + {format_fraction(b)}x + {format_fraction(c)}")
                        
                        st.markdown("**完全平方式に置き換えると:**")
                        st.code(f"""
(x + {format_fraction(p_val)})² - {format_fraction(square_term)} + {format_fraction(c)}
= (x + {format_fraction(p_val)})² + [{format_fraction(c)} - {format_fraction(square_term)}]
                        """)
                        
                        adjustment = Fraction(c) - square_term
                        st.markdown(f"**定数項の計算:**")
                        st.code(f"""
q = {format_fraction(c)} - {format_fraction(square_term)} = {format_fraction(adjustment)}
                        """)
                    
                    step_num += 1
                    
                    # Step 5: 最終答え
                    st.markdown(f"#### 🎯 Step {step_num}: 最終答え")
                    st.success(f"**平方完成の結果:** {format_completed_square(correct_a, correct_p, correct_q)}")
                    
                    # Step 6: 検算
                    st.markdown(f"#### ✅ Step {step_num + 1}: 検算（必ず行いましょう！）")
                    st.markdown("**方法:** 平方完成した式を展開して、元の式になるか確認")
                    
                    # 展開の詳細
                    st.markdown("**展開過程:**")
                    if a != 1:
                        st.code(f"""
{format_completed_square(correct_a, correct_p, correct_q)}
= {format_fraction(correct_a)}(x + {format_fraction(correct_p)})² + {format_fraction(correct_q)}
= {format_fraction(correct_a)}[x² + {format_fraction(2*correct_p)}x + {format_fraction(correct_p**2)}] + {format_fraction(correct_q)}
= {format_fraction(correct_a)}x² + {format_fraction(correct_a * 2 * correct_p)}x + {format_fraction(correct_a * correct_p**2)} + {format_fraction(correct_q)}
= {format_fraction(correct_a)}x² + {format_fraction(correct_a * 2 * correct_p)}x + {format_fraction(correct_a * correct_p**2 + correct_q)}
                        """)
                    else:
                        st.code(f"""
{format_completed_square(correct_a, correct_p, correct_q)}
= (x + {format_fraction(correct_p)})² + {format_fraction(correct_q)}
= x² + {format_fraction(2*correct_p)}x + {format_fraction(correct_p**2)} + {format_fraction(correct_q)}
= x² + {format_fraction(2*correct_p)}x + {format_fraction(correct_p**2 + correct_q)}
                        """)
                    
                    # 係数の確認
                    expanded_a = correct_a
                    expanded_b = correct_a * 2 * correct_p
                    expanded_c = correct_a * correct_p**2 + correct_q
                    
                    st.markdown("**係数の確認:**")
                    st.code(f"""
元の式の係数: a={format_fraction(a)}, b={format_fraction(b)}, c={format_fraction(c)}
展開した係数: a={format_fraction(expanded_a)}, b={format_fraction(expanded_b)}, c={format_fraction(expanded_c)}
                    """)
                    
                    # 一致確認
                    a_match = abs(float(expanded_a) - float(a)) < 1e-10
                    b_match = abs(float(expanded_b) - float(b)) < 1e-10
                    c_match = abs(float(expanded_c) - float(c)) < 1e-10
                    
                    if a_match and b_match and c_match:
                        st.success("✅ すべての係数が一致しました！平方完成は正しいです。")
                    else:
                        st.error("❌ 係数が一致しません。計算を見直してください。")
                    
                    # 視覚的な流れの確認
                    st.markdown("---")
                    st.markdown("### 🔄 変形の流れ（まとめ）")
                    st.code(f"""
{format_quadratic(a, b, c)}
          ↓ 平方完成
{format_completed_square(correct_a, correct_p, correct_q)}
                    """)
                    
                    # 頂点の情報
                    vertex_x_val = -float(correct_p)
                    vertex_y_val = float(correct_q)
                    st.markdown(f"**📍 頂点の座標:** ({format_fraction(vertex_x_val)}, {format_fraction(vertex_y_val)})")
                    st.markdown(f"**📈 軸の方程式:** x = {format_fraction(vertex_x_val)}")
                    
                    if float(a) > 0:
                        st.markdown(f"**📊 最小値:** {format_fraction(vertex_y_val)} (x = {format_fraction(vertex_x_val)}のとき)")
                    else:
                        st.markdown(f"**📊 最大値:** {format_fraction(vertex_y_val)} (x = {format_fraction(vertex_x_val)}のとき)")
                
                
                # よくある間違い
                with st.expander("⚠️ よくある間違いと対策"):
                    st.markdown("### 🚫 つまずきポイント TOP 5")
                    
                    st.markdown("#### 1️⃣ 符号の間違い")
                    st.error("**間違い例:** y = (x - 3)² + 2 の頂点を (3, 2) と答える")
                    st.success("**正解:** y = (x - 3)² + 2 = (x - (+3))² + 2 なので頂点は (3, 2)")
                    st.info("**覚え方:** y = (x + p)² + q の頂点は (-p, q)")
                    
                    st.markdown("#### 2️⃣ p値の計算ミス")
                    st.error("**間違い例:** 2x² + 8x + 3 で p = 8/(2×2) = 2 と計算")
                    st.success("**正解:** p = b/(2a) = 8/(2×2) = 8/4 = 2")
                    st.info("**対策:** 分数の計算は慎重に。約分を忘れずに！")
                    
                    st.markdown("#### 3️⃣ 定数項の調整忘れ")
                    st.error("**間違い例:** x² + 6x + 5 を (x + 3)² とそのまま書く")
                    st.success("**正解:** (x + 3)² - 9 + 5 = (x + 3)² - 4")
                    st.info("**対策:** 完全平方を作ったら、必ず定数項を調整する")
                    
                    st.markdown("#### 4️⃣ a≠1の時の処理忘れ")
                    st.error("**間違い例:** 2x² + 4x + 1 をそのまま平方完成する")
                    st.success("**正解:** まず2で括り出す → 2(x² + 2x) + 1")
                    st.info("**対策:** a≠1の時は必ず最初にaで括り出す")
                    
                    st.markdown("#### 5️⃣ 検算をしない")
                    st.error("**問題:** 計算ミスに気づかない")
                    st.success("**対策:** 必ず展開して元の式になるか確認")
                    st.info("**習慣:** 解答後は必ず検算する癖をつける")
                    
                    st.markdown("---")
                    st.markdown("### 💡 成功のコツ")
                    st.markdown("""
                    1. **順序を守る**: Step1→Step2→...と順番通りに進む
                    2. **途中式を書く**: 暗算せず、必ず途中の計算を書く
                    3. **分数に慣れる**: 分数の計算に慣れておく
                    4. **パターンを覚える**: 典型的な問題のパターンを覚える
                    5. **検算を習慣化**: 必ず最後に検算する
                    """)
                
                
                # 関連する概念
                with st.expander("🔗 深く理解するために"):
                    vertex_x_val = -float(b) / (2 * float(a))
                    vertex_y_val = float(correct_q)
                    
                    st.markdown("### 🎯 平方完成の意味と目的")
                    
                    st.markdown("#### 📊 なぜ平方完成をするの？")
                    st.markdown("""
                    1. **頂点が見つけやすい**: 座標が直接読める
                    2. **最大値・最小値がわかる**: グラフの性質が明確
                    3. **グラフが描きやすい**: 頂点から左右対称に描ける
                    4. **問題が解きやすい**: 不等式や方程式が簡単になる
                    """)
                    
                    st.markdown("#### 🔄 二次関数の3つの表現")
                    
                    col_form1, col_form2, col_form3 = st.columns(3)
                    
                    with col_form1:
                        st.markdown("**標準形**")
                        st.code(f"{format_quadratic(a, b, c)}")
                        st.markdown("- 一般的な形\n- 係数から判別式が計算できる")
                    
                    with col_form2:
                        st.markdown("**頂点形**")
                        st.code(f"{format_completed_square(correct_a, correct_p, correct_q)}")
                        st.markdown("- 頂点が直接読める\n- 最大値・最小値がわかる")
                    
                    with col_form3:
                        st.markdown("**因数分解形**")
                        discriminant = float(b)**2 - 4*float(a)*float(c)
                        if discriminant >= 0:
                            import math
                            x1 = (-float(b) + math.sqrt(discriminant)) / (2*float(a))
                            x2 = (-float(b) - math.sqrt(discriminant)) / (2*float(a))
                            if discriminant > 0:
                                st.code(f"{format_fraction(a)}(x - {x1:.2f})(x - {x2:.2f})")
                                st.markdown("- x切片が直接読める\n- 解が2個ある場合")
                            else:
                                st.code(f"{format_fraction(a)}(x - {x1:.2f})²")
                                st.markdown("- x切片が1個（重根）")
                        else:
                            st.code("因数分解不可")
                            st.markdown("- 実根がない場合")
                    
                    st.markdown("#### 📈 この問題の二次関数の性質")
                    
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.markdown("**基本情報**")
                        st.markdown(f"- **頂点**: ({format_fraction(vertex_x_val)}, {format_fraction(vertex_y_val)})")
                        st.markdown(f"- **軸の方程式**: x = {format_fraction(vertex_x_val)}")
                        st.markdown(f"- **開く向き**: {'上向き ↗️' if float(a) > 0 else '下向き ↙️'}")
                        
                        if float(a) > 0:
                            st.markdown(f"- **最小値**: {format_fraction(vertex_y_val)}")
                        else:
                            st.markdown(f"- **最大値**: {format_fraction(vertex_y_val)}")
                    
                    with info_col2:
                        st.markdown("**詳細分析**")
                        discriminant = float(b)**2 - 4*float(a)*float(c)
                        st.markdown(f"- **判別式**: D = {discriminant:.2f}")
                        
                        if discriminant > 0:
                            st.markdown("- **x切片**: 2個あり")
                            st.markdown("- **実根**: 2個の異なる解")
                        elif discriminant == 0:
                            st.markdown("- **x切片**: 1個（接する）")
                            st.markdown("- **実根**: 1個（重根）")
                        else:
                            st.markdown("- **x切片**: なし")
                            st.markdown("- **実根**: なし（虚根）")
                        
                        st.markdown(f"- **y切片**: {format_fraction(c)}")
                    
                    st.markdown("#### 🧮 計算のポイント")
                    st.markdown("""
                    **平方完成の核心:**
                    - `(x + p)² = x² + 2px + p²` の形を作る
                    - `p = b/(2a)` で必要な値を計算
                    - 余分な定数項 `p²` を調整する
                    
                    **覚えておくべき公式:**
                    - 頂点のx座標: `-b/(2a)`
                    - 頂点のy座標: 元の式に x座標を代入
                    - 判別式: `D = b² - 4ac`
                    """)
                    
                    st.markdown("#### 🎓 実際の応用例")
                    st.markdown("""
                    **平方完成が役立つ場面:**
                    1. **最大値・最小値問題**: 関数の極値を求める
                    2. **グラフの描画**: 頂点から左右対称に描く
                    3. **二次不等式**: 解の範囲を求める
                    4. **物理の問題**: 放物運動の最高点など
                    5. **最適化問題**: コストや利益の最適値
                    """)
                
                
        
        with col2:
            # グラフ表示
            st.markdown("### 📈 グラフ")
            x_vals, y_vals, vertex_x, vertex_y = plot_quadratic(a, b, c)
            
            # DataFrameでグラフを作成
            import pandas as pd
            chart_data = pd.DataFrame({
                'x': x_vals,
                'y': y_vals
            })
            st.line_chart(chart_data.set_index('x'))
            
            # 頂点の情報
            st.markdown("### 📊 頂点の情報")
            st.write(f"**x座標**: {format_fraction(vertex_x)}")
            st.write(f"**y座標**: {format_fraction(vertex_y)}")
            st.write(f"**頂点**: ({format_fraction(vertex_x)}, {format_fraction(vertex_y)})")
            
            # 二次関数の式
            st.markdown("### 📐 関数の情報")
            st.write(f"**元の式**: {format_quadratic(a, b, c)}")
            if st.session_state.show_solution:
                st.write(f"**平方完成**: {format_completed_square(correct_a, correct_p, correct_q)}")
            
            # 判別式と性質
            discriminant = float(b)**2 - 4*float(a)*float(c)
            st.write(f"**判別式 D**: {discriminant:.2f}")
            if discriminant > 0:
                st.write("**実根**: 2個")
            elif discriminant == 0:
                st.write("**実根**: 1個（重根）")
            else:
                st.write("**実根**: なし（虚根）")
                
            if float(a) > 0:
                st.write("**開く向き**: 上向き（最小値あり）")
            else:
                st.write("**開く向き**: 下向き（最大値あり）")
        
        # スコア表示
        if st.session_state.total_problems > 0:
            accuracy = st.session_state.score / st.session_state.total_problems * 100
            st.sidebar.markdown("### 📊 成績")
            st.sidebar.write(f"正解数: {st.session_state.score}/{st.session_state.total_problems}")
            st.sidebar.write(f"正解率: {accuracy:.1f}%")
            
            # 難易度別の詳細表示
            st.sidebar.markdown("### 🎯 難易度別ガイド")
            if difficulty == "初級":
                st.sidebar.info("💡 a=1の基本的な平方完成を練習します")
            elif difficulty == "中級":
                st.sidebar.info("💡 a≠1の場合の平方完成を練習します")
            else:
                st.sidebar.info("💡 分数係数を含む上級問題を練習します")
            
            if st.sidebar.button("成績をリセット"):
                st.session_state.score = 0
                st.session_state.total_problems = 0
    
    # 平方完成の説明
    with st.expander("📚 平方完成とは？"):
        st.markdown("""
        **平方完成(Completing the Square)**とは、二次関数を標準形から頂点形に変形する方法です。
        
        **変形の目的:**
        - ax² + bx + c → a(x + p)² + q
        - 頂点の座標(-p, q)が簡単に読み取れる
        - グラフの性質(最大値・最小値)が分かりやすい
        
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
        - 整数は普通に入力(例: 2, -5)
        """)

if __name__ == "__main__":
    main()