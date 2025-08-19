import streamlit as st
import random
import math
import time
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
        h = -b / 2
        k = c - (b**2) / 4
        return 1, h, k
    else:
        h = -b / (2 * a)
        k = c - (b**2) / (4 * a)
        return a, h, k

def format_completion_answer(a, h, k):
    """平方完成の答えを文字列で表示"""
    h_frac = Fraction(h).limit_denominator()
    k_frac = Fraction(k).limit_denominator()
    
    a_str = "" if a == 1 else f"{a}"
    
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

def create_simple_graph_data(a, b, c):
    """グラフデータを作成（Streamlitの標準チャート用）"""
    import math
    
    # x値の範囲を決定
    vertex_x = -b / (2 * a)
    x_min = vertex_x - 5
    x_max = vertex_x + 5
    
    # データポイント生成
    x_values = []
    y_values = []
    
    for i in range(50):
        x = x_min + (x_max - x_min) * i / 49
        y = a * x**2 + b * x + c
        x_values.append(x)
        y_values.append(y)
    
    return {
        'x': x_values,
        'y': y_values,
        'vertex_x': vertex_x,
        'vertex_y': a * vertex_x**2 + b * vertex_x + c
    }

def explain_solution_detailed(a, b, c):
    """詳しい解説を生成（改良版）"""
    explanation = "## 🔍 ステップバイステップ解説\n\n"
    
    # 元の式
    original = format_quadratic(a, b, c)
    explanation += f"### 📝 元の式\n**{original}**\n\n"
    
    if a != 1:
        explanation += "### 📌 上級レベルの解法（a ≠ 1の場合）\n\n"
        
        # ステップ1: aでくくる
        explanation += f"**Step 1️⃣: 最高次の係数 `{a}` でくくり出す**\n\n"
        explanation += f"```\n{original}\n= {a}(x² + {Fraction(b, a)}x) + {c}\n```\n\n"
        explanation += f"💡 **ポイント**: `{a}x²` と `{b}x` から `{a}` をくくり出すと、括弧の中は `x²` と `{Fraction(b, a)}x` になります\n\n"
        
        # ステップ2: 平方完成の準備
        half_coeff = Fraction(b, 2*a)
        explanation += f"**Step 2️⃣: 平方完成の準備**\n\n"
        explanation += f"```\nx の係数: {Fraction(b, a)}\nその半分: {Fraction(b, a)} ÷ 2 = {half_coeff}\n```\n\n"
        explanation += f"💡 **覚え方**: 平方完成では「xの係数の半分」を使います！\n\n"
        
        # ステップ3: 平方完成
        explanation += f"**Step 3️⃣: 平方完成を実行**\n\n"
        half_squared = Fraction(b**2, 4*a**2)
        explanation += f"```\n{a}(x² + {Fraction(b, a)}x)\n= {a}(x² + {Fraction(b, a)}x + {half_squared} - {half_squared})\n= {a}((x + {half_coeff})² - {half_squared})\n= {a}(x + {half_coeff})² - {Fraction(b**2, 4*a)}\n```\n\n"
        
        # ステップ4: 定数項の整理
        explanation += f"**Step 4️⃣: 定数項をまとめる**\n\n"
        k_final = Fraction(4*a*c - b**2, 4*a)
        explanation += f"```\n= {a}(x + {half_coeff})² - {Fraction(b**2, 4*a)} + {c}\n= {a}(x + {half_coeff})² + {k_final}\n```\n\n"
        
    else:
        explanation += "### 📌 初級・中級レベルの解法（a = 1の場合）\n\n"
        
        # ステップ1: xの係数の半分
        half_coeff = Fraction(b, 2)
        explanation += f"**Step 1️⃣: xの係数の半分を求める**\n\n"
        explanation += f"```\nx の係数: {b}\nその半分: {b} ÷ 2 = {half_coeff}\n```\n\n"
        explanation += f"💡 **重要**: この値 `{half_coeff}` が平方完成のカギです！\n\n"
        
        # ステップ2: 平方完成
        half_squared = Fraction(b**2, 4)
        explanation += f"**Step 2️⃣: 平方完成の魔法 ✨**\n\n"
        explanation += f"```\n{original}\n= x² + {b}x + {half_squared} - {half_squared} + {c}\n= (x + {half_coeff})² - {half_squared} + {c}\n```\n\n"
        explanation += f"💡 **なぜこうなる？**: `(x + {half_coeff})²` を展開すると `x² + {b}x + {half_squared}` になるからです！\n\n"
        
        # ステップ3: 定数項の計算
        k_final = Fraction(4*c - b**2, 4)
        explanation += f"**Step 3️⃣: 定数項の計算**\n\n"
        explanation += f"```\n= (x + {half_coeff})² + (-{half_squared} + {c})\n= (x + {half_coeff})² + {k_final}\n```\n\n"
    
    # 最終答え
    a_ans, h_ans, k_ans = calculate_completion(a, b, c)
    final_answer = format_completion_answer(a_ans, h_ans, k_ans)
    
    explanation += f"### 🎯 **最終答え**\n"
    explanation += f"```\n{final_answer}\n```\n\n"
    
    # 頂点の説明を追加
    explanation += f"### 📍 頂点について\n\n"
    explanation += f"この二次関数の頂点は `({Fraction(h_ans).limit_denominator()}, {Fraction(k_ans).limit_denominator()})` です。\n\n"
    if a_ans > 0:
        explanation += f"係数 a = {a_ans} > 0 なので、放物線は**下に凸**で、頂点が**最小値**になります。\n\n"
    else:
        explanation += f"係数 a = {a_ans} < 0 なので、放物線は**上に凸**で、頂点が**最大値**になります。\n\n"
    
    # 理解のポイント
    explanation += f"### 💭 理解のポイント\n\n"
    explanation += f"1. **「xの係数の半分」** が平方完成の基本です\n"
    explanation += f"2. **「足して引く」** テクニックで完全平方式を作ります\n"
    explanation += f"3. **定数項の計算** を慎重に行いましょう\n"
    if a != 1:
        explanation += f"4. **係数のくくり出し** を最初に忘れずに！\n"
    
    return explanation

def get_achievement_badge(accuracy, time_finished, level):
    """成績に応じてバッジを返す"""
    badges = []
    
    # 正答率バッジ
    if accuracy >= 95:
        badges.append("🏆 パーフェクトマスター")
    elif accuracy >= 85:
        badges.append("🥇 ゴールドメダル")
    elif accuracy >= 70:
        badges.append("🥈 シルバーメダル")
    elif accuracy >= 50:
        badges.append("🥉 ブロンズメダル")
    
    # スピードバッジ
    if time_finished and time_finished < 60:
        badges.append("⚡ スピードマスター")
    elif time_finished and time_finished < 120:
        badges.append("🚀 高速解答")
    
    # レベル別バッジ
    if level == "上級" and accuracy >= 80:
        badges.append("👑 上級マスター")
    elif level == "中級" and accuracy >= 85:
        badges.append("🎖️ 中級エキスパート")
    elif level == "初級" and accuracy >= 90:
        badges.append("🌟 初級チャンピオン")
    
    return badges

# Streamlit アプリのメイン部分
st.set_page_config(
    page_title="平方完成チャレンジ",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ 平方完成 チャレンジ")
st.markdown("**制限時間内に平方完成をマスターしよう！**")

# セッション状態の初期化
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'time_up' not in st.session_state:
    st.session_state.time_up = False
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'problems' not in st.session_state:
    st.session_state.problems = []
if 'wrong_problems' not in st.session_state:
    st.session_state.wrong_problems = []
if 'show_graph' not in st.session_state:
    st.session_state.show_graph = False

# 設定パネル
if not st.session_state.quiz_started:
    st.header("🎮 クイズ設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 前回選択したレベルがあれば初期値に設定
        default_level_index = 0
        if 'selected_level' in st.session_state:
            level_options = ["初級", "中級", "上級"]
            if st.session_state.selected_level in level_options:
                default_level_index = level_options.index(st.session_state.selected_level)
        
        level = st.selectbox(
            "難易度を選択：",
            ["初級", "中級", "上級"],
            index=default_level_index,
            help="初級：x² + bx、中級：x² + bx + c、上級：ax² + bx + c"
        )
        
        problem_count = st.selectbox(
            "問題数を選択：",
            [5, 10, 15, 20],
            index=1
        )
        
        show_graph = st.checkbox(
            "グラフ表示機能を有効にする",
            value=False,
            help="問題のグラフを表示してより視覚的に学習できます（簡易版）"
        )
    
    with col2:
        time_limit = st.selectbox(
            "制限時間を選択：",
            [60, 120, 180, 300, 600],  # 10分まで追加
            format_func=lambda x: f"{x//60}分" if x >= 60 else f"{x}秒",
            index=1  # デフォルト2分
        )
        
        st.write("**レベル説明：**")
        if level == "初級":
            st.info("📚 x² + bx の形（基礎）\n平方完成の基本を学びます")
        elif level == "中級":
            st.info("📖 x² + bx + c の形（標準）\n定数項がある標準的な問題")
        else:
            st.info("📘 ax² + bx + c の形（応用）\n係数のくくり出しが必要な応用問題")
    
    # 練習モードの説明
    st.markdown("---")
    st.subheader("🎯 モード説明")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏃‍♂️ タイムアタックモード**
        - 制限時間内に多くの問題を解く
        - スピードと正確性を競う
        - リアルタイムで進捗確認
        """)
    
    with col2:
        st.markdown("""
        **📊 学習サポート機能**
        - 詳細なステップ解説
        - グラフによる視覚的理解
        - 間違った問題の復習機能
        """)
    
    if st.button("🚀 クイズスタート！", type="primary", use_container_width=True):
        # 問題を事前生成
        st.session_state.problems = []
        for _ in range(problem_count):
            a, b, c = generate_problem(level)
            st.session_state.problems.append((a, b, c))
        
        st.session_state.quiz_started = True
        st.session_state.start_time = time.time()
        st.session_state.current_problem = 0
        st.session_state.correct_answers = 0
        st.session_state.time_up = False
        st.session_state.quiz_finished = False
        st.session_state.wrong_problems = []
        st.session_state.level = level
        st.session_state.problem_count = problem_count
        st.session_state.time_limit = time_limit
        st.session_state.show_graph = show_graph
        st.rerun()

# クイズ実行中
elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    # 残り時間計算
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.time_limit - elapsed_time)
    
    if remaining_time <= 0:
        st.session_state.time_up = True
        st.session_state.quiz_finished = True
        st.rerun()
    
    # 上部に進捗とタイマー表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        progress = st.session_state.current_problem / st.session_state.problem_count
        st.metric("進捗", f"{st.session_state.current_problem}/{st.session_state.problem_count}")
        st.progress(progress)
    
    with col2:
        st.metric("正解数", st.session_state.correct_answers)
    
    with col3:
        accuracy = (st.session_state.correct_answers / max(1, st.session_state.current_problem)) * 100
        st.metric("正答率", f"{accuracy:.1f}%")
    
    with col4:
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        time_color = "🔴" if remaining_time < 30 else "🟡" if remaining_time < 60 else "🟢"
        st.metric("残り時間", f"{time_color} {minutes:02d}:{seconds:02d}")
    
    # 現在の問題
    if st.session_state.current_problem < len(st.session_state.problems):
        st.header(f"問題 {st.session_state.current_problem + 1}")
        
        a, b, c = st.session_state.problems[st.session_state.current_problem]
        problem_text = format_quadratic(a, b, c)
        
        st.write("次の二次式を平方完成してください：")
        st.markdown(f"### 📝 {problem_text}")
        
        # グラフ表示（有効な場合）
        if st.session_state.show_graph:
            with st.expander("📊 グラフを見る", expanded=False):
                graph_data = create_simple_graph_data(a, b, c)
                
                # Streamlit標準のline_chartを使用
                import pandas as pd
                df = pd.DataFrame({'y': graph_data['y']}, index=graph_data['x'])
                st.line_chart(df)
                
                # 頂点情報を表示
                st.info(f"📍 頂点: ({graph_data['vertex_x']:.2f}, {graph_data['vertex_y']:.2f})")
                
                convexity = "下に凸（最小値）" if a > 0 else "上に凸（最大値）"
                st.info(f"📈 形状: {convexity}")
        
        # 初級レベルのみ「やり方」を表示
        if st.session_state.level == "初級":
            with st.expander("💡 やり方（初級向けヒント）", expanded=False):
                st.markdown("""
                ### 🔍 平方完成の基本手順（初級：x² + bx の形）
                
                **Step 1️⃣: xの係数を確認**
                - x² + bx の「b」を見つける
                
                **Step 2️⃣: xの係数の半分を計算**
                - b ÷ 2 = ? を計算
                
                **Step 3️⃣: その値を2乗して足し引き**
                - x² + bx + (半分)² - (半分)²
                
                **Step 4️⃣: 完全平方式を作る**
                - (x + 半分)² - (半分)²
                
                **例：x² + 6x の場合**
                1. xの係数：6
                2. その半分：6 ÷ 2 = 3
                3. 足して引く：x² + 6x + 9 - 9
                4. 完成：(x + 3)² - 9
                
                💡 **覚え方**: 「半分の2乗を足して引く」！
                """)
        
        # 正解計算
        correct_a, correct_h, correct_k = calculate_completion(a, b, c)
        correct_answer = format_completion_answer(correct_a, correct_h, correct_k)
        
        # 回答入力
        user_answer = st.text_input(
            "答えを入力：",
            key=f"answer_{st.session_state.current_problem}",
            help="例: (x - 2)² + 3, 2(x + 1/2)² - 1",
            placeholder="ここに答えを入力してください..."
        )
        
        col1, col2, col3 = st.columns(3)
        
        # 回答状態をチェック
        answered_key = f"answered_{st.session_state.current_problem}"
        
        with col1:
            if answered_key not in st.session_state:
                if st.button("✅ 回答", type="primary"):
                    if user_answer.strip():
                        # 答え合わせ
                        user_clean = user_answer.replace(" ", "").replace("²", "^2")
                        correct_clean = correct_answer.replace(" ", "").replace("²", "^2")
                        
                        # 正誤判定を保存
                        if user_clean.lower() == correct_clean.lower():
                            st.session_state[f"result_{st.session_state.current_problem}"] = "correct"
                            st.session_state.correct_answers += 1
                        else:
                            st.session_state[f"result_{st.session_state.current_problem}"] = "incorrect"
                            st.session_state.wrong_problems.append((a, b, c, user_answer))
                        
                        # 回答済みフラグを設定
                        st.session_state[answered_key] = True
                        st.rerun()
                    else:
                        st.warning("答えを入力してください")
            else:
                # 既に回答済みの場合は結果を表示
                result_key = f"result_{st.session_state.current_problem}"
                if result_key in st.session_state:
                    if st.session_state[result_key] == "correct":
                        st.success("🎉 正解！")
                    else:
                        st.error(f"❌ 不正解")
                        st.info(f"正解: **{correct_answer}**")
        
        with col2:
            # 解説表示ボタン
            explanation_key = f"show_explanation_{st.session_state.current_problem}"
            if explanation_key not in st.session_state:
                st.session_state[explanation_key] = False
            
            if st.button("📖 解説を見る", type="secondary"):
                st.session_state[explanation_key] = not st.session_state[explanation_key]
                st.rerun()
        
        with col3:
            # 回答後は「次の問題へ」ボタンを表示
            if answered_key in st.session_state and st.session_state[answered_key]:
                if st.button("➡️ 次の問題へ", type="primary"):
                    # 次の問題へ
                    st.session_state.current_problem += 1
                    
                    if st.session_state.current_problem >= st.session_state.problem_count:
                        st.session_state.quiz_finished = True
                    
                    st.rerun()
            else:
                if st.button("⏭️ スキップ"):
                    st.session_state.wrong_problems.append((a, b, c, "スキップ"))
                    st.session_state.current_problem += 1
                    
                    if st.session_state.current_problem >= st.session_state.problem_count:
                        st.session_state.quiz_finished = True
                    
                    st.rerun()
        
        # 解説表示
        explanation_key = f"show_explanation_{st.session_state.current_problem}"
        if explanation_key in st.session_state and st.session_state[explanation_key]:
            st.markdown("---")
            with st.container():
                explanation = explain_solution_detailed(a, b, c)
                st.markdown(explanation)
            st.markdown("---")

# 結果表示
elif st.session_state.quiz_finished:
    st.header("🎊 クイズ終了！")
    
    # 結果サマリー
    accuracy = (st.session_state.correct_answers / st.session_state.problem_count) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("正解数", f"{st.session_state.correct_answers}/{st.session_state.problem_count}")
    
    with col2:
        st.metric("正答率", f"{accuracy:.1f}%")
    
    with col3:
        if st.session_state.time_up:
            st.metric("結果", "⏰ 時間切れ")
            finish_time = None
        else:
            elapsed = time.time() - st.session_state.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            st.metric("完了時間", f"{minutes:02d}:{seconds:02d}")
            finish_time = elapsed
    
    with col4:
        st.metric("レベル", st.session_state.level)
    
    # バッジ表示
    badges = get_achievement_badge(accuracy, finish_time, st.session_state.level)
    if badges:
        st.subheader("🏅 獲得バッジ")
        badge_cols = st.columns(len(badges))
        for i, badge in enumerate(badges):
            with badge_cols[i]:
                st.info(badge)
    
    # 評価コメント
    if accuracy >= 90:
        st.success("🏆 素晴らしい！平方完成を完全にマスターしていますね！")
    elif accuracy >= 70:
        st.info("👍 良い調子です！もう少し練習すれば完璧です！")
    elif accuracy >= 50:
        st.warning("📚 基礎は理解できています。解説を読んで復習しましょう！")
    else:
        st.error("💪 諦めずに！解説をしっかり読んで再挑戦しましょう！")
    
    # 間違った問題の解説
    if st.session_state.wrong_problems:
        st.header("📖 復習：間違った問題の解説")
        
        for i, (a, b, c, user_ans) in enumerate(st.session_state.wrong_problems):
            with st.expander(f"問題 {i+1}：{format_quadratic(a, b, c)}", expanded=False):
                st.write(f"**あなたの答え:** {user_ans}")
                
                correct_a, correct_h, correct_k = calculate_completion(a, b, c)
                correct_answer = format_completion_answer(correct_a, correct_h, correct_k)
                st.write(f"**正解:** {correct_answer}")
                
                # 詳細解説
                explanation