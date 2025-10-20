from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Teacher routes
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/outputs/<int:id>/', views.teacher_outputs, name='teacher_outputs'),
    path('teacher/class/<str:grade_section>/', views.teacher_class, name='teacher_class'),
    path('teacher/notify/', views.teacher_notify, name='teacher_notify'),
    path('teacher/progress/', views.teacher_progress, name='teacher_progress'),
    path('teacher/sprogress/', views.teacher_sprogress, name='teacher_sprogress'),
    path('teacher/remarks/', views.teacher_remarks, name='teacher_remarks'),
    path('teacher/notice/', views.teacher_notice, name='teacher_notice'),
    path('teacher/archived/', views.teacher_archived, name='teacher_archived'),
    
    # Student routes
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/newsfeed/', views.student_newsfeed, name='student_newsfeed'),
    path('student/sketch/', views.student_sketch, name='student_sketch'),
    path('student/archived/', views.student_archived, name='student_archived'),
    path('student/class/<str:grade_section>/', views.student_class, name='student_class'),
    path('student/notifications/', views.student_notifications, name='student_notifications'),
    
    # API routes
    path('api/validate-session/', views.validate_session, name='validate_session'),
    path('api/validate_session/', views.validate_session, name='validate_session_underscore'),  # Handle underscore variant
    path('api/validate_session/<int:id>/', views.validate_session, name='validate_session_with_id'),  # Handle incorrect calls with ID
    
    # Portfolio API routes
    path('api/portfolio/folders/', views.portfolio_folders_api, name='portfolio_folders_api'),
    path('api/portfolio/folders/<int:folder_id>/', views.portfolio_folder_detail_api, name='portfolio_folder_detail_api'),
    path('api/portfolio/folders/<int:folder_id>/activities/', views.portfolio_activities_api, name='portfolio_activities_api'),
    path('api/activities/<int:activity_id>/', views.activity_detail_api, name='activity_detail_api'),
    
    # Submission API routes
    path('api/activities/<int:activity_id>/submissions/', views.activity_submissions_api, name='activity_submissions_api'),
    path('api/submissions/<int:submission_id>/', views.submission_detail_api, name='submission_detail_api'),
    path('api/submissions/unscored/', views.unscored_submissions_api, name='unscored_submissions_api'),
    path('api/submissions/scored/', views.scored_submissions_api, name='scored_submissions_api'),
    path('api/submissions/<int:submission_id>/score/', views.score_submission_api, name='score_submission_api'),
    
    # Feed approval routes
    path('api/submissions/pending-approvals/', views.pending_approvals_api, name='pending_approvals_api'),
    path('api/submissions/<int:submission_id>/approve/', views.approve_submission_api, name='approve_submission_api'),
    
    # Newsfeed route
    path('api/newsfeed/', views.newsfeed_api, name='newsfeed_api'),
    
    # Sketch submission route
    path('api/sketch/submit/', views.sketch_submission_api, name='sketch_submission_api'),
    
    # Sketch management routes
    path('api/sketches/', views.sketches_api, name='sketches_api'),
    path('api/sketches/<int:sketch_id>/', views.sketch_delete_api, name='sketch_delete_api'),
    
    # Notification routes
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/unread-count/', views.unread_notifications_count_api, name='unread_notifications_count_api'),
    
    # Student progress routes
    path('api/students/progress/', views.student_progress_list_api, name='student_progress_list_api'),
    path('api/students/<int:student_id>/progress/', views.student_progress_detail_api, name='student_progress_detail_api'),
    
    # Remark routes
    path('api/remarks/', views.remark_list, name='remark_list'),
    path('api/remarks/<int:pk>/', views.remark_detail, name='remark_detail'),
    path('api/remarks/<int:pk>/mark-read/', views.mark_remark_read, name='mark_remark_read'),
    
    # Submission Remark routes
    path('api/submissions/<int:submission_id>/remarks/', views.submission_remarks_api, name='submission_remarks_api'),
    path('api/submissions/<int:submission_id>/remarks/<int:remark_id>/', views.submission_remark_detail_api, name='submission_remark_detail_api'),
    path('api/student/submission-remarks/', views.student_submission_remarks_api, name='student_submission_remarks_api'),
]