import requests

# Test the API
base_url = "http://localhost:8000"

# Test root
response = requests.get(f"{base_url}/")
print("Root status:", response.status_code)
if response.status_code == 200:
    print("Frontend served successfully")

# Test detect with an image
image_path = "shared/Screenshot 2026-03-08 213256 - Copy.png"
with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(f"{base_url}/detect", files=files)

print("Detect status:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Task ID:", data.get("task_id"))
    task_id = data.get("task_id")
    if task_id:
        # Poll for result
        import time
        for _ in range(10):  # Poll up to 10 times
            response = requests.get(f"{base_url}/result/{task_id}")
            data = response.json()
            print("Status:", data.get("status"))
            if data.get("status") == "SUCCESS":
                print("Result:", data.get("result"))
                break
            time.sleep(1)
        else:
            print("Task did not complete in time")
else:
    print("Detect failed:", response.text)