# Bộ Gõ Claude AI

Công cụ hỗ trợ gõ văn bản thông minh sử dụng Claude AI (Anthropic) để tự động sửa lỗi chính tả và cải thiện văn bản theo thời gian thực.

## Tính năng chính

-   Theo dõi và sửa lỗi văn bản real-time
-   Hỗ trợ đa ngôn ngữ (Tiếng Việt, Tiếng Anh)
-   Tự động ghi log API responses
-   Xử lý thông minh với context từ file `my_prompt.md`
-   System tray icon cho dễ dàng quản lý

## Cách hoạt động

1. Theo dõi keyboard input
2. Kích hoạt bằng:
    - Double Space
    - Double Right Shift
3. Lấy văn bản từ vị trí con trỏ đến đầu dòng
4. Gửi API đến Claude AI để sửa lỗi
5. Thay thế văn bản cũ bằng văn bản đã sửa

## Cài đặt

1. Tạo môi trường ảo:

`python -m venv claude-env`

2. Kích hoạt môi trường ảo:

-   Windows:
    `claude-env\Scripts\activate`
-   Linux/Mac:
    `source claude-env/bin/activate`

4. Tạo file `.env` và thêm API key:
   `ANTHROPIC_API_KEY=your_api_key_here`

## Cách sử dụng

1. Chạy file `run_bo_go_claude.bat` hoặc:
   pythonw run_bo_go_claude.py

2. Kích hoạt bằng một trong các cách:

    - Nhấn Double Space
    - Nhấn Double Right Shift
    - Chọn text và nhấn Double Right Shift

3. Chương trình sẽ tự động:
    - Hiển thị "..." khi đang xử lý
    - Thay thế văn bản cũ bằng văn bản đã sửa
    - Ghi log vào thư mục `logs`

## Cấu trúc thư mục

```
.
├── run_bo_go_claude.py # File chính
├── run_bo_go_claude.bat # File khởi chạy cho Windows
├── requirements.txt # Các thư viện cần thiết
├── my_prompt.md # File chứa context và persona
├── icon.png # Icon cho system tray
├── .env # File chứa API key
└── logs/ # Thư mục chứa logs
└── api_responses.jsonl
```
## Tùy chỉnh

-   Chỉnh sửa `my_prompt.md` để thay đổi persona và context
-   Điều chỉnh các thông số trong code:
    -   `DOUBLE_SPACE_THRESHOLD`: Thời gian giữa 2 lần nhấn space
    -   `max_tokens`: Giới hạn tokens cho mỗi request

## Ghi chú

-   Cần có API key hợp lệ từ Anthropic
-   Sử dụng Claude 3 Haiku model
-   Hỗ trợ Windows, Linux và macOS (một số tính năng có thể khác nhau)

## Tác giả

[IRONTAN Vietnam LTD.]

# Claude AI Typing Assistant

A smart text input assistant powered by Claude AI

## Features

-   Real-time text monitoring and correction
-   Multi-language support (VN, EN)
-   Automatic token usage tracking
-   Smart context handling

## Installation

1. Clone the repository:
   `git clone https://github.com/yourusername/claude-typing-assistant.git`

2. Install dependencies:
   pip install -r requirements.txt

3. Create virtual environment:

-   Windows:
    `python -m venv claude-env`
    `claude-env\Scripts\activate`

-   Linux/Mac:
    `python -m venv claude-env`
    `source claude-env/bin/activate`

4. Create `.env` file and add API key:
   `ANTHROPIC_API_KEY=your_api_key_here`

## Usage

1. Run `run_bo_go_claude.bat` or:
   pythonw run_bo_go_claude.py

2. Activate using one of these methods:

    - Press Double Space
    - Press Double Right Shift
    - Select text and press Double Right Shift

3. The program will automatically:
    - Show "..." while processing
    - Replace old text with corrected text
    - Log to the `logs` directory

## Directory Structure

```
.
├── run_bo_go_claude.py # Main script
├── run_bo_go_claude.bat # Windows launcher
├── requirements.txt # Required libraries
├── my_prompt.md # Context and persona file
├── icon.png # System tray icon
├── .env # API key file
└── logs/ # Log directory
└── api_responses.jsonl
```
## Customization

-   Edit `my_prompt.md` to change persona and context
-   Adjust parameters in code:
    -   `DOUBLE_SPACE_THRESHOLD`: Time between space presses
    -   `max_tokens`: Token limit per request

## Notes

-   Requires valid Anthropic API key
-   Uses Claude 3 Haiku model
-   Supports Windows, Linux and macOS (some features may vary)

## Author

[IRONTAN Vietnam LTD.]
