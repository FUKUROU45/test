import streamlit as st
import random
import time

def generate_question():
    # 平方完成の問題を作る
    # 例: x^2 + bx + c の形。bは偶数にすることで平方完成しやすく
    b = random.choice(range(-10, 11, 2))  # 偶数のみ
    # cは b^2/4 + 定数
    # だからcは (b/2)^2 + q として q は -10〜10
    q = random.randint(-10, 10)
    c = (b/2)**2 + q
    # 問題は x^2 + b x + c = 0の平方完成を答える（p, q）
    # 平方完成形は (x + b/2)^2 + q
    return b, c, (b/2, q)

def main():
    st.title("🧮 高速平方完成マルチプレイヤーゲーム")

    if "players" not in st.session_state:
        st.session_state.players = []
    if "player_scores" not in st.session_state:
        st.session_state.player_scores = {}
    if "current_player_idx" not in st.session_state:
        st.session_state.current_player_idx = 0
    if "game_state" not in st.session_state:
        st.session_state.game_state = "setup"  # setup, playing, ended
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "game_duration" not in st.session_state:
        st.session_state.game_duration = 60
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    # ゲームセットアップ画面
    if st.session_state.game_state == "setup":
        st.subheader("👥 プレイヤー設定")
        new_player = st.text_input("プレイヤー名を入力:")
        if st.button("プレイヤー追加") and new_player:
            if new_player not in st.session_state.players:
                st.session_state.players.append(new_player)
                st.session_state.player_scores[new_player] = 0
                st.success(f"{new_player}を追加しました！")
            else:
                st.error("そのプレイヤー名は既に存在します。")

        if st.session_state.players:
            st.write("**現在のプレイヤー:**")
            for i, p in enumerate(st.session_state.players):
                st.write(f"{i+1}. {p} (得点: {st.session_state.player_scores[p]})")

        if st.button("プレイヤーリストをリセット"):
            st.session_state.players = []
            st.session_state.player_scores = {}

        st.subheader("制限時間を選択してください（秒）")
        duration = st.selectbox("制限時間", [30, 60, 90, 120], index=[30, 60, 90, 120].index(st.session_state.game_duration))
        st.session_state.game_duration = duration

        if len(st.session_state.players) >= 2:
            if st.button("ゲームスタート"):
                st.session_state.game_state = "playing"
                st.session_state.start_time = time.time()
                st.session_state.current_player_idx = 0
                st.session_state.current_question = generate_question()
                st.session_state.answer_submitted = False
                st.experimental_rerun()
        else:
            st.info("マルチプレイヤーゲームには最低2人のプレイヤーが必要です。")

    # ゲーム中画面
    elif st.session_state.game_state == "playing":
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.game_duration - elapsed
        if remaining <= 0:
            st.session_state.game_state = "ended"
            st.experimental_rerun()

        current_player = st.session_state.players[st.session_state.current_player_idx]
        st.subheader(f"🎯 現在のプレイヤー: {current_player}")
        st.write(f"残り時間: {int(remaining)}秒")

        b, c, (p_correct, q_correct) = st.session_state.current_question
        st.write(f"問題: 次の式を平方完成してください。\n\n`x² + {b}x + {round(c, 2)}`\n\n答えは `(x + p)² + q` の形で入力してください。")

        with st.form("answer_form"):
            p_input = st.text_input("pの値 (例: -3.5)")
            q_input = st.text_input("qの値 (例: 2)")
            submitted = st.form_submit_button("回答")

            if submitted:
                try:
                    p_user = float(p_input)
                    q_user = float(q_input)
                    # 小数第2位まで丸めて比較
                    if round(p_user, 2) == round(p_correct, 2) and round(q_user, 2) == round(q_correct, 2):
                        st.success("正解！")
                        st.session_state.player_scores[current_player] += 1
                    else:
                        st.error(f"不正解。正しい答えは p={round(p_correct, 2)}, q={round(q_correct, 2)} です。")
                    st.session_state.answer_submitted = True
                except:
                    st.error("数値で入力してください。")

        if st.session_state.answer_submitted:
            if st.button("次の問題へ"):
                st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                st.session_state.current_question = generate_question()
                st.session_state.answer_submitted = False
                st.experimental_rerun()

        st.subheader("📊 スコアボード")
        for p in st.session_state.players:
            st.write(f"{p}: {st.session_state.player_scores[p]}点")

    # ゲーム終了画面
    else:
        st.subheader("⌛ ゲーム終了")
        st.write("最終スコア:")
        for p in st.session_state.players:
            st.write(f"{p}: {st.session_state.player_scores[p]}点")

        if st.button("リスタート"):
            for key in ["game_state", "players", "player_scores", "current_player_idx", "start_time", "current_question", "answer_submitted"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()
