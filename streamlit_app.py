import random

def generate_question():
    """問題を生成"""
    a = random.choice([1, -1])
    b = random.randint(-9, 9)
    c = random.randint(-9, 9)
    return a, b, c

def calculate_completion(a, b, c):
    """平方完成の答えを計算（修正済）"""
    h = -b / (2 * a)
    k = a * h**2 + b * h + c  # ← ここを修正
    return a, h, k

def format_quadratic(a, b, c):
    """2次関数を文字列で表示"""
    terms = []
    if a == 1:
        terms.append("x²")
    elif a == -1:
        terms.append("-x²")
    else:
        terms.append(f"{a}x²")

    if b > 0:
        terms.append(f"+ {b}x")
    elif b < 0:
        terms.append(f"- {-b}x")

    if c > 0:
        terms.append(f"+ {c}")
    elif c < 0:
        terms.append(f"- {-c}")

    return " ".join(terms)

def format_completion_answer(a, h, k):
    """平方完成の形を整形"""
    if h == 0:
        x_part = "x²"
    elif h > 0:
        x_part = f"(x - {h})²"
    else:
        x_part = f"(x + {-h})²"

    if k > 0:
        return f"{a}{x_part} + {k}"
    elif k < 0:
        return f"{a}{x_part} - {-k}"
    else:
        return f"{a}{x_part}"

def ask_question():
    """問題を出して答え合わせする"""
    a, b, c = generate_question()
    correct_a, h, k = calculate_completion(a, b, c)

    question_str = format_quadratic(a, b, c)
    correct_answer = format_completion_answer(correct_a, h, k)

    print(f"次の式を平方完成してください：\n  f(x) = {question_str}\n")

    user_answer = input("あなたの答えを入力してください（例: 2(x + 3)² - 4）：\n> ")

    if user_answer.replace(" ", "") == correct_answer.replace(" ", ""):
        print("正解です！ 🎉")
    else:
        print(f"不正解です。正しい答えは: {correct_answer}")

# --- 実行部分 ---
if __name__ == "__main__":
    ask_question()
