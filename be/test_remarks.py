import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import Remark

print("Testing Remark model...")
print(f"Total remarks: {Remark.objects.count()}")

# Get all remarks
remarks = Remark.objects.all()
for remark in remarks:
    print(f"Remark ID: {remark.id}, is_read: {remark.is_read}, text: {remark.text[:50]}...")

# Test updating a remark
if remarks.exists():
    test_remark = remarks.first()
    print(f"\nTesting update on remark {test_remark.id}...")
    print(f"Before: is_read = {test_remark.is_read}")
    
    test_remark.is_read = True
    test_remark.save()
    
    # Reload from database
    test_remark.refresh_from_db()
    print(f"After: is_read = {test_remark.is_read}")
    
    if test_remark.is_read:
        print("✓ SUCCESS: is_read field is working correctly!")
    else:
        print("✗ FAILED: is_read field not persisting")
else:
    print("No remarks found in database")
