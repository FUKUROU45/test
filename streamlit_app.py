import streamlit as st
import random
import time
import math
import numpy as np

# ページ設定
st.set_page_config(page_title="二次関数高速暗算ゲーム", page_icon="📊", layout="wide")

# セッション状態の初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'game_duration' not in st.session_state:
    st.session_state.game_duration = 60
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'medium'
if 'problem_types' not in st.session_state:
    st.session_state.problem_types = ['basic_calculation']
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# マルチプレイヤー用
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'single'
if 'players' not in st.session_state:
    st.session_state.players = []
if 'current_player' not in st.session_state:
    st.session_state.current_player = 0
if 'player_scores' not in st.session_state:
    st.session_state.player_scores = {}
if 'player_questions' not in st.session_state:
    st.session_state.player_questions = {}
if 'multiplayer_results' not in st.session_state:
    st.session_state.multiplayer_results = []

def generate_basic_calculation_question(difficulty):
    """基本的な二次関数の値を求める問題"""
    if difficulty == 'easy':
        # y = x² + bx + c の形で、x = 1, 2, 3などの簡単な値
        a = 1
        b = random.randint(-5, 5)
        c = random.randint(-10, 10)
        x = random.randint(1, 3)
        
        question = f"f(x) = x² + {b}x + {c} のとき、f({x}) = ?"
        if b >= 0:
            question = f"f(x) = x² + {b}x + {c} のとき、f({x}) = ?"
        else:
            question = f"f(x) = x² - {abs(b)}x + {c} のとき、f({x}) = ?"
        
        answer = x*x + b*x + c
        
    elif difficulty == 'medium':
        # y = ax² + bx + c の形で、a ≠ 1
        a = random.randint(2, 4)
        b = random.randint(-6, 6)
        c = random.randint(-10, 10)
        x = random.randint(1, 4)
        
        question = f"f(x) = {a}x² + {b}x + {c} のとき、f({x}) = ?"
        if b >= 0:
            question = f"f(x) = {a}x² + {b}x + {c} のとき、f({x}) = ?"
        else:
            question = f"f(x) = {a}x² - {abs(b)}x + {c} のとき、f({x}) = ?"
        
        answer = a*x*x + b*x + c
        
    else:  # hard
        # より複雑な係数と負の値も含む
        a = random.randint(-3, 5)
        if a == 0:
            a = 1
        b = random.randint(-8, 8)
        c = random.randint(-15, 15)
        x = random.randint(-3, 5)
        
        # 係数の表示を調整
        a_str = f"{a}" if a != 1 else ""
        if a == -1:
            a_str = "-"
        
        b_str = f" + {b}x" if b > 0 else f" - {abs(b)}x" if b < 0 else ""
        c_str = f" + {c}" if c > 0 else f" - {abs(c)}" if c < 0 else ""
        
        question = f"f(x) = {a_str}x²{b_str}{c_str} のとき、f({x}) = ?"
        answer = a*x*x + b*x + c
        
    return question, answer

def generate_vertex_question(difficulty):
    """頂点を求める問題"""
    if difficulty == 'easy':
        # y = (x - h)² + k の形
        h = random.randint(-3, 3)
        k = random.randint(-5, 5)
        
        if h >= 0:
            question = f"y = (x - {h})² + {k} の頂点の座標は？"
        else:
            question = f"y = (x + {abs(h)})² + {k} の頂点の座標は？"
        
        answer = f"({h}, {k})"
        
    elif difficulty == 'medium':
        # y = a(x - h)² + k の形
        a = random.randint(2, 4)
        h = random.randint(-4, 4)
        k = random.randint(-8, 8)
        
        if h >= 0:
            question = f"y = {a}(x - {h})² + {k} の頂点のx座標は？"
        else:
            question = f"y = {a}(x + {abs(h)})² + {k} の頂点のx座標は？"
        
        answer = h
        
    else:  # hard
        # y = ax² + bx + c から頂点を求める
        a = random.randint(1, 4)
        b = random.randint(-6, 6)
        c = random.randint(-10, 10)
        
        question = f"y = {a}x² + {b}x + {c} の頂点のx座標は？"
        answer = -b / (2 * a)
        
        # 分数の場合は分数形式で答える
        if answer == int(answer):
            answer = int(answer)
        else:
            # 分数として表示
            numerator = -b
            denominator = 2 * a
            # 約分
            gcd = math.gcd(abs(numerator), abs(denominator))
            numerator //= gcd
            denominator //= gcd
            answer = f"{numerator}/{denominator}"
        
    return question, answer

def generate_discriminant_question(difficulty):
    """判別式を求める問題"""
    if difficulty == 'easy':
        # 簡単な係数での判別式
        a = random.randint(1, 3)
        b = random.randint(2, 6)
        c = random.randint(1, 5)
        
        question = f"ax² + bx + c = 0 で a={a}, b={b}, c={c} のとき、判別式D = ?"
        answer = b*b - 4*a*c
        
    elif difficulty == 'medium':
        # 中程度の係数
        a = random.randint(1, 4)
        b = random.randint(-8, 8)
        c = random.randint(-6, 6)
        
        question = f"{a}x² + {b}x + {c} = 0 の判別式D = ?"
        answer = b*b - 4*a*c
        
    else:  # hard
        # 解の個数を答える問題
        a = random.randint(1, 3)
        b = random.randint(-6, 6)
        c = random.randint(-8, 8)
        
        discriminant = b*b - 4*a*c
        
        question = f"{a}x² + {b}x + {c} = 0 の実数解の個数は？"
        if discriminant > 0:
            answer = 2
        elif discriminant == 0:
            answer = 1
        else:
            answer = 0
        
    return question, answer

def generate_axis_of_symmetry_question(difficulty):
    """対称軸を求める問題"""
    if difficulty == 'easy':
        # y = x² + bx + c の対称軸
        b = random.randint(-6, 6)
        c = random.randint(-10, 10)
        
        question = f"y = x² + {b}x + {c} の対称軸の方程式は？"
        x_axis = -b / 2
        
        if x_axis == int(x_axis):
            answer = f"x = {int(x_axis)}"
        else:
            # 分数として表示
            numerator = -b
            denominator = 2
            gcd = math.gcd(abs(numerator), abs(denominator))
            numerator //= gcd
            denominator //= gcd
            answer = f"x = {numerator}/{denominator}"
        
    elif difficulty == 'medium':
        # y = ax² + bx + c の対称軸
        a = random.randint(2, 4)
        b = random.randint(-8, 8)
        c = random.randint(-10, 10)
        
        question = f"y = {a}x² + {b}x + {c} の対称軸は？"
        x_axis = -b / (2 * a)
        
        if x_axis == int(x_axis):
            answer = f"x = {int(x_axis)}"
        else:
            # 分数として表示
            numerator = -b
            denominator = 2 * a
            gcd = math.gcd(abs(numerator), abs(denominator))
            numerator //= gcd
            denominator //= gcd
            answer = f"x = {numerator}/{denominator}"
        
    else:  # hard
        # 対称軸のx座標だけを答える
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(-15, 15)
        
        question = f"y = {a}x² + {b}x + {c} の対称軸のx座標は？"
        x_axis = -b / (2 * a)
        
        if x_axis == int(x_axis):
            answer = int(x_axis)
        else:
            # 分数として表示
            numerator = -b
            denominator = 2 * a
            gcd = math.gcd(abs(numerator), abs(denominator))
            numerator //= gcd
            denominator //= gcd
            answer = f"{numerator}/{denominator}"
        
    return question, answer

def generate_roots_question(difficulty):
    """解（根）を求める問題"""
    if difficulty == 'easy':
        # 簡単に因数分解できる形
        roots = [random.randint(-3, 3), random.randint(-3, 3)]
        while roots[0] == roots[1]:
            roots[1] = random.randint(-3, 3)
        
        # (x - r1)(x - r2) = x² - (r1+r2)x + r1*r2
        r1, r2 = roots
        b = -(r1 + r2)
        c = r1 * r2
        
        question = f"x² + {b}x + {c} = 0 の解は？（小さい方）"
        answer = min(r1, r2)
        
    elif difficulty == 'medium':
        # 解の公式を使う必要がある問題
        a = random.randint(1, 3)
        b = random.randint(-6, 6)
        c = random.randint(-8, 8)
        
        # 判別式が完全平方数になるように調整
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            c = random.randint(-2, 2)
            discriminant = b*b - 4*a*c
        
        if discriminant >= 0 and int(math.sqrt(discriminant))**2 == discriminant:
            question = f"{a}x² + {b}x + {c} = 0 の解の個数は？"
            if discriminant > 0:
                answer = 2
            elif discriminant == 0:
                answer = 1
            else:
                answer = 0
        else:
            # 別の問題に変更
            question = f"{a}x² + {b}x + {c} = 0 の判別式は？"
            answer = discriminant
        
    else:  # hard
        # 完全平方式かどうかを判定
        a = 1
        b = random.randint(-6, 6)
        c = random.randint(1, 9)
        
        # 完全平方数にする
        if random.choice([True, False]):
            # 完全平方式にする
            k = random.randint(-4, 4)
            b = -2 * k
            c = k * k
            question = f"x² + {b}x + {c} は完全平方式か？(Yes=1, No=0)"
            answer = 1
        else:
            # 完全平方式ではない
            question = f"x² + {b}x + {c} は完全平方式か？(Yes=1, No=0)"
            discriminant = b*b - 4*a*c
            answer = 1 if discriminant == 0 else 0
        
    return question, answer

def generate_y_intercept_question(difficulty):
    """y切片を求める問題"""
    if difficulty == 'easy':
        # 基本的なy切片
        a = random.randint(1, 3)
        b = random.randint(-5, 5)
        c = random.randint(-10, 10)
        
        question = f"y = {a}x² + {b}x + {c} のy切片は？"
        answer = c
        
    elif difficulty == 'medium':
        # グラフとy軸の交点
        a = random.randint(1, 4)
        b = random.randint(-6, 6)
        c = random.randint(-15, 15)
        
        question = f"y = {a}x² + {b}x + {c} がy軸と交わる点の座標は？"
        answer = f"(0, {c})"
        
    else:  # hard
        # x切片（y = 0のときのx）
        # 簡単に因数分解できる形を作る
        r1 = random.randint(-3, 3)
        r2 = random.randint(-3, 3)
        while r1 == r2:
            r2 = random.randint(-3, 3)
        
        # (x - r1)(x - r2) = x² - (r1+r2)x + r1*r2
        b = -(r1 + r2)
        c = r1 * r2
        
        question = f"y = x² + {b}x + {c} のx切片のうち小さい方は？"
        answer = min(r1, r2)
        
    return question, answer

def generate_question(difficulty, problem_types):
    """指定された問題タイプから問題を生成"""
    problem_type = random.choice(problem_types)
    
    if problem_type == 'basic_calculation':
        return generate_basic_calculation_question(difficulty)
    elif problem_type == 'vertex':
        return generate_vertex_question(difficulty)
    elif problem_type == 'discriminant':
        return generate_discriminant_question(difficulty)
    elif problem_type == 'axis_of_symmetry':
        return generate_axis_of_symmetry_question(difficulty)
    elif problem_type == 'roots':
        return generate_roots_question(difficulty)
    elif problem_type == 'y_intercept':
        return generate_y_intercept_question(difficulty)
    else:
        return generate_basic_calculation_question(difficulty)

def start_single_game():
    """シングルプレイヤーゲーム開始"""
    st.session_state.game_state = 'playing'
    st.session_state.game_mode = 'single'
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.start_time = time.time()
    question, answer = generate_question(st.session_state.difficulty, st.session_state.problem_types)
    st.session_state.current_question = question
    st.session_state.correct_answer = answer

def start_multiplayer_game():
    """マルチプレイヤーゲーム開始"""
    st.session_state.game_state = 'multiplayer_playing'
    st.session_state.game_mode = 'multiplayer'
    st.session_state.current_player = 0
    st.session_state.player_scores = {player: 0 for player in st.session_state.players}
    st.session_state.player_questions = {player: 0 for player in st.session_state.players}
    st.session_state.start_time = time.time()
    question, answer = generate_question(st.session_state.difficulty, st.session_state.problem_types)
    st.session_state.current_question = question
    st.session_state.correct_answer = answer

def check_answer(user_answer, is_multiplayer=False):
    """回答をチェック"""
    try:
        correct_answer = st.session_state.correct_answer
        
        # 答えが文字列の場合（座標、分数など）
        if isinstance(correct_answer, str):
            # 空白を除去して比較
            user_answer_clean = str(user_answer).replace(" ", "")
            correct_answer_clean = str(correct_answer).replace(" ", "")
            is_correct = user_answer_clean == correct_answer_clean
        else:
            # 数値の場合
            try:
                user_num = float(user_answer)
                correct_num = float(correct_answer)
                is_correct = abs(user_num - correct_num) < 0.01
            except:
                is_correct = False
        
        if is_correct:
            if is_multiplayer:
                current_player = st.session_state.players[st.session_state.current_player]
                st.session_state.player_scores[current_player] += 1
                st.session_state.player_questions[current_player] += 1
            else:
                st.session_state.score += 1
                st.session_state.question_count += 1
            st.success("正解！ 🎉")
        else:
            if is_multiplayer:
                current_player = st.session_state.players[st.session_state.current_player]
                st.session_state.player_questions[current_player] += 1
            else:
                st.session_state.question_count += 1
            st.error(f"不正解。正解は {correct_answer} でした。")
        
        # 次の問題を生成
        question, answer = generate_question(st.session_state.difficulty, st.session_state.problem_types)
        st.session_state.current_question = question
        st.session_state.correct_answer = answer
        
        # マルチプレイヤーの場合、次のプレイヤーに交代
        if is_multiplayer:
            st.session_state.current_player = (st.session_state.current_player + 1) % len(st.session_state.players)
        
    except Exception as e:
        st.error("正しい形式で入力してください。")

def end_game():
    """ゲーム終了"""
    if st.session_state.game_mode == 'single':
        st.session_state.game_state = 'finished'
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
    else:
        st.session_state.game_state = 'finished'
        st.session_state.multiplayer_results = [
            {
                'player': player,
                'score': st.session_state.player_scores[player],
                'questions': st.session_state.player_questions[player],
                'accuracy': (st.session_state.player_scores[player] / st.session_state.player_questions[player] * 100) if st.session_state.player_questions[player] > 0 else 0
            }
            for player in st.session_state.players
        ]
        st.session_state.multiplayer_results.sort(key=lambda x: x['score'], reverse=True)

# メインアプリケーション
st.title("📊 二次関数高速暗算ゲーム")

# メニュー画面
if st.session_state.game_state == 'menu':
    st.header("ゲーム設定")
    
    # ゲームモード選択
    game_mode = st.selectbox(
        "ゲームモード:",
        ['single', 'multiplayer'],
        format_func=lambda x: {'single': 'シングルプレイヤー', 'multiplayer': 'マルチプレイヤー'}[x]
    )
    st.session_state.game_mode = game_mode
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("難易度選択")
        difficulty = st.selectbox(
            "難易度を選択してください:",
            ['easy', 'medium', 'hard'],
            index=['easy', 'medium', 'hard'].index(st.session_state.difficulty),
            format_func=lambda x: {'easy': '簡単', 'medium': '普通', 'hard': '難しい'}[x]
        )
        st.session_state.difficulty = difficulty
        
        st.subheader("問題タイプ")
        problem_types = st.multiselect(
            "問題タイプを選択してください:",
            ['basic_calculation', 'vertex', 'discriminant', 'axis_of_symmetry', 'roots', 'y_intercept'],
            default=st.session_state.problem_types,
            format_func=lambda x: {
                'basic_calculation': '関数値の計算',
                'vertex': '頂点',
                'discriminant': '判別式',
                'axis_of_symmetry': '対称軸',
                'roots': '解・因数分解',
                'y_intercept': '切片'
            }[x]
        )
        if problem_types:
            st.session_state.problem_types = problem_types
        
        st.subheader("制限時間")
        duration = st.selectbox(
            "制限時間を選択してください:",
            [60, 90, 120, 180],
            index=[60, 90, 120, 180].index(st.session_state.game_duration),
            format_func=lambda x: f"{x}秒"
        )
        st.session_state.game_duration = duration
    
    with col2:
        if game_mode == 'multiplayer':
            st.subheader("👥 プレイヤー設定")
            
            # プレイヤー名入力
            new_player = st.text_input("プレイヤー名を入力:")
            if st.button("プレイヤー追加") and new_player:
                if new_player not in st.session_state.players:
                    st.session_state.players.append(new_player)
                    st.success(f"{new_player}を追加しました！")
                else:
                    st.error("そのプレイヤー名は既に存在します。")
            
            # 現在のプレイヤーリスト
            if st.session_state.players:
                st.write("**現在のプレイヤー:**")
                for i, player in enumerate(st.session_state.players):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"{i+1}. {player}")
                    with col_b:
                        if st.button("削除", key=f"del_{i}"):
                            st.session_state.players.remove(player)
                            st.rerun()
            
            # プレイヤーリセット
            if st.button("プレイヤーリストをリセット"):
                st.session_state.players = []
                st.rerun()
                
        else:
            st.subheader("📊 統計")
            st.metric("最高スコア", st.session_state.high_score)
        
        st.subheader("📋 ルール")
        st.write("• 制限時間内に二次関数の問題を解く")
        st.write("• 正解すると1点獲得")
        st.write("• 分数は a/b の形式で入力")
        st.write("• 座標は (x, y) の形式で入力")
        if game_mode == 'multiplayer':
            st.write("• プレイヤーが順番に問題を解く")
        st.write("• 時間切れでゲーム終了")
    
    st.markdown("---")
    
    # ゲーム開始ボタン
    if game_mode == 'single':
        if st.button("🎮 ゲームスタート", type="primary", use_container_width=True):
            start_single_game()
            st.rerun()
    else:
        if len(st.session_state.players) >= 2:
            if st.button("🎮 マルチプレイヤーゲーム開始", type="primary", use_container_width=True):
                start_multiplayer_game()
                st.rerun()
        else:
            st.warning("マルチプレイヤーゲームには最低2人のプレイヤーが必要です。")

# ゲーム中（シングルプレイヤー）
elif st.session_state.game_state == 'playing':
    # 残り時間を計算
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.game_duration - elapsed_time)
    
    # 時間切れチェック
    if remaining_time <= 0:
        end_game()
        st.rerun()
    
    # ゲーム情報表示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("スコア", st.session_state.score)
    with col2:
        st.metric("問題数", st.session_state.question_count)
    with col3:
        st.metric("残り時間", f"{remaining_time:.1f}秒")
    
    # プログレスバー
    progress = 1 - (remaining_time / st.session_state.game_duration)
    st.progress(progress)
    
    # 問題表示
    st.markdown("---")
    st.subheader("問題")
    st.markdown(f"## {st.session_state.current_question}")
    
    # 回答入力
    with st.form("answer_form"):
        user_answer = st.text_input("答え:", key="answer_input", help="分数は a/b、座標は (x, y) の形式で入力")
        submitted = st.form_submit_button("回答", type="primary")
        
        if submitted and user_answer:
            check_answer(user_answer, False)
            st.rerun()
    
    # ゲーム終了ボタン
    if st.button("ゲームを終了", type="secondary"):
        end_game()
        st.rerun()

# ゲーム中（マルチプレイヤー）
elif st.session_state.game_state == 'multiplayer_playing':
    # 残り時間を計算
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.game_duration - elapsed_time)
    
    # 時間切れチェック
    if remaining_time <= 0:
        end_game()
        st.rerun()
    
    # 現在のプレイヤー
    current_player = st.session_state.players[st.session_state.current_player]
    
    # ゲーム情報表示
    st.subheader(f"🎯 現在のプレイヤー: {current_player}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("残り時間", f"{remaining_time:.1f}秒")
    with col2:
        progress = 1 - (remaining_time / st.session_state.game_duration)
        st.progress(progress)
    
    # スコアボード
    st.subheader("📊 スコアボード")
    score_cols = st.columns(len(st.session_state.players))
    for i, player in enumerate(st.session_state.players):
        with score_cols[i]:
            score = st.session_state.player_scores[player]
            questions = st.session_state.player_questions[player]