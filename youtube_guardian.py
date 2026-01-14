import time
import random
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import threading
import json
import logging
import os
import sys


# ==========================================
# PHẦN 1: CLASS SINH ĐỀ TOÁN LỜI VĂN
# ==========================================
class WordProblemGenerator:
    def __init__(self):
        self.names = ["Nam", "Bình", "Lan", "Hoa", "Tuấn", "Minh", "Chi", "Mai"]
        self.items = ["quả táo", "cái kẹo", "viên bi", "quyển vở", "cây bút", "bông hoa"]

    def generate_two_step_problem(self):
        name1 = random.choice(self.names)
        remaining_names = [n for n in self.names if n != name1]
        name2 = random.choice(remaining_names)
        item = random.choice(self.items)

        num1 = random.randint(5, 20)
        problem_type = random.choice(['gap_lan', 'nhieu_hon', 'kem_hon'])

        question_text = ""
        ans_num2 = 0

        if problem_type == 'gap_lan':
            factor = random.randint(2, 4)
            question_text = f"{name1} có {num1} {item}. {name2} có gấp {factor} lần {name1}. Hỏi cả hai bạn có bao nhiêu {item}?"
            ans_num2 = num1 * factor
        elif problem_type == 'nhieu_hon':
            diff = random.randint(5, 15)
            question_text = f"{name1} có {num1} {item}. {name2} nhiều hơn {name1} {diff} {item}. Hỏi cả hai bạn có bao nhiêu {item}?"
            ans_num2 = num1 + diff
        elif problem_type == 'kem_hon':
            num1 = random.randint(20, 50)
            diff = random.randint(5, 10)
            question_text = f"{name1} có {num1} {item}. {name2} ít hơn {name1} {diff} {item}. Hỏi cả hai bạn có bao nhiêu {item}?"
            ans_num2 = num1 - diff

        total_ans = num1 + ans_num2
        return {"question": question_text, "answer": total_ans}


# ==========================================
# PHẦN 2: CẤU HÌNH & LOGGING
# ==========================================
def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


APP_PATH = get_app_path()
CONFIG_PATH = os.path.join(APP_PATH, "config.json")

# Cấu hình mặc định (Phòng trường hợp file lỗi)
DEFAULT_CONFIG = {
    "allowed_time_seconds": 1800,
    "target_keywords": ["YouTube"],
    "parent_passcode": "admin",
    "problem_ratios": {"basic": 20, "round": 20, "roman": 10, "geometry": 0, "word_problem": 50}
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc config: {e}")
            return DEFAULT_CONFIG
    else:
        return DEFAULT_CONFIG


config = load_config()
LOG_PATH = os.path.join(APP_PATH, config.get("log_filename", "nhat_ky_hoc_tap.txt"))

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)


def write_log(message):
    print(message)
    try:
        logging.info(message)
    except Exception:
        pass


# ==========================================
# PHẦN 3: GIAO DIỆN KHÓA MÀN HÌNH (GUI)
# ==========================================
class MathLockScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Giờ học toán!")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.configure(bg="#2C3E50")

        self.word_gen = WordProblemGenerator()
        self.correct_answer = 0

        self.setup_ui()
        self.generate_question()

        write_log("Hệ thống ĐÃ KHÓA màn hình.")

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="Hết giờ chơi rồi!",
                 font=("Arial", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

        tk.Label(main_frame, text="Giải bài toán sau để mở khóa:",
                 font=("Arial", 14), fg="#BDC3C7", bg="#2C3E50").pack(pady=5)

        self.lbl_question = tk.Label(main_frame, text="...", font=("Arial", 40, "bold"),
                                     fg="#F1C40F", bg="#2C3E50", wraplength=0)
        self.lbl_question.pack(pady=30)

        self.entry_answer = tk.Entry(main_frame, font=("Arial", 30), justify='center')
        self.entry_answer.pack(pady=10)
        self.entry_answer.focus_set()

        tk.Button(main_frame, text="Nộp bài", font=("Arial", 20),
                  bg="#27AE60", fg="white", command=self.check_answer).pack(pady=20)
        self.root.bind('<Return>', lambda event: self.check_answer())

    def to_roman(self, num):
        val = [100, 90, 50, 40, 10, 9, 5, 4, 1]
        syb = ["C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num

    def generate_question(self):
        """
        Logic chọn đề bài dựa trên tỉ lệ trong config.json
        """
        # 1. Lấy tỉ lệ từ config
        ratios = config.get("problem_ratios", {})

        # Danh sách các dạng bài hỗ trợ
        # basic: Cộng trừ nhân chia
        # round: Làm tròn số
        # roman: Số La Mã
        # geometry: Hình học (Chu vi, Diện tích)
        # word_problem: Toán lời văn

        # Nếu config chưa có key nào thì set mặc định 0
        w_basic = ratios.get("basic", 0)
        w_round = ratios.get("round", 0)
        w_roman = ratios.get("roman", 0)
        w_geo = ratios.get("geometry", 0)
        w_word = ratios.get("word_problem", 0)

        # Kiểm tra nếu tất cả bằng 0 thì ép về toán cơ bản
        if sum([w_basic, w_round, w_roman, w_geo, w_word]) == 0:
            w_basic = 100

        # Chọn dạng bài dựa trên trọng số (weights)
        choices = ['basic', 'round', 'roman', 'geometry', 'word_problem']
        weights = [w_basic, w_round, w_roman, w_geo, w_word]

        selected_type = random.choices(choices, weights=weights, k=1)[0]

        # --- XỬ LÝ RA ĐỀ THEO DẠNG ĐÃ CHỌN ---

        if selected_type == 'geometry':
            # === DẠNG HÌNH HỌC (CHU VI - DIỆN TÍCH) ===
            self.lbl_question.config(font=("Arial", 30, "bold"), wraplength=900)

            shape = random.choice(['square', 'rect'])  # Vuông hoặc Chữ nhật
            task = random.choice(['chu_vi', 'dien_tich'])  # Tính gì?

            if shape == 'square':
                # HÌNH VUÔNG (Cạnh a)
                a = random.randint(2, 10)  # Cạnh nhỏ để tính diện tích cho dễ
                if task == 'chu_vi':
                    self.correct_answer = a * 4
                    display_text = f"Hình vuông cạnh {a}.\nTính CHU VI?"
                else:
                    self.correct_answer = a * a
                    display_text = f"Hình vuông cạnh {a}.\nTính DIỆN TÍCH?"
            else:
                # HÌNH CHỮ NHẬT (Dài d, Rộng r)
                r = random.randint(2, 9)
                d = random.randint(r + 1, 15)  # Dài phải lớn hơn Rộng
                if task == 'chu_vi':
                    self.correct_answer = (d + r) * 2
                    display_text = f"HCN dài {d}, rộng {r}.\nTính CHU VI?"
                else:
                    self.correct_answer = d * r
                    display_text = f"HCN dài {d}, rộng {r}.\nTính DIỆN TÍCH?"

            self.lbl_question.config(text=display_text)

        elif selected_type == 'roman':
            # === DẠNG SỐ LA MÃ ===
            self.lbl_question.config(font=("Arial", 40, "bold"), wraplength=0)
            roman_sub_type = random.choice(['convert', 'calc'])
            if roman_sub_type == 'convert':
                val = random.randint(1, 50)
                roman_str = self.to_roman(val)
                self.correct_answer = val
                self.lbl_question.config(text=f"{roman_str} = ?", font=("Arial", 35, "bold"))
            else:
                op = random.choice(['+', '-'])
                a = random.randint(1, 20)
                b = random.randint(1, 10)
                if op == '+':
                    self.correct_answer = a + b
                    self.lbl_question.config(text=f"{self.to_roman(a)} + {self.to_roman(b)} = ?")
                else:
                    if a < b: a, b = b, a
                    self.correct_answer = a - b
                    self.lbl_question.config(text=f"{self.to_roman(a)} - {self.to_roman(b)} = ?")

        elif selected_type == 'round':
            # === DẠNG LÀM TRÒN ===
            self.lbl_question.config(font=("Arial", 30, "bold"), wraplength=900)
            number = random.randint(1000, 9999)
            round_target = random.choice(['chuc', 'tram'])
            if round_target == 'chuc':
                self.correct_answer = (number + 5) // 10 * 10
                self.lbl_question.config(text=f"Làm tròn số {number}\nđến hàng chục?")
            else:
                self.correct_answer = (number + 50) // 100 * 100
                self.lbl_question.config(text=f"Làm tròn số {number}\nđến hàng trăm?")

        elif selected_type == 'word_problem':
            # === DẠNG TOÁN LỜI VĂN ===
            problem = self.word_gen.generate_two_step_problem()
            self.correct_answer = problem['answer']
            self.lbl_question.config(text=problem['question'], font=("Arial", 22, "bold"), wraplength=900)

        else:  # selected_type == 'basic'
            # === DẠNG CƠ BẢN (+ - * /) ===
            self.lbl_question.config(font=("Arial", 40, "bold"), wraplength=0)
            type_math = random.choice(['+', '-', '*', '/'])
            if type_math == '+':
                a, b = random.randint(100, 500), random.randint(100, 500)
                self.correct_answer = a + b
                self.lbl_question.config(text=f"{a} + {b} = ?")
            elif type_math == '-':
                a = random.randint(200, 900)
                b = random.randint(100, a)
                self.correct_answer = a - b
                self.lbl_question.config(text=f"{a} - {b} = ?")
            elif type_math == '*':
                a, b = random.randint(2, 9), random.randint(2, 10)
                self.correct_answer = a * b
                self.lbl_question.config(text=f"{a} x {b} = ?")
            elif type_math == '/':
                b = random.randint(2, 9)
                ans = random.randint(2, 10)
                a = b * ans
                self.correct_answer = ans
                self.lbl_question.config(text=f"{a} : {b} = ?")

        self.entry_answer.delete(0, 'end')

    def check_answer(self):
        user_input = self.entry_answer.get()
        if user_input == config.get("parent_passcode", "admin"):
            if messagebox.askyesno("Admin", "Tắt chương trình?"):
                write_log("Admin tắt thủ công.")
                self.root.destroy()
                global keep_running
                keep_running = False
                return

        try:
            val = int(user_input)
            if val == self.correct_answer:
                q_text = self.lbl_question.cget('text').replace('\n', ' ')
                write_log(f"ĐÚNG. Câu: '{q_text}' - Đáp án: {val}")
                messagebox.showinfo("Giỏi lắm!", "Chính xác! Con được xem tiếp.")
                self.root.destroy()
            else:
                write_log(f"SAI. Nhập: {val} - Đáp án đúng: {self.correct_answer}")
                messagebox.showwarning("Sai rồi", "Thử tính lại đi!")
                self.entry_answer.delete(0, 'end')
        except ValueError:
            messagebox.showwarning("Lỗi", "Nhập số thôi nhé!")

    def on_closing(self):
        messagebox.showwarning("Không được!", "Giải toán đi đã!")

    def start(self):
        self.root.mainloop()


# ==========================================
# PHẦN 4: VÒNG LẶP GIÁM SÁT
# ==========================================
keep_running = True


def monitor_activity():
    global config
    write_log("--- Bắt đầu phiên giám sát ---")

    allowed_time = config.get("allowed_time_seconds", 1800)
    keywords = config.get("target_keywords", ["YouTube"])

    watch_time = 0

    while keep_running:
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                title = active_window.title
                if any(k in title for k in keywords):
                    watch_time += 1
                    if watch_time % 60 == 0:
                        print(f"Đang xem: {watch_time}/{allowed_time}")

                    if watch_time >= allowed_time:
                        app = MathLockScreen()
                        app.start()

                        watch_time = 0
                        config = load_config()  # Reload config sau khi mở khóa
                        allowed_time = config.get("allowed_time_seconds", 1800)
                        keywords = config.get("target_keywords", ["YouTube"])
                        write_log(f"Reset đồng hồ. Giới hạn: {allowed_time}s")
                else:
                    pass
            time.sleep(1)
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(1)


if __name__ == "__main__":
    monitor_activity()