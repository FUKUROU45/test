import streamlit as st

st.title("🎓 高校1年生向け 情報クイズ")

questions = [
    {
        "question": "Q1. 次のうち、デジタルデータの特徴はどれ？",
        "options": ["連続的である", "連続と離散が混在する", "離散的である", "常にアナログ信号である"],
        "answer": "離散的である",
        "explanation": "デジタルデータは、0と1のような離散的な値で表されるのが特徴です。"
    },
    {
        "question": "Q2. コンピュータが使う2進数で「10」は何を表す？",
        "options": ["1", "2", "3", "4"],
        "answer": "2",
        "explanation": "2進数の『10』は、10進数の『2』を表します。"
    },
    {
        "question": "Q3. 強いパスワードの条件として適切なのは？",
        "options": ["誕生日を使う", "8文字以下にする", "英数字と記号を組み合わせる", "同じ文字を繰り返す"],
        "answer": "英数字と記号を組み合わせる",
        "explanation": "強いパスワードには、大文字・小文字・数字・記号の組み合わせが推奨されます。"
    }
]

score = 0

for q in questions:
    st.subheader(q["question"])
    user_answer = st.radio("選択肢を選んでください", q["options"], key=q["question"])
    if st.button("答え合わせ", key="btn_" + q["question"]):
        if user_answer == q["answer"]:
            st.success("正解！ 🎉")
            score += 1
        else:
            st.error("不正解 😢")
        st.info(f"解説：{q['explanation']}")

st.markdown("---")
st.subheader(f"あなたのスコア：{score} / {len(questions)}")



