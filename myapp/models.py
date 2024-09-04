from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # esto es util para ver el nombre del proyecto y no el nombre del objecto
        return self.name 
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        # esto es util para ver el nombre de la tarea y no el nombre del objecto
        return self.title + ' - ' + self.project.name