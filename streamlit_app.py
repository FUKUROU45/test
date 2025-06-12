import streamlit as st

st.title("⭕✖️ マルバツゲーム")

# セッションステートで盤面とターンを管理
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "⭕"  # 先攻は⭕
    st.session_state.winner = None

def check_winner(board):
    # 横・縦・斜めで3つ揃っているかチェック
    lines = []

    # 横
    lines.extend(board)
    # 縦
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])
    # 斜め
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line == ["⭕", "⭕", "⭕"]:
            return "⭕"
        if line == ["✖️", "✖️", "✖️"]:
            return "✖️"
    return None

def board_full(board):
    for row in board:
        if "" in row:
            return False
    return True

# ボタンでマスをクリックするとマークを置く処理
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        label = st.session_state.board[r][c] if st.session_state.board[r][c] != "" else " "
        if cols[c].button(label, key=f"{r}-{c}"):
            if st.session_state.winner or st.session_state.board[r][c] != "":
                # 勝者がいるか、すでにマークがあれば何もしない
                pass
            else:
                st.session_state.board[r][c] = st.session_state.turn
                st.session_state.winner = check_winner(st.session_state.board)
                if st.session_state.winner:
                    st.success(f"勝者は {st.session_state.winner} です！")
                elif board_full(st.session_state.board):
                    st.info("引き分けです！")
                    st.session_state.winner = "引き分け"
                else:
                    # ターン交代
                    st.session_state.turn = "✖️" if st.session_state.turn == "⭕" else "⭕"

st.write(f"現在のターン: {st.session_state.turn}")

# リセットボタン
if st.button("ゲームをリセット"):
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "⭕"
    st.session_state.winner = None
    st.experimental_rerun()




