import os
import json
import requests
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

def chat_with_claude(prompt):
    try:
        headers = {
            "x-api-key": os.getenv('ANTHROPIC_API_KEY'),
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": "claude-3-haiku-20240307",  # Chuyển sang model Haiku
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

        if response.status_code == 200:
            api_response = response.json()

            # Tạo JSON response
            result = {
                "status": "success",
                "message": api_response['content'][0]['text'],
                "model": api_response['model'],
                "role": api_response['role']
            }
            return json.dumps(result, ensure_ascii=False, indent=2)
        else:
            error_result = {
                "status": "error",
                "error_code": response.status_code,
                "error_message": response.text
            }
            return json.dumps(error_result, ensure_ascii=False, indent=2)

    except Exception as e:
        error_result = {
            "status": "error",
            "error_message": str(e)
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)

def main():
    # Ví dụ sử dụng
    prompt = "Xin chào, bạn là ai?"
    response = chat_with_claude(prompt)
    print(response)  # In ra JSON response

if __name__ == "__main__":
    main()
