import streamlit as st
import random
import time

st.set_page_config(page_title="平方完成チャレンジ", layout="centered")
st.title("🎯 平方完成 タイムアタック")

# --------------------
# ゲーム設定
# --------------------
LEVEL_TIMES = {"初級": 30, "中級": 45, "上級": 60}  # 各難易度の制限時間
TOTAL_QUESTIONS = 5  # 出題数

# --------------------
# セッション初期化
# --------------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.level = "初級"
    st.session_state.question_num = 1
    st.session_state.correct_count = 0
    st.session_state.total_time = 0.0
    st.session_state.finished = False
    st.session_state.problem = None
    st.session_state.start_time = None
    st.session_state.show_result = False

# --------------------
# ゲーム開始前：難易度選択
# --------------------
if not st.session_state.started:
    st.markdown("## 🎮 ゲーム設定")
    st.session_state.level = st.radio("難易度を選んでください", ["初級", "中級", "上級"], horizontal=True)
    
    if st.button("▶ ゲームスタート"):
        st.session_state.started = True
        st.session_state.problem = None
        st.rerun()  # 再読み込みしてUIリセット
    st.stop()

# --------------------
# 問題生成関数
# --------------------
def generate_problem(level):
    if level == "初級":
        a = 1
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
    elif level == "中級":
        a = random.choice([1, -1, 2, -2])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
    else:
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-20, 20)
        c = random.randint(-20, 20)
    return a, b, c

# --------------------
# 正誤判定関数
# --------------------
def is_correct(a, b, c, user_str):
    try:
        half = b / (2 * a)
        delta = b**2 - 4*a*c
        const = -delta / (4 * a)
        expected1 = f"(x + {round(half, 2)})"
        expected2 = f"(x - {round(-half, 2)})"
        return (expected1 in user_str or expected2 in user_str) and str(round(const, 2)) in user_str
    except:
        return False

# --------------------
# 問題未生成なら生成
# --------------------
if st.session_state.problem is None:
    st.session_state.problem = generate_problem(st.session_state.level)
    st.session_state.start_time = time.time()
    st.session_state.show_result = False

a, b, c = st.session_state.problem
time_limit = LEVEL_TIMES[st.session_state.level]
elapsed = time.time() - st.session_state.start_time
remaining = int(time_limit - elapsed)

# --------------------
# 表示（タイマー・問題）
# --------------------
st.markdown(f"### 🧮 第 {st.session_state.question_num} 問 / 全 {TOTAL_QUESTIONS} 問")
st.markdown(f"⏱ 残り時間：**{max(0, remaining)} 秒**")
st.latex(f"{a}x^2 + {b}x + {c}")

# --------------------
# 入力と回答処理
# --------------------
if not st.session_state.show_result and remaining > 0:
    user_input = st.text_input("平方完成した式を入力（例：1*(x + 2)**2 - 3）")

    if st.button("解答する"):
        time_taken = round(time.time() - st.session_state.start_time, 2)
        correct = is_correct(a, b, c, user_input)
        st.session_state.total_time += time_taken
        st.session_state.show_result = True

        if correct:
            st.success(f"✅ 正解！ ⏱ 解答時間：{time_taken} 秒")
            st.session_state.correct_count += 1
        else:
            st.error(f"❌ 不正解… ⏱ 解答時間：{time_taken} 秒")
elif not st.session_state.show_result and remaining <= 0:
    st.warning("⌛ 時間切れ！")
    st.session_state.show_result = True

# --------------------
# 解説と模範解答
# --------------------
if st.session_state.show_result:
    half = b / (2 * a)
    delta = b**2 - 4*a*c
    const = -delta / (4 * a)

    st.markdown("### ✅ 模範解答")
    st.latex(f"{a}(x + {round(half, 2)})^2 + {round(const, 2)}")

    st.markdown("### 🧠 解説")
    st.markdown(f"""
- 与式：\\({a}x^2 + {b}x + {c}\\)
- \\(a = {a}\\), \\(b = {b}\\), \\(c = {c}\\)
- \\(\\frac{{b}}{{2a}} = {round(half, 2)}\\)：これが平方の中の数になります
- 判別式 \\(\\Delta = b^2 - 4ac = {delta}\\)
- 補正項：\\(-\\frac{{\\Delta}}{{4a}} = {round(const, 2)}\\)
- よって、平方完成の形は：\\({a}(x + {round(half, 2)})^2 + {round(const, 2)}\\)
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("次の問題へ"):
            st.session_state.question_num += 1
            st.session_state.problem = None
    with col2:
        if st.button("問題をスキップ"):
            st.session_state.question_num += 1
            st.session_state.problem = None

# --------------------
# 最終結果表示
# --------------------
if st.session_state.question_num > TOTAL_QUESTIONS:
    st.session_state.finished = True

if st.session_state.finished:
    accuracy = round((st.session_state.correct_count / TOTAL_QUESTIONS) * 100, 2)
    avg_time = round(st.session_state.total_time / TOTAL_QUESTIONS, 2)
    st.markdown("---")
    st.markdown("## 📊 結果発表")
    st.markdown(f"""
- 正解数：**{st.session_state.correct_count} / {TOTAL_QUESTIONS}**
- 正答率：**{accuracy}%**
- 平均解答時間：**{avg_time} 秒**
""")
    if st.button("🔁 最初からやり直す"):
        st.session_state.clear()
        st.rerun()






