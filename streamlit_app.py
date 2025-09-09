import streamlit as st
import random
import re
import time
import json
from typing import Dict, Tuple, List, Any

def main():
    st.set_page_config(
        page_title="四則演算クイズアプリ",
        page_icon="📚",
        layout="wide"
    )
    
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
    defaults = {
        'quiz_active': False,
        'current_question': 0,
        'score': 0,
        'total_questions': 0,
        'current_problem': None,
        'correct_answer': None,
        'user_answers': [],
        'problems_history': [],
        'start_time': None,
        'answer_submitted': False,
        'quiz_history': [],
        'streak': 0,  # 連続正解数
        'hint_used': False  # ヒント使用フラグ
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def show_level_info(level):
    """レベル情報を表示"""
    level_info = {
        "初級": ("🟢", "一桁の数での四則演算（+, -, ×, ÷）", "primary"),
        "中級": ("🟡", "二桁の数での四則演算 + 累乗（^）", "secondary"),
        "上級": ("🔴", "文字式の計算・展開・因数分解（x, yを含む式）", "error")
    }
    
    icon, description, alert_type = level_info[level]
    if alert_type == "primary":
        st.info(f"{icon} **{level}**: {description}")
    elif alert_type == "secondary":
        st.warning(f"{icon} **{level}**: {description}")
    else:
        st.error(f"{icon} **{level}**: {description}")

def show_start_interface(level, quiz_length):
    """クイズ開始画面"""
    st.header("🚀 クイズを始めよう！")
    
    # 設定確認
    col1, col2 = st.columns(2)
    with col1:
        st.metric("選択レベル", level)
    with col2:
        st.metric("問題数", f"{quiz_length}問")
    
    # 予想時間を表示
    estimated_time = estimate_quiz_time(level, quiz_length)
    st.info(f"⏱️ 予想所要時間: 約{estimated_time}分")
    
    if st.button("クイズ開始", type="primary", use_container_width=True):
        start_quiz(quiz_length)
        st.rerun()
    
    # 過去の結果表示
    show_past_results()
    
    # 統計情報
    show_user_stats()

def estimate_quiz_time(level: str, quiz_length: int) -> int:
    """予想所要時間を計算"""
    time_per_question = {"初級": 0.5, "中級": 1, "上級": 2}
    return int(quiz_length * time_per_question[level])

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
    st.session_state.streak = 0
    st.session_state.hint_used = False

def show_quiz_interface(level, quiz_length):
    """クイズ進行画面"""
    # プログレスバー
    progress = st.session_state.current_question / st.session_state.total_questions
    st.progress(progress, f"問題 {st.session_state.current_question + 1} / {st.session_state.total_questions}")
    
    # 現在のスコア表示
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("正解数", st.session_state.score)
    with col2:
        st.metric("問題番号", f"{st.session_state.current_question + 1}")
    with col3:
        if st.session_state.current_question > 0:
            accuracy = (st.session_state.score / st.session_state.current_question) * 100
            st.metric("正解率", f"{accuracy:.1f}%")
    with col4:
        st.metric("連続正解", st.session_state.streak)
    
    # 問題生成（新しい問題の場合のみ）
    if not st.session_state.answer_submitted:
        if st.session_state.current_problem is None:
            st.session_state.current_problem, st.session_state.correct_answer = generate_problem(level)
            st.session_state.hint_used = False
    
    # 問題表示
    st.header("📝 問題")
    st.markdown(f"### {st.session_state.current_problem}")
    
    # ヒント機能（上級のみ）
    if level == "上級" and not st.session_state.answer_submitted:
        show_hint_section()
    
    # 回答入力
    placeholder = "例: x^2+3x+2 または 15" if level == "上級" else "例: 42"
    user_answer = st.text_input(
        "答えを入力してください:",
        key=f"answer_{st.session_state.current_question}",
        placeholder=placeholder,
        disabled=st.session_state.answer_submitted
    )
    
    # ボタンの配置
    col1, col2, col3 = st.columns([2, 2, 1])
    
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
    
    with col3:
        if st.button("終了", help="クイズを中断します"):
            if st.session_state.current_question > 0:
                finish_quiz()
            else:
                st.session_state.quiz_active = False
            st.rerun()
    
    # 回答後のフィードバック
    if st.session_state.answer_submitted:
        show_answer_feedback(user_answer, level)

def show_hint_section():
    """ヒント表示セクション"""
    if not st.session_state.hint_used:
        with st.expander("💡 ヒントを見る（正解率には影響しません）"):
            if st.button("ヒントを表示", type="secondary"):
                st.session_state.hint_used = True
                st.rerun()
    else:
        with st.expander("💡 ヒント", expanded=True):
            show_hint(st.session_state.current_problem)

def show_hint(problem: str):
    """問題に応じたヒントを表示"""
    if "展開" in problem:
        st.info("💡 (a+b)(c+d) = ac + ad + bc + bd の公式を使います")
    elif "因数分解" in problem:
        st.info("💡 x² + bx + c = (x + p)(x + q) の形で、p + q = b, p × q = c を満たすp, qを探します")
    elif "値を求めよ" in problem:
        st.info("💡 xの値を式に代入して計算します。累乗から先に計算しましょう")

def submit_answer(user_answer, level):
    """回答を提出"""
    st.session_state.answer_submitted = True
    
    # 回答の正誤判定
    is_correct = check_answer(user_answer, level)
    
    if is_correct:
        st.session_state.score += 1
        st.session_state.streak += 1
    else:
        st.session_state.streak = 0
    
    # 履歴に記録
    st.session_state.user_answers.append({
        'question': st.session_state.current_problem,
        'user_answer': user_answer,
        'correct_answer': st.session_state.correct_answer,
        'is_correct': is_correct,
        'hint_used': st.session_state.hint_used
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
    st.session_state.hint_used = False

def finish_quiz():
    """クイズを終了"""
    st.session_state.quiz_active = False
    
    # 結果を保存
    end_time = time.time()
    duration = end_time - st.session_state.start_time
    
    st.session_state.quiz_history.append({
        'score': st.session_state.score,
        'total': st.session_state.total_questions,
        'accuracy': (st.session_state.score / max(st.session_state.current_question, 1)) * 100,
        'duration': duration,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'max_streak': max([len([1 for answer in st.session_state.user_answers[:i] if answer['is_correct']]) 
                          for i in range(1, len(st.session_state.user_answers) + 1)], default=0)
    })
    
    # 状態をリセット
    st.session_state.current_question = 0
    st.session_state.current_problem = None
    st.session_state.correct_answer = None
    st.session_state.answer_submitted = False
    st.session_state.streak = 0
    
    # 結果画面表示
    show_quiz_results(duration)

def show_quiz_results(duration):
    """クイズ結果を表示"""
    st.header("🎉 クイズ完了！")
    
    questions_attempted = len(st.session_state.user_answers)
    accuracy = (st.session_state.score / questions_attempted) * 100 if questions_attempted > 0 else 0
    
    # 結果メトリクス
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("正解数", f"{st.session_state.score}/{questions_attempted}")
    with col2:
        st.metric("正解率", f"{accuracy:.1f}%")
    with col3:
        st.metric("所要時間", f"{int(duration//60)}分{int(duration%60)}秒")
    with col4:
        grade = get_grade(accuracy)
        st.metric("評価", grade)
    
    # 追加統計
    if st.session_state.user_answers:
        max_streak = calculate_max_streak(st.session_state.user_answers)
        hint_usage = sum(1 for answer in st.session_state.user_answers if answer.get('hint_used', False))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("最大連続正解", f"{max_streak}問")
        with col2:
            st.metric("ヒント使用", f"{hint_usage}回")
    
    # 結果に応じたメッセージとアドバイス
    show_result_message_and_advice(accuracy)
    
    # 詳細結果
    show_detailed_results()

def calculate_max_streak(user_answers: List[Dict]) -> int:
    """最大連続正解数を計算"""
    max_streak = 0
    current_streak = 0
    
    for answer in user_answers:
        if answer['is_correct']:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    return max_streak

def show_result_message_and_advice(accuracy: float):
    """結果メッセージとアドバイスを表示"""
    if accuracy >= 90:
        st.success("🌟 素晴らしい！完璧に近い成績です！")
        st.info("💡 次は上のレベルに挑戦してみましょう！")
    elif accuracy >= 80:
        st.success("👏 よくできました！とても良い成績です！")
        st.info("💡 安定して高得点が取れています。問題数を増やして挑戦してみませんか？")
    elif accuracy >= 70:
        st.info("😊 頑張りました！もう少しで上級者です！")
        st.info("💡 間違えた問題を復習すると、さらに上達できます！")
    elif accuracy >= 60:
        st.info("📖 まずまずです！練習を続けましょう！")
        st.info("💡 基礎をしっかり固めて、同じレベルで繰り返し練習することをお勧めします。")
    else:
        st.warning("💪 次回はもっと頑張りましょう！練習あるのみです！")
        st.info("💡 一つ下のレベルから始めて、基礎を固めることをお勧めします。")

def show_detailed_results():
    """詳細結果を表示"""
    with st.expander("📊 詳細結果を見る"):
        for i, answer_data in enumerate(st.session_state.user_answers, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                if answer_data['is_correct']:
                    st.write(f"✅ 問題{i}: {answer_data['question']} → {answer_data['user_answer']}")
                else:
                    st.write(f"❌ 問題{i}: {answer_data['question']}")
                    st.write(f"　　あなたの答え: {answer_data['user_answer']}")
                    st.write(f"　　正解: {answer_data['correct_answer']}")
            with col2:
                if answer_data.get('hint_used', False):
                    st.write("💡")

def get_grade(accuracy):
    """正解率に応じた評価を返す"""
    grade_thresholds = [
        (95, "S+"), (90, "S"), (85, "A+"), (80, "A"),
        (75, "B+"), (70, "B"), (65, "C+"), (60, "C")
    ]
    
    for threshold, grade in grade_thresholds:
        if accuracy >= threshold:
            return grade
    return "D"

def show_answer_feedback(user_answer, level):
    """回答後のフィードバック表示"""
    is_correct = st.session_state.user_answers[-1]['is_correct'] if st.session_state.user_answers else False
    
    if is_correct:
        encouragements = ["🎉 正解！", "✨ その通り！", "👏 素晴らしい！", "🌟 完璧！"]
        st.success(random.choice(encouragements))
        
        # 連続正解のお祝い
        if st.session_state.streak >= 3:
            st.balloons()
            st.success(f"🔥 {st.session_state.streak}問連続正解！調子がいいですね！")
    else:
        st.error("❌ 不正解")
        st.info(f"正解: {st.session_state.correct_answer}")
        
        # 上級の場合は解説を表示
        if level == "上級":
            show_explanation(st.session_state.current_problem)

def show_explanation(problem):
    """解説表示"""
    with st.expander("💡 解説", expanded=True):
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
    if st.session_state.quiz_history:
        with st.expander("📈 過去の成績（最新5回）"):
            for i, result in enumerate(reversed(st.session_state.quiz_history[-5:]), 1):
                accuracy = result['accuracy']
                grade = get_grade(accuracy)
                st.write(f"{i}. {result['timestamp']}: {result['score']}/{result['total']}問正解 "
                        f"({accuracy:.1f}% - {grade}) - {int(result['duration']//60)}分{int(result['duration']%60)}秒")

def show_user_stats():
    """ユーザー統計情報を表示"""
    if st.session_state.quiz_history:
        with st.expander("📊 あなたの統計"):
            total_quizzes = len(st.session_state.quiz_history)
            total_questions = sum(result['total'] for result in st.session_state.quiz_history)
            total_correct = sum(result['score'] for result in st.session_state.quiz_history)
            avg_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("総クイズ数", f"{total_quizzes}回")
            with col2:
                st.metric("総問題数", f"{total_questions}問")
            with col3:
                st.metric("平均正解率", f"{avg_accuracy:.1f}%")

def generate_problem(level):
    """レベルに応じた問題を生成"""
    generators = {
        "初級": generate_basic_problem,
        "中級": generate_intermediate_problem,
        "上級": generate_advanced_problem
    }
    return generators[level]()

def generate_basic_problem():
    """初級問題生成（一桁）"""
    operations = ["+", "-", "×", "÷"]
    operation = random.choice(operations)
    
    if operation == "÷":
        # 割り切れる数を生成
        num2 = random.randint(2, 9)
        result = random.randint(2, 9)
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
    problem_types = ["basic", "power", "mixed"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "power":
        base = random.randint(2, 6)
        exponent = random.randint(2, 3)
        problem = f"{base}^{exponent}"
        answer = base ** exponent
    elif problem_type == "mixed":
        # 四則演算と累乗の混合
        base = random.randint(2, 4)
        exponent = 2
        num = random.randint(5, 20)
        operation = random.choice(["+", "-"])
        
        if operation == "+":
            problem = f"{base}^{exponent} + {num}"
            answer = base ** exponent + num
        else:
            problem = f"{base}^{exponent} - {num}"
            answer = base ** exponent - num
    else:
        operations = ["+", "-", "×", "÷"]
        operation = random.choice(operations)
        
        if operation == "÷":
            num2 = random.randint(3, 15)
            result = random.randint(3, 25)
            num1 = num2 * result
            problem = f"{num1} ÷ {num2}"
            answer = result
        else:
            if operation == "×":
                num1 = random.randint(11, 25)
                num2 = random.randint(3, 15)
            else:
                num1 = random.randint(20, 99)
                num2 = random.randint(10, 40)
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
    problem_types = ["linear_sub", "quadratic_sub", "expand", "factorize", "simplify"]
    problem_type = random.choice(problem_types)
    
    if problem_type == "linear_sub":
        a = random.randint(2, 8)
        b = random.randint(-10, 10)
        x_val = random.randint(1, 6)
        sign = "+" if b >= 0 else "-"
        b_abs = abs(b)
        problem = f"{a}x {sign} {b_abs} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val + b)
    
    elif problem_type == "quadratic_sub":
        a = random.randint(1, 4)
        b = random.randint(1, 5)
        c = random.randint(1, 8)
        x_val = random.randint(1, 4)
        problem = f"{a}x^2 + {b}x + {c} の値を求めよ（x = {x_val}）"
        answer = str(a * x_val**2 + b * x_val + c)
    
    elif problem_type == "expand":
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        problem = f"(x + {a})(x + {b}) を展開せよ"
        answer = f"x^2+{a+b}x+{a*b}"
    
    elif problem_type == "factorize":
        p = random.randint(1, 5)
        q = random.randint(1, 5)
        b = p + q
        c = p * q
        problem = f"x^2 + {b}x + {c} を因数分解せよ"
        answer = f"(x+{p})(x+{q})"
    
    else:  # simplify
        a = random.randint(2, 5)
        b = random.randint(1, 4)
        c = random.randint(1, 3)
        problem = f"{a*c}x + {b*c} = {c}({a}x + {b}) を簡単にせよ"
        answer = f"{c}(x+{b//c if b%c==0 else f'{b}/{c}'})" if c > 1 else f"{a}x+{b}"
    
    return problem, answer

def check_answer(user_answer: str, level: str) -> bool:
    """回答をチェック"""
    if level == "上級":
        user_clean = normalize_expression(user_answer)
        correct_clean = normalize_expression(st.session_state.correct_answer)
        
        try:
            # 数値として評価可能な場合
            user_num = float(user_answer)
            correct_num = float(st.session_state.correct_answer)
            return abs(user_num - correct_num) < 0.01
        except:
            # 文字式の場合
            return user_clean == correct_clean or check_equivalent_expressions(user_clean, correct_clean)
    else:
        try:
            return abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01
        except:
            return False

def normalize_expression(expr: str) -> str:
    """式を正規化"""
    return expr.replace(" ", "").replace("*", "").lower()

def check_equivalent_expressions(user_expr: str, correct_expr: str) -> bool:
    """数学的に等価な式かチェック"""
    try:
        # 因数分解の順序違い: (x+a)(x+b) = (x+b)(x+a)
        factorization_pattern = r'\(x\+(\d+)\)\(x\+(\d+)\)'
        
        user_match = re.match(factorization_pattern, user_expr)
        correct_match = re.match(factorization_pattern, correct_expr)
        
        if user_match and correct_match:
            user_factors = sorted([int(user_match.group(1)), int(user_match.group(2))])
            correct_factors = sorted([int(correct_match.group(1)), int(correct_match.group(2))])
            return user_factors == correct_factors
        
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
        
        **新機能**:
        - 連続正解数の表示
        - ヒント機能（上級のみ）
        - 詳細な統計情報
        - 予想所要時間の表示
        """)

if __name__ == "__main__":
    show_tips()
    main()
    
    st.markdown("---")
    st.markdown("*四則演算クイズアプリ - 頑張って高得点を目指そう！*")