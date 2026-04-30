from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
 path('', views.home, name='home'),
 path('register/', views.register_view, name='register'),
 path('login/', auth_views.LoginView.as_view(template_name='assessment/login.html'), name='login'),
 path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('smart-dashboard/', views.smart_dashboard, name='smart_dashboard'),
 path('start/', views.start_test, name='start_test'),
 path('test/<int:attempt_id>/<int:index>/', views.test_question, name='test_question'),
 path('submit/<int:attempt_id>/', views.submit_test, name='submit_test'),
 path('report/<int:attempt_id>/', views.report, name='report'),
 path('manage/questions/', views.question_list, name='question_list'),
 path('manage/questions/add/', views.question_create, name='question_create'),
 path('manage/questions/<int:pk>/edit/', views.question_update, name='question_update'),
 path('manage/questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
 path('manage/attempts/', views.test_attempt_list, name='test_attempt_list'),
]
