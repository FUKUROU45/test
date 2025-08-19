import streamlit as st

# サンプル問題リスト（問題文と選択肢、正解インデックス）
questions = [
    {
        "question": "Pythonの関数定義はどれ？",
        "choices": ["func myfunc():", "def myfunc():", "function myfunc():"],
        "answer": 1
    },
    {
        "question": "変数xに5を代入する正しい文は？",
        "choices": ["x == 5", "x = 5", "let x = 5"],
        "answer": 1
    },
    {
        "question": "リストの末尾に要素を追加するメソッドは？",
        "choices": ["append()", "add()", "push()"],
        "answer": 0
    }
]

st.title("問題をすべて答えてから採点")

# 全問の回答を表示して入力を受け取る
for i, q in enumerate(questions):
    st.write(f"### 問題{i+1}: {q['question']}")
    selected_key = f"selected_{i}"

    # st.session_stateの初期化（Noneや未登録の場合は0に）
    if selected_key not in st.session_state or st.session_state[selected_key] is None:
        st.session_state[selected_key] = 0

    selected = st.radio(
        "選択肢：",
        options=range(len(q['choices'])),
        format_func=lambda x, choices=q['choices']: f"{chr(65 + x)}. {choices[x]}",
        key=selected_key,
        index=st.session_state[selected_key]
    )
    st.write("---")

# 採点ボタン
if st.button("採点する"):
    correct_count = 0
    st.write("## 採点結果")
    for i, q in enumerate(questions):
        selected_key = f"selected_{i}"
        user_ans = st.session_state[selected_key]
        correct = user_ans == q["answer"]
        if correct:
            correct_count += 1
        st.write(f"問題{i+1}: あなたの答え → {chr(65 + user_ans)}. {q['choices'][user_ans]}")
        st.write(f"正解 → {chr(65 + q['answer'])}. {q['choices'][q['answer']]}")
        st.write(f"結果: {'✅ 正解' if correct else '❌ 不正解'}")
        st.write("---")
    st.write(f"### 合計: {correct_count} / {len(questions)} 問正解しました！")

