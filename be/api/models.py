from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Classroom(models.Model):
    """Classroom model for managing classes"""
    name = models.CharField(max_length=100)  # e.g., "Grade 1 - A"
    grade_level = models.IntegerField()  # 1, 2, 3, 4, 5, 6
    section = models.CharField(max_length=10)  # A, B
    room_number = models.CharField(max_length=50)  # Room 111, Room 121, etc.
    capacity = models.IntegerField(default=30)
    school_year = models.CharField(max_length=20, default='2024-2025')
    
    # Teacher assignment
    teacher = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='taught_classrooms', limit_choices_to={'role': 'teacher'})
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'classrooms'
        ordering = ['grade_level', 'section']
        unique_together = ['grade_level', 'section', 'school_year']
    
    def __str__(self):
        return f"Grade {self.grade_level} - {self.section}"
    
    @property
    def student_count(self):
        """Get the number of students in this classroom"""
        return self.students.filter(role='student').count()
    
    @property
    def is_full(self):
        """Check if classroom is at capacity"""
        return self.student_count >= self.capacity


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
    class_name = models.CharField(max_length=255, default='General')
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
    approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='approved')
    is_active = models.BooleanField(default=True)  # Track if submission is active
    is_late = models.BooleanField(default=False)  # Track if submission was submitted after due date
    submission_version = models.IntegerField(default=1)  # Track version for resubmissions
    resubmit_count = models.IntegerField(default=0)  # Track number of resubmissions
    last_resubmit_at = models.DateTimeField(null=True, blank=True)  # Track last resubmit time
    submitted_at = models.DateTimeField(null=True, blank=True)  # Set when actually turned in, not when draft created
    scored_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'student_submissions'

    def __str__(self):
        activity_title = self.activity.title if self.activity else 'Sketch Pad'
        return f"{self.student.username} - {activity_title} ({self.status})"


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
    file_path = models.TextField(blank=True, null=True)  # Base64 encoded image/file
    file_type = models.CharField(max_length=50, default='image')
    activity_title = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=100, blank=True, null=True)

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
    class_name = models.CharField(max_length=255)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compilation_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'portfolio_compilation_requests'
        ordering = ['-requested_at']

    def __str__(self):
        return f"Compilation request for {self.class_name} by {self.requested_by.username}"


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
