import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
import django
django.setup()

from api.models import PortfolioFolder, User, Classroom

print("=" * 80)
print("ORPHAN FOLDERS TO DELETE")
print("=" * 80)

orphan_folders = []
all_folders = PortfolioFolder.objects.select_related('teacher', 'classroom').all()

for folder in all_folders:
    if folder.classroom and folder.teacher:
        if folder.classroom.teacher != folder.teacher:
            orphan_folders.append(folder)
            print(f"ID {folder.id}: '{folder.name}' in {folder.classroom.name} by {folder.teacher.username}")

print(f"\nTotal: {len(orphan_folders)}")
print("\nDeleting...")

for f in orphan_folders:
    f.delete()

print("Done!")
