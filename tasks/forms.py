from django.forms import ModelForm
from .models import Task

#Este formulario se puede enviar al FRONTEND
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
