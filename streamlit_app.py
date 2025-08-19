import streamlit as st
import random
import time
from sympy import Rational

# ---------------------
# 平方完成の答えを計算
# ---------------------
def calculate_completion(a, b, c):
    h = Rational(b, 2 * a)
    k = Rational(c - (b ** 2) / (4 * a))
    return a, h, k

# ---------------------
# 式を文字列に変換
# ---------------------
def format_quadratic(a, b, c):
    expr = f"{a}x²"
    if b != 0:
        expr += f" {'+' if b > 0 else '-'} {abs(b)}x"
    if c != 0:
        expr += f" {'+' if c > 0 else '-'} {abs(c)}"
    return expr

def format_completion_answer(a, h, k):
    h_str = f"(x {'-' if h > 0 else '+'} {abs(h)})"
    k_str = f"{'+' if k >= 0 else '-'} {abs(k)}"
    return f"{a} * {h_str}² {k_str}"

# ---------------------
# 解説生成（例）
# ---------------------
def explain_solution_detailed(a, b, c):
    h = Rational(b, 2 * a)
    k = Rational(c - (b ** 2) / (4 * a))
    return f"""
平方完成の手順：
1. 一次の係数の半分を求める：{b}/(2×{a}) = {h}
2. 定数項を調整する：{c} - ({b}² / (4×{a})) = {k}
3. 結果：{a}(x {'-' if h > 0 else '+'} {abs(h)})² {'+' if k >= 0 else '-'} {abs(k)}
"""

# ---------------------
# 達成バッジ（省略可能）
# ---------------------
def get_achievement_badge(accuracy, time_taken, level):
    badges = []
    if accuracy == 100:
        badges.append("🌟 完璧！全問正解！")
    elif accuracy >= 80:
        badges.append("👍 よくできました！")
    if time_taken < 60:
        badges.append("⏱️ スピードスター")
    return badges

# ---------------------
# 初期化
# ---------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.problems = []
    st.session_state.choices = []
    st.session_state.wrong_problems = []
    st.session_state.correct_answers = 0
    st.session_state.level = 1

st.title("🧮 平方完成クイズ")

# ---------------------
# 設定（開始前）
# ---------------------
if not st.session_state.quiz_started:
    st.markdown("### 設定")

    level = st.slider("難易度（1〜5）", 1, 5, 1)
    count = st.selectbox("出題数", [3, 5, 10], index=1)
    duration = st.selectbox("制限時間（分）", [1, 2, 3, 5], index=1)

    if st.button("▶️ クイズを始める", type="primary"):
        st.session_state.quiz_started = True
        st.session_state.level = level
        st.session_state.problem_count = count
        st.session_state.time_limit = duration * 60
        st.session_state.start_time = time.time()

        # 問題生成
        st.session_state.problems = []
        st.session_state.choices = []
        for _ in range(count):
            a = random.choice([1, 2]) if level < 4 else random.randint(1, level)
            b = random.randint(-level * 5, level * 5)
            c = random.randint(-level * 5, level * 5)
            st.session_state.problems.append((a, b, c))

            correct_a, h, k = calculate_completion(a, b, c)
            correct_answer = format_completion_answer(correct_a, h, k)

            # ダミー選択肢
            choices = [correct_answer]
            while len(choices) < 4:
                delta = random.choice([-1, 1])
                fake_h = h + delta
                fake_k = k + random.choice([-1, 1])
                fake_ans = format_completion_answer(correct_a, fake_h, fake_k)
                if fake_ans not in choices:
                    choices.append(fake_ans)
            random.shuffle(choices)
            st.session_state.choices.append((choices, choices.index(correct_answer)))

        st.rerun()

# ---------------------
# クイズ実行中
# ---------------------
elif st.session_state.quiz_started and not st.session_state.quiz_finished:

    elapsed = time.time() - st.session_state.start_time
    remaining = int(st.session_state.time_limit - elapsed)

    if remaining <= 0:
        st.warning("⏰ 時間切れ！自動的に採点します。")
        st.session_state.quiz_finished = True
        st.rerun()

    st.info(f"残り時間：{remaining} 秒")

    all_answered = True

    for i in range(st.session_state.problem_count):
        a, b, c = st.session_state.problems[i]
        choices, correct_index = st.session_state.choices[i]
        st.subheader(f"問題 {i+1}")
        st.markdown(f"{format_quadratic(a, b, c)} を平方完成してください：")

        selected_key = f"selected_{i}"
        if selected_key not in st.session_state:
            st.session_state[selected_key] = None
            all_answered = False
        elif st.session_state[selected_key] is None:
            all_answered = False

        selected = st.radio(
            "選択肢：",
            options=range(len(choices)),
            format_func=lambda x: f"{chr(65+x)}. {choices[x]}",
            key=selected_key,
            index=st.session_state[selected_key] if st.session_state[selected_key] is not None else 0
        )

        st.session_state[selected_key] = selected
        st.markdown("---")

    if all_answered:
        if st.button("🔍 採点する", type="primary"):
            correct = 0
            st.session_state.wrong_problems = []

            for i in range(st.session_state.problem_count):
                selected = st.session_state[f"selected_{i}"]
                _, correct_index = st.session_state.choices[i]

                if selected == correct_index:
                    correct += 1
                else:
                    a, b, c = st.session_state.problems[i]
                    selected_text = st.session_state.choices[i][0][selected]
                    st.session_state.wrong_problems.append((a, b, c, selected_text, selected))

            st.session_state.correct_answers = correct
            st.session_state.quiz_finished = True
            st.rerun()
    else:
        st.warning("すべての問題に回答してください。")

# ---------------------
# 結果表示
# ---------------------
elif st.session_state.quiz_finished:
    st.success("🎉 クイズが終了しました！")
    total = st.session_state.problem_count
    correct = st.session_state.correct_answers
    accuracy = correct / total * 100
    elapsed_time = time.time() - st.session_state.start_time

    st.markdown(f"### ✅ 正解数：{correct} / {total}（{accuracy:.1f}%）")
    
    badges = get_achievement_badge(accuracy, elapsed_time, st.session_state.level)
    if badges:
        st.markdown("### 🏅 バッジ")
        for badge in badges:
            st.markdown(f"- {badge}")

    if st.session_state.wrong_problems:
        st.markdown("### ❌ 間違った問題と解説")
        for idx, (a, b, c, selected_text, _) in enumerate(st.session_state.wrong_problems):
            correct_a, h, k = calculate_completion(a, b, c)
            correct_answer = format_completion_answer(correct_a, h, k)
            st.markdown(f"**問題 {idx+1}:** {format_quadratic(a, b, c)}")
            st.markdown(f"- あなたの答え：❌ {selected_text}")
            st.markdown(f"- 正解：✅ {correct_answer}")
            with st.expander("📖 解説を表示"):
                st.markdown(explain_solution_detailed(a, b, c))
            st.markdown("---")

    if st.button("🔁 もう一度挑戦"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
