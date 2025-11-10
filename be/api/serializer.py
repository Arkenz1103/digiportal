from rest_framework import serializers
from .models import User, LessonPlan, PortfolioFolder, PortfolioActivity, StudentSubmission, Sketch, NewsfeedPost, Notification, Remark, RemarkReadStatus, UserSettings, Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile with role-specific fields"""
    profile_picture_url = serializers.SerializerMethodField()
    student_id = serializers.CharField(source='id_number', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'first_name', 'last_name',
            'phone_number', 'bio', 'profile_picture', 'profile_picture_url',
            'id_number', 'department', 'years_of_experience',
            'grade_level', 'section', 'student_id'
        ]
        read_only_fields = ['id', 'username', 'role', 'id_number']
    
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
        return None
    
    def to_representation(self, instance):
        """Return only role-appropriate fields"""
        data = super().to_representation(instance)
        
        # Remove fields based on role
        if instance.role == 'student':
            # Remove teacher-specific fields for students
            fields_to_remove = ['department', 'years_of_experience']
            for field in fields_to_remove:
                data.pop(field, None)
        elif instance.role == 'teacher':
            # Remove student-specific fields for teachers
            fields_to_remove = ['grade_level', 'section', 'student_id']
            for field in fields_to_remove:
                data.pop(field, None)
        
        return data


class UserSettingsSerializer(serializers.ModelSerializer):
    """Serializer for user settings"""
    class Meta:
        model = UserSettings
        exclude = ['user', 'created_at', 'updated_at']
        read_only_fields = ['id']


class LessonPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = LessonPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PortfolioActivitySerializer(serializers.ModelSerializer):
    # Override scoring_criteria to handle JSON parsing for GET requests
    scoring_criteria = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def to_representation(self, instance):
        """Convert model instance to JSON - parse scoring_criteria"""
        data = super().to_representation(instance)
        
        # Parse scoring_criteria from JSON string to array
        if data.get('scoring_criteria'):
            try:
                import json
                criteria = json.loads(data['scoring_criteria'])
                data['scoring_criteria'] = criteria if isinstance(criteria, list) else []
            except (json.JSONDecodeError, TypeError, ValueError):
                data['scoring_criteria'] = []
        else:
            data['scoring_criteria'] = []
        
        return data
    
    class Meta:
        model = PortfolioActivity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at']


class PortfolioFolderSerializer(serializers.ModelSerializer):
    activities = PortfolioActivitySerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        model = PortfolioFolder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)
    activity_title = serializers.SerializerMethodField()
    activity_type = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    max_score = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    display_status = serializers.SerializerMethodField()
    submitted_at = serializers.SerializerMethodField()
    
    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else 'Sketch Pad'
    
    def get_activity_type(self, obj):
        return obj.activity.activity_type if obj.activity else 'Sketch'
    
    def get_total_score(self, obj):
        # First try to calculate from criteria_scores JSON
        if obj.criteria_scores:
            try:
                import json
                criteria = json.loads(obj.criteria_scores) if isinstance(obj.criteria_scores, str) else obj.criteria_scores
                total = sum(int(c.get('score', 0)) for c in criteria)
                return total
            except:
                pass
        return obj.score  # Fallback to simple score
    
    def get_max_score(self, obj):
        # First try to calculate from criteria_scores JSON
        if obj.criteria_scores:
            try:
                import json
                criteria = json.loads(obj.criteria_scores) if isinstance(obj.criteria_scores, str) else obj.criteria_scores
                max_total = sum(int(c.get('maxScore', 0)) for c in criteria)
                return max_total
            except:
                pass
        return 10  # Default max score
    
    def get_file_url(self, obj):
        """Return the proper file URL - prefer actual file over base64"""
        if obj.file:
            # If file field has actual file, return its URL
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        # Fallback to file_path (base64 or old data)
        return obj.file_path
    
    def get_submitted_at(self, obj):
        """Return submitted_at in Manila timezone"""
        if not obj.submitted_at:
            return None
        
        from django.utils import timezone
        import pytz
        
        manila_tz = pytz.timezone('Asia/Manila')
        
        # Convert to Manila timezone
        if timezone.is_naive(obj.submitted_at):
            # If naive, assume UTC and add 8 hours
            from datetime import timedelta
            manila_time = manila_tz.localize(obj.submitted_at + timedelta(hours=8))
        else:
            # If aware, convert to Manila timezone
            manila_time = obj.submitted_at.astimezone(manila_tz)
        
        # Return ISO format string
        return manila_time.isoformat()
    
    def get_display_status(self, obj):
        """Return display status - always show 'Submitted' to teacher even when student is resubmitting"""
        # For teachers, always show 'Submitted' for the original submission
        # even if student is resubmitting (status = draft with resubmit_count > 0)
        if obj.status == 'draft' and obj.resubmit_count > 0:
            return 'Submitted'  # Show as submitted to teacher
        elif obj.resubmit_count > 0 and obj.status == 'unscored':
            return 'Resubmitted'
        elif obj.status == 'unscored':
            return 'Submitted'
        elif obj.status == 'scored':
            return 'Scored'
        return obj.status.title()
    
    class Meta:
        model = StudentSubmission
        fields = '__all__'
        read_only_fields = ['id', 'submitted_at', 'scored_at', 'resubmit_count', 'last_resubmit_at', 'file_url']


class StudentSubmissionListSerializer(serializers.ModelSerializer):
    """Serializer for list views - includes file_path for teachers to view outputs"""
    student = UserSerializer(read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)
    activity_title = serializers.SerializerMethodField()
    activity_type = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    max_score = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    display_status = serializers.SerializerMethodField()
    
    def get_file_url(self, obj):
        """Return file URL if file exists, otherwise return file_path (base64)"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return obj.file_path  # Fallback to base64
    
    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else 'Sketch Pad'
    
    def get_activity_type(self, obj):
        return obj.activity.activity_type if obj.activity else 'Sketch'
    
    def get_total_score(self, obj):
        # First try to calculate from criteria_scores JSON
        if obj.criteria_scores:
            try:
                import json
                criteria = json.loads(obj.criteria_scores) if isinstance(obj.criteria_scores, str) else obj.criteria_scores
                total = sum(int(c.get('score', 0)) for c in criteria)
                return total
            except:
                pass
        
        # Fallback to detailed_score if available
        if hasattr(obj, 'detailed_score') and obj.detailed_score:
            detailed = obj.detailed_score
            total = (detailed.creativity_score + 
                    detailed.technical_skill_score + 
                    detailed.requirements_score)
            return total
        
        return obj.score  # Final fallback to simple score
    
    def get_max_score(self, obj):
        # First try to calculate from criteria_scores JSON
        if obj.criteria_scores:
            try:
                import json
                criteria = json.loads(obj.criteria_scores) if isinstance(obj.criteria_scores, str) else obj.criteria_scores
                max_total = sum(int(c.get('maxScore', 0)) for c in criteria)
                return max_total
            except:
                pass
        
        # Fallback to detailed_score if available
        if hasattr(obj, 'detailed_score') and obj.detailed_score:
            detailed = obj.detailed_score
            max_total = (detailed.creativity_max + 
                        detailed.technical_skill_max + 
                        detailed.requirements_max)
            return max_total
        
        return 10  # Default max score
    
    def get_display_status(self, obj):
        """Return display status - always show 'Submitted' to teacher even when student is resubmitting"""
        # For teachers, always show 'Submitted' for the original submission
        # even if student is resubmitting (status = draft with resubmit_count > 0)
        if obj.status == 'draft' and obj.resubmit_count > 0:
            return 'Submitted'  # Show as submitted to teacher
        elif obj.resubmit_count > 0 and obj.status == 'unscored':
            return 'Resubmitted'
        elif obj.status == 'unscored':
            return 'Submitted'
        elif obj.status == 'scored':
            return 'Scored'
        return obj.status.title()
    
    class Meta:
        model = StudentSubmission
        fields = '__all__'  # Include all fields including file_path
        read_only_fields = ['id', 'submitted_at', 'scored_at']


class SketchSerializer(serializers.ModelSerializer):
    """Serializer for student sketches"""
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = Sketch
        fields = '__all__'
        read_only_fields = ['id', 'student', 'created_at', 'updated_at']


class NewsfeedPostSerializer(serializers.ModelSerializer):
    """Serializer for newsfeed posts"""
    
    class Meta:
        model = NewsfeedPost
        fields = '__all__'
        read_only_fields = ['id', 'posted_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'read_at']


class RemarkSerializer(serializers.ModelSerializer):
    """Serializer for remarks"""
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    teacher_username = serializers.CharField(source='teacher.username', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_id = serializers.CharField(source='student.username', read_only=True)
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Remark
        fields = ['id', 'teacher', 'teacher_name', 'teacher_username', 'student', 'student_name', 'student_username', 'student_id', 'text', 'is_read', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_read(self, obj):
        """Check if the current user has read this remark"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.is_read_by(request.user)
        return False


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    full_name = serializers.ReadOnlyField()
    grade_section = serializers.ReadOnlyField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'middle_name', 'last_name', 'full_name',
            'grade_level', 'section', 'grade_section', 'gender', 'date_of_birth',
            'email', 'contact_number', 'address',
            'guardian_name', 'guardian_contact', 'guardian_email',
            'current_average', 'attendance_percentage',
            'is_active', 'enrollment_date',
            'user', 'user_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'full_name', 'grade_section']


class StudentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing students"""
    full_name = serializers.ReadOnlyField()
    grade_section = serializers.ReadOnlyField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'full_name', 'grade_section', 
            'gender', 'current_average', 'attendance_percentage', 'is_active'
        ]