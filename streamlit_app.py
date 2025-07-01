import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, sympify

# タイトル
st.title("関数の問題を解こう")

# 数式入力（ユーザー）
expression = st.text_input("関数を入力してください（例: x**2 + 2*x + 1）", "x**2 + 2*x + 1")

# x のシンボル
x = symbols('x')

# 数式を解析する
try:
    func = sympify(expression)
except:
    st.error("無効な数式です。正しい数式を入力してください。")
    func = None

# 関数を描画する
if func:
    st.subheader("関数のグラフを表示")
    
    # xの範囲を設定
    x_vals = np.linspace(-10, 10, 400)
    y_vals = np.array([float(func.subs(x, val)) for val in x_vals])

    # グラフを描画
    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_vals, label=str(func))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f"グラフ: y = {func}")
    plt.grid(True)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.legend(loc="upper left")
    
    st.pyplot(plt)

    # 特定の x 値で関数を計算
    x_value = st.number_input("x の値を入力してください", value=0)
    
    try:
        y_value = func.subs(x, x_value)
        st.write(f"f({x_value}) = {y_value}")
    except:
        st.error("関数の計算に失敗しました。")

