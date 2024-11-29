from image import convert_and_resize_to_jpeg
from geekmagic import upload_image_from_bytes, set_photo_album_image, set_image_theme, set_weather_forecast

set_weather_forecast()
with open("aaaa.jpg", "rb") as image_file:
    image_bytes = image_file.read()
    
    jpeg_buffer = convert_and_resize_to_jpeg(image_bytes)
    
    if jpeg_buffer:
        upload_url = "http://192.168.1.145/doUpload?dir=/image/"
        upload_image_from_bytes(jpeg_buffer.read(), "auto.jpg", upload_url)
        set_photo_album_image("auto.jpg")
        set_image_theme()