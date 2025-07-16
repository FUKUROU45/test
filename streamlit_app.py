import streamlit as st
import random
import time
import math
import streamlit.components.v1 as components

# === 音の再生 ===
def play_sound(correct=True):
    sound_url = "https://www.soundjay.com/buttons/sounds/button-3.mp3" if correct else "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    components.html(f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mpeg">
        </audio>
    """, height=0)

# === セッション初期化 ===
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.start_time = None
    st.session_state.problem = ""
    st.session_state.answer = None
    st.session_state.difficulty = "ふつう"
    st.session_state.time_limit = 30

# === サイドバー設定 ===
st.sidebar.title("⚙️ 設定")
difficulty = st.sidebar.selectbox("難易度", ["かんたん", "ふつう", "むずかしい"])
time_limit_option = st.sidebar.selectbox("制限時間（秒）", [30, 60, 90, 120])

# ユーザーの設定をセッションに保存
st.session_state.difficulty = difficulty
st.session_state.time_limit = time_limit_option

# === 問題生成 ===
def generate_problem(difficulty):
    op_list = ["+", "-", "*", "/", "√"]

    op = random.choice(op_list)

    if difficulty == "かんたん":
        a = random.randint(1, 9)
        b = random.randint(1, 9)
    elif difficulty == "ふつう":
        a = random.randint(10, 99)
        b = random.randint(2, 20)
    else:
        a = random.randint(50, 200)
        b = random.randint(5, 30)

    if op == "√":
        n = random.choice([x**2 for x in range(2, 21)])  # 整数平方根
        return f"√{n}", int(math.sqrt(n))

    if op == "/":
        result = a // b
        a = result * b
        return f"{a} / {b}", result

    problem = f"{a} {op} {b}"
    answer = eval(problem)
    return problem, int(answer)

# === ゲーム開始 ===
if st.button("スタート！"):
    st.session_state.start_time = time.time()
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.problem, st.session_state.answer = generate_problem(st.session_state.difficulty)

# === ゲーム中 ===
if st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    remaining = st.session_state.time_limit - elapsed

    if remaining > 0:
        st.write(f"🕒 残り時間: {int(remaining)} 秒")
        st.write(f"🧮 問題: {st.session_state.problem}")
        answer = st.text_input("答えを入力", key=st.session_state.total)

        if answer:
            try:
                if int(answer) == st.session_state.answer:
                    st.success("✅ 正解！")
                    play_sound(True)
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 不正解… 答えは {st.session_state.answer}")
                    play_sound(False)
            except:
                st.warning("⚠️ 数値を入力してください")
                play_sound(False)

            st.session_state.total += 1
            st.session_state.problem, st.session_state.answer = generate_problem(st.session_state.difficulty)
            st.experimental_rerun()

    else:
        st.write("🛑 タイムアップ！")
        st.write(f"✅ 正解数: {st.session_state.score}")
        st.write(f"🔢 問題数: {st.session_state.total}")
        if st.session_state.total > 0:
            rate = st.session_state.score / st.session_state.total * 100
            st.write(f"🎯 正答率: {rate:.1f}%")
        else:
            st.write("😅 1問も答えられませんでした")

