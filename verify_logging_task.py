import subprocess
import time
import urllib.request
import urllib.error
import sys
import os
import signal

def verify_logging():
    # Start the FastAPI application in the background
    # We use uvicorn directly to control it easier
    print("🚀 Starting FastAPI server...")
    log_file = open("server_logs.txt", "w")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8001", "--no-access-log"],
        stdout=log_file,
        stderr=log_file,
        cwd="/mnt/cachyos/tom/projects/my-fastapi-app",
        env=os.environ.copy() # pass current env
    )

    try:
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5) 

        base_url = "http://127.0.0.1:8001"

        # 1. Successful Request
        print(f"👉 Making request to {base_url}/")
        try:
            with urllib.request.urlopen(f"{base_url}/") as response:
                print(f"   Status: {response.getcode()}")
        except urllib.error.URLError as e:
            print(f"❌ Failed to connect: {e}")
        except Exception as e:
             print(f"❌ Error: {e}")

        # 2. 404 Request
        print(f"👉 Making request to {base_url}/non-existent-route")
        try:
            with urllib.request.urlopen(f"{base_url}/non-existent-route") as response:
                print(f"   Status: {response.getcode()}")
        except urllib.error.HTTPError as e:
             print(f"   Status: {e.code} (Expected)")
        except Exception as e:
             print(f"❌ Error: {e}")

        # Let logs flush
        time.sleep(2)
        
    finally:
        # Terminate the server
        print("🛑 Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        log_file.close()

    # Analyze logs
    print("\n🔍 Analyzing logs...")
    with open("server_logs.txt", "r") as f:
        logs = f.read()
        print("--- raw logs start ---")
        print(logs)
        print("--- raw logs end ---")

        if "INFO:api_logger:method=GET path=/ status=" in logs:
            print("✅ SUCCESS: Found structured log for root path.")
        else:
            print("❌ FAILURE: Did not find structured log for root path.")

        if "INFO:api_logger:method=GET path=/non-existent-route status=404" in logs:
            print("✅ SUCCESS: Found structured log for 404 path.")
        else:
             print("❌ FAILURE: Did not find structured log for 404 path.")

if __name__ == "__main__":
    verify_logging()
