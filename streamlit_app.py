import streamlit as st

# アプリのタイトル
st.title("漢字リスト表示")

# ファイルアップロード
uploaded_file = st.file_uploader("漢字リストをアップロードしてください（テキストファイル）", type=["txt"])

if uploaded_file is not None:
    # ファイルを読み込み、内容を表示
    content = uploaded_file.read().decode("utf-8")
    kanji_list = content.splitlines()

    # 漢字リストを表示
    st.subheader("読み込んだ漢字リスト:")
    for kanji in kanji_list:
        st.write(kanji)

else:
    # ファイルがアップロードされていない場合
    st.info("漢字リストをアップロードしてください。")



