import streamlit as st
import random

st.title("平方完成の練習アプリ（難易度選択＆解答表示）")

# 難易度選択
level = st.selectbox("難易度を選んでください", ["初級", "中級", "上級"])

def generate_problem(level):
    if level == "初級":
        a = 1
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
    elif level == "中級":
        a = random.choice([1, -1, 2, -2])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
    else:  # 上級
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-20, 20)
        c = random.randint(-20, 20)
    return (a, b, c)

def is_correct_answer(a, b, c, user_str):
    try:
        half_b_over_a = b / (2 * a)
        expected_term1 = f"(x + {round(half_b_over_a, 2)})"
        expected_term2 = f"(x - {round(-half_b_over_a, 2)})"
        delta = b**2 - 4*a*c
        const_term = -delta / (4 * a)
        if (expected_term1 in user_str or expected_term2 in user_str) and str(round(const_term, 2)) in user_str:
            return True
        else:
            return False
    except:
        return False

if "current_problem" not in st.session_state or st.session_state.get("last_level", None) != level:
    st.session_state.current_problem = generate_problem(level)
    st.session_state.last_level = level

a, b, c = st.session_state.current_problem

st.markdown(f"次の式を平方完成してください。")
st.latex(f"{a}x^2 + {b}x + {c}")

user_input = st.text_input("平方完成した式を入力してください（例：2*(x + 3)**2 - 5）")

if user_input:
    correct = is_correct_answer(a, b, c, user_input)
    if correct:
        st.success("正解です！🎉")
    else:
        st.error("残念、不正解です。")

if st.button("模範解答を表示"):
    delta = b**2 - 4*a*c
    half = b / (2 * a)
    const = -delta / (4 * a)
    
    st.markdown("### 模範解答")
    st.markdown(f"{a}*(x + {round(half, 2)})^2 + {round(const, 2)}")

    st.markdown("### 解説（手順）")
    st.markdown(f"""
1. 係数 \( a = {a} \)、\( b = {b} \)、定数項 \( c = {c} \) を確認します。  
2. \(\displaystyle \frac{{b}}{{2a}} = \frac{{{b}}}{{2 \times {a}}} = {round(half, 2)}\) を計算します。  
3. 式の中の \( x^2 \) と \( x \) の項をまとめて、平方の形に変えます:  
\[
a x^2 + b x = a \left(x^2 + \frac{{b}}{{a}} x \right) = a \left(x^2 + 2 \times {round(half, 2)} x \right)
\]  
4. 平方の形に直すために、  
\[
a \left(x + {round(half, 2)} \right)^2 = a \left( x^2 + 2 \times {round(half, 2)} x + \left({round(half, 2)}\right)^2 \right)
\]  
なので、元の式との差を調整します。  
5. 判別式を使って調整項を求めます。  
\[
\Delta = b^2 - 4ac = {b}^2 - 4 \times {a} \times {c} = {delta}
\]

調整項は、
\[
-\frac{{\Delta}}{{4a}} = -\frac{{{delta}}}{{4 \times {a}}} = {round(const, 2)}
\]

6. よって平方完成の形は、
\[
{a} \left(x + {round(half, 2)} \right)^2 + {round(const, 2)}
\]
となります。
    """)


