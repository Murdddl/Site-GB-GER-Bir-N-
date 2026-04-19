from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/all/', views.all_reviews, name='all_reviews'),
    path('faq/', views.faq, name='faq'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('moderation/', views.moderation, name='moderation'),
    path('moderation/<int:question_id>/', views.answer_question, name='answer_question'),
    path('moderation/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('donate/', views.donate, name='donate'),
    path('moderation_rev/', views.moderation_rev, name='moderation_rev'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/review/<int:review_id>/approve/', views.approve_review, name='approve_review'),
    path('admin-panel/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('export/<str:model_type>/', views.export_csv, name='export_csv'),
    path('google1234567890abcdef.html', views.google_verification),
]