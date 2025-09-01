import streamlit as st
import re
import math

def main():
    st.title("🧮 四則演算計算機")
    st.write("レベル別計算機アプリです")
    
    # サイドバーでレベルと計算方法を選択
    st.sidebar.header("設定")
    level = st.sidebar.selectbox(
        "レベルを選択してください",
        ["初級", "中級", "上級"]
    )
    
    calc_mode = st.sidebar.selectbox(
        "計算モードを選択してください",
        ["基本計算", "連続計算", "履歴付き計算"]
    )
    
    # レベル説明
    show_level_info(level)
    
    if calc_mode == "基本計算":
        basic_calculator(level)
    elif calc_mode == "連続計算":
        continuous_calculator(level)
    else:
        history_calculator(level)

def show_level_info(level):
    """レベル情報を表示"""
    if level == "初級":
        st.info("🟢 **初級**: 基本的な四則演算（+, -, ×, ÷）")
    elif level == "中級":
        st.info("🟡 **中級**: 四則演算 + 累乗（^）+ 平方根（√）")
    else:
        st.info("🔴 **上級**: 文字式の計算（x, y使用可）+ 全ての演算")

def basic_calculator(level):
    """基本的な四則演算"""
    st.header("基本計算")
    
    if level == "上級":
        # 上級：式入力モード
        st.subheader("式を入力してください")
        st.write("例: 2*x + 3, x^2 + 2*x + 1, (x+1)*(x-1)")
        
        expression = st.text_input("計算式", placeholder="例: 2*x + 3")
        x_value = st.number_input("xの値", value=1.0, format="%.2f")
        y_value = st.number_input("yの値（使用する場合）", value=1.0, format="%.2f")
        
        if st.button("計算実行", type="primary"):
            if expression:
                result = calculate_expression(expression, x_value, y_value)
                if result is not None:
                    st.success(f"結果: {expression} (x={x_value}, y={y_value}) = **{result}**")
                else:
                    st.error("式の計算でエラーが発生しました")
            else:
                st.warning("計算式を入力してください")
    else:
        # 初級・中級：通常モード
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num1 = st.number_input("数値1", value=0.0, format="%.2f")
        
        with col2:
            if level == "初級":
                operations = ["+", "-", "×", "÷"]
            else:  # 中級
                operations = ["+", "-", "×", "÷", "^", "√"]
            operation = st.selectbox("演算子", operations)
        
        with col3:
            if operation == "√":
                st.write("√の計算（数値1の平方根）")
                num2 = None
            else:
                num2 = st.number_input("数値2", value=0.0, format="%.2f")
        
        if st.button("計算実行", type="primary"):
            result = calculate(num1, operation, num2)
            if result is not None:
                if operation == "√":
                    st.success(f"結果: √{num1} = **{result}**")
                else:
                    st.success(f"結果: {num1} {operation} {num2} = **{result}**")
            else:
                st.error("計算エラーが発生しました")

def continuous_calculator(level):
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
    
    if level == "上級":
        # 上級：式入力モード
        st.subheader("現在の値を使った式計算")
        st.write("現在の値をxとして使用します")
        
        expression = st.text_input("計算式", placeholder="例: x + 5, x^2, 2*x + 3")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("計算", type="primary"):
                if expression:
                    # 現在の値をxとして代入
                    result = calculate_expression(expression, st.session_state.current_value, 0)
                    if result is not None:
                        st.session_state.display_calculation += f" → {expression.replace('x', str(st.session_state.current_value))} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("式の計算でエラーが発生しました")
                else:
                    st.warning("計算式を入力してください")
        
        with col2:
            if st.button("クリア"):
                st.session_state.current_value = 0.0
                st.session_state.display_calculation = "0"
                st.rerun()
    else:
        # 初級・中級：通常モード
        col1, col2 = st.columns(2)
        
        with col1:
            if level == "初級":
                operations = ["+", "-", "×", "÷"]
            else:  # 中級
                operations = ["+", "-", "×", "÷", "^", "√"]
            operation = st.selectbox("演算子", operations, key="cont_op")
            
            if operation != "√":
                num = st.number_input("数値", value=0.0, format="%.2f", key="cont_num")
            else:
                num = None
        
        with col2:
            if st.button("計算", type="primary"):
                if operation == "√":
                    result = math.sqrt(st.session_state.current_value) if st.session_state.current_value >= 0 else None
                    if result is not None:
                        st.session_state.display_calculation += f" → √{st.session_state.current_value} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("負の数の平方根は計算できません")
                else:
                    result = calculate(st.session_state.current_value, operation, num)
                    if result is not None:
                        st.session_state.display_calculation += f" {operation} {num} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("計算エラーが発生しました")
            
            if st.button("クリア"):
                st.session_state.current_value = 0.0
                st.session_state.display_calculation = "0"
                st.rerun()

def history_calculator(level):
    """履歴付き計算"""
    st.header("履歴付き計算")
    
    # 履歴の初期化
    if 'calculation_history' not in st.session_state:
        st.session_state.calculation_history = []
    
    if level == "上級":
        # 上級：式入力モード
        st.subheader("式を入力してください")
        expression = st.text_input("計算式", placeholder="例: 2*x^2 + 3*x + 1", key="hist_expr")
        
        col1, col2 = st.columns(2)
        with col1:
            x_value = st.number_input("xの値", value=1.0, format="%.2f", key="hist_x")
        with col2:
            y_value = st.number_input("yの値", value=1.0, format="%.2f", key="hist_y")
        
        col_calc, col_clear = st.columns(2)
        
        with col_calc:
            if st.button("計算実行", type="primary", key="hist_calc_adv"):
                if expression:
                    result = calculate_expression(expression, x_value, y_value)
                    if result is not None:
                        calculation = f"{expression} (x={x_value}, y={y_value}) = {result}"
                        st.session_state.calculation_history.append(calculation)
                        st.success(f"結果: **{result}**")
                        st.rerun()
                    else:
                        st.error("式の計算でエラーが発生しました")
                else:
                    st.warning("計算式を入力してください")
        
        with col_clear:
            if st.button("履歴クリア", key="hist_clear_adv"):
                st.session_state.calculation_history = []
                st.rerun()
    else:
        # 初級・中級：通常モード
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num1 = st.number_input("数値1", value=0.0, format="%.2f", key="hist_num1")
        
        with col2:
            if level == "初級":
                operations = ["+", "-", "×", "÷"]
            else:  # 中級
                operations = ["+", "-", "×", "÷", "^", "√"]
            operation = st.selectbox("演算子", operations, key="hist_op")
        
        with col3:
            if operation == "√":
                st.write("√の計算（数値1の平方根）")
                num2 = None
            else:
                num2 = st.number_input("数値2", value=0.0, format="%.2f", key="hist_num2")
        
        col_calc, col_clear = st.columns(2)
        
        with col_calc:
            if st.button("計算実行", type="primary", key="hist_calc"):
                result = calculate(num1, operation, num2)
                if result is not None:
                    if operation == "√":
                        calculation = f"√{num1} = {result}"
                    else:
                        calculation = f"{num1} {operation} {num2} = {result}"
                    st.session_state.calculation_history.append(calculation)
                    st.success(f"結果: **{result}**")
                    st.rerun()
                else:
                    st.error("計算エラーが発生しました")
        
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
        elif operation == "^":
            return num1 ** num2
        elif operation == "√":
            if num1 < 0:
                return None
            return math.sqrt(num1)
    except Exception:
        return None

def calculate_expression(expression, x_value, y_value=0):
    """文字式を計算"""
    try:
        # 式を安全な形に変換
        safe_expr = prepare_expression(expression, x_value, y_value)
        if safe_expr is None:
            return None
        
        # 計算実行
        result = eval(safe_expr)
        return round(result, 6)  # 小数点以下6桁で丸める
    except Exception:
        return None

def prepare_expression(expression, x_value, y_value):
    """式を安全に評価できる形に変換"""
    try:
        # 小文字に統一
        expr = expression.lower().replace(" ", "")
        
        # 危険な関数や文字をチェック
        forbidden = ['import', 'exec', 'eval', '__', 'open', 'file']
        if any(word in expr for word in forbidden):
            return None
        
        # 変数を値で置換
        expr = expr.replace('x', str(x_value))
        expr = expr.replace('y', str(y_value))
        
        # ^を**に変換（累乗）
        expr = expr.replace('^', '**')
        
        # √を数学関数に変換
        expr = re.sub(r'√\(([^)]+)\)', r'math.sqrt(\1)', expr)
        expr = re.sub(r'√(\d+(?:\.\d+)?)', r'math.sqrt(\1)', expr)
        
        # 暗黙の乗算を明示的に（例：2x → 2*x）
        expr = re.sub(r'(\d)([a-z])', r'\1*\2', expr)
        expr = re.sub(r'([a-z])(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
        
        # 許可された文字のみかチェック
        allowed_chars = set('0123456789+-*/.()** ')
        if not all(c in allowed_chars or c.isspace() for c in expr.replace('math.sqrt', '')):
            # math.sqrt部分を除いて文字チェック
            clean_expr = expr.replace('math.sqrt', '')
            if not all(c in allowed_chars for c in clean_expr):
                return None
        
        return expr
    except Exception:
        return None

def continuous_calculator(level):
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
    
    if level == "上級":
        # 上級：式入力モード
        st.subheader("現在の値を使った式計算")
        st.write("現在の値をxとして使用します")
        
        expression = st.text_input("計算式", placeholder="例: x + 5, x^2, 2*x + 3")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("計算", type="primary"):
                if expression:
                    # 現在の値をxとして代入
                    result = calculate_expression(expression, st.session_state.current_value, 0)
                    if result is not None:
                        st.session_state.display_calculation += f" → {expression.replace('x', str(st.session_state.current_value))} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("式の計算でエラーが発生しました")
                else:
                    st.warning("計算式を入力してください")
        
        with col2:
            if st.button("クリア"):
                st.session_state.current_value = 0.0
                st.session_state.display_calculation = "0"
                st.rerun()
    else:
        # 初級・中級：通常モード
        col1, col2 = st.columns(2)
        
        with col1:
            if level == "初級":
                operations = ["+", "-", "×", "÷"]
            else:  # 中級
                operations = ["+", "-", "×", "÷", "^", "√"]
            operation = st.selectbox("演算子", operations, key="cont_op")
            
            if operation != "√":
                num = st.number_input("数値", value=0.0, format="%.2f", key="cont_num")
            else:
                num = None
        
        with col2:
            if st.button("計算", type="primary"):
                if operation == "√":
                    if st.session_state.current_value >= 0:
                        result = math.sqrt(st.session_state.current_value)
                        st.session_state.display_calculation += f" → √{st.session_state.current_value} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("負の数の平方根は計算できません")
                else:
                    result = calculate(st.session_state.current_value, operation, num)
                    if result is not None:
                        st.session_state.display_calculation += f" {operation} {num} = {result}"
                        st.session_state.current_value = result
                        st.rerun()
                    else:
                        st.error("計算エラーが発生しました")
            
            if st.button("クリア"):
                st.session_state.current_value = 0.0
                st.session_state.display_calculation = "0"
                st.rerun()

def history_calculator(level):
    """履歴付き計算"""
    st.header("履歴付き計算")
    
    # 履歴の初期化
    if 'calculation_history' not in st.session_state:
        st.session_state.calculation_history = []
    
    if level == "上級":
        # 上級：式入力モード
        st.subheader("式を入力してください")
        expression = st.text_input("計算式", placeholder="例: 2*x^2 + 3*x + 1", key="hist_expr")
        
        col1, col2 = st.columns(2)
        with col1:
            x_value = st.number_input("xの値", value=1.0, format="%.2f", key="hist_x")
        with col2:
            y_value = st.number_input("yの値", value=1.0, format="%.2f", key="hist_y")
        
        col_calc, col_clear = st.columns(2)
        
        with col_calc:
            if st.button("計算実行", type="primary", key="hist_calc_adv"):
                if expression:
                    result = calculate_expression(expression, x_value, y_value)
                    if result is not None:
                        calculation = f"{expression} (x={x_value}, y={y_value}) = {result}"
                        st.session_state.calculation_history.append(calculation)
                        st.success(f"結果: **{result}**")
                        st.rerun()
                    else:
                        st.error("式の計算でエラーが発生しました")
                else:
                    st.warning("計算式を入力してください")
        
        with col_clear:
            if st.button("履歴クリア", key="hist_clear_adv"):
                st.session_state.calculation_history = []
                st.rerun()
    else:
        # 初級・中級：通常モード
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num1 = st.number_input("数値1", value=0.0, format="%.2f", key="hist_num1")
        
        with col2:
            if level == "初級":
                operations = ["+", "-", "×", "÷"]
            else:  # 中級
                operations = ["+", "-", "×", "÷", "^", "√"]
            operation = st.selectbox("演算子", operations, key="hist_op")
        
        with col3:
            if operation == "√":
                st.write("√の計算（数値1の平方根）")
                num2 = None
            else:
                num2 = st.number_input("数値2", value=0.0, format="%.2f", key="hist_num2")
        
        col_calc, col_clear = st.columns(2)
        
        with col_calc:
            if st.button("計算実行", type="primary", key="hist_calc"):
                result = calculate(num1, operation, num2)
                if result is not None:
                    if operation == "√":
                        calculation = f"√{num1} = {result}"
                    else:
                        calculation = f"{num1} {operation} {num2} = {result}"
                    st.session_state.calculation_history.append(calculation)
                    st.success(f"結果: **{result}**")
                    st.rerun()
                else:
                    st.error("計算エラーが発生しました")
        
        with col_clear:
            if st.button("履歴クリア"):
                st.session_state.calculation_history = []
                st.rerun()
    
    # 履歴表示
    if st.session_state.calculation_history:
        st.subheader("計算履歴")
        for i, calc in enumerate(reversed(st.session_state.calculation_history[-10:]), 1):
            st.write(f"{i}. {calc}")

def show_tips():
    """使い方のヒント"""
    with st.expander("💡 使い方のヒント"):
        st.write("""
        **レベル別機能**:
        - **初級**: 基本四則演算（+, -, ×, ÷）
        - **中級**: 四則演算 + 累乗（^）+ 平方根（√）
        - **上級**: 文字式計算（x, y使用可）
        
        **上級の式入力例**:
        - `2*x + 3` （一次式）
        - `x^2 + 2*x + 1` （二次式）
        - `(x+1)*(x-1)` （因数分解形）
        - `x^2 + y^2` （二変数）
        
        **計算モード**:
        - **基本計算**: 単発の計算
        - **連続計算**: 前の結果を使って続けて計算
        - **履歴付き計算**: 計算履歴を確認（最新10件）
        
        **注意事項**:
        - 累乗は x^2 の形式で入力
        - 0で割る計算はエラー
        - 負の数の平方根はエラー
        """)

if __name__ == "__main__":
    # ヒント表示
    show_tips()
    
    # メインアプリ実行
    main()
    
    # フッター
    st.markdown("---")
    st.markdown("*レベル別四則演算アプリ - Streamlit*")