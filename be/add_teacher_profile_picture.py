#!/usr/bin/env python
"""
Add a profile picture to test_teacher user
This script creates a simple colored avatar as a placeholder
"""
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import User

def create_avatar_image(initials, size=200, bg_color=(99, 102, 241), text_color=(255, 255, 255)):
    """Create a simple avatar image with initials"""
    # Create image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size // 2)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2 - 10)
    
    # Draw text
    draw.text(position, initials, fill=text_color, font=font)
    
    return img

def add_profile_picture():
    try:
        # Get test_teacher user
        teacher = User.objects.get(username='test_teacher')
        
        print(f"\n{'='*60}")
        print(f"Adding Profile Picture to test_teacher")
        print(f"{'='*60}")
        
        # Create avatar image
        initials = "TT"  # Test Teacher
        img = create_avatar_image(initials)
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Create InMemoryUploadedFile
        img_file = InMemoryUploadedFile(
            img_io,
            None,
            'test_teacher_avatar.png',
            'image/png',
            img_io.getbuffer().nbytes,
            None
        )
        
        # Save to user
        teacher.profile_picture = img_file
        teacher.save()
        
        print(f"✅ Profile picture added successfully!")
        print(f"   Path: {teacher.profile_picture.path}")
        print(f"   URL: {teacher.profile_picture.url}")
        print(f"{'='*60}\n")
        
    except User.DoesNotExist:
        print("❌ test_teacher user not found!")
        print("   Run the application first to create the test user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_profile_picture()
