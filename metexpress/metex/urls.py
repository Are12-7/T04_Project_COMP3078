from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('village/<int:id>/', views.village, name="village"),
    path('create-village/', views.createVillage, name="create-village"),
    path('update-village/<int:id>/', views.updateVillage, name="update-village"),
    path('delete-village/<int:id>/', views.deleteVillage, name="delete-village"),
    path('delete-discussion/<int:id>/',
         views.deleteDiscussion, name="delete-discussion"),
]
