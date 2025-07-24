import streamlit as st
import random
import time

st.title("🎯 平方完成 タイムアタックモード（連続問題 & スコア付き）")

# --------------------
# 設定
# --------------------
LEVEL_TIMES = {"初級": 30, "中級": 45, "上級": 60}
TOTAL_QUESTIONS = 5

# --------------------
# セッション初期化
# --------------------
if "question_num" not in st.session_state:
    st.session_state.question_num = 1
    st.session_state.correct_count = 0
    st.session_state.total_time = 0.0
    st.session_state.finished = False
    st.session_state.problem = None
    st.session_state.start_time = None
    st.session_state.user_input = ""
    st.session_state.level = "初級"

# --------------------
# 関数
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
# 難易度設定（初回のみ）
# --------------------
if st.session_state.question_num == 1:
    st.session_state.level = st.selectbox("難易度を選んでください", ["初級", "中級", "上級"])

# 問題生成（初期 or 次の問題）
if st.session_state.problem is None:
    st.session_state.problem = generate_problem(st.session_state.level)
    st.session_state.start_time = time.time()

a, b, c = st.session_state.problem
time_limit = LEVEL_TIMES[st.session_state.level]
elapsed = time.time() - st.session_state.start_time
remaining = int(time_limit - elapsed)

# --------------------
# タイマー表示 & 入力
# --------------------
st.markdown(f"🕒 残り時間：**{max(0, remaining)} 秒**")
st.latex(f"{a}x^2 + {b}x + {c}")
user_input = st.text_input("平方完成した式を入力（例：1*(x + 2)**2 - 3）", key=st.session_state.question_num)

# --------------------
# 判定処理
# --------------------
answered = False
if user_input:
    time_taken = round(time.time() - st.session_state.start_time, 2)
    correct = is_correct(a, b, c, user_input)
    st.session_state.total_time += time_taken
    answered = True

    if correct:
        st.success(f"正解！ ⏱ {time_taken}秒")
        st.session_state.correct_count += 1
    else:
        st.error(f"不正解… ⏱ {time_taken}秒")

    # 模範解答と解説
    half = b / (2 * a)
    delta = b**2 - 4*a*c
    const = -delta / (4 * a)

    st.markdown("### 模範解答")
    st.markdown(f"{a}*(x + {round(half, 2)})^2 + {round(const, 2)}")

    st.markdown("### 解説")
    st.markdown(f"""
- \( a = {a} \), \( b = {b} \), \( c = {c} \)  
- \( \\frac{{b}}{{2a}} = {round(half, 2)} \)  
- 判別式 \( \\Delta = b^2 - 4ac = {delta} \)  
- 補正項 \( -\\frac{{\\Delta}}{{4a}} = {round(const, 2)} \)  
- よって平方完成形：\({a}(x + {round(half, 2)})^2 + {round(const, 2)}\)
    """)

# --------------------
# 次の問題 or 終了処理
# --------------------
if answered or remaining <= 0:
    if st.session_state.question_num >= TOTAL_QUESTIONS:
        st.session_state.finished = True
    else:
        if st.button("次の問題へ"):
            st.session_state.question_num += 1
            st.session_state.problem = None
            st.experimental_rerun()

# --------------------
# 結果表示
# --------------------
if st.session_state.finished:
    avg_time = round(st.session_state.total_time / TOTAL_QUESTIONS, 2)
    st.markdown("---")
    st.markdown("## ✅ 結果")
    st.markdown(f"""
- 正解数：**{st.session_state.correct_count} / {TOTAL_QUESTIONS}**
- 平均解答時間：**{avg_time} 秒**
""")
    if st.button("🔁 もう一度挑戦"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

