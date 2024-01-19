import requests

url = "http://127.0.0.1:8000/inference-image"
files = {"file": ("test.jpg", open("test.jpg", "rb"), "image/png")}
headers = {"accept": "application/json"}

response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:
    # do something with the response
    pass
else:
    print("Error:", response.text)