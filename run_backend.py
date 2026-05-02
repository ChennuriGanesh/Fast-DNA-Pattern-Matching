import requests

url = "http://127.0.0.1:5000/run"

files = {
    "fasta_file": open("ecoli.fasta", "rb")
}

data = {
    "algorithm": "wm",   # or "wm"
    "m": 64,
    "d": 1000
}

response = requests.post(url, files=files, data=data)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())
