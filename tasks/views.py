from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')
            
def signup(request):
    if request.method == 'GET': 
        print('Enviando formulario')
        return render(request, 'signup.html', {
        'form' : UserCreationForm
        })

    else:
        #Validar contraseñas
        if request.POST['password1'] == request.POST ['password2']:
            try:
                #Register user
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1']) #Este metodo recibe el usuario y contraseña y devuelve un objeto user    
                user.save() #Lo guarda en la db, por defecto sqlite3
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Username already exists'
                })
                
        else:
            return render(request, 'signup.html', {
                'form' : UserCreationForm,
                'error' : 'Password do not match'
            }) 

@login_required
def tasks(request):
    #tasks = Task.objects.all() #Consulta a la BD , pero muestra todos los datos
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True) #Usa un filtro para mirar cual muestra
    return render(request, 'tasks.html', {
        'tasks' : tasks
    } )

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted') #Usa un filtro para mirar cual muestra
    return render(request, 'tasks.html', {
        'tasks' : tasks
    } )

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False) #Lo devuelve pero no lo guarda
            new_task.user = request.user #User logueado
            new_task.save() #Se guarda en la BD
            return redirect('tasks')
        except ValueError: 
            return render(request, 'create_task.html', {
            'form' : TaskForm,
            'error' : 'Please provide valide data'
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task) #Llena el formulario con esa tarea
        return render (request, 'task_detail.html', {
            'task': task, 
            'form' : form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'task_detail.html', {
            'task': task, 
            'form' : form, 
            'error' : 'Error updating Task'
        })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')
    
def signin(request):
    if request.method == 'GET': 
        return render(request, 'signin.html', {
            'form' : AuthenticationForm
        })
    else: 
        #Devuelve un user si es válido
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form' : AuthenticationForm,
            'error' : 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')


        