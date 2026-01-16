from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class SchoolYear(models.Model):
    """School Year model for managing academic years - per teacher"""
    name = models.CharField(max_length=20)  # e.g., "2024-2025"
    teacher = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, 
                                related_name='school_years', limit_choices_to={'role': 'teacher'})
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    promotion_done = models.BooleanField(default=False)  # Track if promotion was done
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_years'
        ordering = ['-created_at']
        unique_together = ['name', 'teacher']  # Each teacher can have their own school years

    def __str__(self):
        return f"{self.name} ({self.teacher.username if self.teacher else 'Global'})"

    def save(self, *args, **kwargs):
        # Ensure only one school year is current per teacher
        if self.is_current and self.teacher:
            SchoolYear.objects.filter(is_current=True, teacher=self.teacher).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current_for_teacher(cls, teacher):
        """Get the current active school year for a specific teacher"""
        # First check for teacher's own school year
        teacher_sy = cls.objects.filter(is_current=True, is_archived=False, teacher=teacher).first()
        if teacher_sy:
            return teacher_sy
        # Fall back to global school year (created by admin, teacher=None)
        return cls.objects.filter(is_current=True, is_archived=False, teacher__isnull=True).first()

    @classmethod
    def get_current(cls):
        """Get the current active school year (legacy - returns first current)"""
        return cls.objects.filter(is_current=True, is_archived=False).first()


class StudentPromotionHistory(models.Model):
    """Track student promotions for undo functionality - per teacher"""
    student = models.ForeignKey('User', on_delete=models.CASCADE, related_name='promotion_history')
    teacher = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, 
                                related_name='promotions_made', limit_choices_to={'role': 'teacher'})
    school_year = models.ForeignKey('SchoolYear', on_delete=models.CASCADE, related_name='promotions')
    previous_classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_students')
    previous_grade_level = models.IntegerField(null=True, blank=True)
    previous_section = models.CharField(max_length=10, null=True, blank=True)
    new_classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='promoted_students')
    new_grade_level = models.IntegerField(null=True, blank=True)
    new_section = models.CharField(max_length=10, null=True, blank=True)
    is_graduated = models.BooleanField(default=False)  # True if student graduated (was Grade 6)
    promoted_at = models.DateTimeField(auto_now_add=True)
    is_undone = models.BooleanField(default=False)  # Track if promotion was undone

    class Meta:
        db_table = 'student_promotion_history'
        ordering = ['-promoted_at']

    def __str__(self):
        return f"{self.student.username}: Grade {self.previous_grade_level} -> Grade {self.new_grade_level}"


class Classroom(models.Model):
    """Classroom model for managing classes"""
    name = models.CharField(max_length=100)  # e.g., "Grade 1 - A"
    grade_level = models.IntegerField()  # 1, 2, 3, 4, 5, 6
    section = models.CharField(max_length=10)  # A, B
    room_number = models.CharField(max_length=50)  # Room 111, Room 121, etc.
    capacity = models.IntegerField(default=30)
    school_year = models.CharField(max_length=20, default='2024-2025')
    school_year_obj = models.ForeignKey('SchoolYear', on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')

    # Class code for student enrollment (6 characters: mix of uppercase, lowercase, numbers)
    class_code = models.CharField(max_length=6, unique=True, null=True, blank=True)

    # Teacher assignment
    teacher = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='taught_classrooms', limit_choices_to={'role': 'teacher'})

    # Archiving fields
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'classrooms'
        ordering = ['grade_level', 'section']
        unique_together = ['grade_level', 'section', 'school_year']

    def __str__(self):
        return f"Grade {self.grade_level} - {self.section}"

    @classmethod
    def generate_class_code(cls):
        """Generate a unique 6-character class code"""
        import random
        import string
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        while True:
            code = ''.join(random.choices(characters, k=6))
            if not cls.objects.filter(class_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        # Auto-generate class code if not set
        if not self.class_code:
            self.class_code = Classroom.generate_class_code()
        super().save(*args, **kwargs)

    @property
    def student_count(self):
        """Get the number of students in this classroom"""
        return self.students.filter(role='student').count()

    @property
    def is_full(self):
        """Check if classroom is at capacity"""
        return self.student_count >= self.capacity


class StudentClassroomHistory(models.Model):
    """Track student's classroom history across school years"""
    student = models.ForeignKey('User', on_delete=models.CASCADE, related_name='classroom_history')
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='student_history')
    school_year = models.CharField(max_length=20)
    grade_level = models.IntegerField()
    section = models.CharField(max_length=10)
    classroom_name = models.CharField(max_length=100)  # Store name in case classroom is deleted
    teacher_name = models.CharField(max_length=200, null=True, blank=True)  # Store teacher name
    joined_at = models.DateTimeField()
    archived_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student_classroom_history'
        ordering = ['-archived_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.classroom_name} ({self.school_year})"


class User(AbstractUser):
    """Custom User model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)  # Student ID number

    # Profile fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    # Teacher-specific fields
    department = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)

    # Student-specific fields
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=50, blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='students', limit_choices_to={'school_year': '2024-2025'})

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"

    @classmethod
    def generate_student_id(cls, grade_level):
        """
        Generate student ID based on school year batch and grade level.
        Format: BBBXXX where BBB = batch prefix, XXX = sequence (001, 002, ...)
        
        The batch prefix is calculated as: (school_year_number - 1) * 6 + grade_level
        - School Year 1: Grade 1=001, Grade 2=002, Grade 3=003, Grade 4=004, Grade 5=005, Grade 6=006
        - School Year 2: Grade 1=007, Grade 2=008, Grade 3=009, Grade 4=010, Grade 5=011, Grade 6=012
        - School Year 3: Grade 1=013, Grade 2=014, Grade 3=015, Grade 4=016, Grade 5=017, Grade 6=018
        
        The sequence (XXX) resets to 001 for each new school year batch.
        """
        # Parse grade level to get the number
        grade_num = cls._parse_grade_level(grade_level)
        if not grade_num or grade_num < 1 or grade_num > 6:
            grade_num = 1  # Default to grade 1 if invalid
        
        # Get the current school year's batch number (1-based)
        current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
        
        if current_sy:
            # Count school years to determine batch number
            all_school_years = list(SchoolYear.objects.order_by('created_at').values_list('id', flat=True))
            school_year_num = all_school_years.index(current_sy.id) + 1 if current_sy.id in all_school_years else 1
        else:
            school_year_num = 1  # Default to first school year if none exists
        
        # Calculate batch prefix: (school_year_num - 1) * 6 + grade_level
        # SY1: G1=001, G2=002, G3=003, G4=004, G5=005, G6=006
        # SY2: G1=007, G2=008, G3=009, G4=010, G5=011, G6=012
        batch_prefix_num = (school_year_num - 1) * 6 + grade_num
        batch_prefix = f"{batch_prefix_num:03d}"
        
        # Find the highest sequence number for this batch prefix
        existing_ids = cls.objects.filter(
            role='student',
            id_number__startswith=batch_prefix
        ).values_list('id_number', flat=True)
        
        max_seq = 0
        for id_num in existing_ids:
            if id_num and len(id_num) >= 6:
                try:
                    seq = int(id_num[3:6])
                    if seq > max_seq:
                        max_seq = seq
                except (ValueError, IndexError):
                    pass
        
        # Generate next sequence number
        next_seq = max_seq + 1
        return f"{batch_prefix}{next_seq:03d}"

    @classmethod
    def generate_teacher_id(cls):
        """
        Generate teacher ID.
        Format: 00XXX where XXX = sequence starting from 101
        Example: 00101, 00102, 00103, ...
        """
        # Find the highest teacher ID number
        existing_ids = cls.objects.filter(
            role='teacher',
            id_number__startswith='00'
        ).values_list('id_number', flat=True)
        
        max_seq = 100  # Start from 100 so first ID is 00101
        for id_num in existing_ids:
            if id_num and len(id_num) >= 5:
                try:
                    seq = int(id_num[2:5])
                    if seq > max_seq:
                        max_seq = seq
                except (ValueError, IndexError):
                    pass
        
        # Generate next sequence number
        next_seq = max_seq + 1
        return f"00{next_seq:03d}"

    @staticmethod
    def _parse_grade_level(grade_level):
        """Parse grade level string to integer (1-6)"""
        if not grade_level:
            return None
        
        # Handle various formats: "1", "Grade 1", "grade1", etc.
        grade_str = str(grade_level).lower().replace('grade', '').strip()
        try:
            return int(grade_str)
        except ValueError:
            return None


class UserSettings(models.Model):
    """User settings and preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    activity_reminders = models.BooleanField(default=True)
    score_notifications = models.BooleanField(default=True)
    remark_notifications = models.BooleanField(default=True)

    # Privacy settings
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('students', 'Students Only'),
        ('classmates', 'Classmates Only'),
        ('teachers', 'Teachers Only'),
        ('private', 'Private'),
    ]
    profile_visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    show_scores = models.BooleanField(default=True)

    # Preferences
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fil', 'Filipino'),
        ('es', 'Spanish'),
    ]
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')

    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')

    timezone = models.CharField(max_length=50, default='Asia/Manila')
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')

    # Teacher-specific settings
    submission_alerts = models.BooleanField(default=True)

    # Student-specific settings
    study_reminders = models.BooleanField(default=True)
    daily_goals = models.BooleanField(default=True)
    weekly_reports = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_settings'

    def __str__(self):
        return f"Settings for {self.user.username}"


class LessonPlan(models.Model):
    """Lesson plan model for teachers"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_plans')
    title = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    uploaded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lesson_plans'

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class PortfolioFolder(models.Model):
    """Portfolio folder model"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_folders', db_column='teacher_id')
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255, default='General')  # Legacy field, kept for backwards compatibility
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='portfolio_folders')  # New field linking to Classroom
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio_folders'

    def __str__(self):
        return f"{self.name} - {self.teacher.username}"


class PortfolioActivity(models.Model):
    """Portfolio activity model"""
    ACTIVITY_TYPE_CHOICES = [
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
        ('Exam', 'Exam'),
        ('Presentation', 'Presentation'),
        ('Contest', 'Contest'),
    ]

    folder = models.ForeignKey(PortfolioFolder, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPE_CHOICES, default='Quiz')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    scoring_criteria = models.TextField(null=True, blank=True)  # JSON string of criteria
    is_published = models.BooleanField(default=False)  # Track if activity is published to students
    published_at = models.DateTimeField(null=True, blank=True)  # When the activity was published
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio_activities'

    def __str__(self):
        return f"{self.title} ({self.activity_type}) - {self.folder.name}"


class ActivityInstructionFile(models.Model):
    """Instruction files attached to portfolio activities"""
    activity = models.ForeignKey(PortfolioActivity, on_delete=models.CASCADE, related_name='instruction_files')
    file = models.FileField(upload_to='instruction_files/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, null=True, blank=True)
    file_size = models.IntegerField(default=0)  # Size in bytes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_instruction_files'

    def __str__(self):
        return f"{self.file_name} - {self.activity.title}"


class StudentSubmission(models.Model):
    """Student submission model for portfolio activities"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('unscored', 'Unscored'),
        ('scored', 'Scored'),
    ]

    APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    activity = models.ForeignKey(PortfolioActivity, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    caption = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True)  # Actual file storage
    file_path = models.TextField(null=True, blank=True)  # Keep for base64 compatibility
    file_type = models.CharField(max_length=50, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    criteria_scores = models.TextField(null=True, blank=True)  # JSON string of criteria scores
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unscored')
    post_to_feed = models.BooleanField(default=False)
    post_file_ids = models.TextField(null=True, blank=True)  # JSON array of file IDs selected for posting
    post_caption = models.TextField(null=True, blank=True)  # Caption for the post to feed request
    post_requested_at = models.DateTimeField(null=True, blank=True)  # When the post was requested
    approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='approved')
    is_active = models.BooleanField(default=True)  # Track if submission is active
    is_late = models.BooleanField(default=False)  # Track if submission was submitted after due date
    submission_version = models.IntegerField(default=1)  # Track version for resubmissions
    resubmit_count = models.IntegerField(default=0)  # Track number of resubmissions
    last_resubmit_at = models.DateTimeField(null=True, blank=True)  # Track last resubmit time
    submitted_at = models.DateTimeField(null=True, blank=True)  # Set when actually turned in, not when draft created
    scored_at = models.DateTimeField(null=True, blank=True)

    # Portfolio Compilation Fields
    is_compilation = models.BooleanField(default=False)  # True if this is a portfolio compilation submission
    compiled = models.BooleanField(default=False)
    missing = models.BooleanField(default=True)  # True until compiled
    compiled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'student_submissions'

    def __str__(self):
        activity_title = self.activity.title if self.activity else 'Sketch Pad'
        return f"{self.student.username} - {activity_title} ({self.status})"


class SubmissionFile(models.Model):
    """Individual file attached to a student submission - supports multiple files per submission"""
    submission = models.ForeignKey(StudentSubmission, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True)
    file_path = models.TextField(null=True, blank=True)  # For base64 compatibility
    file_type = models.CharField(max_length=50, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # Size in bytes
    order = models.IntegerField(default=0)  # For ordering files
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'submission_files'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"File {self.file_name} for submission {self.submission_id}"

    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return self.file_path


class SubmissionScore(models.Model):
    """Detailed scoring criteria for student submissions"""
    submission = models.OneToOneField(StudentSubmission, on_delete=models.CASCADE, related_name='detailed_score')
    creativity_score = models.IntegerField(default=0)
    creativity_max = models.IntegerField(default=10)
    technical_skill_score = models.IntegerField(default=0)
    technical_skill_max = models.IntegerField(default=10)
    requirements_score = models.IntegerField(default=0)
    requirements_max = models.IntegerField(default=10)
    total_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=30)
    scored_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='scored_submissions')
    scored_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'submission_scores'

    def __str__(self):
        return f"Score for {self.submission} - {self.total_score}/{self.max_score}"


class Sketch(models.Model):
    """Student sketch model for saving drawings"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sketches')
    title = models.CharField(max_length=255, default='Untitled Sketch')
    image_data = models.TextField()  # Base64 encoded image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sketches'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.title}"


class NewsfeedPost(models.Model):
    """Newsfeed post model - separate from submissions so posts persist even if submission is deleted"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsfeed_posts')
    student_name = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)  # Base64 encoded image/file (legacy - single file)
    file_type = models.CharField(max_length=50, default='image')
    activity_title = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=100, blank=True, null=True)

    # Classroom filter - posts are only visible to users in the same classroom
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, null=True, blank=True, related_name='newsfeed_posts')

    # Optional reference to original submission (can be null if submission is deleted)
    original_submission = models.ForeignKey(
        'StudentSubmission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsfeed_posts'
    )

    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'newsfeed_posts'
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.student_name} - {self.activity_title or 'Post'}"

    @property
    def likes_count(self):
        """Get total number of likes for this post"""
        return self.likes.count()

    @property
    def comments_count(self):
        """Get total number of comments for this post"""
        return self.comments.count()


class NewsfeedPostFile(models.Model):
    """Individual file attached to a newsfeed post - supports multiple files per post"""
    post = models.ForeignKey(NewsfeedPost, on_delete=models.CASCADE, related_name='files')
    file_path = models.TextField(blank=True, null=True)
    file_type = models.CharField(max_length=50, default='image')
    file_name = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'newsfeed_post_files'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"File {self.file_name} for post {self.post_id}"


class PostLike(models.Model):
    """Like model for newsfeed posts"""
    post = models.ForeignKey(NewsfeedPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_likes'
        unique_together = ['post', 'user']  # Each user can only like a post once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class PostComment(models.Model):
    """Comment model for newsfeed posts"""
    post = models.ForeignKey(NewsfeedPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_comments'
        ordering = ['created_at']  # Oldest first for comments

    def __str__(self):
        return f"{self.user.username} commented on post {self.post.id}"


class PostCommentLike(models.Model):
    """Like model for post comments"""
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_comment_likes'
        unique_together = ['comment', 'user']

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"


class PostCommentReply(models.Model):
    """Reply model for post comments"""
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_comment_replies'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} replied to comment {self.comment.id}"


class Remark(models.Model):
    """Remark model for teacher remarks to students"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_given')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_received')
    submission = models.ForeignKey('StudentSubmission', on_delete=models.CASCADE, related_name='remarks', null=True, blank=True)
    text = models.TextField()
    is_read = models.BooleanField(default=False)  # Kept for backward compatibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'remarks'
        ordering = ['-created_at']

    def __str__(self):
        return f"Remark from {self.teacher.username} to {self.student.username}"

    def is_read_by(self, user):
        """Check if this remark has been read by a specific user"""
        return RemarkReadStatus.objects.filter(remark=self, user=user).exists()


class RemarkReadStatus(models.Model):
    """Track which users have read which remarks"""
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE, related_name='read_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_read')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'remark_read_status'
        unique_together = ['remark', 'user']  # Each user can only mark a remark as read once
        ordering = ['-read_at']

    def __str__(self):
        return f"{self.user.username} read remark {self.remark.id}"


class Notification(models.Model):
    """Notification model for user notifications"""
    NOTIFICATION_TYPES = [
        # Student notifications
        ('portfolio_created', 'Portfolio Created'),
        ('portfolio_updated', 'Portfolio Updated'),
        ('portfolio_deleted', 'Portfolio Deleted'),
        ('activity_created', 'Activity Created'),
        ('activity_updated', 'Activity Updated'),
        ('activity_deleted', 'Activity Deleted'),
        ('submission_approved', 'Submission Approved'),
        ('submission_rejected', 'Submission Rejected'),
        ('score_added', 'Score Added'),
        ('remark_added', 'Remark Added'),
        ('remark_updated', 'Remark Updated'),
        ('remark_deleted', 'Remark Deleted'),
        ('portfolio_compilation', 'Portfolio Compilation'),

        # Teacher notifications
        ('submission_received', 'Submission Received'),
        ('approval_requested', 'Approval Requested'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()

    # Optional references (SET_NULL so notifications persist after entity deletion)
    portfolio = models.ForeignKey(PortfolioFolder, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(PortfolioActivity, on_delete=models.SET_NULL, null=True, blank=True)
    submission = models.ForeignKey(StudentSubmission, on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.ForeignKey(Remark, on_delete=models.SET_NULL, null=True, blank=True)

    # Metadata
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"


class PortfolioCompilationRequest(models.Model):
    """Track portfolio compilation requests per class"""
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='compilation_requests', null=True, blank=True)
    class_name = models.CharField(max_length=255, default='General')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compilation_requests_made')
    requested_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'portfolio_compilation_requests'
        ordering = ['-requested_at']
        unique_together = ['classroom', 'requested_by']

    def __str__(self):
        return f"Compilation request for {self.classroom.name if self.classroom else 'N/A'} by {self.requested_by.username}"


class PortfolioEnvelope(models.Model):
    """Student portfolio envelope designs"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_envelopes')
    class_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    color = models.CharField(max_length=50, default='#4F46E5')
    pattern = models.CharField(max_length=50, default='solid')
    is_submitted = models.BooleanField(default=False)  # Track if student submitted the portfolio
    submitted_at = models.DateTimeField(null=True, blank=True)  # When the portfolio was submitted
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio_envelopes'
        ordering = ['-created_at']
        unique_together = ['student', 'class_name']  # One envelope per student per class

    def __str__(self):
        return f"{self.student.username} - {self.title} ({self.class_name})"


class Student(models.Model):
    """Comprehensive Student model for managing student data"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    GRADE_CHOICES = [
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
    ]

    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
    ]

    # Link to User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)

    # Student Information
    student_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    # Academic Information
    grade_level = models.IntegerField(choices=GRADE_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

    # Personal Information
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    # Contact Information
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Guardian Information
    guardian_name = models.CharField(max_length=200, blank=True, null=True)
    guardian_contact = models.CharField(max_length=20, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)

    # Academic Performance
    current_average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    enrollment_date = models.DateField(default=timezone.now)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['grade_level', 'section', 'last_name', 'first_name']
        unique_together = [['student_id', 'grade_level', 'section']]
        indexes = [
            models.Index(fields=['grade_level', 'section']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    @property
    def full_name(self):
        """Returns the full name of the student"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def grade_section(self):
        """Returns grade and section combined"""
        return f"Grade {self.grade_level} - Section {self.section}"

    def __str__(self):
        return f"{self.student_id} - {self.full_name} ({self.grade_section})"
