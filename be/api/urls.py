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
    path('api/auth/login/', views.login_api, name='login_api'),
    path('api/auth/logout/', views.logout_api, name='logout_api'),
    path('api/validate-session/', views.validate_session, name='validate_session'),
    path('api/validate_session/', views.validate_session, name='validate_session_underscore'),  # Handle underscore variant
    path('api/validate_session/<int:id>/', views.validate_session, name='validate_session_with_id'),  # Handle incorrect calls with ID

    # Portfolio API routes
    path('api/portfolio/folders/', views.portfolio_folders_api, name='portfolio_folders_api'),
    path('api/portfolio/folders/<int:folder_id>/', views.portfolio_folder_detail_api, name='portfolio_folder_detail_api'),
    path('api/portfolio/folders/<int:folder_id>/activities/', views.portfolio_activities_api, name='portfolio_activities_api'),
    path('api/folders/<int:folder_id>/delete/', views.delete_folder_api, name='delete_folder_api'),
    path('api/activities/<int:activity_id>/', views.activity_detail_api, name='activity_detail_api'),
    path('api/activities/<int:activity_id>/publish/', views.publish_activity_api, name='publish_activity_api'),
    path('api/activities/<int:activity_id>/retract/', views.retract_activity_api, name='retract_activity_api'),

    # Submission API routes
    path('api/activities/<int:activity_id>/submissions/', views.activity_submissions_api, name='activity_submissions_api'),
    path('api/activities/<int:activity_id>/submissions/<int:submission_id>/convert-to-final/', views.convert_draft_to_final_api, name='convert_draft_to_final_api'),
    path('api/submissions/<int:submission_id>/', views.submission_detail_api, name='submission_detail_api'),
    path('api/submissions/unscored/', views.unscored_submissions_api, name='unscored_submissions_api'),
    path('api/submissions/scored/', views.scored_submissions_api, name='scored_submissions_api'),
    path('api/submissions/<int:submission_id>/score/', views.score_submission_api, name='score_submission_api'),
    path('api/submissions/my-collection/', views.student_submitted_collection_api, name='student_submitted_collection_api'),
    path('api/submissions/<int:submission_id>/request-post-approval/', views.request_post_approval_api, name='request_post_approval_api'),

    # Feed approval routes
    path('api/submissions/pending-approvals/', views.pending_approvals_api, name='pending_approvals_api'),
    path('api/submissions/<int:submission_id>/approve/', views.approve_submission_api, name='approve_submission_api'),

    # Newsfeed route
    path('api/newsfeed/', views.newsfeed_api, name='newsfeed_api'),

    # Post interaction routes (likes and comments)
    path('api/posts/<int:post_id>/like/', views.post_like_api, name='post_like_api'),
    path('api/posts/<int:post_id>/comments/', views.post_comments_api, name='post_comments_api'),
    path('api/posts/<int:post_id>/delete/', views.delete_post_api, name='delete_post_api'),

    # Sketch submission route
    path('api/sketch/submit/', views.sketch_submission_api, name='sketch_submission_api'),

    # Sketch management routes
    path('api/sketches/', views.sketches_api, name='sketches_api'),
    path('api/sketches/<int:sketch_id>/', views.sketch_delete_api, name='sketch_delete_api'),

    # Notification routes
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/unread-count/', views.unread_notifications_count_api, name='unread_notifications_count_api'),
    path('api/notifications/check-edit-deadlines/', views.check_activity_edit_deadlines_api, name='check_activity_edit_deadlines_api'),

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

    # Portfolio Compilation routes
    path('api/notifications/portfolio-compilation/', views.request_portfolio_compilation_api, name='request_portfolio_compilation_api'),
    path('api/notifications/portfolio-compilation/<int:classroom_id>/', views.check_portfolio_compilation_status_api, name='check_portfolio_compilation_status_api'),

    # Portfolio Envelope routes
    path('api/portfolio-envelope/create/', views.create_portfolio_envelope_api, name='create_portfolio_envelope_api'),
    path('api/portfolio-envelope/student/<str:class_name>/', views.get_student_envelope_api, name='get_student_envelope_api'),
    path('api/portfolio-envelope/<str:class_name>/', views.get_portfolio_envelopes_api, name='get_portfolio_envelopes_api'),
    path('api/portfolio-envelope/activities/<str:class_name>/', views.get_student_portfolio_activities_api, name='get_student_portfolio_activities_api'),
    path('api/portfolio-envelope/teacher-activities/<str:class_name>/<int:student_id>/', views.get_teacher_student_activities_api, name='get_teacher_student_activities_api'),
    path('api/portfolio-envelope/submit-missing/<int:activity_id>/', views.submit_missing_activity_api, name='submit_missing_activity_api'),
    path('api/portfolio-envelope/submit-compilation/<int:activity_id>/', views.submit_compilation_api, name='submit_compilation_api'),
    path('api/portfolio-envelope/submit/<str:class_name>/', views.submit_portfolio_api, name='submit_portfolio_api'),

    # Profile and Settings API routes
    path('api/user/profile/', views.user_profile_api, name='user_profile_api'),
    path('api/user/settings/', views.user_settings_api, name='user_settings_api'),
    path('api/user/change-password/', views.change_password_api, name='change_password_api'),
    path('api/user/export-data/', views.export_user_data_api, name='export_user_data_api'),

    # Student management routes
    path('api/students/', views.student_list_api, name='student_list_api'),
    path('api/students/export/', views.export_students_api, name='export_students_api'),

    # Classroom routes
    path('api/classrooms/', views.classroom_list_api, name='classroom_list_api'),
    path('api/classrooms/<int:classroom_id>/', views.classroom_detail_api, name='classroom_detail_api'),

    # AI routes
    path('api/ai/test/', views.ai_test, name='ai_test'),
    path('api/ai/generate-questions/', views.generate_ai_questions, name='generate_ai_questions'),
]
