import requests
import sys
import argparse
import json
from typing import Dict, Any

def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description="Send input to LangChain server")
    parser.add_argument('input', type=str, help='Input to send to the server')
    args = parser.parse_args()
    return args.input

def send_request(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        sys.exit(1)

def main():
    url = "https://4bc7-185-213-82-87.ngrok-free.app/execute_chain/"
    # url = "http://localhost:8000/chain/"

    user_input = parse_arguments()
    data = {"input": user_input}

    result = send_request(url, data)
    
    print("Result:", json.dumps(result["result"], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()