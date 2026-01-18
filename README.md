# 🛡️ YouTube Guardian - Học Toán Để Xem YouTube

**YouTube Guardian** là một công cụ Python giúp phụ huynh quản lý thời gian xem YouTube của con trên máy tính Windows. Phần mềm áp dụng cơ chế **"Học để được xem tiếp"**: Khi hết thời gian quy định, màn hình sẽ khóa lại và yêu cầu trẻ giải toán để mở khóa.

> **Phiên bản mới:** Hỗ trợ tùy chỉnh tỉ lệ các dạng toán và tách file nhật ký theo ngày.

## ✨ Tính năng nổi bật

* **⏱️ Giám sát thông minh:** Tự động đếm giờ khi con mở các cửa sổ chứa từ khóa (ví dụ: "YouTube", "Hoạt hình").
* **🔒 Khóa màn hình tuyệt đối:** Chế độ Full-screen và Topmost khiến trẻ không thể tắt hay chuyển tab khi hết giờ.
* **📚 Ngân hàng câu hỏi đa dạng (Lớp 3):**
* **Toán cơ bản:** Cộng, Trừ, Nhân, Chia.
* **Toán lời văn:** Tự sinh đề bài ngẫu nhiên (Dạng toán giải bằng 2 bước tính).
* **Làm tròn số:** Làm tròn đến hàng chục, hàng trăm.
* **Số La Mã:** Đổi số sang La Mã và tính toán cộng trừ đơn giản.
* **Hình học (Mới):** Tính Chu vi & Diện tích Hình vuông, Hình chữ nhật, chu vi hình tam giác


* **🎛️ Tùy chỉnh tỉ lệ đề bài:** Phụ huynh có thể cài đặt muốn con làm 100% hình học hoặc 50% toán lời văn thông qua file cấu hình.
* **📝 Nhật ký chi tiết:** Tự động tạo thư mục `logs` và lưu file nhật ký riêng cho từng ngày (Ví dụ: `nhat_ky_2024-01-15.txt`).
* **🕵️ Chế độ ẩn:** Chạy ngầm (Background), không hiện icon gây mất tập trung.

## 🛠️ Cài đặt & Cấu hình

### 1. Yêu cầu hệ thống

* Python 3.x
* Thư viện hỗ trợ:
```bash
pip install pygetwindow pyinstaller

```



### 2. File cấu hình (`config.json`)

File này **BẮT BUỘC** phải nằm cùng thư mục với file `.exe` hoặc file code.

```json
{
    "allowed_time_seconds": 1800,
    "target_keywords": ["YouTube", "YouTube Kids", "Hoạt hình"],
    "parent_passcode": "boeucon",
    "problem_ratios": {
        "basic": 20,
        "round": 20,
        "roman": 10,
        "geometry": 50,
        "word_problem": 0
    }
}

```

**Giải thích tham số:**

* `allowed_time_seconds`: Thời gian xem cho phép (giây). 1800s = 30 phút.
* `parent_passcode`: Mật khẩu để bố/mẹ tắt nóng chương trình (nhập vào ô đáp án).
* **`problem_ratios` (Tỉ lệ dạng bài):** Bạn điền trọng số cho từng dạng.
* `basic`: Cộng trừ nhân chia thường.
* `round`: Làm tròn số.
* `roman`: Số La Mã.
* `geometry`: Hình học (Chu vi/Diện tích).
* `word_problem`: Toán lời văn.
* *Mẹo:* Nếu muốn con ôn tập trung dạng nào, hãy để số đó là 100 và các số khác là 0.



## 🚀 Hướng dẫn đóng gói (.EXE)

Để chạy trên máy con mà không cần cài Python:

1. Mở Terminal tại thư mục dự án.
2. Chạy lệnh build (lệnh này giúp sửa lỗi đường dẫn Windows):
```bash
python -m PyInstaller --noconsole --onefile youtube_guardian.py

```


3. Vào thư mục `dist`, lấy file `youtube_guardian.exe`.
4. **QUAN TRỌNG:** Tạo một thư mục mới, copy **cả 2 file** sau vào đó:
* `youtube_guardian.exe`
* `config.json`



## 📖 Hướng dẫn sử dụng

### Cho con:

1. Con xem YouTube bình thường.
2. Hết giờ -> Màn hình khóa hiện ra kèm bài toán.
3. Con giải đúng -> Màn hình mở, đồng hồ reset.
4. Con giải sai -> Phải tính lại.

### Cho bố mẹ (Admin):

* **Xem nhật ký:** Vào thư mục `logs` (nằm cạnh file exe), mở file theo ngày tương ứng để xem con làm bài đúng hay sai, vào lúc mấy giờ.
* **Tắt khẩn cấp:** Khi màn hình khóa hiện lên, nhập `parent_passcode` vào ô đáp án -> Chọn Yes.
* **Kiểm tra chương trình:** Mở **Task Manager** -> Tab **Details** -> Tìm `youtube_guardian.exe`.

## 🔄 Cách thiết lập tự khởi động

1. Nhấn **Windows + R**, gõ `shell:startup` và Enter.
2. Tạo **Shortcut** của file `.exe`.
3. Kéo Shortcut đó vào thư mục Startup vừa mở.

---

**Made with ❤️ by Dad.**