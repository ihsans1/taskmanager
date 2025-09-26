from django.urls import path, include
from .views import RegisterView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,activate
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Change the root URL to the login page.
    path("", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    
    # Add a dedicated URL for registration.
    path("register/", RegisterView.as_view(), name="register"),
    
    # Add a URL for logging out.
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # Task-related URLs remain the same.
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/add/", TaskCreateView.as_view(), name="task_add"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]