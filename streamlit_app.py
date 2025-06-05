import streamlit as st
import pandas as pd

st.title("漢字リスト読み込みアプリ")

uploaded_file = st.file_uploader("漢字リストファイル（CSV形式）をアップロードしてください", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("ファイルを正常に読み込みました！")
        st.write(df)
    except Exception as e:
        st.error(f"読み込みエラー: {e}")

