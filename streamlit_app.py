import streamlit as st
import sympy as sp

def explain_solution_simple(a, b, c):
    explanation = f"二次式：{a}x² + {b}x + {c}\n\n"

    # 平方完成の計算
    h = b / (2 * a)
    k = c - a * h**2

    explanation += f"平方完成の形は次の通りです：\n"
    explanation += f"{a}(x + ({-h}))² + ({k})\n\n"

    # 検算部分(sympyで元の式と完成形の一致を確認)
    x = sp.symbols('x')
    original_expr = a * x**2 + b * x + c
    completed_expr = a * (x + (-h))**2 + k

    original_expanded = sp.expand(original_expr)
    completed_expanded = sp.expand(completed_expr)

    explanation += f"元の式を展開すると： {original_expanded}\n"
    explanation += f"平方完成形を展開すると： {completed_expanded}\n"

    # 差が0かどうか
    if sp.simplify(original_expanded - completed_expanded) == 0:
        explanation += "検算結果：展開した式は元の式と一致します ✅\n"
    else:
        explanation += "検算結果：展開した式は元の式と一致しません ❌\n"

    return explanation

def main():
    st.title("二次式の平方完成説明ツール")

    st.write("二次式の係数を入力してください。")

    a = st.number_input("a (2次の係数)", value=1.0, step=0.1)
    b = st.number_input("b (1次の係数)", value=0.0, step=0.1)
    c = st.number_input("c (定数項)", value=0.0, step=0.1)

    if st.button("平方完成の説明を表示"):
        if a == 0:
            st.error("aは0以外の値を入力してください。")
        else:
            explanation = explain_solution_simple(a, b, c)
            st.text(explanation)

if __name__ == "__main__":
    main()
