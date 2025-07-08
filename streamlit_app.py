import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
import sympy as sp

# 問題データベース
class MathQuestionDatabase:
    def __init__(self):
        self.questions = {
            "中学1年": {
                "正負の数": [
                    {
                        "question": "次の計算をしなさい: (-3) + 5",
                        "type": "calculation",
                        "answer": 2,
                        "explanation": "(-3) + 5 = 5 - 3 = 2"
                    },
                    {
                        "question": "次の計算をしなさい: (-4) × (-6)",
                        "type": "calculation", 
                        "answer": 24,
                        "explanation": "負の数同士の掛け算は正の数になるので (-4) × (-6) = 24"
                    },
                    {
                        "question": "次の計算をしなさい: 8 ÷ (-2)",
                        "type": "calculation",
                        "answer": -4,
                        "explanation": "正の数を負の数で割ると負の数になるので 8 ÷ (-2) = -4"
                    }
                ],
                "文字式": [
                    {
                        "question": "次の式を簡単にしなさい: 3x + 2x",
                        "type": "algebra",
                        "answer": "5x",
                        "explanation": "同類項をまとめて 3x + 2x = 5x"
                    },
                    {
                        "question": "次の式を簡単にしなさい: 4a - 2a + 3",
                        "type": "algebra",
                        "answer": "2a + 3",
                        "explanation": "同類項をまとめて 4a - 2a + 3 = 2a + 3"
                    }
                ],
                "1次方程式": [
                    {
                        "question": "方程式 2x + 3 = 11 を解きなさい",
                        "type": "equation",
                        "answer": 4,
                        "explanation": "2x + 3 = 11\n2x = 11 - 3\n2x = 8\nx = 4"
                    },
                    {
                        "question": "方程式 3x - 5 = x + 7 を解きなさい",
                        "type": "equation",
                        "answer": 6,
                        "explanation": "3x - 5 = x + 7\n3x - x = 7 + 5\n2x = 12\nx = 6"
                    }
                ]
            },
            "中学2年": {
                "連立方程式": [
                    {
                        "question": "連立方程式を解きなさい:\nx + y = 7\nx - y = 3",
                        "type": "system",
                        "answer": {"x": 5, "y": 2},
                        "explanation": "加減法で解くと:\n(x + y) + (x - y) = 7 + 3\n2x = 10\nx = 5\ny = 7 - 5 = 2"
                    }
                ],
                "1次関数": [
                    {
                        "question": "直線 y = 2x - 3 の傾きと切片を答えなさい",
                        "type": "function",
                        "answer": {"傾き": 2, "切片": -3},
                        "explanation": "y = ax + b の形で、傾きは a = 2、y切片は b = -3"
                    }
                ],
                "図形の性質": [
                    {
                        "question": "三角形の内角の和は何度ですか？",
                        "type": "geometry",
                        "answer": 180,
                        "explanation": "三角形の内角の和は常に180度です"
                    }
                ]
            },
            "中学3年": {
                "2次方程式": [
                    {
                        "question": "方程式 x² - 5x + 6 = 0 を解きなさい",
                        "type": "quadratic",
                        "answer": [2, 3],
                        "explanation": "因数分解すると (x - 2)(x - 3) = 0\nよって x = 2, 3"
                    },
                    {
                        "question": "方程式 x² - 4 = 0 を解きなさい",
                        "type": "quadratic",
                        "answer": [-2, 2],
                        "explanation": "x² = 4 なので x = ±2"
                    }
                ],
                "2次関数": [
                    {
                        "question": "放物線 y = x² - 2x + 1 の頂点の座標を求めなさい",
                        "type": "parabola",
                        "answer": {"x": 1, "y": 0},
                        "explanation": "y = (x - 1)² と変形できるので、頂点は (1, 0)"
                    }
                ],
                "円": [
                    {
                        "question": "半径 5cm の円の面積を求めなさい（π を使って答えなさい）",
                        "type": "circle",
                        "answer": "25π",
                        "explanation": "円の面積 = π × r² = π × 5² = 25π cm²"
                    }
                ]
            },
            "高校1年": {
                "数と式": [
                    {
                        "question": "次の式を因数分解しなさい: x² - 9",
                        "type": "factoring",
                        "answer": "(x + 3)(x - 3)",
                        "explanation": "平方差の公式: a² - b² = (a + b)(a - b) を使って\nx² - 9 = x² - 3² = (x + 3)(x - 3)"
                    },
                    {
                        "question": "次の式を展開しなさい: (x + 2)²",
                        "type": "expansion",
                        "answer": "x² + 4x + 4",
                        "explanation": "(a + b)² = a² + 2ab + b² の公式を使って\n(x + 2)² = x² + 2·x·2 + 2² = x² + 4x + 4"
                    }
                ],
                "2次関数": [
                    {
                        "question": "関数 y = x² - 4x + 3 の最小値を求めなさい",
                        "type": "quadratic_function",
                        "answer": -1,
                        "explanation": "y = x² - 4x + 3 = (x - 2)² - 1\n頂点は (2, -1) なので最小値は -1"
                    }
                ],
                "三角比": [
                    {
                        "question": "sin 30° の値を求めなさい",
                        "type": "trigonometry",
                        "answer": "1/2",
                        "explanation": "基本的な三角比の値: sin 30° = 1/2"
                    },
                    {
                        "question": "cos 60° の値を求めなさい",
                        "type": "trigonometry",
                        "answer": "1/2",
                        "explanation": "基本的な三角比の値: cos 60° = 1/2"
                    }
                ]
            }
        }

# 問題生成関数
def generate_random_question(grade, unit):
    """指定された学年と単元からランダムに問題を生成"""
    db = MathQuestionDatabase()
    questions = db.questions[grade][unit]
    return random.choice(questions)

# 数式の可視化
def plot_quadratic_function(a, b, c):
    """2次関数のグラフを描画"""
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'b-', linewidth=2)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'y = {a}x² + {b}x + {c}')
    
    # 頂点をプロット
    vertex_x = -b / (2 * a)
    vertex_y = a * vertex_x**2 + b * vertex_x + c
    ax.plot(vertex_x, vertex_y, 'ro', markersize=8, label=f'頂点({vertex_x:.1f}, {vertex_y:.1f})')
    ax.legend()
    
    return fig

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
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""
    if 'history' not in st.session_state:
        st.session_state.history = []

def main():
    st.set_page_config(page_title="中学～高校数学問題集", page_icon="📐", layout="wide")
    
    # タイトル
    st.title("📐 中学～高校数学問題集")
    st.markdown("中学1年生から高校1年生までの数学問題を練習できます")
    st.markdown("---")
    
    # 初期化
    initialize_session_state()
    
    # サイドバー
    with st.sidebar:
        st.header("📚 学習設定")
        
        # 学年選択
        grade = st.selectbox(
            "学年を選択",
            ["中学1年", "中学2年", "中学3年", "高校1年"],
            help="学習したい学年を選択してください"
        )
        
        # 単元選択
        db = MathQuestionDatabase()
        units = list(db.questions[grade].keys())
        unit = st.selectbox(
            "単元を選択",
            units,
            help="学習したい単元を選択してください"
        )
        
        st.markdown("---")
        
        # 成績表示
        st.header("📊 学習成績")
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.metric("正答率", f"{accuracy:.1f}%")
            st.metric("正解数", f"{st.session_state.score}/{st.session_state.total_questions}")
            
            # 成績の詳細
            if st.session_state.history:
                st.subheader("最近の結果")
                for i, result in enumerate(st.session_state.history[-5:]):
                    icon = "✅" if result['correct'] else "❌"
                    st.write(f"{icon} {result['unit']}")
        else:
            st.info("まだ問題を解いていません")
        
        if st.button("成績をリセット"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.history = []
            st.success("成績をリセットしました")
    
    # メインコンテンツ
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"📖 {grade} - {unit}")
        
        # 新しい問題を生成
        if st.button("新しい問題を生成", type="primary"):
            st.session_state.current_question = generate_random_question(grade, unit)
            st.session_state.show_answer = False
            st.session_state.user_answer = ""
            st.rerun()
        
        # 問題表示
        if st.session_state.current_question:
            question = st.session_state.current_question
            
            st.subheader("問題")
            st.write(question["question"])
            
            # グラフの表示（2次関数の場合）
            if question["type"] == "parabola" and "y = x²" in question["question"]:
                st.subheader("グラフ")
                fig = plot_quadratic_function(1, -2, 1)
                st.pyplot(fig)
            
            # 答えの入力
            if not st.session_state.show_answer:
                if question["type"] in ["calculation", "equation", "geometry", "quadratic_function"]:
                    user_answer = st.number_input("答えを入力してください", key="number_input")
                    st.session_state.user_answer = user_answer
                elif question["type"] in ["algebra", "factoring", "expansion", "trigonometry"]:
                    user_answer = st.text_input("答えを入力してください（例: 2x + 3）", key="text_input")
                    st.session_state.user_answer = user_answer
                elif question["type"] == "system":
                    st.write("x と y の値を入力してください")
                    x_val = st.number_input("x = ", key="x_input")
                    y_val = st.number_input("y = ", key="y_input")
                    st.session_state.user_answer = {"x": x_val, "y": y_val}
                elif question["type"] == "function":
                    st.write("傾きと切片を入力してください")
                    slope = st.number_input("傾き = ", key="slope_input")
                    intercept = st.number_input("切片 = ", key="intercept_input")
                    st.session_state.user_answer = {"傾き": slope, "切片": intercept}
                elif question["type"] == "circle":
                    user_answer = st.text_input("答えを入力してください（例: 25π）", key="circle_input")
                    st.session_state.user_answer = user_answer
                elif question["type"] == "quadratic":
                    st.write("解を入力してください（2つある場合は両方入力）")
                    sol1 = st.number_input("解1 = ", key="sol1_input")
                    sol2 = st.number_input("解2 = ", key="sol2_input")
                    st.session_state.user_answer = [sol1, sol2]
                elif question["type"] == "parabola":
                    st.write("頂点の座標を入力してください")
                    x_coord = st.number_input("x座標 = ", key="x_coord_input")
                    y_coord = st.number_input("y座標 = ", key="y_coord_input")
                    st.session_state.user_answer = {"x": x_coord, "y": y_coord}
                
                if st.button("答え合わせ"):
                    st.session_state.show_answer = True
                    st.session_state.total_questions += 1
                    
                    # 正解判定
                    is_correct = False
                    if question["type"] in ["calculation", "equation", "geometry", "quadratic_function"]:
                        is_correct = abs(st.session_state.user_answer - question["answer"]) < 0.001
                    elif question["type"] in ["algebra", "factoring", "expansion", "trigonometry", "circle"]:
                        is_correct = str(st.session_state.user_answer).strip() == str(question["answer"]).strip()
                    elif question["type"] in ["system", "function", "parabola"]:
                        is_correct = st.session_state.user_answer == question["answer"]
                    elif question["type"] == "quadratic":
                        user_set = set(st.session_state.user_answer)
                        answer_set = set(question["answer"])
                        is_correct = user_set == answer_set
                    
                    if is_correct:
                        st.session_state.score += 1
                    
                    # 履歴に追加
                    st.session_state.history.append({
                        'unit': unit,
                        'correct': is_correct,
                        'question': question["question"]
                    })
                    
                    st.rerun()
            
            # 結果表示
            if st.session_state.show_answer:
                # 正解判定の再実行
                is_correct = False
                if question["type"] in ["calculation", "equation", "geometry", "quadratic_function"]:
                    is_correct = abs(st.session_state.user_answer - question["answer"]) < 0.001
                elif question["type"] in ["algebra", "factoring", "expansion", "trigonometry", "circle"]:
                    is_correct = str(st.session_state.user_answer).strip() == str(question["answer"]).strip()
                elif question["type"] in ["system", "function", "parabola"]:
                    is_correct = st.session_state.user_answer == question["answer"]
                elif question["type"] == "quadratic":
                    user_set = set(st.session_state.user_answer)
                    answer_set = set(question["answer"])
                    is_correct = user_set == answer_set
                
                if is_correct:
                    st.success("🎉 正解！")
                else:
                    st.error("❌ 不正解")
                
                st.info(f"**正解:** {question['answer']}")
                
                # 解説表示
                st.subheader("解説")
                st.write(question["explanation"])
        
        else:
            st.info("「新しい問題を生成」ボタンをクリックして問題を始めてください。")
    
    with col2:
        st.subheader("📋 学習のポイント")
        
        # 学年別の学習ポイント
        learning_points = {
            "中学1年": {
                "正負の数": "符号のルールをしっかり覚えよう",
                "文字式": "同類項をまとめる練習をしよう",
                "1次方程式": "移項のルールを身につけよう"
            },
            "中学2年": {
                "連立方程式": "加減法と代入法を使い分けよう",
                "1次関数": "グラフと式の関係を理解しよう",
                "図形の性質": "角度の性質を覚えよう"
            },
            "中学3年": {
                "2次方程式": "因数分解と解の公式を使い分けよう",
                "2次関数": "放物線の性質を理解しよう",
                "円": "円周角の定理を覚えよう"
            },
            "高校1年": {
                "数と式": "因数分解の公式を完璧に覚えよう",
                "2次関数": "平方完成の方法を身につけよう",
                "三角比": "基本の角度の値を覚えよう"
            }
        }
        
        if unit in learning_points[grade]:
            st.write(f"💡 {learning_points[grade][unit]}")
        
        st.markdown("---")
        
        # 公式集
        st.subheader("📐 重要な公式")
        
        formulas = {
            "中学1年": [
                "移項: a + b = c → a = c - b",
                "分配法則: a(b + c) = ab + ac"
            ],
            "中学2年": [
                "1次関数: y = ax + b",
                "三角形の内角の和: 180°"
            ],
            "中学3年": [
                "2次方程式の解の公式: x = (-b ± √(b²-4ac)) / 2a",
                "円の面積: S = πr²"
            ],
            "高校1年": [
                "平方差: a² - b² = (a+b)(a-b)",
                "完全平方式: a² + 2ab + b² = (a+b)²",
                "sin²θ + cos²θ = 1"
            ]
        }
        
        if grade in formulas:
            for formula in formulas[grade]:
                st.write(f"• {formula}")
        
        st.markdown("---")
        
        # 学習のコツ
        st.subheader("🎯 学習のコツ")
        st.markdown("""
        1. **基本から着実に**: 前の単元の理解を確認
        2. **計算練習**: 毎日少しずつ計算練習
        3. **間違いノート**: 間違えた問題をまとめる
        4. **図やグラフ**: 視覚的に理解する
        5. **反復練習**: 同じ問題を繰り返し解く
        """)

if __name__ == "__main__":
    main()













