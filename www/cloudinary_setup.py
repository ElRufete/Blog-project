import os
import cloudinary

def setup_cloudinary():
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key = os.environ.get('CLOUDINARY_API_KEY'),
        api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    )
    print("✅ Cloudinary configurado con:", os.environ.get('CLOUDINARY_CLOUD_NAME'))
