import streamlit as st
import pandas as pd

st.title("Excel 漢字リスト表示アプリ")

# Excelファイルをアップロード
uploaded_file = st.file_uploader("Excelファイル（.xlsx）をアップロードしてください", type=["xlsx"])

if uploaded_file is not None:
    # ExcelをDataFrameに読み込む
    df = pd.read_excel(uploaded_file)

    # データフレームの内容を表示
    st.subheader("読み込んだデータ")
    st.dataframe(df)

else:
    st.info("左上のボタンからExcelファイルをアップロードしてください。")
