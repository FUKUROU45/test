import streamlit as st

st.title("漢字リスト表示アプリ")

# ファイルアップロードオプション（任意）
uploaded_file = st.file_uploader("漢字リストファイルをアップロードしてください（1文字ずつ改行）", type=["txt"])

if uploaded_file is not None:
    # ファイルを読み込んで表示
    content = uploaded_file.read().decode("utf-8")
    kanji_list = content.splitlines()

    st.subheader("読み込んだ漢字リスト")
    for kanji in kanji_list:
        st.write(kanji)
else:
    st.info("上のファイルアップロードから漢字リストを読み込んでください。")



