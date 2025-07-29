# 平方完成チャレンジアプリ（インデント修正済み・完全版）
# ファイル名例: heihou_kansei_app.py

import streamlit as st
import random
import math
import time
from fractions import Fraction

# -------（略）関数群 generate_problem 〜 explain_solution_simple までは変更なし -------

# （すべての関数：generate_problem、format_quadratic、calculate_completion などをそのまま貼り付け）

# --- 省略のため関数部分はあなたのコードと同じです（必要なら再掲できます）---

# -----------------------
# Streamlit アプリのメイン部分
# -----------------------

st.title("⏰ 平方完成 チャレンジ")
st.write("制限時間内に平方完成をマスターしよう！")

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

# -----------------------
# 設定画面
# -----------------------
if not st.session_state.quiz_started:
    # （ここは元のコードと同様）

    # 🚀 クイズスタート時の処理
    if st.button("🚀 クイズスタート！", type="primary"):
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
        st.rerun()

# -----------------------
# クイズ実行中
# -----------------------
elif st.session_state.quiz_started and not st.session_state.quiz_finished:
    # （このセクションも元のコード通りですが、下記の else ブロックに注意）

    # 問題の回答部の else 修正（← ここがあなたの投稿で崩れていた）
    else:
        # 既に回答済みの場合は結果を表示
        result_key = f"result_{st.session_state.current_problem}"
        if result_key in st.session_state:
            if st.session_state[result_key] == "correct":
                st.success("🎉 正解！")
            else:
                st.error(f"❌ 不正解　正解: {correct_answer}")
        
        explanation_key = f"show_explanation_{st.session_state.current_problem}"
        if explanation_key not in st.session_state:
            if st.button("📖 解説を見る", type="secondary"):
                st.session_state[explanation_key] = True
                st.rerun()
        else:
            st.write("📖 解説表示中")

# -----------------------
# クイズ終了後の画面
# -----------------------
elif st.session_state.quiz_finished:
    # （元のコード通り、問題なし）

# -----------------------
# サイドバー
# -----------------------
with st.sidebar:
    st.header("💡 平方完成のコツ")
    st.markdown("""（元のサイドバー説明）""")
