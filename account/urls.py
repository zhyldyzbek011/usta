from django.urls import path, include
from rest_auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

from account import views

from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views



router = DefaultRouter()
router.register('cards', views.Worker_cardViewSet)

urlpatterns = [
    path('register/', views.RegistrationApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('login/', LogoutView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('change-password/', views.NewPasswordVew.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('', include(router.urls)),

]


    # path('posts/', views.PostListView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
    # path('posts/create/', views.PostCreateView.as_view()),
    # path('posts/update/<int:pk>/', views.PostUpdateView.as_view()),
    # path('posts/delete/<int:pk>/', views.PostDeleteView.as_view()),
    # path('posts/', views.PostView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),

