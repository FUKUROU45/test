import streamlit as st
import random
import re

def main():
    st.title("📚 四則演算学習アプリ")
    st.write("問題を解いて計算力を鍛えよう！")
    
    # サイドバーでレベルを選択
    st.sidebar.header("設定")
    level = st.sidebar.selectbox(
        "レベルを選択してください",
        ["初級", "中級", "上級"]
    )
    
    # セッション状態の初期化
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_problems' not in st.session_state:
        st.session_state.total_problems = 0
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    
    # レベル説明
    show_level_info(level)
    
    # スコア表示
    if st.session_state.total_problems > 0:
        accuracy = (st.session_state.score / st.session_state.total_problems) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("正解数", st.session_state.score)
        with col2:
            st.metric("問題数", st.session_state.total_problems)
        with col3:
            st.metric("正解率", f"{accuracy:.1f}%")
    
    # 問題生成・表示
    show_problem(level)

def show_level_info(level):
    """レベル情報を表示"""
    if level == "初級":
        st.info("🟢 **初級**: 一桁の数での四則演算（+, -, ×, ÷）")
    elif level == "中級":
        st.info("🟡 **中級**: 二桁の数での四則演算 + 累乗（^）")
    else:
        st.info("🔴 **上級**: 文字式の計算問題（x, yを含む式）")

def show_problem(level):
    """問題を生成・表示"""
    st.header("問題")
    
    # 新しい問題を生成
    if st.button("新しい問題", type="primary") or st.session_state.current_problem is None:
        st.session_state.current_problem, st.session_state.correct_answer = generate_problem(level)
        st.session_state.answered = False
        st.rerun()
    
    # 問題表示
    if st.session_state.current_problem:
        st.subheader("問題:")
        st.markdown(f"### {st.session_state.current_problem}")
        
        if level == "上級":
            # 上級では文字式なので答えも式の場合がある
            user_answer = st.text_input("答えを入力してください", key="answer_input", disabled=st.session_state.answered)
        else:
            # 初級・中級では数値回答
            user_answer = st.number_input("答えを入力してください", format="%.2f", key="answer_input", disabled=st.session_state.answered)
        
        if st.button("回答", disabled=st.session_state.answered):
            check_answer(user_answer, level)
            st.session_state.answered = True
            st.rerun()
        
        # 回答後のフィードバック表示
        if st.session_state.answered:
            show_feedback(user_answer, level)

def generate_problem(level):
    """レベルに応じた問題を生成"""
    if level == "初級":
        return generate_basic_problem()
    elif level == "中級":
        return generate_intermediate_problem()
    else:
        return generate_advanced_problem()

def generate_basic_problem():
    """初級問題生成（一桁）"""
    operations = ["+", "-", "×", "÷"]
    operation = random.choice(operations)
    
    if operation == "÷":
        # 割り切れる数を生成
        num2 = random.randint(1, 9)
        result = random.randint(1, 9)
        num1 = num2 * result
        problem = f"{num1} ÷ {num2}"
        answer = result
    else:
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        
        if operation == "+":
            problem = f"{num1} + {num2}"
            answer = num1 + num2
        elif operation == "-":
            # 負の数を避けるため大きい数から小さい数を引く
            if num1 < num2:
                num1, num2 = num2, num1
            problem = f"{num1} - {num2}"
            answer = num1 - num2
        elif operation == "×":
            problem = f"{num1} × {num2}"
            answer = num1 * num2
    
    return problem, answer

def generate_intermediate_problem():
    """中級問題生成（二桁 + 累乗）"""
    problem_types = ["basic", "power"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "power":
        base = random.randint(2, 5)
        exponent = random.randint(2, 3)
        problem = f"{base}^{exponent}"
        answer = base ** exponent
    else:
        operations = ["+", "-", "×", "÷"]
        operation = random.choice(operations)
        
        if operation == "÷":
            # 割り切れる数を生成
            num2 = random.randint(2, 12)
            result = random.randint(2, 15)
            num1 = num2 * result
            problem = f"{num1} ÷ {num2}"
            answer = result
        else:
            num1 = random.randint(10, 50)
            num2 = random.randint(2, 20)
            
            if operation == "+":
                problem = f"{num1} + {num2}"
                answer = num1 + num2
            elif operation == "-":
                if num1 < num2:
                    num1, num2 = num2, num1
                problem = f"{num1} - {num2}"
                answer = num1 - num2
            elif operation == "×":
                num1 = random.randint(2, 12)
                num2 = random.randint(2, 12)
                problem = f"{num1} × {num2}"
                answer = num1 * num2
    
    return problem, answer

def generate_advanced_problem():
    """上級問題生成（文字式）"""
    problem_types = ["linear", "quadratic", "substitution"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "linear":
        # 一次式の値を求める問題
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        x_val = random.randint(1, 5)
        problem = f"{a}x + {b} の値を求めよ（x = {x_val}）"
        answer = f"{a * x_val + b}"
    
    elif problem_type == "quadratic":
        # 二次式の値を求める問題
        a = random.randint(1, 3)
        b = random.randint(1, 4)
        c = random.randint(1, 5)
        x_val = random.randint(1, 3)
        problem = f"{a}x^2 + {b}x + {c} の値を求めよ（x = {x_val}）"
        answer = f"{a * x_val**2 + b * x_val + c}"
    
    else:  # substitution
        # 式の展開・計算
        patterns = [
            ("(x + a)(x + b)を展開せよ", "expand"),
            ("ax + b = c のときのxの値", "solve"),
            ("a*x + b*y の値を求めよ", "substitute")
        ]
        
        pattern_type = random.choice(patterns)
        
        if "expand" in pattern_type[1]:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            problem = f"(x + {a})(x + {b}) を展開せよ"
            answer = f"x^2 + {a+b}x + {a*b}"
        
        elif "solve" in pattern_type[1]:
            a = random.randint(2, 5)
            c = random.randint(5, 20)
            b = random.randint(1, 4)
            x_answer = (c - b) / a
            if x_answer == int(x_answer):
                x_answer = int(x_answer)
            problem = f"{a}x + {b} = {c} のときのxの値を求めよ"
            answer = f"{x_answer}"
        
        else:  # substitute
            a = random.randint(2, 4)
            b = random.randint(2, 4)
            x_val = random.randint(1, 5)
            y_val = random.randint(1, 5)
            problem = f"{a}x + {b}y の値を求めよ（x = {x_val}, y = {y_val}）"
            answer = f"{a * x_val + b * y_val}"
    
    return problem, answer

def check_answer(user_answer, level):
    """回答をチェック"""
    st.session_state.total_problems += 1
    
    if level == "上級":
        # 文字式の場合は文字列比較（空白除去して正規化）
        user_clean = str(user_answer).replace(" ", "").lower()
        correct_clean = str(st.session_state.correct_answer).replace(" ", "").lower()
        
        # 数値の場合は数値として比較
        try:
            user_num = float(user_answer)
            correct_num = float(st.session_state.correct_answer)
            is_correct = abs(user_num - correct_num) < 0.01
        except:
            # 文字式の場合
            is_correct = user_clean == correct_clean
    else:
        # 初級・中級は数値比較
        try:
            is_correct = abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01
        except:
            is_correct = False
    
    if is_correct:
        st.session_state.score += 1

def show_feedback(user_answer, level):
    """回答後のフィードバック表示"""
    if level == "上級":
        # 上級の判定
        user_clean = str(user_answer).replace(" ", "").lower()
        correct_clean = str(st.session_state.correct_answer).replace(" ", "").lower()
        
        try:
            user_num = float(user_answer)
            correct_num = float(st.session_state.correct_answer)
            is_correct = abs(user_num - correct_num) < 0.01
        except:
            is_correct = user_clean == correct_clean
    else:
        # 初級・中級の判定
        try:
            is_correct = abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01
        except:
            is_correct = False
    
    if is_correct:
        st.success(f"🎉 正解！ 答え: {st.session_state.correct_answer}")
    else:
        st.error(f"❌ 不正解　正解: {st.session_state.correct_answer}")
        
        # 上級の場合は解説を追加
        if level == "上級":
            show_explanation()

def show_explanation():
    """上級問題の解説表示"""
    problem = st.session_state.current_problem
    
    with st.expander("💡 解説"):
        if "展開" in problem:
            st.write("**展開の手順:**")
            st.write("1. (x + a)(x + b) = x² + ax + bx + ab")
            st.write("2. = x² + (a+b)x + ab")
            st.write("3. 係数を計算して整理する")
        
        elif "のときのx" in problem:
            st.write("**一次方程式の解き方:**")
            st.write("1. ax + b = c")
            st.write("2. ax = c - b")
            st.write("3. x = (c - b) / a")
        
        elif "値を求めよ" in problem and "x =" in problem:
            st.write("**代入計算の手順:**")
            st.write("1. 与えられた式にx, yの値を代入")
            st.write("2. 四則演算の順序に従って計算")
            st.write("3. 結果を求める")

def show_practice_mode():
    """練習モード選択"""
    st.sidebar.markdown("---")
    st.sidebar.header("練習設定")
    
    practice_type = st.sidebar.selectbox(
        "練習タイプ",
        ["ランダム", "加法のみ", "減法のみ", "乗法のみ", "除法のみ"]
    )
    
    if st.sidebar.button("練習リセット"):
        st.session_state.score = 0
        st.session_state.total_problems = 0
        st.session_state.current_problem = None
        st.session_state.answered = False
        st.rerun()
    
    return practice_type

def generate_problem_by_type(level, practice_type):
    """練習タイプに応じた問題生成"""
    if practice_type == "加法のみ":
        return generate_addition_problem(level)
    elif practice_type == "減法のみ":
        return generate_subtraction_problem(level)
    elif practice_type == "乗法のみ":
        return generate_multiplication_problem(level)
    elif practice_type == "除法のみ":
        return generate_division_problem(level)
    else:
        return generate_problem(level)

def generate_addition_problem(level):
    """加法問題生成"""
    if level == "初級":
        num1, num2 = random.randint(1, 9), random.randint(1, 9)
    elif level == "中級":
        num1, num2 = random.randint(10, 50), random.randint(10, 50)
    else:  # 上級
        a, b = random.randint(2, 5), random.randint(1, 10)
        x_val = random.randint(1, 5)
        problem = f"{a}x + {b} の値を求めよ（x = {x_val}）"
        answer = a * x_val + b
        return problem, answer
    
    problem = f"{num1} + {num2}"
    answer = num1 + num2
    return problem, answer

def generate_subtraction_problem(level):
    """減法問題生成"""
    if level == "初級":
        num1, num2 = random.randint(5, 9), random.randint(1, 4)
    elif level == "中級":
        num1, num2 = random.randint(20, 80), random.randint(10, 30)
    else:  # 上級
        a, b = random.randint(2, 8), random.randint(1, 5)
        x_val = random.randint(2, 6)
        problem = f"{a}x - {b} の値を求めよ（x = {x_val}）"
        answer = a * x_val - b
        return problem, answer
    
    problem = f"{num1} - {num2}"
    answer = num1 - num2
    return problem, answer

def generate_multiplication_problem(level):
    """乗法問題生成"""
    if level == "初級":
        num1, num2 = random.randint(2, 9), random.randint(2, 9)
    elif level == "中級":
        num1, num2 = random.randint(11, 25), random.randint(2, 12)
    else:  # 上級
        a, b = random.randint(2, 4), random.randint(2, 5)
        x_val = random.randint(1, 4)
        problem = f"{a}x × {b} の値を求めよ（x = {x_val}）"
        answer = a * x_val * b
        return problem, answer
    
    problem = f"{num1} × {num2}"
    answer = num1 * num2
    return problem, answer

def generate_division_problem(level):
    """除法問題生成"""
    if level == "初級":
        num2 = random.randint(2, 9)
        result = random.randint(2, 9)
        num1 = num2 * result
    elif level == "中級":
        num2 = random.randint(2, 15)
        result = random.randint(3, 20)
        num1 = num2 * result
    else:  # 上級
        a = random.randint(2, 6)
        divisor = random.randint(2, 4)
        x_val = random.randint(2, 5)
        # 割り切れるようにする
        numerator = a * divisor
        problem = f"{numerator}x ÷ {divisor} の値を求めよ（x = {x_val}）"
        answer = (numerator * x_val) // divisor
        return problem, answer
    
    problem = f"{num1} ÷ {num2}"
    answer = result
    return problem, answer

def generate_problem(level):
    """ランダム問題生成"""
    if level == "初級":
        return generate_basic_problem()
    elif level == "中級":
        return generate_intermediate_problem()
    else:
        return generate_advanced_problem()

def generate_intermediate_problem():
    """中級問題生成（二桁 + 累乗）"""
    problem_types = ["basic", "power"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "power":
        base = random.randint(2, 5)
        exponent = random.randint(2, 3)
        problem = f"{base}^{exponent}"
        answer = base ** exponent
    else:
        operations = ["+", "-", "×", "÷"]
        operation = random.choice(operations)
        
        if operation == "÷":
            num2 = random.randint(2, 12)
            result = random.randint(3, 20)
            num1 = num2 * result
            problem = f"{num1} ÷ {num2}"
            answer = result
        else:
            if operation == "×":
                num1 = random.randint(11, 25)
                num2 = random.randint(2, 12)
            else:
                num1 = random.randint(20, 80)
                num2 = random.randint(10, 30)
            
            if operation == "+":
                problem = f"{num1} + {num2}"
                answer = num1 + num2
            elif operation == "-":
                if num1 < num2:
                    num1, num2 = num2, num1
                problem = f"{num1} - {num2}"
                answer = num1 - num2
            elif operation == "×":
                problem = f"{num1} × {num2}"
                answer = num1 * num2
    
    return problem, answer

def generate_advanced_problem():
    """上級問題生成（文字式）"""
    problem_types = ["linear_sub", "quadratic_sub", "expand", "factorize"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "linear_sub":
        # 一次式の値を求める
        a = random.randint(2, 6)
        b = random.randint(1, 10)
        x_val = random.randint(1, 5)
        problem = f"{a}x + {b} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val + b)
    
    elif problem_type == "quadratic_sub":
        # 二次式の値を求める
        a = random.randint(1, 3)
        b = random.randint(1, 4)
        c = random.randint(1, 5)
        x_val = random.randint(1, 3)
        problem = f"{a}x^2 + {b}x + {c} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val**2 + b * x_val + c)
    
    elif problem_type == "expand":
        # 展開問題
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        problem = f"(x + {a})(x + {b}) を展開せよ"
        answer = f"x^2+{a+b}x+{a*b}"
    
    else:  # factorize - 簡単な因数分解
        # x^2 + bx + c = (x + p)(x + q) の形
        p = random.randint(1, 4)
        q = random.randint(1, 4)
        b = p + q
        c = p * q
        problem = f"x^2 + {b}x + {c} を因数分解せよ"
        answer = f"(x+{p})(x+{q})"
    
    return problem, answer

def check_answer(user_answer, level):
    """回答をチェック"""
    st.session_state.total_problems += 1
    
    if level == "上級":
        # 文字式の場合
        user_clean = str(user_answer).replace(" ", "").lower()
        correct_clean = str(st.session_state.correct_answer).replace(" ", "").lower()
        
        # 数値かどうかチェック
        try:
            user_num = float(user_answer)
            correct_num = float(st.session_state.correct_answer)
            is_correct = abs(user_num - correct_num) < 0.01
        except:
            # 文字式として比較
            is_correct = user_clean == correct_clean or check_equivalent_expressions(user_clean, correct_clean)
    else:
        # 初級・中級は数値比較
        try:
            is_correct = abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01
        except:
            is_correct = False
    
    if is_correct:
        st.session_state.score += 1

def check_equivalent_expressions(user_expr, correct_expr):
    """数学的に等価な式かチェック（簡易版）"""
    # 順序の違いを許容（例：x^2+3x+2 と 3x+x^2+2）
    try:
        # 基本的な項の順序違いをチェック
        user_terms = set(re.findall(r'[^+\-]+', user_expr))
        correct_terms = set(re.findall(r'[^+\-]+', correct_expr))
        return user_terms == correct_terms
    except:
        return False

def show_tips():
    """使い方のヒント"""
    with st.expander("💡 使い方のヒント"):
        st.write("""
        **レベル別問題**:
        - **初級**: 一桁の数での四則演算
        - **中級**: 二桁の数での四則演算 + 累乗（2^3など）
        - **上級**: 文字式の計算・展開・因数分解
        
        **上級の回答方法**:
        - 数値の場合: そのまま数字を入力
        - 式の場合: x^2+3x+2 のように入力
        - 因数分解: (x+1)(x+2) のように入力
        
        **累乗の書き方**: x^2（x の二乗）
        
        **練習のコツ**:
        - 間違えても解説を読んで理解しよう
        - 同じタイプの問題を繰り返し練習
        - 正解率を上げることを目標に
        """)

if __name__ == "__main__":
    # ヒント表示
    show_tips()
    
    # 練習モード選択
    practice_type = show_practice_mode()
    
    # メインアプリ実行
    main()
    
    # フッター
    st.markdown("---")
    st.markdown("*四則演算学習アプリ - がんばって練習しよう！*")