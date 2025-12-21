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
# PHẦN 1: CLASS SINH ĐỀ TOÁN (Đã gộp vào đây)
# ==========================================
class WordProblemGenerator:
    def __init__(self):
        self.names = ["Nam", "Bình", "Lan", "Hoa", "Tuấn", "Minh", "Chi", "Mai"]
        self.items = ["quả táo", "cái kẹo", "viên bi", "quyển vở", "cây bút", "bông hoa"]

    def generate_two_step_problem(self):
        """
        Sinh ra bài toán 2 bước tính (Lớp 3)
        Dạng: A có X. B quan hệ với A (gấp/hơn/kém). Hỏi cả hai?
        """
        name1 = random.choice(self.names)
        remaining_names = [n for n in self.names if n != name1]
        name2 = random.choice(remaining_names)
        item = random.choice(self.items)

        # Số lượng của người thứ nhất (A)
        num1 = random.randint(5, 20)

        # Chọn dạng bài toán quan hệ
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
            num1 = random.randint(20, 50)  # Tăng số lên để trừ không bị âm
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


# ==========================================
# PHẦN 2: CẤU HÌNH & LOGGING
# ==========================================

# Hàm lấy đường dẫn file (Dùng để fix lỗi path khi chạy file .exe)
def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


APP_PATH = get_app_path()
CONFIG_PATH = os.path.join(APP_PATH, "config.json")

# Cấu hình mặc định nếu không tìm thấy file json
DEFAULT_CONFIG = {
    "allowed_time_seconds": 1800,  # 30 phút
    "target_keywords": ["YouTube", "YouTube Kids", "Hoạt hình"],
    "parent_passcode": "admin",
    "log_filename": "nhat_ky_hoc_tap.txt"
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


# Biến config toàn cục
config = load_config()
LOG_PATH = os.path.join(APP_PATH, config.get("log_filename", "nhat_ky_hoc_tap.txt"))

# Thiết lập ghi log
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)


def write_log(message):
    print(message)  # In ra console
    try:
        logging.info(message)  # Ghi vào file
    except Exception:
        pass


# ==========================================
# PHẦN 3: GIAO DIỆN KHÓA MÀN HÌNH (GUI)
# ==========================================
class MathLockScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Giờ học toán!")

        # Fullscreen và Luôn hiện trên cùng
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)

        # Chặn nút tắt
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Màu nền Dark Blue
        self.root.configure(bg="#2C3E50")

        self.word_gen = WordProblemGenerator()
        self.correct_answer = 0

        self.setup_ui()
        self.generate_question()

        write_log("Hệ thống ĐÃ KHÓA màn hình do hết giờ xem.")

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="Hết giờ giải trí rồi!",
                 font=("Arial", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

        tk.Label(main_frame, text="Giải bài toán sau để mở khóa:",
                 font=("Arial", 14), fg="#BDC3C7", bg="#2C3E50").pack(pady=5)

        # Label câu hỏi
        self.lbl_question = tk.Label(main_frame, text="...", font=("Arial", 40, "bold"),
                                     fg="#F1C40F", bg="#2C3E50", wraplength=0)
        self.lbl_question.pack(pady=30)

        # Ô nhập liệu
        self.entry_answer = tk.Entry(main_frame, font=("Arial", 30), justify='center')
        self.entry_answer.pack(pady=10)
        self.entry_answer.focus_set()

        # Nút nộp
        tk.Button(main_frame, text="Nộp bài", font=("Arial", 20),
                  bg="#27AE60", fg="white", command=self.check_answer).pack(pady=20)

        self.root.bind('<Return>', lambda event: self.check_answer())

    def generate_question(self):
        # 50% Toán thường, 50% Toán lời văn
        if random.random() > 0.5:
            # --- Nhánh Toán Cơ Bản ---
            self.lbl_question.config(font=("Arial", 40, "bold"), wraplength=0)

            type_math = random.choice(['+', '-', '*', '/'])
            display_text = ""

            if type_math == '+':
                a = random.randint(100, 500)
                b = random.randint(100, 500)
                self.correct_answer = a + b
                display_text = f"{a} + {b} = ?"

            elif type_math == '-':
                a = random.randint(200, 900)
                b = random.randint(100, a)
                self.correct_answer = a - b
                display_text = f"{a} - {b} = ?"

            elif type_math == '*':
                a = random.randint(2, 9)
                b = random.randint(2, 10)
                self.correct_answer = a * b
                display_text = f"{a} x {b} = ?"

            elif type_math == '/':
                b = random.randint(2, 9)
                ans = random.randint(2, 10)
                a = b * ans
                self.correct_answer = ans
                display_text = f"{a} : {b} = ?"

            self.lbl_question.config(text=display_text)

        else:
            # --- Nhánh Toán Lời Văn ---
            problem = self.word_gen.generate_two_step_problem()
            self.correct_answer = problem['answer']

            self.lbl_question.config(text=problem['question'],
                                     font=("Arial", 22, "bold"),
                                     wraplength=900)

        self.entry_answer.delete(0, 'end')

    def check_answer(self):
        user_input = self.entry_answer.get()

        # Check mật khẩu Admin
        if user_input == config.get("parent_passcode", "admin"):
            if messagebox.askyesno("Admin", "Bố muốn tắt chương trình giám sát không?"):
                write_log("Phụ huynh đã tắt chương trình thủ công.")
                self.root.destroy()
                global keep_running
                keep_running = False
                return

        try:
            val = int(user_input)
            if val == self.correct_answer:
                write_log(f"Con trả lời ĐÚNG. Mở khóa.")
                messagebox.showinfo("Giỏi lắm!", "Chính xác! Con được xem tiếp.")
                self.root.destroy()
            else:
                write_log(f"Con trả lời SAI. Nhập: {val} - Đáp án: {self.correct_answer}")
                messagebox.showwarning("Sai rồi", "Thử tính lại xem nào!")
                self.entry_answer.delete(0, 'end')
        except ValueError:
            messagebox.showwarning("Lỗi", "Con phải nhập số nhé!")

    def on_closing(self):
        messagebox.showwarning("Không được!", "Hãy giải toán để mở khóa!")

    def start(self):
        self.root.mainloop()


# ==========================================
# PHẦN 4: VÒNG LẶP GIÁM SÁT (MAIN LOOP)
# ==========================================
keep_running = True


def monitor_activity():
    global config  # Khai báo global ngay đầu hàm để tránh lỗi

    write_log("--- Bắt đầu phiên giám sát mới ---")
    write_log(f'Thời gian cho phép {config['allowed_time_seconds']}')
    allowed_time = config.get("allowed_time_seconds", 1800)
    keywords = config.get("target_keywords", ["YouTube"])

    watch_time = 0

    while keep_running:
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                title = active_window.title
                # Kiểm tra từ khóa
                if any(k in title for k in keywords):
                    watch_time += 1
                    if watch_time % 60 == 0:
                        write_log(f"Đang xem: {watch_time}/{allowed_time} giây")

                    if watch_time >= allowed_time:
                        # Hết giờ -> Hiện GUI khóa
                        app = MathLockScreen()
                        app.start()  # Code sẽ dừng ở đây cho đến khi cửa sổ bị đóng (giải đúng)

                        # --- Sau khi mở khóa ---
                        watch_time = 0

                        # Nạp lại config mới nhất
                        config = load_config()
                        allowed_time = config.get("allowed_time_seconds", 1800)
                        keywords = config.get("target_keywords", ["YouTube"])

                        write_log(f"Reset đồng hồ. Giới hạn hiện tại: {allowed_time}s")
                else:
                    pass
            time.sleep(1)
        except Exception as e:
            print(f"Lỗi monitor: {e}")
            time.sleep(1)


# ==========================================
# CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    monitor_activity()