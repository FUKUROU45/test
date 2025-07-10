import streamlit as st
import random
import math

# ページ設定
st.set_page_config(
    page_title="平方完成問題解答アプリ",
    page_icon="🧮",
    layout="wide"
)

# アプリタイトル
st.title("🧮 平方完成問題解答アプリ")
st.markdown("**二次関数の平方完成を実際に解いてみましょう！**")

# セッション状態の初期化
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_problems' not in st.session_state:
    st.session_state.total_problems = 0

def generate_problem(difficulty="standard"):
    """問題を生成する関数"""
    if difficulty == "easy":
        a = random.choice([1, 2, -1])
        b = random.choice([-4, -2, 2, 4, 6])
        c = random.choice([-2, -1, 0, 1, 2, 3])
    elif difficulty == "hard":
        a = random.choice([1, 2, 3, -1, -2, -3])
        b = random.choice([-8, -6, -4, -2, 2, 4, 6, 8, 10])
        c = random.choice([-5, -3, -1, 1, 3, 5, 7, 9])
    else:  # standard
        a = random.choice([1, 2, -1, -2])
        b = random.choice([-6, -4, -2, 2, 4, 6])
        c = random.choice([-3, -1, 1, 3, 5])
    
    return {"a": a, "b": b, "c": c}

def format_expression(a, b, c):
    """二次式を文字列で表示"""
    expr = ""
    
    # x²の項
    if a == 1:
        expr = "x²"
    elif a == -1:
        expr = "-x²"
    else:
        expr = f"{a}x²"
    
    # xの項
    if b > 0:
        expr += f" + {b}x"
    elif b < 0:
        expr += f" - {abs(b)}x"
    
    # 定数項
    if c > 0:
        expr += f" + {c}"
    elif c < 0:
        expr += f" - {abs(c)}"
    
    return expr

def solve_completion(a, b, c):
    """平方完成の解を求める"""
    # ax² + bx + c = a(x + p)² + q
    p = b / (2 * a)
    q = c - (b * b) / (4 * a)
    
    # 分数で表現
    from fractions import Fraction
    p_frac = Fraction(b, 2 * a)
    q_frac = Fraction(c) - Fraction(b * b, 4 * a)
    
    return p, q, p_frac, q_frac

def format_answer(a, p_frac, q_frac):
    """答えを美しく表示"""
    # a(x + p)² + q の形
    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "-"
    else:
        a_str = f"{a}"
    
    # pの部分
    if p_frac > 0:
        p_str = f"x + {p_frac}"
    elif p_frac < 0:
        p_str = f"x - {abs(p_frac)}"
    else:
        p_str = "x"
    
    # qの部分
    if q_frac > 0:
        q_str = f" + {q_frac}"
    elif q_frac < 0:
        q_str = f" - {abs(q_frac)}"
    else:
        q_str = ""
    
    return f"{a_str}({p_str})²{q_str}"

# サイドバー
st.sidebar.header("🎯 問題設定")
difficulty = st.sidebar.selectbox(
    "難易度を選択",
    ["easy", "standard", "hard"],
    format_func=lambda x: {"easy": "簡単", "standard": "標準", "hard": "難しい"}[x]
)

st.sidebar.header("📊 成績")
if st.session_state.total_problems > 0:
    accuracy = (st.session_state.score / st.session_state.total_problems) * 100
    st.sidebar.metric("正答率", f"{accuracy:.1f}%")
    st.sidebar.metric("正解数", f"{st.session_state.score}/{st.session_state.total_problems}")

st.sidebar.header("📚 平方完成の手順")
st.sidebar.markdown("""
1. **係数を確認**: a, b, c を特定
2. **公式適用**: p = b/(2a), q = c - b²/(4a)
3. **答えを記述**: a(x + p)² + q
4. **検証**: 展開して元の式と比較
""")

# メインコンテンツ
col1, col2 = st.columns([3, 2])

with col1:
    st.header("📝 問題を解こう")
    
    # 新しい問題を生成
    if st.button("🎲 新しい問題", type="primary"):
        st.session_state.current_problem = generate_problem(difficulty)
        st.session_state.show_hint = False
        st.session_state.show_answer = False
        st.session_state.user_answer = ""
        st.rerun()
    
    # 問題を表示
    if st.session_state.current_problem:
        problem = st.session_state.current_problem
        a, b, c = problem["a"], problem["b"], problem["c"]
        
        st.subheader("問題")
        st.markdown(f"次の二次式を平方完成してください：")
        st.latex(f"y = {format_expression(a, b, c)}")
        
        # 解答入力エリア
        st.subheader("あなたの解答")
        st.markdown("**a(x + p)² + q** の形で答えてください")
        
        # 入力フォーム
        col_a, col_b = st.columns(2)
        
        with col_a:
            if a == 1:
                st.write("係数 a = 1 なので、(x + p)² + q の形です")
            else:
                st.write(f"係数 a = {a} なので、{a}(x + p)² + q の形です")
        
        with col_b:
            user_p = st.number_input("p の値", value=0.0, step=0.5, format="%.2f")
            user_q = st.number_input("q の値", value=0.0, step=0.5, format="%.2f")
        
        # 答えをチェック
        if st.button("✅ 答えをチェック"):
            p, q, p_frac, q_frac = solve_completion(a, b, c)
            st.session_state.total_problems += 1
            
            # 正解判定（小数点以下の誤差を考慮）
            if abs(user_p - p) < 0.01 and abs(user_q - q) < 0.01:
                st.success("🎉 正解です！おめでとうございます！")
                st.session_state.score += 1
                st.balloons()
            else:
                st.error("❌ 残念！正解ではありません。")
                st.write(f"あなたの答え: {format_answer(a, Fraction(user_p).limit_denominator(), Fraction(user_q).limit_denominator())}")
        
        # ヒント表示
        if st.button("💡 ヒントを見る"):
            st.session_state.show_hint = True
            st.rerun()
        
        if st.session_state.show_hint:
            st.info(f"**ヒント**: p = b/(2a) = {b}/(2×{a}) を計算してみてください")
        
        # 解答表示
        if st.button("📋 解答を見る"):
            st.session_state.show_answer = True
            st.rerun()
        
        if st.session_state.show_answer:
            p, q, p_frac, q_frac = solve_completion(a, b, c)
            
            st.subheader("📋 詳細な解答")
            
            # ステップ1
            st.markdown("**ステップ1: 係数の確認**")
            st.write(f"a = {a}, b = {b}, c = {c}")
            
            # ステップ2
            st.markdown("**ステップ2: 公式の適用**")
            st.write(f"p = b/(2a) = {b}/(2×{a}) = {p_frac}")
            st.write(f"q = c - b²/(4a) = {c} - {b}²/(4×{a}) = {c} - {b*b/(4*a)} = {q_frac}")
            
            # ステップ3
            st.markdown("**ステップ3: 最終答え**")
            answer = format_answer(a, p_frac, q_frac)
            st.latex(f"y = {answer}")
            st.success(f"**答え**: y = {answer}")
            
            # ステップ4
            st.markdown("**ステップ4: 検証**")
            # 展開して確認
            expanded_a = a
            expanded_b = 2 * a * p
            expanded_c = a * (p * p) + q
            
            st.write("答えを展開してみます：")
            st.write(f"展開結果: {format_expression(expanded_a, int(expanded_b), int(expanded_c))}")
            st.write(f"元の式: {format_expression(a, b, c)}")
            
            if abs(expanded_b - b) < 0.001 and abs(expanded_c - c) < 0.001:
                st.success("✅ 検証完了！正しく平方完成されています。")
            else:
                st.error("❌ 計算に誤りがあります。")

with col2:
    st.header("🎯 練習のコツ")
    
    if st.session_state.current_problem:
        problem = st.session_state.current_problem
        a, b, c = problem["a"], problem["b"], problem["c"]
        
        st.markdown("**現在の問題の係数:**")
        st.write(f"• a = {a}")
        st.write(f"• b = {b}")
        st.write(f"• c = {c}")
        
        st.markdown("**計算のポイント:**")
        st.write(f"• p = b/(2a) = {b}/(2×{a})")
        st.write(f"• q = c - b²/(4a)")
        st.write(f"• 分数の計算に注意！")
        
        # 公式を表示
        st.markdown("**平方完成の公式:**")
        st.latex(r"ax^2 + bx + c = a\left(x + \frac{b}{2a}\right)^2 + c - \frac{b^2}{4a}")
    
    else:
        st.markdown("**学習のステップ:**")
        st.write("1. 新しい問題を生成")
        st.write("2. 公式を使って計算")
        st.write("3. 答えを入力してチェック")
        st.write("4. 間違えたらヒントを見る")
        st.write("5. 解答で理解を深める")
        
        st.markdown("**平方完成とは？**")
        st.write("二次式 ax² + bx + c を")
        st.write("a(x + p)² + q の形に変形すること")
        st.write("これにより頂点の座標が")
        st.write("(-p, q) として求まります")

# リセットボタン
if st.button("🔄 成績をリセット"):
    st.session_state.score = 0
    st.session_state.total_problems = 0
    st.success("成績をリセットしました！")
    st.rerun()

# フッター
st.markdown("---")
st.markdown("**💪 継続して練習することで、平方完成をマスターできます！**")
st.markdown("*問題を解いて、数学の力を伸ばしましょう！*")