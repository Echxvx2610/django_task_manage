from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), # http://localhost:8000/login
    path('signup/', views.signup_view, name='signup'), # http://localhost:8000/signup
    path('index/', views.index,name = 'index'), # http://localhost:8000/index
    path('about/', views.about,name = 'about'), # http://localhost:8000/about
    path('hello/<str:username>', views.hello,name = 'hello'), # http://localhost:8000/hello/username
    path('projects/', views.projects_view,name = 'projects'), # http://localhost:8000/projects
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'), # URL para detalles de proyecto
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/create/', views.create_task_general, name='create_task_general'),
    path('tasks/', views.tasks_view,name = 'tasks'), # http://localhost:8000/tasks
    path('tasks/<int:task_id>/delete/',views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/done/', views.mark_task_done, name='mark_task_done'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    #path('', views.login_view,name = 'login'), # http://localhost:8000
]