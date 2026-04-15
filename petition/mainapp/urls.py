from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
print('aaaa')
urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/all/', views.all_reviews, name='all_reviews'),
    path('faq/', views.faq, name='faq'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('moderation/', views.moderation, name='moderation'),
    path('moderation/<int:question_id>/', views.answer_question, name='answer_question'),
    path('moderation/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('donate/', views.donate, name='donate'),
    path('moderation_rev/', views.moderation_rev, name='moderation_rev'),
]
