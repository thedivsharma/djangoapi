from django.urls import path
from .views import login_view, token_verification_view, StudentListView, verify_otp,StudentDetailView, logout_view, view_tokens, test_send_email,generate_otp

urlpatterns = [
    path('login/', login_view, name='login'),
    path('token-verification/', token_verification_view, name='token_verification'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:id>/', StudentDetailView.as_view(), name='student-detail'),
    path('logout/', logout_view, name='logout'),
    path('view-tokens/', view_tokens, name='view_tokens'),
    path('send-email/', test_send_email, name='test_email'),
    path('generate-otp/', generate_otp, name='generate_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]
