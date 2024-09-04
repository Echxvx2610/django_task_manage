from django.contrib import admin
from .models import Project, Task
# Register your models here.
#agregamos nuestros modelos al admin del proyecto
projects = admin.site.register(Project)
tasks = admin.site.register(Task)
