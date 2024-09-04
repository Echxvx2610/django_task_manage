from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), # http://localhost:8000/login
    path('signup/', views.signup_view, name='signup'), # http://localhost:8000/signup
    path('index/', views.index,name = 'index'), # http://localhost:8000/index
    path('about/', views.about,name = 'about'), # http://localhost:8000/about
    path('hello/<str:username>', views.hello,name = 'hello'), # http://localhost:8000/hello/username
    path('projects/', views.projects,name = 'projects'), # http://localhost:8000/projects
    path('tasks/', views.tasks,name = 'tasks'), # http://localhost:8000/tasks
    # path('', views.login_view,name = 'login'), # http://localhost:8000
]