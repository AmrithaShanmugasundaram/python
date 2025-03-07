import requests

url = "http://localhost:8080/upload"
files = {"file": open(r"C:\Users\amrit\Downloads\Balancesheet_Rep 1.pdf", "rb")}  # Corrected absolute path

response = requests.post(url, files=files)
print(response.json())  # Should return success message
