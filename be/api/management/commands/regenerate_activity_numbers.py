from django.core.management.base import BaseCommand
from api.models import PortfolioActivity, PortfolioFolder


class Command(BaseCommand):
    help = 'Regenerate activity numbers for all existing activities'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting activity number regeneration...')
        
        # Get all folders
        folders = PortfolioFolder.objects.all()
        total_updated = 0
        
        for folder in folders:
            if not folder.classroom:
                continue
            
            school_year = folder.classroom.school_year
            
            # Get all activities in this folder, ordered by creation date
            activities = PortfolioActivity.objects.filter(
                folder=folder
            ).order_by('created_at')
            
            # Assign sequential numbers starting from 001
            for index, activity in enumerate(activities, start=1):
                activity.activity_number = f"{index:03d}"
                activity.save(update_fields=['activity_number'])
                total_updated += 1
                
                self.stdout.write(
                    f"  Updated: {activity.title} → {activity.activity_number} "
                    f"(Folder: {folder.name}, School Year: {school_year})"
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully regenerated {total_updated} activity numbers!'
            )
        )
