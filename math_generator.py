import random


class WordProblemGenerator:
    def __init__(self):
        self.names = ["Nam", "Bình", "Lan", "Hoa", "Tuấn", "Minh", "Chi"]
        self.items = ["quả táo", "cái kẹo", "viên bi", "quyển vở", "cây bút"]

    def generate_two_step_problem(self):
        """
        Sinh ra bài toán 2 bước tính (Lớp 3)
        Dạng: A có X. B quan hệ với A. Hỏi tổng cả hai?
        """
        name1 = random.choice(self.names)
        remaining_names = [n for n in self.names if n != name1]
        name2 = random.choice(remaining_names)
        item = random.choice(self.items)

        # Số lượng của người thứ nhất (A)
        # Chọn số nhỏ để trẻ dễ nhẩm (Lớp 3 nhẩm trong phạm vi 100 hoặc 1000)
        num1 = random.randint(5, 20)

        # Chọn dạng bài toán quan hệ
        # 1: Gấp n lần (Nam có 5, Bình gấp 3)
        # 2: Nhiều hơn (Nam có 5, Bình nhiều hơn 3)
        # 3: Kém hơn (Nam có 15, Bình kém 5)
        problem_type = random.choice(['gap_lan', 'nhieu_hon', 'kem_hon'])

        question_text = ""
        ans_num2 = 0

        if problem_type == 'gap_lan':
            factor = random.randint(2, 4)  # Gấp 2, 3 hoặc 4 lần
            question_text = f"{name1} có {num1} {item}. {name2} có số {item} gấp {factor} lần {name1}. Hỏi cả hai bạn có tất cả bao nhiêu {item}?"
            ans_num2 = num1 * factor

        elif problem_type == 'nhieu_hon':
            diff = random.randint(5, 15)
            question_text = f"{name1} có {num1} {item}. {name2} có nhiều hơn {name1} {diff} {item}. Hỏi cả hai bạn có tất cả bao nhiêu {item}?"
            ans_num2 = num1 + diff

        elif problem_type == 'kem_hon':
            # Nếu kém hơn thì num1 phải đủ lớn
            num1 = random.randint(20, 50)
            diff = random.randint(5, 10)
            question_text = f"{name1} có {num1} {item}. {name2} có ít hơn {name1} {diff} {item}. Hỏi cả hai bạn có tất cả bao nhiêu {item}?"
            ans_num2 = num1 - diff

        # Tính tổng (Đáp án cuối cùng)
        total_ans = num1 + ans_num2

        return {
            "question": question_text,
            "answer": total_ans,
            "hint": f"Gợi ý: Tính số của {name2} trước, sau đó cộng với số của {name1}."
        }


# --- Test thử ---
if __name__ == "__main__":
    gen = WordProblemGenerator()
    for i in range(3):
        problem = gen.generate_two_step_problem()
        print(f"Câu hỏi: {problem['question']}")
        print(f"Đáp án: {problem['answer']}")
        print("-" * 20)