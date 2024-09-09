from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from . models import Project, Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    'Funcion para el index o primera vista de localhost'
    #return HttpResponse('<h1> Index Page </h1>')
    title = 'Index Page'
    return render(request, 'index.html',{
        'title': title
    })

def hello(request,**kargs):
    'Funcion que retorna un HttpResponse con el nombre de usuario'
    username = kargs.get('username')
    print(f'username: {username}')
    return HttpResponse('<h1> Hello %s! </h1>' % username)
    
def about(request):
    'Funcion para mostrar la vista About'
    #return HttpResponse('<h1> About Page </h1>')
    username = "Cristian Echevarria"
    return render(request, 'about.html',{
        'username':  username  })


def projects_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    
    # Filtrar proyectos según la búsqueda
    projects = Project.objects.filter(name__icontains=search_query)
    
    # Filtrar según el estado de las tareas
    if status_filter == 'with_completed_tasks':
        projects = projects.filter(task__done=True).distinct()
    elif status_filter == 'with_pending_tasks':
        projects = projects.filter(task__done=False).distinct()

    return render(request, 'projects.html', {
        'projects': projects,
        'active_filter': status_filter
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        task = get_object_or_404(Task, id=task_id)

        if action == 'toggle_done':
            task.done = not task.done
            task.save()

        return redirect('project_detail', project_id=project.id)

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks
    })

def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Project.objects.create(name=name)
        return redirect('projects')
    return render(request, 'create_project.html')

def tasks_view(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    
    # Filtrar tareas según la búsqueda
    tasks = Task.objects.filter(title__icontains=search_query)
    
    # Filtrar según el estado
    if status_filter == 'active':
        tasks = tasks.filter(done=False)
    elif status_filter == 'completed':
        tasks = tasks.filter(done=True)

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'active_filter': status_filter
    })

def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Crear una nueva tarea asociada al proyecto
        Task.objects.create(title=title, description=description, project=project)
        
        # Redirigir a la vista de detalles del proyecto
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'create_task.html', {'project': project})


def create_task_general(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, id=project_id)

        # Crear una nueva tarea
        Task.objects.create(title=title, description=description, project=project)

        # Redirigir a la lista de tareas
        return redirect('tasks')

    # Obtener todos los proyectos para mostrarlos en un selector
    projects = Project.objects.all()
    return render(request, 'create_task.html', {'projects': projects})


# Vista para eliminar una tarea
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')

# Vista para marcar una tarea como "hecho"
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.done = True
    task.save()
    return redirect('tasks')

# Vista para actualizar una tarea
# def update_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     projects = Project.objects.all()  # Obtener todos los proyectos

#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         done = 'done' in request.POST
#         project_id = request.POST.get('project')  # Obtener el ID del proyecto

#         # Actualizar la tarea
#         task.title = title
#         task.description = description
#         task.done = done
#         if project_id:
#             task.project = Project.objects.get(id=project_id)
#         task.save()

#         return redirect('tasks')

#     return render(request, 'update_task.html', {
#         'task': task,
#         'projects': projects
#     })

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        done = request.POST.get('done') == 'on'

        task.title = title
        task.description = description
        task.done = done
        task.save()

        # Redirigir según el parámetro redirect_url o a 'tasks' por defecto
        redirect_url = request.POST.get('redirect_url', 'tasks')
        return redirect(redirect_url)

    # Obtener la URL de redirección desde el parámetro GET si está disponible
    redirect_url = request.GET.get('redirect_url', 'tasks')

    return render(request, 'update_task.html', {'task': task, 'redirect_url': redirect_url})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Cambia esto si 'index' no es correcto
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            print(f"Fallo en la autenticación para el usuario: {username}")
    return render(request, 'login.html', {'title': 'Iniciar Sesión'})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('signup')
        
        # Crear el usuario
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Usuario creado con éxito. Ahora puedes iniciar sesión.')
        return redirect('login')
    return render(request, 'signup.html')