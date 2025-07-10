import streamlit as st
import random
import json

# ページ設定
st.set_page_config(
    page_title="中学漢字練習アプリ",
    page_icon="📚",
    layout="wide"
)

# 中学校の漢字データ（各学年の代表的な漢字）
KANJI_DATA = {
    "1年生": {
        "漢字": [
            {"字": "圧", "読み": "アツ", "意味": "おさえつける", "例文": "圧力をかける"},
            {"字": "移", "読み": "イ", "意味": "うつる、うつす", "例文": "移動する"},
            {"字": "因", "読み": "イン", "意味": "もと、原因", "例文": "因果関係"},
            {"字": "永", "読み": "エイ", "意味": "ながい", "例文": "永遠に続く"},
            {"字": "営", "読み": "エイ", "意味": "いとなむ", "例文": "営業する"},
            {"字": "衛", "読み": "エイ", "意味": "まもる", "例文": "衛生管理"},
            {"字": "易", "読み": "エキ", "意味": "やさしい", "例文": "易しい問題"},
            {"字": "益", "読み": "エキ", "意味": "ためになる", "例文": "利益を得る"},
            {"字": "液", "読み": "エキ", "意味": "みずけ", "例文": "液体状態"},
            {"字": "演", "読み": "エン", "意味": "のべる", "例文": "演説する"},
            {"字": "応", "読み": "オウ", "意味": "こたえる", "例文": "応答する"},
            {"字": "往", "読み": "オウ", "意味": "いく", "例文": "往復する"},
            {"字": "桜", "読み": "オウ", "意味": "さくら", "例文": "桜の花"},
            {"字": "恩", "読み": "オン", "意味": "めぐみ", "例文": "恩師への感謝"},
            {"字": "可", "読み": "カ", "意味": "よい", "例文": "可能性"},
            {"字": "仮", "読み": "カ", "意味": "かり", "例文": "仮定する"},
            {"字": "価", "読み": "カ", "意味": "ねだん", "例文": "価格表示"},
            {"字": "河", "読み": "カ", "意味": "かわ", "例文": "河川敷"},
            {"字": "過", "読み": "カ", "意味": "すぎる", "例文": "過去の話"},
            {"字": "快", "読み": "カイ", "意味": "こころよい", "例文": "快適な部屋"}
        ]
    },
    "2年生": {
        "漢字": [
            {"字": "輝", "読み": "キ", "意味": "かがやく", "例文": "輝く星"},
            {"字": "機", "読み": "キ", "意味": "はたらき", "例文": "機械工学"},
            {"字": "技", "読み": "ギ", "意味": "わざ", "例文": "技術革新"},
            {"字": "義", "読み": "ギ", "意味": "ただしい", "例文": "正義感"},
            {"字": "逆", "読み": "ギャク", "意味": "さかさま", "例文": "逆転勝利"},
            {"字": "久", "読み": "キュウ", "意味": "ひさしい", "例文": "久しぶり"},
            {"字": "旧", "読み": "キュウ", "意味": "ふるい", "例文": "旧友に会う"},
            {"字": "居", "読み": "キョ", "意味": "いる", "例文": "居住地"},
            {"字": "許", "読み": "キョ", "意味": "ゆるす", "例文": "許可証"},
            {"字": "境", "読み": "キョウ", "意味": "さかい", "例文": "境界線"},
            {"字": "均", "読み": "キン", "意味": "ひとしい", "例文": "平均値"},
            {"字": "禁", "読み": "キン", "意味": "いましめる", "例文": "禁止事項"},
            {"字": "句", "読み": "ク", "意味": "ことば", "例文": "文句を言う"},
            {"字": "群", "読み": "グン", "意味": "むれ", "例文": "群衆心理"},
            {"字": "経", "読み": "ケイ", "意味": "たつ", "例文": "経験豊富"},
            {"字": "潔", "読み": "ケツ", "意味": "きよい", "例文": "潔白を証明"},
            {"字": "件", "読み": "ケン", "意味": "くだり", "例文": "事件の真相"},
            {"字": "険", "読み": "ケン", "意味": "けわしい", "例文": "険しい山道"},
            {"字": "検", "読み": "ケン", "意味": "しらべる", "例文": "検査結果"},
            {"字": "限", "読み": "ゲン", "意味": "かぎる", "例文": "制限時間"}
        ]
    },
    "3年生": {
        "漢字": [
            {"字": "絹", "読み": "ケン", "意味": "きぬ", "例文": "絹の着物"},
            {"字": "権", "読み": "ケン", "意味": "ちから", "例文": "権利主張"},
            {"字": "憲", "読み": "ケン", "意味": "のり", "例文": "憲法改正"},
            {"字": "源", "読み": "ゲン", "意味": "みなもと", "例文": "源泉徴収"},
            {"字": "厳", "読み": "ゲン", "意味": "きびしい", "例文": "厳格な規則"},
            {"字": "己", "読み": "コ", "意味": "おのれ", "例文": "自分自身"},
            {"字": "呼", "読み": "コ", "意味": "よぶ", "例文": "呼吸困難"},
            {"字": "誤", "読み": "ゴ", "意味": "まちがえる", "例文": "誤解を招く"},
            {"字": "后", "読み": "コウ", "意味": "きさき", "例文": "皇后陛下"},
            {"字": "孝", "読み": "コウ", "意味": "したがう", "例文": "孝行息子"},
            {"字": "皇", "読み": "コウ", "意味": "きみ", "例文": "皇室制度"},
            {"字": "紅", "読み": "コウ", "意味": "べに", "例文": "紅葉の季節"},
            {"字": "降", "読み": "コウ", "意味": "おりる", "例文": "降水確率"},
            {"字": "鋼", "読み": "コウ", "意味": "はがね", "例文": "鋼鉄製品"},
            {"字": "刻", "読み": "コク", "意味": "きざむ", "例文": "刻印を押す"},
            {"字": "穀", "読み": "コク", "意味": "たなつもの", "例文": "穀物生産"},
            {"字": "骨", "読み": "コツ", "意味": "ほね", "例文": "骨組み構造"},
            {"字": "困", "読み": "コン", "意味": "こまる", "例文": "困難な状況"},
            {"字": "砂", "読み": "サ", "意味": "すな", "例文": "砂漠地帯"},
            {"字": "座", "読み": "ザ", "意味": "すわる", "例文": "座席指定"}
        ]
    }
}

# セッション状態の初期化
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'problem_type' not in st.session_state:
    st.session_state.problem_type = "読み方"
if 'grade' not in st.session_state:
    st.session_state.grade = "1年生"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_problems' not in st.session_state:
    st.session_state.total_problems = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""

def generate_problem(grade, problem_type):
    """問題を生成する"""
    kanji_list = KANJI_DATA[grade]["漢字"]
    kanji = random.choice(kanji_list)
    
    if problem_type == "読み方":
        return {
            "type": "読み方",
            "question": f"「{kanji['字']}」の読み方は？",
            "kanji": kanji["字"],
            "correct_answer": kanji["読み"],
            "example": kanji["例文"],
            "meaning": kanji["意味"]
        }
    elif problem_type == "書き方":
        return {
            "type": "書き方",
            "question": f"「{kanji['読み']}」の漢字は？",
            "reading": kanji["読み"],
            "correct_answer": kanji["字"],
            "example": kanji["例文"],
            "meaning": kanji["意味"]
        }
    elif problem_type == "意味":
        return {
            "type": "意味",
            "question": f"「{kanji['字']}」の意味は？",
            "kanji": kanji["字"],
            "correct_answer": kanji["意味"],
            "example": kanji["例文"],
            "reading": kanji["読み"]
        }
    else:  # 例文
        # 例文の漢字を空欄にする
        example_with_blank = kanji["例文"].replace(kanji["字"], "□")
        return {
            "type": "例文",
            "question": f"「□」に入る漢字は？\n例文：{example_with_blank}",
            "correct_answer": kanji["字"],
            "example": kanji["例文"],
            "reading": kanji["読み"],
            "meaning": kanji["意味"]
        }

def generate_choices(correct_answer, grade, problem_type):
    """選択肢を生成する"""
    kanji_list = KANJI_DATA[grade]["漢字"]
    
    if problem_type == "読み方":
        all_answers = [k["読み"] for k in kanji_list]
    elif problem_type == "書き方" or problem_type == "例文":
        all_answers = [k["字"] for k in kanji_list]
    else:  # 意味
        all_answers = [k["意味"] for k in kanji_list]
    
    # 正解以外の選択肢を3つ選ぶ
    wrong_answers = [ans for ans in all_answers if ans != correct_answer]
    choices = random.sample(wrong_answers, min(3, len(wrong_answers)))
    choices.append(correct_answer)
    random.shuffle(choices)
    
    return choices

# アプリタイトル
st.title("📚 中学漢字練習アプリ")
st.markdown("**中学校1年生から3年生の漢字を楽しく学習しよう！**")

# サイドバー設定
st.sidebar.header("📝 学習設定")
grade = st.sidebar.selectbox("学年を選択", ["1年生", "2年生", "3年生"])
problem_type = st.sidebar.selectbox(
    "問題の種類", 
    ["読み方", "書き方", "意味", "例文"]
)

st.sidebar.header("📊 学習成績")
if st.session_state.total_problems > 0:
    accuracy = (st.session_state.score / st.session_state.total_problems) * 100
    st.sidebar.metric("正答率", f"{accuracy:.1f}%")
    st.sidebar.metric("正解数", f"{st.session_state.score}/{st.session_state.total_problems}")

st.sidebar.header("🎯 学習のポイント")
st.sidebar.markdown("""
- **読み方**: 漢字を見て読み方を答える
- **書き方**: 読み方を見て漢字を書く
- **意味**: 漢字の意味を理解する
- **例文**: 文脈から漢字を推測する
""")

# メインコンテンツ
col1, col2 = st.columns([3, 2])

with col1:
    st.header("🎯 漢字問題")
    
    # 新しい問題を生成
    if st.button("🎲 新しい問題", type="primary"):
        st.session_state.current_problem = generate_problem(grade, problem_type)
        st.session_state.show_answer = False
        st.session_state.user_answer = ""
        st.session_state.grade = grade
        st.session_state.problem_type = problem_type
        st.rerun()
    
    # 問題を表示
    if st.session_state.current_problem:
        problem = st.session_state.current_problem
        
        st.subheader(f"【{st.session_state.grade} - {problem['type']}問題】")
        st.markdown(f"**問題**: {problem['question']}")
        
        # 問題の種類に応じた解答方法
        if problem['type'] in ["読み方", "意味"]:
            # 選択肢問題
            choices = generate_choices(problem['correct_answer'], st.session_state.grade, problem['type'])
            selected_answer = st.radio("答えを選んでください：", choices, key="answer_choice")
            
            if st.button("✅ 答えを確認"):
                st.session_state.total_problems += 1
                if selected_answer == problem['correct_answer']:
                    st.success("🎉 正解です！素晴らしい！")
                    st.session_state.score += 1
                    st.balloons()
                else:
                    st.error(f"❌ 残念！正解は「{problem['correct_answer']}」です。")
                
                # 詳細情報を表示
                st.session_state.show_answer = True
                st.rerun()
        
        else:
            # 記述問題（書き方、例文）
            user_input = st.text_input("答えを入力してください：", key="text_input")
            
            if st.button("✅ 答えを確認"):
                st.session_state.total_problems += 1
                if user_input.strip() == problem['correct_answer']:
                    st.success("🎉 正解です！素晴らしい！")
                    st.session_state.score += 1
                    st.balloons()
                else:
                    st.error(f"❌ 残念！正解は「{problem['correct_answer']}」です。")
                
                # 詳細情報を表示
                st.session_state.show_answer = True
                st.rerun()
        
        # 詳細情報表示
        if st.session_state.show_answer:
            st.subheader("📖 詳細情報")
            
            with st.expander("漢字の詳細", expanded=True):
                if problem['type'] == "読み方":
                    st.write(f"**漢字**: {problem['kanji']}")
                    st.write(f"**読み方**: {problem['correct_answer']}")
                    st.write(f"**意味**: {problem['meaning']}")
                    st.write(f"**例文**: {problem['example']}")
                elif problem['type'] == "書き方":
                    st.write(f"**読み方**: {problem['reading']}")
                    st.write(f"**漢字**: {problem['correct_answer']}")
                    st.write(f"**意味**: {problem['meaning']}")
                    st.write(f"**例文**: {problem['example']}")
                elif problem['type'] == "意味":
                    st.write(f"**漢字**: {problem['kanji']}")
                    st.write(f"**読み方**: {problem['reading']}")
                    st.write(f"**意味**: {problem['correct_answer']}")
                    st.write(f"**例文**: {problem['example']}")
                else:  # 例文
                    st.write(f"**漢字**: {problem['correct_answer']}")
                    st.write(f"**読み方**: {problem['reading']}")
                    st.write(f"**意味**: {problem['meaning']}")
                    st.write(f"**例文**: {problem['example']}")

with col2:
    st.header("📚 学習支援")
    
    # 現在の設定を表示
    st.subheader("現在の設定")
    st.write(f"**学年**: {grade}")
    st.write(f"**問題種類**: {problem_type}")
    
    # 学習のコツ
    st.subheader("💡 学習のコツ")
    if problem_type == "読み方":
        st.markdown("""
        - 漢字の部首から推測してみよう
        - 似た漢字と比較してみよう
        - 例文を声に出して読んでみよう
        """)
    elif problem_type == "書き方":
        st.markdown("""
        - 漢字の画数を意識しよう
        - 部首の組み合わせを覚えよう
        - 繰り返し書いて覚えよう
        """)
    elif problem_type == "意味":
        st.markdown("""
        - 漢字の成り立ちを理解しよう
        - 熟語から意味を推測しよう
        - 例文の文脈を考えよう
        """)
    else:  # 例文
        st.markdown("""
        - 文脈から意味を推測しよう
        - 前後の文章をよく読もう
        - 知っている漢字から類推しよう
        """)
    
    # 学年別の特徴
    st.subheader("📖 学年別の特徴")
    if grade == "1年生":
        st.write("基本的な漢字が中心。日常でよく使う漢字を覚えよう。")
    elif grade == "2年生":
        st.write("複雑な漢字が増加。部首の知識を活用しよう。")
    else:  # 3年生
        st.write("高度な漢字が登場。熟語での使い方も覚えよう。")

# 成績リセット
if st.button("🔄 成績をリセット"):
    st.session_state.score = 0
    st.session_state.total_problems = 0
    st.success("成績をリセットしました！")
    st.rerun()

# フッター
st.markdown("---")
st.markdown("**📝 継続的な学習で漢字力を向上させましょう！**")
st.markdown("*毎日少しずつでも続けることが大切です。*")