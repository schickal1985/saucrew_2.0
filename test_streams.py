import requests

url = "https://www.saucrew.de/streams"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    print(f"Testing {url}...")
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    if response.status_code == 200:
        print("Success! Head of content:")
        print(response.text[:200])
    else:
        print("Failed.")
except Exception as e:
    print(f"Error: {e}")
