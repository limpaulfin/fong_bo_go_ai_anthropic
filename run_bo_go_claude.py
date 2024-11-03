"""
Bộ Gõ Claude AI - Công cụ hỗ trợ gõ văn bản thông minh với Claude AI

Chức năng chính:
- Theo dõi và sửa lỗi văn bản real-time
- Hỗ trợ đa ngôn ngữ (VN, EN)
- Tự động thống kê token usage
- Xử lý thông minh với context

Author: [Lam Thanh Phong]
Version: 1.0.0
"""

import os
import json
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import requests
from dotenv import load_dotenv
import re
import threading
from datetime import datetime
from PIL import Image
import pystray
import signal
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

keyboard_controller = Controller()
should_scan = False
last_space_time = 0
space_count = 0
DOUBLE_SPACE_THRESHOLD = 0.2

is_calling_api = False

# Constants cho file paths
LOG_FOLDER = "logs"
MY_PROMPT = "my_prompt.md"
API_LOG_FILE = os.path.join(LOG_FOLDER, "api_responses.jsonl")

# Tạo thư mục logs nếu chưa tồn tại
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

def get_correction(text):
    """
    Gửi văn bản đến Claude AI API để sửa lỗi
    """
    global is_calling_api
    try:
        is_calling_api = True
        show_api_status()

        # Đọc context từ file
        context = read_context()

        # Tạo prompt theo format giống file gốc
        prompt = f"""
        {context}

        Format:
        - json, nằm trong dấu ```json
        - cấu trúc của json trả về phải có cấu trúc như sau (đây chỉ là ví dụ):
            {{
                \"correction\": \"[văn bản được sửa]\"
            }}

        Input: \"\"\" {text} \"\"\"
        """

        headers = {
            "x-api-key": api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )

        is_calling_api = False
        clear_api_status()

        if response.status_code == 200:
            api_response = response.json()
            response_text = api_response['content'][0]['text'].strip()

            # Xử lý JSON response như file gốc
            try:
                # Loại bỏ các ký tự markdown ```json và ```
                json_text = re.sub(r'^```json\s*|\s*```$', '', response_text.strip())
                # Parse JSON
                result = json.loads(json_text)
                corrected_text = result.get("correction", text)

                # Log API response
                log_api_response(api_response, text, corrected_text)

                return corrected_text
            except json.JSONDecodeError as e:
                print(f"Lỗi khi phân tích JSON: {str(e)}")
                return text
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return text

    except Exception as e:
        is_calling_api = False
        clear_api_status()
        print(f"Lỗi khi gọi API: {str(e)}")
        return text

def log_api_response(response_data, text_input, corrected_output):
    """
    Ghi log API response với format JSONL
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "input": text_input,
        "output": corrected_output,
        "response_id": response_data.get('id'),
        "model": response_data.get('model'),
        "status": "success"
    }

    try:
        with open(API_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Lỗi khi ghi API log: {str(e)}")

# Thêm các hàm hỗ trợ khác từ file gốc:
# - show_api_status()
# - clear_api_status()
# - read_context()
# - get_selected_text()
# - replace_current_line()
# - on_press()
# - create_tray_icon()
# [Thêm code từ file gốc vào đây]

def show_api_status():
    """Hiển thị trạng thái đang gọi API"""
    if is_calling_api:
        keyboard_controller.type('...')

def clear_api_status():
    """Xóa trạng thái API"""
    for _ in range(3):
        keyboard_controller.press(Key.backspace)
        keyboard_controller.release(Key.backspace)
        time.sleep(0.01)

def read_context():
    """
    Đọc nội dung từ file my_prompt.md
    """
    try:
        if os.path.exists(MY_PROMPT):
            with open(MY_PROMPT, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return ""
    except Exception as e:
        print(f"Lỗi khi đọc context: {str(e)}")
        return ""

def get_selected_text():
    """
    Lấy văn bản được chọn hoặc văn bản từ vị trí hiện tại đến đầu dòng
    """
    original = pyperclip.paste()  # Lưu clipboard gốc
    has_selection = False
    selected_text = ""

    try:
        # Thử lấy selection hiện tại (nếu có)
        with keyboard_controller.pressed(Key.ctrl):
            keyboard_controller.tap('c')
        time.sleep(0.1)

        selected_text = pyperclip.paste()
        has_selection = selected_text != original and selected_text.strip() != ""

        if not has_selection:
            # Select từ vị trí hiện tại đến đầu dòng
            keyboard_controller.press(Key.shift)
            keyboard_controller.press(Key.home)
            keyboard_controller.release(Key.home)
            keyboard_controller.release(Key.shift)
            time.sleep(0.1)

            # Copy với retry
            max_retries = 3
            for _ in range(max_retries):
                with keyboard_controller.pressed(Key.ctrl):
                    keyboard_controller.tap('c')
                time.sleep(0.1)

                selected_text = pyperclip.paste()
                if selected_text and selected_text != original:
                    break
                time.sleep(0.1)

            # Hủy selection
            keyboard_controller.tap(Key.right)

        return selected_text, has_selection

    except Exception as e:
        print(f"Lỗi khi lấy text: {str(e)}")
        return "", False

    finally:
        # Restore clipboard gốc
        time.sleep(0.1)
        pyperclip.copy(original)

def replace_current_line(new_text, has_selection):
    """
    Thay thế dòng hiện tại với văn bản mới
    """
    original = pyperclip.paste()
    max_retries = 3

    try:
        # Copy new_text vào clipboard
        for _ in range(max_retries):
            pyperclip.copy(new_text)
            time.sleep(0.1)
            if pyperclip.paste() == new_text:
                break

        if has_selection:
            # Paste vào vùng đã select
            with keyboard_controller.pressed(Key.ctrl):
                keyboard_controller.tap('v')
            time.sleep(0.1)
        else:
            # Select từ vị trí hiện tại đến đầu dòng
            keyboard_controller.press(Key.shift)
            keyboard_controller.press(Key.home)
            keyboard_controller.release(Key.home)
            keyboard_controller.release(Key.shift)
            time.sleep(0.1)

            # Paste text mới
            with keyboard_controller.pressed(Key.ctrl):
                keyboard_controller.tap('v')
            time.sleep(0.1)

            # Di chuyển con trỏ về cuối
            keyboard_controller.tap(Key.end)

    finally:
        # Restore clipboard gốc
        time.sleep(0.2)
        for _ in range(max_retries):
            pyperclip.copy(original)
            if pyperclip.paste() == original:
                break
            time.sleep(0.1)

def on_press(key):
    """
    Xử lý sự kiện nhấn phím
    """
    global should_scan, last_space_time, space_count
    try:
        # Xử lý Double Right Shift
        if key == Key.shift_r:
            current_time = time.time()
            time_diff = current_time - last_space_time

            if time_diff < DOUBLE_SPACE_THRESHOLD:
                space_count += 1
                if space_count == 2:
                    should_scan = True
                    space_count = 0
            else:
                space_count = 1

            last_space_time = current_time

        # Xử lý Double Space
        elif key == Key.space:
            current_time = time.time()
            time_diff = current_time - last_space_time

            if time_diff < DOUBLE_SPACE_THRESHOLD:
                space_count += 1
                if space_count == 2:
                    should_scan = True
                    space_count = 0
            else:
                space_count = 1

            last_space_time = current_time
        else:
            if space_count > 0:
                space_count = 0

    except AttributeError:
        pass

def create_tray_icon():
    """
    Tạo system tray icon với menu context
    """
    def on_quit(icon):
        icon.stop()
        os._exit(0)

    def restart_script(icon):
        icon.stop()
        script_path = os.path.abspath(__file__)
        if os.name == 'nt':  # Windows
            os.system(f'start pythonw "{script_path}"')
        else:  # Linux/Mac
            os.system(f'python3 "{script_path}" &')
        os._exit(0)

    def open_source_location(icon):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.startfile(script_dir) if os.name == 'nt' else os.system(f'xdg-open "{script_dir}"')

    try:
        image = Image.open("icon.png")
    except Exception as e:
        print(f"Lỗi khi load icon: {str(e)}")
        image = Image.new('RGB', (64, 64), color='red')

    menu = pystray.Menu(
        pystray.MenuItem("Cách sử dụng Bộ Gõ Claude AI:", None, enabled=False),
        pystray.MenuItem("- Double Space để scan", None, enabled=False),
        pystray.MenuItem("- Double Right Shift để scan", None, enabled=False),
        pystray.MenuItem("Open Location", open_source_location),
        pystray.MenuItem("Restart Script", restart_script),
        pystray.MenuItem("Terminate Script", on_quit)
    )

    icon = pystray.Icon(
        "bo_go_claude_ai",
        image,
        "Bộ Gõ Claude AI (Double Space/Right Shift để scan)",
        menu
    )

    return icon

def main():
    global should_scan
    try:
        print("Bộ Gõ Claude AI đang chạy...")

        # Khởi tạo listener và tray icon
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        tray_icon = create_tray_icon()
        tray_icon.run_detached()

        while True:
            time.sleep(0.5)
            if should_scan:
                line, has_selection = get_selected_text()
                if line.strip():
                    print("\n" + "="*50)
                    print(f"Văn bản gốc: '{line}'")
                    corrected_text = get_correction(line)
                    print(f"Văn bản đã sửa: '{corrected_text}'")
                    print("="*50)
                    replace_current_line(corrected_text, has_selection)
                should_scan = False

    except KeyboardInterrupt:
        print("\nĐã dừng script.")
        sys.exit(0)

if __name__ == "__main__":
    main()

