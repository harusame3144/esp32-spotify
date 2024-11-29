import requests
from io import BytesIO

address = "http://192.168.1.145"

def set_image_theme():
    requests.get(f"{address}/set?theme=3")
    
def set_weather_forecast():
    requests.get(f"{address}/set?theme=1")
    

def upload_image_from_bytes(image_bytes, filename):
    try:
        image_file = BytesIO(image_bytes)
        image_file.seek(0)

        files = {
            "file": (filename, image_file, "image/jpeg")
        }
        
        response = requests.post(f"{address}/doUpload?dir=/image/", files=files)
        response.raise_for_status()

        print("Image uploaded successfully.")
        print("Server response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        
def set_photo_album_image(image_name):
    requests.get(f"{address}/set?img=%2Fimage%2F%{image_name}")