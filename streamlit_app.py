import streamlit as st

def main():
    st.title("🧮 四則演算計算機")
    st.write("簡単な計算機アプリです")
    
    # サイドバーで計算方法を選択
    st.sidebar.header("計算設定")
    calc_mode = st.sidebar.selectbox(
        "計算モードを選択してください",
        ["基本計算", "連続計算", "履歴付き計算"]
    )
    
    if calc_mode == "基本計算":
        basic_calculator()
    elif calc_mode == "連続計算":
        continuous_calculator()
    else:
        history_calculator()

def basic_calculator():
    """基本的な四則演算"""
    st.header("基本計算")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num1 = st.number_input("数値1", value=0.0, format="%.2f")
    
    with col2:
        operation = st.selectbox("演算子", ["+", "-", "×", "÷"])
    
    with col3:
        num2 = st.number_input("数値2", value=0.0, format="%.2f")
    
    if st.button("計算実行", type="primary"):
        result = calculate(num1, operation, num2)
        if result is not None:
            st.success(f"結果: {num1} {operation} {num2} = **{result}**")
        else:
            st.error("0で割ることはできません")

def continuous_calculator():
    """連続計算モード"""
    st.header("連続計算")
    
    # セッション状態の初期化
    if 'current_value' not in st.session_state:
        st.session_state.current_value = 0.0
    if 'display_calculation' not in st.session_state:
        st.session_state.display_calculation = "0"
    
    # 現在の値を表示
    st.metric("現在の値", st.session_state.current_value)
    st.code(st.session_state.display_calculation)
    
    col1, col2 = st.columns(2)
    
    with col1:
        operation = st.selectbox("演算子", ["+", "-", "×", "÷"], key="cont_op")
        num = st.number_input("数値", value=0.0, format="%.2f", key="cont_num")
    
    with col2:
        if st.button("計算", type="primary"):
            result = calculate(st.session_state.current_value, operation, num)
            if result is not None:
                st.session_state.display_calculation += f" {operation} {num} = {result}"
                st.session_state.current_value = result
                st.rerun()
            else:
                st.error("0で割ることはできません")
        
        if st.button("クリア"):
            st.session_state.current_value = 0.0
            st.session_state.display_calculation = "0"
            st.rerun()

def history_calculator():
    """履歴付き計算"""
    st.header("履歴付き計算")
    
    # 履歴の初期化
    if 'calculation_history' not in st.session_state:
        st.session_state.calculation_history = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num1 = st.number_input("数値1", value=0.0, format="%.2f", key="hist_num1")
    
    with col2:
        operation = st.selectbox("演算子", ["+", "-", "×", "÷"], key="hist_op")
    
    with col3:
        num2 = st.number_input("数値2", value=0.0, format="%.2f", key="hist_num2")
    
    col_calc, col_clear = st.columns(2)
    
    with col_calc:
        if st.button("計算実行", type="primary", key="hist_calc"):
            result = calculate(num1, operation, num2)
            if result is not None:
                calculation = f"{num1} {operation} {num2} = {result}"
                st.session_state.calculation_history.append(calculation)
                st.success(f"結果: **{result}**")
                st.rerun()
            else:
                st.error("0で割ることはできません")
    
    with col_clear:
        if st.button("履歴クリア"):
            st.session_state.calculation_history = []
            st.rerun()
    
    # 履歴表示
    if st.session_state.calculation_history:
        st.subheader("計算履歴")
        for i, calc in enumerate(reversed(st.session_state.calculation_history[-10:]), 1):
            st.write(f"{i}. {calc}")

def calculate(num1, operation, num2):
    """四則演算を実行"""
    try:
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "×":
            return num1 * num2
        elif operation == "÷":
            if num2 == 0:
                return None
            return num1 / num2
    except Exception:
        return None

def show_tips():
    """使い方のヒント"""
    with st.expander("💡 使い方のヒント"):
        st.write("""
        **基本計算**: 単発の計算を行います
        
        **連続計算**: 前の計算結果を使って続けて計算できます
        
        **履歴付き計算**: 過去の計算履歴を確認できます（最新10件まで表示）
        
        **注意事項**:
        - 0で割る計算はエラーになります
        - 小数点以下2桁まで入力可能です
        """)

if __name__ == "__main__":
    # ヒント表示
    show_tips()
    
    # メインアプリ実行
    main()
    
    # フッター
    st.markdown("---")
    st.markdown("*Streamlit四則演算アプリ*")