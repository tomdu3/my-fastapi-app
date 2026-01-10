import httpx
import time

def test_signup_background():
    url = "http://127.0.0.1:8000/signup/"
    params = {"email": "test@example.com"}
    
    start_time = time.time()
    
    print(f"🚀 Sending request to {url}...")
    response = httpx.post(url, params=params)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️ Response received in {duration:.4f}s")
    print(f"📦 Response JSON: {response.json()}")
    
    # Assertions
    assert response.status_code == 200
    assert "Signup successful" in response.json()["message"]
    assert duration < 1.0, f"Response was too slow: {duration:.4f}s"
    
    print("✅ Test passed! Response was immediate.")
    print("🔔 NOTE: Check the FastAPI server logs to confirm 'Email sent' appears in ~5 seconds.")

if __name__ == "__main__":
    try:
        test_signup_background()
    except Exception as e:
        print(f"❌ Test failed: {e}")
