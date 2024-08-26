import requests

url = "http://localhost:8000/execute_chain/"

# The input you want to send to the agent
data = {
    "input": "onglory last 5 days's net value"
}

# Send the POST request to the server
response = requests.post(url, json=data)

# Check for a successful response
if response.status_code == 200:
    result = response.json()
    print("Result:", result["result"])
else:
    print(f"Error: {response.status_code}, {response.text}")