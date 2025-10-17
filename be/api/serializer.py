from rest_framework import serializers
from .models import User, LessonPlan, PortfolioFolder, PortfolioActivity, StudentSubmission


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
    """Lightweight serializer for list views - excludes large file_path data"""
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
        exclude = ['file_path']  # Exclude the large base64 image data
        read_only_fields = ['id', 'submitted_at', 'scored_at']