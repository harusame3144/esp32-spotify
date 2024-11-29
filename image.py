from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def convert_and_resize_to_jpeg(image_bytes, size=(240, 240)):
    try:
        original_image = Image.open(BytesIO(image_bytes))
        
        converted_image = original_image.convert("RGB")
        
        resized_image = converted_image.resize(size, Image.ANTIALIAS)
        
        jpeg_buffer = BytesIO()
        resized_image.save(jpeg_buffer, format="JPEG")
        jpeg_buffer.seek(0)
        
        print(f"Image resized to {size} and converted to JPEG.")
        return jpeg_buffer
    
    except Exception as e:
        print(f"Image conversion and resizing failed: {e}")
        return None
    
def draw_information(image_bytes, title, artist, position=(10, 10), font_size=20, pg=0):
    try:
        image = Image.open(BytesIO(image_bytes))
        
        image = image.convert("RGBA")
        
        draw = ImageDraw.Draw(image)
        
        font = ImageFont.truetype("NotoSansCJK-Regular.ttc", font_size)
        
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        overlay_draw.rectangle((0, 160, 240, 240), fill=(0, 0, 0, 125))
        
        image = Image.alpha_composite(image, overlay)
        
        draw = ImageDraw.Draw(image)
        
        draw.text(
            position,
            title,
            font=font,
            fill="white",
            font_size=font_size,
            stroke_fill="black",
            stroke_width=2
        )
        
        artistXY = (position[0], position[1]+30)
        
        font = ImageFont.truetype("NotoSansCJK-Regular.ttc", font_size - 4)
        draw.text(
            artistXY,
            artist,
            font=font,
            fill="white",
            stroke_fill="black",
            stroke_width=2
        )
        
        def draw_progress_bar(x, y, width, height, progress, fg=(200, 200, 200), fg2=(50, 50, 50)):
            draw.rectangle((x + (height / 2), y, x + width + (height / 2), y + height), fill=fg2, width=10)
            draw.ellipse((x + width, y, x + height + width, y + height), fill=fg2)
            draw.ellipse((x, y, x + height, y + height), fill=fg2)
            
            width = int(width * progress)
            
            draw.rectangle((x + (height / 2), y, x + width + (height / 2), y + height), fill=fg, width=10)
            draw.ellipse((x + width, y, x + height + width, y + height), fill=fg)
            draw.ellipse((x, y, x + height, y + height), fill=fg)
        
        draw_progress_bar(10, 220, 210, 10, pg)
        
        image = image.convert("RGB")
        
        jpeg_buffer = BytesIO()
        image.save(jpeg_buffer, format="JPEG")
        jpeg_buffer.seek(0)
        
        return jpeg_buffer
    
    except Exception as e:
        print(f"Failed to add text: {e}")
        
        return image_bytes