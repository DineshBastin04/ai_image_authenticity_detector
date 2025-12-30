import requests
import sys

def test_api():
    url = "http://localhost:8000/detect"
    
    # Create a dummy image for testing if one doesn't exist
    from PIL import Image
    import io
    
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
    
    print(f"Testing API at {url}...")
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print("✅ API Connection Successful!")
            print("Response:", response.json())
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server.")
        print("Make sure you are running: 'uvicorn main:app --reload' in the backend folder.")

if __name__ == "__main__":
    test_api()
