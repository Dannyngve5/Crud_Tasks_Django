from django import forms
from .models import Task

#Este formulario se puede enviar al FRONTEND
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'deadline']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Write a tittle'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'rows': '5',  'placeholder' : 'Write a description'}),
            #'important' : forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}), 
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
