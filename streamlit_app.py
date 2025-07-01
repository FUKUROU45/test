import streamlit as st

st.title("四則演算ウェブアプリ")

# ユーザー入力
num1 = st.number_input("1つ目の数値を入力してください", value=0.0)
num2 = st.number_input("2つ目の数値を入力してください", value=0.0)

operation = st.selectbox("演算子を選んでください", ("足し算 (+)", "引き算 (-)", "掛け算 (×)", "割り算 (÷)"))

# 計算
def calculate(n1, n2, op):
    if op == "足し算 (+)":
        return n1 + n2
    elif op == "引き算 (-)":
        return n1 - n2
    elif op == "掛け算 (×)":
        return n1 * n2
    elif op == "割り算 (÷)":
        if n2 == 0:
            return "エラー（0で割ることはできません）"
        return n1 / n2

# ボタンで実行
if st.button("計算する"):
    result = calculate(num1, num2, operation)
    st.success(f"計算結果： {result}")
