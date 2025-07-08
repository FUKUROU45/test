import streamlit as st
import random
import json
from datetime import datetime

# 問題データベース
class QuestionDatabase:
    def __init__(self):
        self.questions = {
            "grade4": {
                "vocabulary": [
                    {
                        "question": "I have a ( ) dog. It's very cute.",
                        "options": ["small", "big", "loud", "fast"],
                        "answer": 0,
                        "explanation": "小さな犬についての文脈から「small」が正解です。"
                    },
                    {
                        "question": "We ( ) dinner at 6 o'clock every day.",
                        "options": ["eat", "drink", "sleep", "play"],
                        "answer": 0,
                        "explanation": "夕食を食べることは「eat」で表現します。"
                    },
                    {
                        "question": "The weather is very ( ) today.",
                        "options": ["hot", "dog", "book", "table"],
                        "answer": 0,
                        "explanation": "天気について説明するときは「hot」が適切です。"
                    },
                    {
                        "question": "I go to ( ) by bus every morning.",
                        "options": ["school", "cat", "red", "run"],
                        "answer": 0,
                        "explanation": "毎朝バスで行く場所として「school」が自然です。"
                    },
                    {
                        "question": "My favorite ( ) is summer.",
                        "options": ["season", "number", "color", "animal"],
                        "answer": 0,
                        "explanation": "夏は季節なので「season」が正解です。"
                    }
                ],
                "grammar": [
                    {
                        "question": "She ( ) to the library yesterday.",
                        "options": ["go", "goes", "went", "going"],
                        "answer": 2,
                        "explanation": "「yesterday」があるので過去形の「went」が正解です。"
                    },
                    {
                        "question": "( ) you like apples?",
                        "options": ["Do", "Does", "Are", "Is"],
                        "answer": 0,
                        "explanation": "主語がyouなので「Do」を使います。"
                    },
                    {
                        "question": "There ( ) two cats in the garden.",
                        "options": ["is", "are", "was", "were"],
                        "answer": 1,
                        "explanation": "「two cats」と複数なので「are」を使います。"
                    },
                    {
                        "question": "I ( ) my homework now.",
                        "options": ["do", "doing", "am doing", "did"],
                        "answer": 2,
                        "explanation": "現在進行形で「am doing」が正解です。"
                    }
                ],
                "reading": [
                    {
                        "passage": "Tom is a student. He is twelve years old. He goes to Green School. He likes English and math. After school, he plays soccer with his friends.",
                        "question": "What does Tom do after school?",
                        "options": ["Studies English", "Plays soccer", "Goes home", "Eats dinner"],
                        "answer": 1,
                        "explanation": "文章に「After school, he plays soccer with his friends.」とあります。"
                    }
                ]
            },
            "grade3": {
                "vocabulary": [
                    {
                        "question": "The movie was so ( ) that I fell asleep.",
                        "options": ["exciting", "boring", "interesting", "funny"],
                        "answer": 1,
                        "explanation": "眠ってしまうほどなので「boring」が正解です。"
                    },
                    {
                        "question": "I need to ( ) my English vocabulary.",
                        "options": ["improve", "ignore", "forget", "avoid"],
                        "answer": 0,
                        "explanation": "語彙力を向上させるという意味で「improve」が適切です。"
                    },
                    {
                        "question": "The museum is ( ) from 9 to 5.",
                        "options": ["closed", "open", "empty", "full"],
                        "answer": 1,
                        "explanation": "9時から5時までは開いているので「open」が正解です。"
                    },
                    {
                        "question": "Please ( ) the door when you leave.",
                        "options": ["open", "close", "break", "paint"],
                        "answer": 1,
                        "explanation": "出るときはドアを閉めるので「close」が適切です。"
                    },
                    {
                        "question": "The test was very ( ) for me.",
                        "options": ["easy", "difficult", "simple", "hard"],
                        "answer": 1,
                        "explanation": "文脈から困難だったことを表す「difficult」が適切です。"
                    }
                ],
                "grammar": [
                    {
                        "question": "If it ( ) tomorrow, we will stay home.",
                        "options": ["rain", "rains", "will rain", "rained"],
                        "answer": 1,
                        "explanation": "if節では現在形を使うので「rains」が正解です。"
                    },
                    {
                        "question": "I have ( ) finished my homework.",
                        "options": ["yet", "already", "just", "still"],
                        "answer": 1,
                        "explanation": "完了を表す「already」が適切です。"
                    },
                    {
                        "question": "This book is ( ) interesting than that one.",
                        "options": ["more", "most", "much", "many"],
                        "answer": 0,
                        "explanation": "比較級なので「more」が正解です。"
                    },
                    {
                        "question": "She has been studying English ( ) three years.",
                        "options": ["since", "for", "from", "during"],
                        "answer": 1,
                        "explanation": "期間を表すので「for」が適切です。"
                    }
                ],
                "reading": [
                    {
                        "passage": "Climate change is one of the biggest problems facing the world today. Rising temperatures are causing ice to melt and sea levels to rise. Many animals are losing their homes, and weather patterns are becoming more extreme. Scientists believe that human activities are the main cause of these changes.",
                        "question": "According to the passage, what is the main cause of climate change?",
                        "options": ["Natural disasters", "Human activities", "Animal behavior", "Weather patterns"],
                        "answer": 1,
                        "explanation": "文章の最後に「Scientists believe that human activities are the main cause」とあります。"
                    }
                ]
            }
        }

# セッション状態の初期化
def initialize_session_state():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None

def main():
    st.set_page_config(page_title="英検4級～3級練習問題", page_icon="📚", layout="wide")
    
    # タイトル
    st.title("📚 英検4級～3級練習問題")
    st.markdown("---")
    
    # 初期化
    initialize_session_state()
    db = QuestionDatabase()
    
    # サイドバー
    with st.sidebar:
        st.header("設定")
        grade = st.selectbox(
            "級を選択",
            ["4級", "3級"],
            help="練習したい級を選択してください"
        )
        
        question_type = st.selectbox(
            "問題タイプ",
            ["語彙", "文法", "読解"],
            help="練習したい問題タイプを選択してください"
        )
        
        st.markdown("---")
        st.header("成績")
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.metric("正答率", f"{accuracy:.1f}%")
            st.metric("正解数", f"{st.session_state.score}/{st.session_state.total_questions}")
        else:
            st.info("まだ問題を解いていません")
        
        if st.button("成績をリセット"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.success("成績をリセットしました")
    
    # メインコンテンツ
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 問題の種類に応じたキーを設定
        grade_key = "grade4" if grade == "4級" else "grade3"
        type_key = {"語彙": "vocabulary", "文法": "grammar", "読解": "reading"}[question_type]
        
        # 新しい問題を生成
        if st.button("新しい問題を生成", type="primary"):
            questions = db.questions[grade_key][type_key]
            st.session_state.current_question = random.choice(questions)
            st.session_state.show_answer = False
            st.session_state.selected_answer = None
        
        # 現在の問題を表示
        if st.session_state.current_question:
            question = st.session_state.current_question
            
            st.subheader(f"問題 ({grade} - {question_type})")
            
            # 読解問題の場合は文章を表示
            if question_type == "読解":
                st.text_area("文章", value=question["passage"], height=150, disabled=True)
            
            # 問題文を表示
            st.write(f"**問題:** {question['question']}")
            
            # 選択肢を表示
            if not st.session_state.show_answer:
                answer_choice = st.radio(
                    "選択肢を選んでください:",
                    question["options"],
                    key="answer_radio"
                )
                st.session_state.selected_answer = question["options"].index(answer_choice)
                
                if st.button("答え合わせ"):
                    st.session_state.show_answer = True
                    st.session_state.total_questions += 1
                    if st.session_state.selected_answer == question["answer"]:
                        st.session_state.score += 1
                    st.experimental_rerun()
            
            # 答えを表示
            if st.session_state.show_answer:
                correct_answer = question["answer"]
                selected_answer = st.session_state.selected_answer
                
                if selected_answer == correct_answer:
                    st.success("✅ 正解!")
                else:
                    st.error("❌ 不正解")
                
                # 正解を表示
                st.info(f"正解: {question['options'][correct_answer]}")
                
                # 解説を表示
                st.write("**解説:**")
                st.write(question["explanation"])
        
        else:
            st.info("「新しい問題を生成」ボタンをクリックして問題を開始してください。")
    
    with col2:
        st.subheader("学習のヒント")
        
        if grade == "4級":
            st.markdown("""
            **4級レベルの特徴:**
            - 基本的な文法と語彙
            - 日常会話レベル
            - 現在形、過去形、未来形
            - 基本的な疑問文
            - 約600語の単語
            """)
        else:
            st.markdown("""
            **3級レベルの特徴:**
            - より複雑な文法構造
            - 現在完了形、関係代名詞
            - 長文読解力が必要
            - 約1,250語の単語
            - 社会的な話題も含む
            """)
        
        st.markdown("---")
        st.subheader("学習のコツ")
        st.markdown("""
        1. 毎日少しずつ学習する
        2. 間違えた問題を復習する
        3. 辞書を使って新しい単語を覚える
        4. 音読練習も取り入れる
        5. 過去問題も併せて活用する
        """)

if __name__ == "__main__":
    main()














