
import requests
import logging
import schedule
import time
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

# Configure logging for DuckDNS updates
duckdns_logger = logging.getLogger("DuckDNS")
duckdns_handler = logging.FileHandler("duckdns.log")
duckdns_formatter = logging.Formatter("| %(asctime)s | %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p")
duckdns_handler.setFormatter(duckdns_formatter)
duckdns_logger.addHandler(duckdns_handler)
duckdns_logger.setLevel(logging.INFO)

# Configure logging for sending IP to personal server
ip_logger = logging.getLogger("IPUpdater")
ip_handler = logging.FileHandler("stillkonfuzed.log")
ip_formatter = logging.Formatter("| %(asctime)s | %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p")
ip_handler.setFormatter(ip_formatter)
ip_logger.addHandler(ip_handler)
ip_logger.setLevel(logging.INFO)

load_dotenv()

# Get credentials from .env
DUCKDNS_DOMAIN = os.getenv("DUCKDNS_DOMAIN")
DUCKDNS_TOKEN = os.getenv("DUCKDNS_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

DUCKDNS_URL = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&verbose=true"

IP_SERVICE_URL = "https://api64.ipify.org?format=json"
SERVER_URL = f"{SERVER_URL}"
# Secret Key for Server Authentication
SECRET = f"{SECRET_KEY}"

def update_duckdns():
    """Updates DuckDNS and logs response."""
    try:
        response = requests.get(DUCKDNS_URL)
        response_lines = response.text.strip().split("\n")
        
        status = response_lines[0] if len(response_lines) > 0 else "Unknown"
        ip_address = response_lines[1] if len(response_lines) > 1 else "Unknown"

        log_message = f"| {ip_address} | {'Updated' if status == 'OK' else 'Failed'} | {status} |"
        duckdns_logger.info(log_message)
        print(log_message)

    except Exception as e:
        error_message = f"| Error | {e} |"
        duckdns_logger.error(error_message)
        print(error_message)

def send_ip_to_server():
    """Fetches the external IP and sends it to the personal server."""
    try:
        # Get External IP
        response = requests.get(IP_SERVICE_URL)
        ip_data = response.json()
        ip_address = ip_data.get("ip", "Unknown")

        if ip_address == "Unknown":
            raise ValueError("Failed to fetch external IP")

        # Generate timestamp & encoded secret
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        encoded_secret = base64.b64encode(SECRET.encode("utf-8")).decode("utf-8")

        # Send request to personal server
        payload = {
            "ip": ip_address,
            "timestamp": timestamp,
            "xString": encoded_secret
        }
        # server_response = requests.post(SERVER_URL, data=payload)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        server_response = requests.post(SERVER_URL, data=payload, headers=headers)

        server_response_text = server_response.text.strip()

        log_message = f"| {ip_address} | Sent to Server | Response: {server_response_text} |"
        ip_logger.info(log_message)
        print(log_message)

    except Exception as e:
        error_message = f"| Error | {e} |"
        ip_logger.error(error_message)
        print(error_message)

# Schedule both tasks
schedule.every(10).minutes.do(update_duckdns)
schedule.every(10).minutes.do(send_ip_to_server)

if __name__ == "__main__":
    print("DuckDNS & IP Updater Service Started...")
    update_duckdns()  # Run once immediately
    send_ip_to_server()  # Run once immediately
    while True:
        schedule.run_pending()
        time.sleep(1)

