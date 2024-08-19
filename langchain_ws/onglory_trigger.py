import requests

# Define the server URL and the endpoint
url = "http://localhost:8000/onglory"

# Define the payload with the question and session_id
data = {
    "input": {
        "question": "Not trading history, but investment overview",
        "session_id": "test_session_123"
    }
}

# Send a POST request to the server
response = requests.post(url, json=data)

# Print the server's response
print("Server response:\n", response.json()['result'])