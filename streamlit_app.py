import streamlit as st
import random
import time
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(page_title="高速暗算ゲーム", page_icon="🧮", layout="wide")

# セッション状態の初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'  # menu, playing, finished
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
    st.session_state.game_duration = 60  # デフォルト60秒
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'medium'
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

def generate_question(difficulty):
    """難易度に応じて問題を生成"""
    if difficulty == 'easy':
        # 一桁の計算
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
        # 二桁の計算
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
        # より複雑な計算
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

def start_game():
    """ゲーム開始"""
    st.session_state.game_state = 'playing'
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.start_time = time.time()
    # 最初の問題を生成
    question, answer = generate_question(st.session_state.difficulty)
    st.session_state.current_question = question
    st.session_state.correct_answer = answer

def check_answer(user_answer):
    """回答をチェック"""
    try:
        if int(user_answer) == st.session_state.correct_answer:
            st.session_state.score += 1
            st.success("正解！ 🎉")
        else:
            st.error(f"不正解。正解は {st.session_state.correct_answer} でした。")
        
        st.session_state.question_count += 1
        
        # 次の問題を生成
        question, answer = generate_question(st.session_state.difficulty)
        st.session_state.current_question = question
        st.session_state.correct_answer = answer
        
    except ValueError:
        st.error("数字を入力してください。")

def end_game():
    """ゲーム終了"""
    st.session_state.game_state = 'finished'
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

# メインアプリケーション
st.title("🧮 高速暗算ゲーム")

# メニュー画面
if st.session_state.game_state == 'menu':
    st.header("ゲーム設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("難易度選択")
        difficulty = st.selectbox(
            "難易度を選択してください:",
            ['easy', 'medium', 'hard'],
            index=['easy', 'medium', 'hard'].index(st.session_state.difficulty),
            format_func=lambda x: {'easy': '簡単 (一桁)', 'medium': '普通 (二桁)', 'hard': '難しい (複雑)'}[x]
        )
        st.session_state.difficulty = difficulty
        
        st.subheader("制限時間")
        duration = st.selectbox(
            "制限時間を選択してください:",
            [30, 60, 90, 120],
            index=[30, 60, 90, 120].index(st.session_state.game_duration),
            format_func=lambda x: f"{x}秒"
        )
        st.session_state.game_duration = duration
    
    with col2:
        st.subheader("📊 統計")
        st.metric("最高スコア", st.session_state.high_score)
        
        st.subheader("📋 ルール")
        st.write("• 制限時間内にできるだけ多くの問題を解く")
        st.write("• 正解すると1点獲得")
        st.write("• 間違えても次の問題に進む")
        st.write("• 時間切れでゲーム終了")
    
    st.markdown("---")
    if st.button("🎮 ゲームスタート", type="primary", use_container_width=True):
        start_game()
        st.rerun()

# ゲーム中
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
            check_answer(user_answer)
            st.rerun()
    
    # ゲーム終了ボタン
    if st.button("ゲームを終了", type="secondary"):
        end_game()
        st.rerun()

# ゲーム終了画面
elif st.session_state.game_state == 'finished':
    st.header("🎉 ゲーム終了！")
    
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
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 もう一度プレイ", type="primary", use_container_width=True):
            start_game()
            st.rerun()
    
    with col2:
        if st.button("📋 メニューに戻る", type="secondary", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()

# サイドバーに説明を追加
with st.sidebar:
    st.header("🧮 高速暗算ゲーム")
    st.write("制限時間内にできるだけ多くの暗算問題を解いて、スコアを競うゲームです。")
    
    st.subheader("💡 上達のコツ")
    st.write("• 計算を頭の中で素早く行う")
    st.write("• 簡単な計算から慣れていく")
    st.write("• 毎日少しずつ練習する")
    st.write("• 間違いを恐れずに挑戦する")
    
    st.subheader("🎯 難易度について")
    st.write("**簡単**: 一桁の加減乗算")
    st.write("**普通**: 二桁の計算")
    st.write("**難しい**: 複雑な四則演算")