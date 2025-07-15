import streamlit as st
import random
import time
from datetime import datetime, timedelta
import json

# ページ設定
st.set_page_config(page_title="高速暗算ゲーム", page_icon="🧮", layout="wide")

# セッション状態の初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'  # menu, playing, finished, multiplayer_setup, multiplayer_playing
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
    st.session_state.problem_types = ['basic']
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# マルチプレイヤー用
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'single'  # single, multiplayer
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

def generate_basic_question(difficulty):
    """基本的な四則演算問題を生成"""
    if difficulty == 'easy':
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        operations = ['+', '-', '×']
        op = random.choice(operations)
        
        if op == '+':
            question = f"{a} + {b}"
            answer = a + b
        elif op == '-':
            if a < b:
                a, b = b, a
            question = f"{a} - {b}"
            answer = a - b
        else:  # ×
            question = f"{a} × {b}"
            answer = a * b
            
    elif difficulty == 'medium':
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        operations = ['+', '-', '×']
        op = random.choice(operations)
        
        if op == '+':
            question = f"{a} + {b}"
            answer = a + b
        elif op == '-':
            question = f"{a} - {b}"
            answer = a - b
        else:  # ×
            a = random.randint(2, 15)
            b = random.randint(2, 15)
            question = f"{a} × {b}"
            answer = a * b
            
    else:  # hard
        operations = ['+', '-', '×', '÷']
        op = random.choice(operations)
        
        if op == '+':
            a = random.randint(50, 200)
            b = random.randint(10, 100)
            question = f"{a} + {b}"
            answer = a + b
        elif op == '-':
            a = random.randint(50, 200)
            b = random.randint(10, a)
            question = f"{a} - {b}"
            answer = a - b
        elif op == '×':
            a = random.randint(10, 30)
            b = random.randint(2, 20)
            question = f"{a} × {b}"
            answer = a * b
        else:  # ÷
            b = random.randint(2, 20)
            answer = random.randint(2, 50)
            a = b * answer
            question = f"{a} ÷ {b}"
            
    return question, answer

def generate_fraction_question(difficulty):
    """分数の問題を生成"""
    if difficulty == 'easy':
        # 簡単な分数の足し算・引き算（同じ分母）
        denominator = random.randint(2, 10)
        a = random.randint(1, denominator-1)
        b = random.randint(1, denominator-1)
        
        if random.choice([True, False]):
            # 足し算
            question = f"{a}/{denominator} + {b}/{denominator}"
            answer_num = a + b
            if answer_num >= denominator:
                answer_whole = answer_num // denominator
                answer_remainder = answer_num % denominator
                if answer_remainder == 0:
                    answer = answer_whole
                else:
                    answer = f"{answer_whole} {answer_remainder}/{denominator}"
            else:
                answer = f"{answer_num}/{denominator}"
        else:
            # 引き算
            if a < b:
                a, b = b, a
            question = f"{a}/{denominator} - {b}/{denominator}"
            answer_num = a - b
            if answer_num == 0:
                answer = 0
            else:
                answer = f"{answer_num}/{denominator}"
                
    elif difficulty == 'medium':
        # 分数の掛け算
        a = random.randint(1, 6)
        b = random.randint(2, 8)
        c = random.randint(1, 6)
        d = random.randint(2, 8)
        
        question = f"{a}/{b} × {c}/{d}"
        answer_num = a * c
        answer_den = b * d
        
        # 約分
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        
        g = gcd(answer_num, answer_den)
        answer_num //= g
        answer_den //= g
        
        if answer_den == 1:
            answer = answer_num
        else:
            answer = f"{answer_num}/{answer_den}"
            
    else:  # hard
        # 分数の割り算
        a = random.randint(1, 6)
        b = random.randint(2, 8)
        c = random.randint(1, 6)
        d = random.randint(2, 8)
        
        question = f"{a}/{b} ÷ {c}/{d}"
        answer_num = a * d
        answer_den = b * c
        
        # 約分
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        
        g = gcd(answer_num, answer_den)
        answer_num //= g
        answer_den //= g
        
        if answer_den == 1:
            answer = answer_num
        else:
            answer = f"{answer_num}/{answer_den}"
    
    return question, answer

def generate_decimal_question(difficulty):
    """小数の問題を生成"""
    if difficulty == 'easy':
        # 一桁小数の足し算・引き算
        a = round(random.uniform(0.1, 9.9), 1)
        b = round(random.uniform(0.1, 9.9), 1)
        
        if random.choice([True, False]):
            question = f"{a} + {b}"
            answer = round(a + b, 1)
        else:
            if a < b:
                a, b = b, a
            question = f"{a} - {b}"
            answer = round(a - b, 1)
            
    elif difficulty == 'medium':
        # 小数の掛け算
        a = round(random.uniform(1.0, 9.9), 1)
        b = round(random.uniform(1.0, 9.9), 1)
        question = f"{a} × {b}"
        answer = round(a * b, 2)
        
    else:  # hard
        # 小数の割り算
        b = round(random.uniform(1.0, 5.0), 1)
        answer = round(random.uniform(1.0, 10.0), 1)
        a = round(b * answer, 2)
        question = f"{a} ÷ {b}"
        
    return question, answer

def generate_percentage_question(difficulty):
    """パーセントの問題を生成"""
    if difficulty == 'easy':
        # 基本的なパーセント計算
        number = random.randint(10, 100)
        percentage = random.choice([10, 20, 25, 50, 75])
        question = f"{number}の{percentage}%"
        answer = (number * percentage) // 100
        
    elif difficulty == 'medium':
        # パーセントの増減
        base = random.randint(50, 200)
        percentage = random.choice([10, 15, 20, 25, 30])
        
        if random.choice([True, False]):
            question = f"{base}を{percentage}%増加"
            answer = base + (base * percentage) // 100
        else:
            question = f"{base}を{percentage}%減少"
            answer = base - (base * percentage) // 100
            
    else:  # hard
        # 逆算問題
        original = random.randint(100, 500)
        percentage = random.choice([10, 20, 25, 50])
        result = original + (original * percentage) // 100
        question = f"{result}は元の数の{100 + percentage}%。元の数は？"
        answer = original
        
    return question, answer

def generate_square_root_question(difficulty):
    """平方根の問題を生成"""
    if difficulty == 'easy':
        # 完全平方数の平方根
        numbers = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        num = random.choice(numbers)
        question = f"√{num}"
        answer = int(num ** 0.5)
        
    elif difficulty == 'medium':
        # 簡単な平方根の計算
        numbers = [121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
        num = random.choice(numbers)
        question = f"√{num}"
        answer = int(num ** 0.5)
        
    else:  # hard
        # 平方根の近似値
        numbers = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13]
        num = random.choice(numbers)
        question = f"√{num} (小数第1位まで)"
        answer = round(num ** 0.5, 1)
        
    return question, answer

def generate_question(difficulty, problem_types):
    """指定された問題タイプから問題を生成"""
    problem_type = random.choice(problem_types)
    
    if problem_type == 'basic':
        return generate_basic_question(difficulty)
    elif problem_type == 'fraction':
        return generate_fraction_question(difficulty)
    elif problem_type == 'decimal':
        return generate_decimal_question(difficulty)
    elif problem_type == 'percentage':
        return generate_percentage_question(difficulty)
    elif problem_type == 'square_root':
        return generate_square_root_question(difficulty)
    else:
        return generate_basic_question(difficulty)

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
        # 答えが文字列の場合（分数など）
        if isinstance(st.session_state.correct_answer, str):
            if str(user_answer) == str(st.session_state.correct_answer):
                is_correct = True
            else:
                is_correct = False
        else:
            # 数値の場合
            if abs(float(user_answer) - float(st.session_state.correct_answer)) < 0.01:
                is_correct = True
            else:
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
            st.error(f"不正解。正解は {st.session_state.correct_answer} でした。")
        
        # 次の問題を生成
        question, answer = generate_question(st.session_state.difficulty, st.session_state.problem_types)
        st.session_state.current_question = question
        st.session_state.correct_answer = answer
        
        # マルチプレイヤーの場合、次のプレイヤーに交代
        if is_multiplayer:
            st.session_state.current_player = (st.session_state.current_player + 1) % len(st.session_state.players)
        
    except ValueError:
        st.error("正しい形式で入力してください。")

def end_game():
    """ゲーム終了"""
    if st.session_state.game_mode == 'single':
        st.session_state.game_state = 'finished'
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
    else:
        st.session_state.game_state = 'finished'
        # マルチプレイヤーの結果を保存
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
st.title("🧮 高速暗算ゲーム")

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
            ['basic', 'fraction', 'decimal', 'percentage', 'square_root'],
            default=st.session_state.problem_types,
            format_func=lambda x: {
                'basic': '基本四則演算',
                'fraction': '分数',
                'decimal': '小数',
                'percentage': 'パーセント',
                'square_root': '平方根'
            }[x]
        )
        if problem_types:
            st.session_state.problem_types = problem_types
        
        st.subheader("制限時間")
        duration = st.selectbox(
            "制限時間を選択してください:",
            [30, 60, 90, 120],
            index=[30, 60, 90, 120].index(st.session_state.game_duration),
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
        st.write("• 制限時間内にできるだけ多くの問題を解く")
        st.write("• 正解すると1点獲得")
        st.write("• 間違えても次の問題に進む")
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
    st.markdown(f"## {st.session_state.current_question} = ?")
    
    # 回答入力
    with st.form("answer_form"):
        user_answer = st.text_input("答え:", key="answer_input")
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
        # プログレスバー
        progress = 1 - (remaining_time / st.session_state.game_duration)
        st.progress(progress)
    
    # スコアボード
    st.subheader("📊 スコアボード")
    score_cols = st.columns(len(st.session_state.players))
    for i, player in enumerate(st.session_state.players):
        with score_cols[i]:
            score = st.session_state.player_scores[player]
            questions = st.session_state.player_questions[player]
            st.metric(player, f"{score}問正解", f"{questions}問中")
    
    # 問題表示
    st.markdown("---")
    st.subheader("問題")
    st.markdown(f"## {st.session_state.current_question} = ?")
    
    # 回答入力
    with st.form("multiplayer_answer_form"):
        user_answer = st.text_input("答え:", key="multiplayer_answer_input")
        submitted = st.form_submit_button("回答", type="primary")
        
        if submitted and user_answer:
            check_answer(user_answer, True)
            st.rerun()
    
    # ゲーム終了ボタン
    if st.button("ゲームを終了", type="secondary"):
        end_game()
        st.rerun()

# ゲーム終了画面
elif st.session_state.game_state == 'finished':
    st.header("🎉 ゲーム終了！")
    
    if st.session_state.game_mode == 'single':
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 結果")
            st.metric("最終スコア", st.session_state.score)
            st.metric("解答した問題数", st.session_state.question_count)
            
            if st.session_state.question_count > 0:
                accuracy = (st.session_state.score / st.session_state.question_count) * 100
                st.metric("正答率", f"{accuracy:.1f}%")
        
        with col2:
            st.subheader("🏆 評価")
            if st.session_state.score >= 20:
                st.success("素晴らしい！暗算の天才です！⭐⭐⭐")
            elif st.session_state.score >= 15:
                st.info("とても良い結果です！⭐⭐")
            elif st.session_state.score >= 10:
                st.info("良い結果です！⭐")
            else:
                st.warning("練習を続けて頑張りましょう！")
            
            if st.session_state.score == st.session_state.high_score:
                st.balloons()
                st.success("🎊 新記録達成！")
    
    else:  # マルチプレイヤー
        st.subheader("🏆 最終結果")
        
        # 勝者の発表
        winner = st.session_state.multiplayer_results[0]
        st.success(f"🎉 優勝: {winner['player']} ({winner['score']}問正解)")
        
        # 結果テーブル
        result_cols = st.columns(4)
        with result_cols[0]:
            st.write("**順位**")
        with result_cols[1]:
            st.write("**プレイヤー**")
        with result_cols[2]:
            st.write("**正解数**")
        with result_cols[3]:
            st.write("**正答率**")
        
        for i, result in enumerate(st.session_state.multiplayer_results):
            with result_cols[0]:
                st.write(f"{i+1}位")
            with result_cols[1]:
                st.write(result['player'])
            with result_cols[2]:
                st.write(f"{result['score']}/{result['questions']}")
            with result_cols[3]:
                st.write(f"{result['accuracy']:.1f}%")
        
        # 最高スコアの更新
        if winner['score'] > st.session_state.high_score:
            st.session_state.high_score = winner['score']
            st.balloons()
            st.success("🎊 新記録達成！")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 もう一度プレイ", type="primary", use_container_width=True):
            if st.session_state.game_mode == 'single':
                start_single_game()
            else:
                start_multiplayer_game()
            st.rerun()
    
    with col2:
        if st.button("📋 メニューに戻る", type="secondary", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()

# サイドバーに説明を追加
with st.sidebar:
    st.header("🧮 高速暗算ゲーム")
    st.write("制限時間内にできるだけ多くの暗算問題を解いて、スコアを競うゲームです。")
    
    st.subheader("🎯 問題タイプ")
    st.write("**基本四則演算**: 足し算、引き算、掛け算、割り算")
    st.write("**分数**: 分数の計算")
    st.write("**小数**: 小数点の計算")
    st.write("**パーセント**: パーセントの計算")
    st.write("**平方根**: 平方根の計算")
    
    st.subheader("💡 上達のコツ")
    st.write('数学やれ')