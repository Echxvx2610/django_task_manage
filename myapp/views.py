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


def projects(request):
    'Funcion para mostrar la vista Projects'
    projects = Project.objects.all()
    #lista de objetos para imprimir en el template
    return render(request, 'projects.html',{
        'projects' : projects
    })

def tasks(request):
    'Funcion para mostrar la vista Tasks'
    tasks = Task.objects.all()
    return render(request, 'tasks.html',{
        'tasks' : tasks
    })

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