from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True) #Blank true es que es opcional para el admin
    created = models.DateTimeField(auto_now_add=True) #Fecha, cuando se crea la tarea coge la hora de ahora como creado
    datecompleted = models.DateTimeField(null=True, blank = True)
    important = models.BooleanField(default=False) #Por defecto las tareas no son importantes
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #Se elimina en cascada, lo relacionado

    def __str__(self):
        return self.title + '- by ' + self.user.username 