"""
Script to update existing activities to published state
Run this once to fix activities created before the is_published field was added
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be.settings')
django.setup()

from api.models import PortfolioActivity
from django.utils import timezone

def update_existing_activities():
    """Set all existing activities to published state"""
    
    # Get all activities that are not published
    unpublished_activities = PortfolioActivity.objects.filter(is_published=False)
    
    count = unpublished_activities.count()
    print(f"Found {count} unpublished activities")
    
    if count == 0:
        print("No activities to update!")
        return
    
    # Update all to published
    for activity in unpublished_activities:
        activity.is_published = True
        activity.published_at = timezone.now()
        activity.save()
        print(f"✅ Updated activity: {activity.title} (ID: {activity.id})")
    
    print(f"\n✅ Successfully updated {count} activities to published state!")

if __name__ == '__main__':
    print("=" * 60)
    print("Updating Existing Activities to Published State")
    print("=" * 60)
    update_existing_activities()
    print("=" * 60)
    print("Done!")
