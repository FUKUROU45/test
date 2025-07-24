import streamlit as st
import random

st.title("平方完成の練習アプリ（難易度選択＆解答表示＆次の問題）")

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

# 初回またはレベル変更時に問題生成
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

# 解答と解説表示
if st.button("模範解答を表示"):
    delta = b**2 - 4*a*c
    half = b / (2 * a)
    const = -delta / (4 * a)

    st.markdown("### 模範解答")
    st.markdown(f"{a}*(x + {round(half, 2)})^2 + {round(const, 2)}")

    st.markdown("### 解説（手順）")
    st.markdown(f"""
1. まず、係数を確認します。  
    - \( a \)（エー）：二次の項の係数、ここでは **{a}**  
    - \( b \)（ビー）：一次の項の係数、ここでは **{b}**  
    - \( c \)（シー）：定数項（数字だけの部分）、ここでは **{c}**

2. 「\( b \) を \( 2a \) で割る」計算をします。  
    \[
    \frac{{b}}{{2a}} = \frac{{{b}}}{{2 \times {a}}} = {round(half, 2)}
    \]  
    これは平方完成の中心となる値です。

3. 次に、もとの式のうち、\( x^2 \) と \( x \) の項だけを考え、括弧の中の平方の形に直します。  
    \[
    a x^2 + b x = a \left(x^2 + \frac{{b}}{{a}} x \right)
    \]  
    ここで、括弧内は  
    \[
    x^2 + 2 \times {round(half, 2)} x
    \]  
    と表せます。

4. この形は次の平方の展開と同じ形です。  
    \[
    (x + {round(half, 2)})^2 = x^2 + 2 \times {round(half, 2)} x + \left({round(half, 2)}\right)^2
    \]  
    ですが、もとの式には \(\left({round(half, 2)}\right)^2\) の項がありません。そこで調整が必要です。

5. その調整に使うのが「判別式」と呼ばれる値で、次の式で求められます。  
    \[
    \Delta = b^2 - 4ac = {b}^2 - 4 \times {a} \times {c} = {delta}
    \]

6. 調整項は判別式を使い、次の式で計算します。  
    \[
    -\frac{{\Delta}}{{4a}} = -\frac{{{delta}}}{{4 \times {a}}} = {round(const, 2)}
    \]

7. したがって、もとの式は次のように平方完成できます。  
    \[
    {a} \left(x + {round(half, 2)} \right)^2 + {round(const, 2)}
    \]

---

### 記号の読み方と意味  
- \( x \)（エックス）：変数。未知の数です。  
- \( a, b, c \)：それぞれ係数と定数項。式の形によって値が決まります。  
- \( \Delta \)（デルタ）：判別式。二次方程式の根の性質を調べるのに使いますが、ここでは平方完成の調整に使っています。  
- \( (x + p)^2 \)：\( x \) に何かを足して、それを二乗（かける）した形。平方完成の「完成形」です。

---

ご不明点あれば遠慮なくどうぞ！  
さらに機能追加もお手伝いします😊
""")

# 「次の問題」ボタン
if st.button("次の問題"):
    st.session_state.current_problem = generate_problem(level)
    st.experimental_rerun()



