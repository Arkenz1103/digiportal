from rest_framework import serializers
from .models import User, LessonPlan, PortfolioFolder, PortfolioActivity, StudentSubmission, Sketch, NewsfeedPost, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


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
        read_only_fields = ['id', 'created_at', 'updated_at']


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
    
    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else 'Sketch Pad'
    
    def get_activity_type(self, obj):
        return obj.activity.activity_type if obj.activity else 'Sketch'
    
    class Meta:
        model = StudentSubmission
        fields = '__all__'
        read_only_fields = ['id', 'submitted_at', 'scored_at']


class StudentSubmissionListSerializer(serializers.ModelSerializer):
    """Serializer for list views - includes file_path for teachers to view outputs"""
    student = UserSerializer(read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)
    activity_title = serializers.SerializerMethodField()
    activity_type = serializers.SerializerMethodField()
    has_file = serializers.SerializerMethodField()
    
    def get_activity_title(self, obj):
        return obj.activity.title if obj.activity else 'Sketch Pad'
    
    def get_activity_type(self, obj):
        return obj.activity.activity_type if obj.activity else 'Sketch'
    
    def get_has_file(self, obj):
        return bool(obj.file_path)
    
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