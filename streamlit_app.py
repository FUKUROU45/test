import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
import sympy as sp

class EquationQuestionDatabase:
    def __init__(self):
        self.questions = {
            "1次方程式": {
                "基本": [
                    {
                        "equation": "x + 3 = 7",
                        "answer": 4,
                        "solution_steps": [
                            "x + 3 = 7",
                            "x = 7 - 3",
                            "x = 4"
                        ],
                        "explanation": "両辺から3を引いて移項します。"
                    },
                    {
                        "equation": "2x = 10",
                        "answer": 5,
                        "solution_steps": [
                            "2x = 10",
                            "x = 10 ÷ 2",
                            "x = 5"
                        ],
                        "explanation": "両辺を2で割ります。"
                    },
                    {
                        "equation": "x - 5 = 2",
                        "answer": 7,
                        "solution_steps": [
                            "x - 5 = 2",
                            "x = 2 + 5",
                            "x = 7"
                        ],
                        "explanation": "両辺に5を足して移項します。"
                    },
                    {
                        "equation": "3x - 1 = 8",
                        "answer": 3,
                        "solution_steps": [
                            "3x - 1 = 8",
                            "3x = 8 + 1",
                            "3x = 9",
                            "x = 9 ÷ 3",
                            "x = 3"
                        ],
                        "explanation": "まず1を右辺に移項し、次に3で割ります。"
                    }
                ],
                "標準": [
                    {
                        "equation": "2x + 3 = x + 7",
                        "answer": 4,
                        "solution_steps": [
                            "2x + 3 = x + 7",
                            "2x - x = 7 - 3",
                            "x = 4"
                        ],
                        "explanation": "xの項を左辺に、数の項を右辺に移項します。"
                    },
                    {
                        "equation": "5x - 4 = 2x + 8",
                        "answer": 4,
                        "solution_steps": [
                            "5x - 4 = 2x + 8",
                            "5x - 2x = 8 + 4",
                            "3x = 12",
                            "x = 4"
                        ],
                        "explanation": "xの項を左辺に、数の項を右辺に移項してまとめます。"
                    },
                    {
                        "equation": "3(x + 2) = 15",
                        "answer": 3,
                        "solution_steps": [
                            "3(x + 2) = 15",
                            "3x + 6 = 15",
                            "3x = 15 - 6",
                            "3x = 9",
                            "x = 3"
                        ],
                        "explanation": "分配法則を使って括弧を展開してから解きます。"
                    }
                ],
                "発展": [
                    {
                        "equation": "2(x - 1) + 3(x + 2) = 17",
                        "answer": 3,
                        "solution_steps": [
                            "2(x - 1) + 3(x + 2) = 17",
                            "2x - 2 + 3x + 6 = 17",
                            "5x + 4 = 17",
                            "5x = 17 - 4",
                            "5x = 13",
                            "x = 13/5"
                        ],
                        "explanation": "分配法則を使って括弧を展開し、同類項をまとめます。"
                    }
                ]
            },
            "2次方程式": {
                "基本": [
                    {
                        "equation": "x² = 9",
                        "answer": [3, -3],
                        "solution_steps": [
                            "x² = 9",
                            "x = ±√9",
                            "x = ±3"
                        ],
                        "explanation": "平方根を取って、正負両方の解を求めます。"
                    },
                    {
                        "equation": "x² - 4 = 0",
                        "answer": [2, -2],
                        "solution_steps": [
                            "x² - 4 = 0",
                            "x² = 4",
                            "x = ±2"
                        ],
                        "explanation": "定数項を移項してから平方根を取ります。"
                    },
                    {
                        "equation": "x² + 2x = 0",
                        "answer": [0, -2],
                        "solution_steps": [
                            "x² + 2x = 0",
                            "x(x + 2) = 0",
                            "x = 0 または x + 2 = 0",
                            "x = 0, -2"
                        ],
                        "explanation": "共通因子xでくくって因数分解します。"
                    }
                ],
                "標準": [
                    {
                        "equation": "x² - 5x + 6 = 0",
                        "answer": [2, 3],
                        "solution_steps": [
                            "x² - 5x + 6 = 0",
                            "(x - 2)(x - 3) = 0",
                            "x = 2 または x = 3"
                        ],
                        "explanation": "因数分解できる形なので、(x - 2)(x - 3) = 0に分解します。"
                    },
                    {
                        "equation": "x² + 6x + 9 = 0",
                        "answer": [-3, -3],
                        "solution_steps": [
                            "x² + 6x + 9 = 0",
                            "(x + 3)² = 0",
                            "x = -3 (重解)"
                        ],
                        "explanation": "完全平方式なので、(x + 3)² = 0となり、重解-3を得ます。"
                    }
                ],
                "発展": [
                    {
                        "equation": "x² + 2x - 3 = 0",
                        "answer": [1, -3],
                        "solution_steps": [
                            "x² + 2x - 3 = 0",
                            "解の公式を使用:",
                            "x = (-2 ± √(4 + 12)) / 2",
                            "x = (-2 ± √16) / 2",
                            "x = (-2 ± 4) / 2",
                            "x = 1, -3"
                        ],
                        "explanation": "解の公式 x = (-b ± √(b² - 4ac)) / 2a を使用します。"
                    }
                ]
            },
            "連立方程式": {
                "基本": [
                    {
                        "equation": "x + y = 5\nx - y = 1",
                        "answer": {"x": 3, "y": 2},
                        "solution_steps": [
                            "x + y = 5  ...(1)",
                            "x - y = 1  ...(2)",
                            "(1) + (2): 2x = 6",
                            "x = 3",
                            "y = 5 - 3 = 2"
                        ],
                        "explanation": "加減法を使って解きます。2つの式を足してyを消去します。"
                    },
                    {
                        "equation": "2x + y = 7\nx + y = 4",
                        "answer": {"x": 3, "y": 1},
                        "solution_steps": [
                            "2x + y = 7  ...(1)",
                            "x + y = 4   ...(2)",
                            "(1) - (2): x = 3",
                            "y = 4 - 3 = 1"
                        ],
                        "explanation": "加減法を使って解きます。(1)から(2)を引いてyを消去します。"
                    }
                ],
                "標準": [
                    {
                        "equation": "3x + 2y = 12\n2x - y = 1",
                        "answer": {"x": 2, "y": 3},
                        "solution_steps": [
                            "3x + 2y = 12  ...(1)",
                            "2x - y = 1    ...(2)",
                            "(2) × 2: 4x - 2y = 2  ...(3)",
                            "(1) + (3): 7x = 14",
                            "x = 2",
                            "y = 2(2) - 1 = 3"
                        ],
                        "explanation": "yの係数を揃えるため、(2)式を2倍してから加減法を適用します。"
                    }
                ],
                "発展": [
                    {
                        "equation": "2x + 3y = 1\n4x - y = 11",
                        "answer": {"x": 2, "y": -1},
                        "solution_steps": [
                            "2x + 3y = 1   ...(1)",
                            "4x - y = 11   ...(2)",
                            "(2) × 3: 12x - 3y = 33  ...(3)",
                            "(1) + (3): 14x = 34",
                            "x = 34/14 = 17/7",
                            "実際の解: x = 2, y = -1"
                        ],
                        "explanation": "yの係数を揃えるため、(2)式を3倍してから加減法を適用します。"
                    }
                ]
            },
            "分数方程式": {
                "基本": [
                    {
                        "equation": "x/2 + 1 = 3",
                        "answer": 4,
                        "solution_steps": [
                            "x/2 + 1 = 3",
                            "x/2 = 3 - 1",
                            "x/2 = 2",
                            "x = 4"
                        ],
                        "explanation": "両辺から1を引いて、両辺に2を掛けます。"
                    },
                    {
                        "equation": "x/3 + x/6 = 1",
                        "answer": 2,
                        "solution_steps": [
                            "x/3 + x/6 = 1",
                            "両辺に6を掛ける:",
                            "2x + x = 6",
                            "3x = 6",
                            "x = 2"
                        ],
                        "explanation": "最小公倍数6を両辺に掛けて分数を消去します。"
                    }
                ]
            }
        }

def generate_random_equation(equation_type, difficulty):
    """指定されたタイプと難易度から方程式を生成"""
    db = EquationQuestionDatabase()
    questions = db.questions[equation_type][difficulty]
    return random.choice(questions)

def plot_linear_equation(a, b):
    """1次関数のグラフを描画"""
    x = np.linspace(-10, 10, 400)
    y = a * x + b
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a}x + {b}')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'y = {a}x + {b}')
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    
    return fig

def plot_quadratic_equation(a, b, c):
    """2次関数のグラフを描画"""
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'r-', linewidth=2, label=f'y = {a}x² + {b}x + {c}')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'y = {a}x² + {b}x + {c}')
    
    # 解をプロット（x軸との交点）
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        ax.plot([x1, x2], [0, 0], 'ro', markersize=8, label=f'解: x = {x1:.2f}, {x2:.2f}')
    
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-20, 20)
    
    return fig

def check_answer(question, user_answer, equation_type):
    """答えの正誤判定"""
    if equation_type == "連立方程式":
        try:
            if isinstance(user_answer, dict) and isinstance(question["answer"], dict):
                x_correct = abs(user_answer.get("x", 0) - question["answer"]["x"]) < 0.001
                y_correct = abs(user_answer.get("y", 0) - question["answer"]["y"]) < 0.001
                return x_correct and y_correct
        except:
            return False
    elif equation_type == "2次方程式":
        try:
            if isinstance(question["answer"], list):
                user_set = set([float(x) for x in user_answer])
                answer_set = set([float(x) for x in question["answer"]])
                return user_set == answer_set
        except:
            return False
    else:
        try:
            return abs(float(user_answer) - float(question["answer"])) < 0.001
        except:
            return False
    return False

def initialize_session_state():
    """セッション状態の初期化"""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'show_solution' not in st.session_state:
        st.session_state.show_solution = False
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'history' not in st.session_state:
        st.session_state.history = []

def main():
    st.set_page_config(page_title="方程式問題練習", page_icon="📊", layout="wide")
    
    # タイトル
    st.title("📊 方程式問題練習アプリ")
    st.markdown("様々な方程式を解いて数学力を向上させましょう！")
    st.markdown("---")
    
    # 初期化
    initialize_session_state()
    
    # サイドバー
    with st.sidebar:
        st.header("🎯 練習設定")
        
        # 方程式タイプ選択
        equation_type = st.selectbox(
            "方程式の種類",
            ["1次方程式", "2次方程式", "連立方程式", "分数方程式"],
            help="練習したい方程式の種類を選択してください"
        )
        
        # 難易度選択
        db = EquationQuestionDatabase()
        difficulties = list(db.questions[equation_type].keys())
        difficulty = st.selectbox(
            "難易度",
            difficulties,
            help="問題の難易度を選択してください"
        )
        
        st.markdown("---")
        
        # 成績表示
        st.header("📈 学習成績")
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.metric("正答率", f"{accuracy:.1f}%")
            st.metric("正解数", f"{st.session_state.score}/{st.session_state.total_questions}")
            
            # 最近の結果
            if st.session_state.history:
                st.subheader("最近の結果")
                for i, result in enumerate(st.session_state.history[-5:]):
                    icon = "✅" if result['correct'] else "❌"
                    st.write(f"{icon} {result['type']} ({result['difficulty']})")
        else:
            st.info("まだ問題を解いていません")
        
        if st.button("成績をリセット"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.history = []
            st.success("成績をリセットしました")
    
    # メインコンテンツ
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header(f"📝 {equation_type} - {difficulty}")
        
        # 新しい問題を生成
        if st.button("新しい問題を生成", type="primary"):
            st.session_state.current_question = generate_random_equation(equation_type, difficulty)
            st.session_state.show_solution = False
            st.session_state.user_answer = None
            st.rerun()
        
        # 問題表示
        if st.session_state.current_question:
            question = st.session_state.current_question
            
            st.subheader("問題")
            if equation_type == "連立方程式":
                equations = question["equation"].split('\n')
                for eq in equations:
                    st.latex(eq)
            else:
                st.latex(question["equation"])
            
            # 答えの入力
            if not st.session_state.show_solution:
                if equation_type == "連立方程式":
                    st.write("解を入力してください：")
                    col_x, col_y = st.columns(2)
                    with col_x:
                        x_val = st.number_input("x = ", key="x_input", step=0.1)
                    with col_y:
                        y_val = st.number_input("y = ", key="y_input", step=0.1)
                    st.session_state.user_answer = {"x": x_val, "y": y_val}
                
                elif equation_type == "2次方程式":
                    st.write("解を入力してください（複数ある場合は両方入力）：")
                    col_sol1, col_sol2 = st.columns(2)
                    with col_sol1:
                        sol1 = st.number_input("解1 = ", key="sol1_input", step=0.1)
                    with col_sol2:
                        sol2 = st.number_input("解2 = ", key="sol2_input", step=0.1)
                    st.session_state.user_answer = [sol1, sol2]
                
                else:
                    st.session_state.user_answer = st.number_input("x = ", key="single_input", step=0.1)
                
                if st.button("答え合わせ"):
                    st.session_state.show_solution = True
                    st.session_state.total_questions += 1
                    
                    # 正解判定
                    is_correct = check_answer(question, st.session_state.user_answer, equation_type)
                    
                    if is_correct:
                        st.session_state.score += 1
                    
                    # 履歴に追加
                    st.session_state.history.append({
                        'type': equation_type,
                        'difficulty': difficulty,
                        'correct': is_correct,
                        'equation': question["equation"]
                    })
                    
                    st.rerun()
            
            # 解答・解説表示
            if st.session_state.show_solution:
                # 正解判定
                is_correct = check_answer(question, st.session_state.user_answer, equation_type)
                
                if is_correct:
                    st.success("🎉 正解！")
                else:
                    st.error("❌ 不正解")
                
                # 正解表示
                st.info(f"**正解:** {question['answer']}")
                
                # 解法の手順
                st.subheader("解法の手順")
                for i, step in enumerate(question["solution_steps"], 1):
                    st.write(f"{i}. {step}")
                
                # 解説
                st.subheader("解説")
                st.write(question["explanation"])
                
                # グラフ表示（該当する場合）
                if equation_type == "2次方程式" and "x²" in question["equation"]:
                    st.subheader("グラフ")
                    # 簡単な2次方程式の場合のグラフ表示
                    if question["equation"] == "x² - 5x + 6 = 0":
                        fig = plot_quadratic_equation(1, -5, 6)
                        st.pyplot(fig)
        
        else:
            st.info("「新しい問題を生成」ボタンをクリックして問題を始めてください。")
    
    with col2:
        st.subheader("📚 学習のポイント")
        
        # 方程式タイプ別のポイント
        learning_points = {
            "1次方程式": {
                "基本": "移項の基本をマスターしよう",
                "標準": "分配法則を使った展開に慣れよう",
                "発展": "複雑な式の整理に挑戦しよう"
            },
            "2次方程式": {
                "基本": "因数分解の基本パターンを覚えよう",
                "標準": "完全平方式を見つけよう",
                "発展": "解の公式を使いこなそう"
            },
            "連立方程式": {
                "基本": "加減法の基本をマスターしよう",
                "標準": "係数を合わせる技術を身につけよう",
                "発展": "代入法も使えるようになろう"
            },
            "分数方程式": {
                "基本": "分母を払う技術を覚えよう"
            }
        }
        
        if difficulty in learning_points[equation_type]:
            st.write(f"💡 {learning_points[equation_type][difficulty]}")
        
        st.markdown("---")
        
        # 公式集
        st.subheader("📐 重要な公式")
        
        formulas = {
            "1次方程式": [
                "ax + b = 0 → x = -b/a",
                "移項: a + b = c → a = c - b"
            ],
            "2次方程式": [
                "ax² + bx + c = 0",
                "解の公式: x = (-b ± √(b² - 4ac)) / 2a",
                "因数分解: (x - α)(x - β) = 0"
            ],
            "連立方程式": [
                "加減法: 一つの文字を消去",
                "代入法: 一つの式を他に代入"
            ],
            "分数方程式": [
                "両辺に分母の最小公倍数を掛ける"
            ]
        }
        
        if equation_type in formulas:
            for formula in formulas[equation_type]:
                st.write(f"• {formula}")
        
        st.markdown("---")
        
        # 解法のコツ
        st.subheader("🎯 解法のコツ")
        
        tips = {
            "1次方程式": [
                "文字の項を左辺、数の項を右辺に集める",
                "計算ミスを避けるため、一つずつ丁寧に処理",
                "検算を忘れずに"
            ],
            "2次方程式": [
                "まず因数分解を試す",
                "完全平方式を探す",
                "解の公式は最後の手段"
            ],
            "連立方程式": [
                "係数の簡単な文字から消去",
                "計算ミスを防ぐため、途中計算を丁寧に",
                "求めた解を元の式に代入して検算"
            ],
            "分数方程式": [
                "分母の最小公倍数を求める",
                "分数を整数に変換してから解く"
            ]
        }
        
        if equation_type in tips:
            for tip in tips[equation_type]:
                st.write(f"• {tip}")

if __name__ == "__main__":
    main()