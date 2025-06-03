import streamlit as st

# サンプル漢検級別漢字データ
kanji_data = {
    "10級": ["日", "月", "火", "水", "木", "金", "土"],
    "9級": ["犬", "虫", "耳", "花", "竹", "糸", "石"],
    "8級": ["海", "風", "雪", "星", "空", "雨", "音"],
    "7級": ["開", "閉", "通", "運", "駅", "歩", "走"],
    "6級": ["重", "軽", "計", "算", "数", "答", "問"]
}

st.title("漢字でGO！〜級別漢字リスト〜")

# ユーザーに漢検級を選ばせる
selected_level = st.selectbox("漢検の級を選んでください（例：10級が最も簡単）", list(kanji_data.keys()))

# 選んだ級の漢字リストを表示
st.subheader(f"{selected_level} の漢字一覧")
st.write("、".join(kanji_data[selected_level]))

