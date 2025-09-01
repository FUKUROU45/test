import streamlit as st
import random
import re
import time

def main():
    st.title("📚 四則演算クイズアプリ")
    st.write("問題を解いて計算力を鍛えよう！")
    
    # サイドバーで設定
    st.sidebar.header("クイズ設定")
    level = st.sidebar.selectbox(
        "レベルを選択してください",
        ["初級", "中級", "上級"]
    )
    
    quiz_length = st.sidebar.selectbox(
        "問題数を選択してください",
        [5, 10, 15, 20, 30]
    )
    
    # セッション状態の初期化
    init_session_state()
    
    # レベル説明
    show_level_info(level)
    
    # クイズの状態に応じて表示切り替え
    if st.session_state.quiz_active:
        show_quiz_interface(level, quiz_length)
    else:
        show_start_interface(level, quiz_length)

def init_session_state():
    """セッション状態の初期化"""
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'problems_history' not in st.session_state:
        st.session_state.problems_history = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False

def show_level_info(level):
    """レベル情報を表示"""
    if level == "初級":
        st.info("🟢 **初級**: 一桁の数での四則演算（+, -, ×, ÷）")
    elif level == "中級":
        st.info("🟡 **中級**: 二桁の数での四則演算 + 累乗（^）")
    else:
        st.info("🔴 **上級**: 文字式の計算・展開・因数分解（x, yを含む式）")

def show_start_interface(level, quiz_length):
    """クイズ開始画面"""
    st.header("🚀 クイズを始めよう！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("選択レベル", level)
    with col2:
        st.metric("問題数", f"{quiz_length}問")
    
    if st.button("クイズ開始", type="primary", use_container_width=True):
        start_quiz(quiz_length)
        st.rerun()
    
    # 過去の結果表示
    show_past_results()

def start_quiz(quiz_length):
    """クイズを開始"""
    st.session_state.quiz_active = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.total_questions = quiz_length
    st.session_state.user_answers = []
    st.session_state.problems_history = []
    st.session_state.start_time = time.time()
    st.session_state.answer_submitted = False

def show_quiz_interface(level, quiz_length):
    """クイズ進行画面"""
    # プログレスバー
    progress = st.session_state.current_question / st.session_state.total_questions
    st.progress(progress, f"問題 {st.session_state.current_question + 1} / {st.session_state.total_questions}")
    
    # 現在のスコア表示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("正解数", st.session_state.score)
    with col2:
        st.metric("問題番号", f"{st.session_state.current_question + 1}")
    with col3:
        if st.session_state.current_question > 0:
            accuracy = (st.session_state.score / st.session_state.current_question) * 100
            st.metric("正解率", f"{accuracy:.1f}%")
    
    # 問題生成（新しい問題の場合のみ）
    if not st.session_state.answer_submitted:
        if st.session_state.current_problem is None:
            st.session_state.current_problem, st.session_state.correct_answer = generate_problem(level)
    
    # 問題表示
    st.header("📝 問題")
    st.markdown(f"### {st.session_state.current_problem}")
    
    # 回答入力
    if level == "上級":
        user_answer = st.text_input(
            "答えを入力してください:",
            key=f"answer_{st.session_state.current_question}",
            placeholder="例: x^2+3x+2 または 15",
            disabled=st.session_state.answer_submitted
        )
    else:
        user_answer = st.text_input(
            "答えを入力してください:",
            key=f"answer_{st.session_state.current_question}",
            placeholder="例: 42",
            disabled=st.session_state.answer_submitted
        )
    
    # ボタンの配置
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("回答", type="primary", disabled=st.session_state.answer_submitted or not user_answer):
            submit_answer(user_answer, level)
            st.rerun()
    
    with col2:
        if st.session_state.answer_submitted:
            if st.session_state.current_question + 1 < st.session_state.total_questions:
                if st.button("次の問題", type="secondary"):
                    next_question()
                    st.rerun()
            else:
                if st.button("結果を見る", type="secondary"):
                    finish_quiz()
                    st.rerun()
    
    # 回答後のフィードバック
    if st.session_state.answer_submitted:
        show_answer_feedback(user_answer, level)

def submit_answer(user_answer, level):
    """回答を提出"""
    st.session_state.answer_submitted = True
    
    # 回答の正誤判定
    is_correct = check_answer(user_answer, level)
    
    if is_correct:
        st.session_state.score += 1
    
    # 履歴に記録
    st.session_state.user_answers.append({
        'question': st.session_state.current_problem,
        'user_answer': user_answer,
        'correct_answer': st.session_state.correct_answer,
        'is_correct': is_correct
    })
    st.session_state.problems_history.append({
        'problem': st.session_state.current_problem,
        'correct_answer': st.session_state.correct_answer
    })

def next_question():
    """次の問題に進む"""
    st.session_state.current_question += 1
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.answer_submitted = False

def finish_quiz():
    """クイズを終了"""
    st.session_state.quiz_active = False
    st.session_state.current_question = 0
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.answer_submitted = False
    
    # 結果を保存（簡単な履歴として）
    end_time = time.time()
    duration = end_time - st.session_state.start_time
    
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []
    
    st.session_state.quiz_history.append({
        'score': st.session_state.score,
        'total': st.session_state.total_questions,
        'accuracy': (st.session_state.score / st.session_state.total_questions) * 100,
        'duration': duration,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # 結果画面表示
    show_quiz_results(duration)

def show_quiz_results(duration):
    """クイズ結果を表示"""
    st.header("🎉 クイズ完了！")
    
    accuracy = (st.session_state.score / st.session_state.total_questions) * 100
    
    # 結果メトリクス
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("正解数", f"{st.session_state.score}/{st.session_state.total_questions}")
    with col2:
        st.metric("正解率", f"{accuracy:.1f}%")
    with col3:
        st.metric("所要時間", f"{int(duration//60)}分{int(duration%60)}秒")
    with col4:
        grade = get_grade(accuracy)
        st.metric("評価", grade)
    
    # 結果に応じたメッセージ
    if accuracy >= 90:
        st.success("🌟 素晴らしい！完璧に近い成績です！")
    elif accuracy >= 80:
        st.success("👏 よくできました！とても良い成績です！")
    elif accuracy >= 70:
        st.info("😊 頑張りました！もう少しで上級者です！")
    elif accuracy >= 60:
        st.info("📖 まずまずです！練習を続けましょう！")
    else:
        st.warning("💪 次回はもっと頑張りましょう！練習あるのみです！")
    
    # 詳細結果
    with st.expander("📊 詳細結果を見る"):
        for i, answer_data in enumerate(st.session_state.user_answers, 1):
            if answer_data['is_correct']:
                st.write(f"✅ 問題{i}: {answer_data['question']} → {answer_data['user_answer']}")
            else:
                st.write(f"❌ 問題{i}: {answer_data['question']}")
                st.write(f"　　あなたの答え: {answer_data['user_answer']}")
                st.write(f"　　正解: {answer_data['correct_answer']}")

def get_grade(accuracy):
    """正解率に応じた評価を返す"""
    if accuracy >= 95:
        return "S+"
    elif accuracy >= 90:
        return "S"
    elif accuracy >= 85:
        return "A+"
    elif accuracy >= 80:
        return "A"
    elif accuracy >= 75:
        return "B+"
    elif accuracy >= 70:
        return "B"
    elif accuracy >= 65:
        return "C+"
    elif accuracy >= 60:
        return "C"
    else:
        return "D"

def show_answer_feedback(user_answer, level):
    """回答後のフィードバック表示"""
    is_correct = st.session_state.user_answers[-1]['is_correct'] if st.session_state.user_answers else False
    
    if is_correct:
        st.success(f"🎉 正解！")
    else:
        st.error(f"❌ 不正解")
        st.info(f"正解: {st.session_state.correct_answer}")
        
        # 上級の場合は解説を表示
        if level == "上級":
            show_explanation(st.session_state.current_problem)

def show_explanation(problem):
    """解説表示"""
    with st.expander("💡 解説"):
        if "展開" in problem:
            st.write("**展開の手順:**")
            st.write("1. (x + a)(x + b) = x² + ax + bx + ab")
            st.write("2. = x² + (a+b)x + ab")
            st.write("3. 係数を計算して整理する")
        
        elif "因数分解" in problem:
            st.write("**因数分解の手順:**")
            st.write("1. x² + bx + c の形を (x + p)(x + q) に変形")
            st.write("2. p + q = b, p × q = c となる p, q を見つける")
            st.write("3. (x + p)(x + q) の形で答える")
        
        elif "値を求めよ" in problem:
            st.write("**代入計算の手順:**")
            st.write("1. 与えられた式にx, yの値を代入")
            st.write("2. 累乗から計算（x²など）")
            st.write("3. 掛け算、足し算の順で計算")

def show_past_results():
    """過去の結果を表示"""
    if 'quiz_history' in st.session_state and st.session_state.quiz_history:
        with st.expander("📈 過去の成績"):
            st.write("最近のクイズ結果:")
            for i, result in enumerate(reversed(st.session_state.quiz_history[-5:]), 1):
                st.write(f"{i}. {result['timestamp']}: {result['score']}/{result['total']}問正解 "
                        f"({result['accuracy']:.1f}%) - {result['duration']//60:.0f}分{result['duration']%60:.0f}秒")

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
            if num1 < num2:
                num1, num2 = num2, num1
            problem = f"{num1} - {num2}"
            answer = num1 - num2
        elif operation == "×":
            problem = f"{num1} × {num2}"
            answer = num1 * num2
    
    return problem, str(answer)

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
                if operation == "-" and num1 < num2:
                    num1, num2 = num2, num1
            
            if operation == "+":
                problem = f"{num1} + {num2}"
                answer = num1 + num2
            elif operation == "-":
                problem = f"{num1} - {num2}"
                answer = num1 - num2
            elif operation == "×":
                problem = f"{num1} × {num2}"
                answer = num1 * num2
    
    return problem, str(answer)

def generate_advanced_problem():
    """上級問題生成（文字式）"""
    problem_types = ["linear_sub", "quadratic_sub", "expand", "factorize"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "linear_sub":
        a = random.randint(2, 6)
        b = random.randint(1, 10)
        x_val = random.randint(1, 5)
        problem = f"{a}x + {b} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val + b)
    
    elif problem_type == "quadratic_sub":
        a = random.randint(1, 3)
        b = random.randint(1, 4)
        c = random.randint(1, 5)
        x_val = random.randint(1, 3)
        problem = f"{a}x^2 + {b}x + {c} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val**2 + b * x_val + c)
    
    elif problem_type == "expand":
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        problem = f"(x + {a})(x + {b}) を展開せよ"
        answer = f"x^2+{a+b}x+{a*b}"
    
    else:  # factorize
        p = random.randint(1, 4)
        q = random.randint(1, 4)
        b = p + q
        c = p * q
        problem = f"x^2 + {b}x + {c} を因数分解せよ"
        answer = f"(x+{p})(x+{q})"
    
    return problem, answer

def check_answer(user_answer, level):
    """回答をチェック"""
    if level == "上級":
        user_clean = str(user_answer).replace(" ", "").lower()
        correct_clean = str(st.session_state.correct_answer).replace(" ", "").lower()
        
        try:
            user_num = float(user_answer)
            correct_num = float(st.session_state.correct_answer)
            return abs(user_num - correct_num) < 0.01
        except:
            return user_clean == correct_clean or check_equivalent_expressions(user_clean, correct_clean)
    else:
        try:
            return abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01
        except:
            return False

def check_equivalent_expressions(user_expr, correct_expr):
    """数学的に等価な式かチェック（簡易版）"""
    try:
        # 基本的なパターンマッチング
        patterns = [
            (r'\(x\+(\d+)\)\(x\+(\d+)\)', r'(x+\2)(x+\1)'),  # 順序の違い
        ]
        
        for pattern, replacement in patterns:
            if re.match(pattern, user_expr) and re.match(pattern.replace(r'\1', r'\2').replace(r'\2', r'\1'), correct_expr):
                return True
        
        return False
    except:
        return False

def show_tips():
    """使い方のヒント"""
    with st.expander("💡 使い方のヒント"):
        st.write("""
        **クイズの流れ**:
        1. レベルと問題数を選択
        2. 「クイズ開始」でスタート
        3. 問題に答えを入力して「回答」
        4. 結果を確認して次の問題へ
        5. 全問題終了後に総合結果を表示
        
        **レベル別問題**:
        - **初級**: 一桁の四則演算
        - **中級**: 二桁の四則演算 + 累乗
        - **上級**: 文字式の計算・展開・因数分解
        
        **上級の回答例**:
        - 数値: 15
        - 展開: x^2+5x+6
        - 因数分解: (x+2)(x+3)
        
        **評価**:
        - S+: 95%以上　- S: 90%以上　- A: 80%以上
        - B: 70%以上　- C: 60%以上　- D: 60%未満
        """)

if __name__ == "__main__":
    show_tips()
    main()
    
    st.markdown("---")
    st.markdown("*四則演算クイズアプリ - 頑張って高得点を目指そう！*")