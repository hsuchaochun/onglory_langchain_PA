import requests
import time
import config
while True:
    body = {
        "params": {
            "number": "1", 
            "interval": "HOUR"
        },
        "project": config.RELEVANCE_PROJECT_ID
    }

    response = requests.post(
        config.RELEVANCE_BASE_URL + f"studios/{config.RELEVANCE_TOOL_ID}/trigger_async", 
        headers=config.RELEVANCE_HEADERS, 
        json=body
    )

    job = response.json()
    job_id = job['job_id']

    poll_url = config.RELEVANCE_BASE_URL + f"/studios/{config.RELEVANCE_TOOL_ID}/async_poll/{job_id}?ending_update_only=true"

    done = False
    while not done:
        poll_response = requests.get(poll_url, headers=config.RELEVANCE_HEADERS).json()
        if poll_response['type'] == "complete" or poll_response['type'] == 'failed':
            done = True
            break
        time.sleep(3)

    print(poll_response)

    time.sleep(3600)
