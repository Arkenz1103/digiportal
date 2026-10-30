import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import SchoolYear, Classroom, PortfolioFolder, User

# Get rafael.gomez
teacher = User.objects.get(username='rafael.gomez')
print(f'Teacher: {teacher.username} (ID: {teacher.id})')

# Get all school years for this teacher
print('\n=== School Years for rafael.gomez ===')
school_years = SchoolYear.objects.filter(teacher=teacher).order_by('-start_date')
for sy in school_years:
    print(f'  ID:{sy.id} | {sy.name} | current:{sy.is_current} | archived:{sy.is_archived}')

# Get folders for rafael.gomez
print('\n=== Folders for rafael.gomez ===')
folders = PortfolioFolder.objects.filter(teacher=teacher).select_related('classroom')
for f in folders:
    if f.classroom:
        print(f'  Folder: {f.name} | Classroom ID:{f.classroom.id} {f.classroom.name} | SY:{f.classroom.school_year} | Archived:{f.classroom.is_archived}')
    else:
        print(f'  Folder: {f.name} | No classroom')

# Check archived school years API logic
print('\n=== Archived School Years API Logic ===')
archived_years = SchoolYear.objects.filter(is_archived=True, teacher=teacher).order_by('-archived_at')
for sy in archived_years:
    print(f'\nSchool Year: {sy.name} (ID: {sy.id})')
    
    # Get classrooms where teacher has folders
    teacher_folders = PortfolioFolder.objects.filter(
        teacher=teacher,
        classroom__school_year=sy.name,
        classroom__is_archived=True
    ).select_related('classroom')
    
    classroom_ids = set(f.classroom_id for f in teacher_folders if f.classroom_id)
    print(f'  Classrooms with folders (archived): {classroom_ids}')
    
    # Also check without is_archived filter
    teacher_folders_all = PortfolioFolder.objects.filter(
        teacher=teacher,
        classroom__school_year=sy.name
    ).select_related('classroom')
    
    classroom_ids_all = set(f.classroom_id for f in teacher_folders_all if f.classroom_id)
    print(f'  Classrooms with folders (all): {classroom_ids_all}')
