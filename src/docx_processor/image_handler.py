import os
import base64
import re
from io import BytesIO
from PIL import Image
import uuid

def extract_images(soup, output_dir, quality=85, max_size=1200):
    """Extract and save images, return image metadata.
    
    Args:
        soup: BeautifulSoup object containing the HTML document
        output_dir: Directory to save extracted images
        quality: JPEG image quality (1-100)
        max_size: Maximum dimension for images
        
    Returns:
        List of dictionaries with image metadata
    """
    # Return empty list if soup is None
    if soup is None:
        print("Warning: BeautifulSoup object is None, no images to extract")
        return []
    
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    images = []
    try:
        # Find all image tags
        img_tags = soup.find_all('img')
        print(f"Found {len(img_tags)} image tags in the document")
        
        for i, img in enumerate(img_tags):
            try:
                # Debug image tag
                print(f"Processing image {i}: {img}")
                
                img_src = img.get('src', '')
                if not img_src:
                    print(f"Image {i} has no src attribute")
                    continue
                
                # Handle different image source formats
                if img_src.startswith('data:image'):
                    # Base64 encoded image (from data_uri)
                    try:
                        # Extract the base64 data
                        parts = img_src.split(';base64,')
                        if len(parts) != 2:
                            print(f"Image {i} has invalid base64 format")
                            continue
                            
                        content_type, data = parts
                        img_format = content_type.split('/')[-1]
                        image_data = base64.b64decode(data)
                        
                        # Generate unique filename
                        filename = f"image_{i}_{uuid.uuid4().hex[:8]}.{img_format}"
                        filepath = os.path.join(images_dir, filename)
                        
                        # Process and save the image
                        process_and_save_image(image_data, filepath, quality, max_size)
                        
                        # Get caption if available
                        caption = extract_caption(img)
                        
                        images.append({
                            "id": i,
                            "filename": filename,
                            "caption": caption,
                            "path": f"images/{filename}"
                        })
                        print(f"Successfully extracted base64 image: {filename}")
                    except Exception as e:
                        print(f"Error processing base64 image {i}: {e}")
                
                elif img_src.startswith('http://') or img_src.startswith('https://'):
                    # External URL - we'd need to download it
                    # This is not implemented to avoid external dependencies
                    print(f"Image {i} is an external URL, not supported: {img_src[:50]}")
                
                elif re.match(r'^[a-zA-Z0-9_./-]+\.(jpg|jpeg|png|gif|bmp|svg|webp)$', img_src, re.IGNORECASE):
                    # Looks like a local file path
                    print(f"Image {i} appears to be a local file reference: {img_src}")
                    # Could implement file copying logic here if needed
                
                else:
                    # Unknown format
                    print(f"Image {i} has unknown source format: {img_src[:50]}")
                    
            except Exception as e:
                print(f"Error processing image {i}: {e}")
                
    except Exception as e:
        print(f"Error finding images: {e}")
        # Continue processing without images
    
    return images

def process_and_save_image(image_data, filepath, quality, max_size):
    """Process and save an image with resizing and quality settings."""
    # Open the image from binary data
    image = Image.open(BytesIO(image_data))
    
    # Resize if necessary
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(new_size, Image.LANCZOS)
    
    # Handle different image formats
    if image.format == 'PNG':
        image.save(filepath, optimize=True)
    else:
        # Default to JPEG for other formats with quality setting
        if image.mode in ('RGBA', 'LA'):
            # Convert transparency to white background for JPEG
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
            background.save(filepath, 'JPEG', quality=quality, optimize=True)
        else:
            image.convert('RGB').save(filepath, 'JPEG', quality=quality, optimize=True)

def extract_caption(img):
    """Extract image caption from different possible sources."""
    caption = ""
    
    # Check for figcaption
    fig_caption = img.find_next('figcaption')
    if fig_caption:
        caption = fig_caption.get_text()
    
    # Check for alt text
    if not caption and img.get('alt'):
        caption = img.get('alt')
    
    # Check for title attribute
    if not caption and img.get('title'):
        caption = img.get('title')
    
    return caption
