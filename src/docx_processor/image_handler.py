import os
import base64
from io import BytesIO
from PIL import Image

def extract_images(soup, output_dir, quality=85, max_size=1200):
    """Extract and save images, return image metadata."""
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    images = []
    for i, img in enumerate(soup.find_all('img')):
        img_src = img.get('src', '')
        
        # For base64 encoded images
        if img_src.startswith('data:image'):
            try:
                # Extract the base64 data
                content_type, data = img_src.split(';base64,')
                image_data = base64.b64decode(data)
                
                # Save the image
                img_format = content_type.split('/')[-1]
                filename = f"image_{i}.{img_format}"
                filepath = os.path.join(images_dir, filename)
                
                # Optimize image size
                image = Image.open(BytesIO(image_data))
                
                # Resize if necessary
                if max(image.size) > max_size:
                    ratio = max_size / max(image.size)
                    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                    image = image.resize(new_size, Image.LANCZOS)
                
                image.save(filepath, optimize=True, quality=quality)
                
                # Get caption if available
                caption = ""
                fig_caption = img.find_next('figcaption')
                if fig_caption:
                    caption = fig_caption.get_text()
                
                images.append({
                    "id": i,
                    "filename": filename,
                    "caption": caption,
                    "path": f"images/{filename}"
                })
                
            except Exception as e:
                print(f"Error processing image {i}: {e}")
    
    return images
