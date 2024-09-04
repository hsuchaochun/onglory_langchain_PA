import requests
import sys

url = "https://4bc7-185-213-82-87.ngrok-free.app/execute_chain/"
# url = "http://localhost:8000/chain/"

# Check if the user has provided the input argument
if len(sys.argv) < 2:
    print("Usage: python3 xxx.py 'input'")
    sys.exit(1)

# Get the input from the command line argument
user_input = sys.argv[1]

# The input you want to send to the agent
data = {
    "input": user_input
}


# Send the POST request to the server
response = requests.post(url, json=data)

# Check for a successful response
if response.status_code == 200:
    result = response.json()
    print("Result:", result["result"])
else:
    print(f"Error: {response.status_code}, {response.text}")