import streamlit as st

# アプリの状態を保持するセッション状態を使う方法
if 'counter' not in st.session_state:
    st.session_state.counter = 0  # 初期カウンター値

# ボタンを押すとカウントアップする
if st.button('カウントアップ'):
    st.session_state.counter += 1

# カウントの表示
st.write(f'現在のカウント: {st.session_state.counter}')

# 再実行ボタン
if st.button('再実行'):
    # 再実行をトリガーする条件を確認
    if st.session_state.counter > 0:  # 例えば、カウントが1以上の場合のみ再実行
        st.experimental_rerun()

# その他のUI要素
st.write("Streamlitアプリが再実行されました！")
