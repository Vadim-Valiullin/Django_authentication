from django.urls import path
from rest_framework.authtoken import views

from aaa.views import *

urlpatterns = [
    path('', index),
    path('ad/', AdsListView.as_view()),
    path('ad/<int:pk>/', AdsDetailView.as_view()),
    path('ad/create/', AdsCreateView.as_view()),
    path('ad/<int:pk>/update/', AdsUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdsDeleteView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
    # path('user/else/', views.UserElseView.as_view()),   # Выводит кол-во объявлений автора
    path('ad/<int:pk>/upload_image/', AdUploadImageView.as_view()),
    path('selections/', SelectionView.as_view()),
    path('selections/<int:pk>/', SelectionDetailView.as_view()),
    path('selections/create/', SelectionCreateView.as_view()),
    path('selections/<int:pk>/update/', SelectionUpdateView.as_view()),
    path('selections/<int:pk>/del/', SelectionDeleteView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
]


# handler404 = pageNotFound