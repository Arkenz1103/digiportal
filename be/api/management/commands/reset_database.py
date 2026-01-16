from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Delete all data from users (except admin), classrooms, and school years'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Disable foreign key checks temporarily
            cursor.execute("SET session_replication_role = 'replica';")
            
            # Delete all related data first
            tables_to_clear = [
                'post_comment_replies',
                'post_comment_likes', 
                'post_comments',
                'post_likes',
                'newsfeed_post_files',
                'newsfeed_posts',
                'remark_read_status',
                'remarks',
                'submission_scores',
                'submission_files',
                'student_submissions',
                'activity_instruction_files',
                'portfolio_activities',
                'portfolio_folders',
                'notifications',
                'sketches',
                'user_settings',
                'student_classroom_history',
                'student_promotion_history',
                'teacher_class_assignments',
            ]
            
            for table in tables_to_clear:
                try:
                    cursor.execute(f'DELETE FROM {table}')
                    self.stdout.write(f'  Cleared {table}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Could not clear {table}: {e}'))
            
            # Delete classrooms
            cursor.execute('DELETE FROM classrooms')
            self.stdout.write(self.style.SUCCESS('  Cleared classrooms'))
            
            # Delete school years
            cursor.execute('DELETE FROM school_years')
            self.stdout.write(self.style.SUCCESS('  Cleared school_years'))
            
            # Delete users except admin
            cursor.execute("DELETE FROM users WHERE role != 'admin'")
            self.stdout.write(self.style.SUCCESS('  Cleared users (except admin)'))
            
            # Re-enable foreign key checks
            cursor.execute("SET session_replication_role = 'origin';")
            
        self.stdout.write(self.style.SUCCESS('\n✅ Database reset complete!'))
        self.stdout.write(self.style.SUCCESS('All users (except admin), classrooms, and school years have been deleted.'))
