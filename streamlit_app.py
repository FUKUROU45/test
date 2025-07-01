import streamlit as st
import random
import json
from datetime import datetime

# アプリの設定
st.set_page_config(
    page_title="英単語学習アプリ",
    page_icon="📚",
    layout="wide"
)

# 単語データベース（実際の使用時にはJSONファイルから読み込むことを推奨）
WORD_DATABASE = {
    "beginner": [
        {"word": "apple", "meaning": "りんご", "pronunciation": "ˈæpl"},
        {"word": "book", "meaning": "本", "pronunciation": "bʊk"},
        {"word": "cat", "meaning": "猫", "pronunciation": "kæt"},
        {"word": "dog", "meaning": "犬", "pronunciation": "dɔːɡ"},
        {"word": "house", "meaning": "家", "pronunciation": "haʊs"},
        {"word": "water", "meaning": "水", "pronunciation": "ˈwɔːtər"},
        {"word": "friend", "meaning": "友達", "pronunciation": "frend"},
        {"word": "school", "meaning": "学校", "pronunciation": "skuːl"},
        {"word": "happy", "meaning": "幸せな", "pronunciation": "ˈhæpi"},
        {"word": "beautiful", "meaning": "美しい", "pronunciation": "ˈbjuːtɪfl"}
    ],
    "intermediate": [
        {"word": "accomplish", "meaning": "達成する", "pronunciation": "əˈkʌmplɪʃ"},
        {"word": "environment", "meaning": "環境", "pronunciation": "ɪnˈvaɪrənmənt"},
        {"word": "opportunity", "meaning": "機会", "pronunciation": "ˌɑːpərˈtuːnəti"},
        {"word": "experience", "meaning": "経験", "pronunciation": "ɪkˈspɪriəns"},
        {"word": "knowledge", "meaning": "知識", "pronunciation": "ˈnɑːlɪdʒ"},
        {"word": "technology", "meaning": "技術", "pronunciation": "tekˈnɑːlədʒi"},
        {"word": "research", "meaning": "研究", "pronunciation": "rɪˈsɜːrtʃ"},
        {"word": "creative", "meaning": "創造的な", "pronunciation": "kriˈeɪtɪv"},
        {"word": "challenge", "meaning": "挑戦", "pronunciation": "ˈtʃælɪndʒ"},
        {"word": "successful", "meaning": "成功した", "pronunciation": "səkˈsesfl"}
    ],
    "advanced": [
        {"word": "sophisticated", "meaning": "洗練された", "pronunciation": "səˈfɪstɪkeɪtɪd"},
        {"word": "phenomenon", "meaning": "現象", "pronunciation": "fəˈnɑːmɪnən"},
        {"word": "accumulate", "meaning": "蓄積する", "pronunciation": "əˈkjuːmjəleɪt"},
        {"word": "magnificent", "meaning": "壮大な", "pronunciation": "mæɡˈnɪfɪsnt"},
        {"word": "emphasize", "meaning": "強調する", "pronunciation": "ˈemfəsaɪz"},
        {"word": "inevitable", "meaning": "避けられない", "pronunciation": "ɪnˈevɪtəbl"},
        {"word": "contemporary", "meaning": "現代の", "pronunciation": "kənˈtempəreri"},
        {"word": "substantial", "meaning": "相当な", "pronunciation": "səbˈstænʃl"},
        {"word": "elaborate", "meaning": "詳細な", "pronunciation": "ɪˈlæbərət"},
        {"word": "comprehensive", "meaning": "包括的な", "pronunciation": "ˌkɑːmprɪˈhensɪv"}
    ]
}

# セッション状態の初期化
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'learned_words' not in st.session_state:
    st.session_state.learned_words = []
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False
if 'quiz_options' not in st.session_state:
    st.session_state.quiz_options = []
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = ""

def get_random_word(level):
    """指定されたレベルからランダムに単語を選択"""
    return random.choice(WORD_DATABASE[level])

def generate_quiz_options(correct_word, level):
    """クイズの選択肢を生成"""
    all_words = WORD_DATABASE[level]
    options = [correct_word['meaning']]
    
    # 他の選択肢を追加
    while len(options) < 4:
        random_word = random.choice(all_words)
        if random_word['meaning'] not in options:
            options.append(random_word['meaning'])
    
    random.shuffle(options)
    return options

def main():
    st.title("📚 英単語学習アプリ")
    st.markdown("---")
    
    # サイドバー
    with st.sidebar:
        st.header("📊 学習統計")
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.metric("正答率", f"{accuracy:.1f}%")
        st.metric("正解数", st.session_state.score)
        st.metric("総問題数", st.session_state.total_questions)
        st.metric("学習済み単語", len(st.session_state.learned_words))
        
        st.markdown("---")
        if st.button("📈 統計をリセット"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.learned_words = []
            st.success("統計をリセットしました！")
    
    # メインコンテンツ
    tab1, tab2, tab3 = st.tabs(["📖 単語学習", "🎯 クイズモード", "📝 学習済み単語"])
    
    with tab1:
        st.header("単語を学習しよう")
        
        # レベル選択
        level = st.select_slider(
            "難易度を選択:",
            options=["beginner", "intermediate", "advanced"],
            value="beginner",
            format_func=lambda x: {"beginner": "初級", "intermediate": "中級", "advanced": "上級"}[x]
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🎲 新しい単語を表示", type="primary"):
                st.session_state.current_word = get_random_word(level)
        
        with col2:
            if st.button("🔄 リセット"):
                st.session_state.current_word = None
        
        # 単語表示
        if st.session_state.current_word:
            word_data = st.session_state.current_word
            
            # 単語カード風のデザイン
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            ">
                <h1 style="color: white; margin-bottom: 0.5rem; font-size: 3rem;">
                    {word_data['word']}
                </h1>
                <p style="color: #f0f0f0; font-size: 1.2rem; margin-bottom: 1rem;">
                    [{word_data['pronunciation']}]
                </p>
                <h2 style="color: #fff; margin-top: 1rem;">
                    {word_data['meaning']}
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # 学習済みに追加ボタン
            if st.button("✅ 学習済みに追加"):
                if word_data not in st.session_state.learned_words:
                    st.session_state.learned_words.append(word_data)
                    st.success(f"'{word_data['word']}' を学習済みに追加しました！")
                else:
                    st.info("この単語は既に学習済みです。")
    
    with tab2:
        st.header("クイズに挑戦")
        
        level = st.select_slider(
            "クイズの難易度:",
            options=["beginner", "intermediate", "advanced"],
            value="beginner",
            format_func=lambda x: {"beginner": "初級", "intermediate": "中級", "advanced": "上級"}[x],
            key="quiz_level"
        )
        
        if st.button("🎯 クイズを開始", type="primary"):
            word = get_random_word(level)
            st.session_state.current_word = word
            st.session_state.quiz_options = generate_quiz_options(word, level)
            st.session_state.correct_answer = word['meaning']
            st.session_state.quiz_mode = True
        
        # クイズ表示
        if st.session_state.quiz_mode and st.session_state.current_word:
            word_data = st.session_state.current_word
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin: 1rem 0;
            ">
                <h2 style="color: white; margin-bottom: 1rem;">
                    この単語の意味は何でしょう？
                </h2>
                <h1 style="color: white; font-size: 3rem;">
                    {word_data['word']}
                </h1>
                <p style="color: #f0f0f0; font-size: 1.2rem;">
                    [{word_data['pronunciation']}]
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 選択肢
            user_answer = st.radio(
                "答えを選んでください:",
                st.session_state.quiz_options,
                key=f"quiz_{st.session_state.total_questions}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("回答する"):
                    st.session_state.total_questions += 1
                    if user_answer == st.session_state.correct_answer:
                        st.session_state.score += 1
                        st.success("🎉 正解です！")
                        if word_data not in st.session_state.learned_words:
                            st.session_state.learned_words.append(word_data)
                    else:
                        st.error(f"❌ 不正解です。正解は '{st.session_state.correct_answer}' でした。")
                    st.session_state.quiz_mode = False
            
            with col2:
                if st.button("スキップ"):
                    st.session_state.quiz_mode = False
                    st.info("スキップしました。")
    
    with tab3:
        st.header("学習済み単語一覧")
        
        if st.session_state.learned_words:
            st.success(f"学習済み単語数: {len(st.session_state.learned_words)}")
            
            # 検索機能
            search_term = st.text_input("🔍 単語を検索:")
            
            filtered_words = st.session_state.learned_words
            if search_term:
                filtered_words = [
                    word for word in st.session_state.learned_words
                    if search_term.lower() in word['word'].lower() or 
                       search_term.lower() in word['meaning'].lower()
                ]
            
            # 単語リスト表示
            for i, word in enumerate(filtered_words):
                with st.expander(f"{word['word']} - {word['meaning']}"):
                    st.markdown(f"""
                    **単語**: {word['word']}<br>
                    **発音**: [{word['pronunciation']}]<br>
                    **意味**: {word['meaning']}
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"削除", key=f"delete_{i}"):
                        st.session_state.learned_words.remove(word)
                        st.success(f"'{word['word']}' を削除しました。")
                        st.rerun()
        else:
            st.info("まだ学習済みの単語がありません。単語学習やクイズで単語を覚えましょう！")

if __name__ == "__main__":
    main()

