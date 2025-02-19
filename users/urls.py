from .views import RegisterView, LoginView, UserListView, UserDetailView
from django.urls import path


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("", UserListView.as_view(), name="user_list"),
    path("detail/<uuid:pk>/", UserDetailView.as_view(), name="user_detail")
]