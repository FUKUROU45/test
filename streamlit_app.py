import streamlit as st
from PIL import Image
import time

st.title("清瀧でGO！🚆")

# 画像の表示（清瀧駅）
st.subheader("現在地：清瀧駅")
image = Image.open("kiyotaki_station.jpg")  # 手元にある清瀧駅の写真など
st.image(image, caption="清瀧駅ホーム", use_column_width=True)

# 速度調整スライダー
speed = st.slider("速度（km/h）", 0, 120, 0, 5)

# 運転開始ボタン
if st.button("運転開始！"):
    st.write("発車します！")
    for s in range(0, speed, 5):
        st.write(f"加速中… 現在の速度: {s} km/h")
        time.sleep(0.5)
    st.success("走行中！")

# 停車テスト
st.subheader("ブレーキテスト")
if st.button("ブレーキ！"):
    st.warning("減速中...")
    for s in range(speed, -1, -10):
        st.write(f"速度: {s} km/h")
        time.sleep(0.5)
    st.success("停止しました。")

# 評価（簡易）
st.subheader("運転評価")
if st.button("評価する"):
    if speed <= 80:
        st.success("安全運転です！")
    else:
        st.error("速度超過！もっとゆっくり運転しましょう。")
