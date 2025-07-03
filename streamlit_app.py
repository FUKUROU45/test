import streamlit as st
import random

st.title("📝 英検3級レベルクイズ")

# 問題リスト（選択式）
quiz_list = [
    {
        "question": "She ___ to school every day.",
        "choices": ["go", "goes", "went", "going"],
        "answer": "goes"
    },
    {
        "question": "I have a ( ) in my bag. — It's red.",
        "choices": ["pen", "apple", "car", "dog"],
        "answer": "apple"
    },
    {
        "question": "A: How are you?  B: ___.",
        "choices": ["I'm fine, thank you", "Nice to meet you", "See you", "Good night"],
        "answer": "I'm fine, thank you"
    },
    {
        "question": "The opposite of 'fast' is ___.",
        "choices": ["slow", "quick", "long", "short"],
        "answer": "slow"
    },
    {
        "question": "Which word means '重要な' in English?",
        "choices": ["important", "interesting", "beautiful", "exciting"],
        "answer": "important"
    }
]

# セッション状態を初期化
if "current_q" not i_












