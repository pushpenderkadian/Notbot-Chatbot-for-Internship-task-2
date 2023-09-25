import subprocess
import requests
import time

ngrok_command = ["ngrok/ngrok", "http", "8000"] 

ngrok_process = subprocess.Popen(ngrok_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

time.sleep(10)  

ngrok_url = None
try:
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = response.json()
    if "tunnels" in data:
        ngrok_url = data["tunnels"][0]["public_url"]
        print("Ngrok Tunnel URL:", ngrok_url)
    else:
        print("Ngrok tunnel URL not found in API response.")
except requests.RequestException as e:
    print("Error fetching Ngrok URL:", e)
