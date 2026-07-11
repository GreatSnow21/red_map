from django import forms
from .models import Node

class RouteForm(forms.Form):
    start_node = forms.ModelChoiceField(queryset=Node.objects.all(), label="Начальная точка")
    end_node = forms.ModelChoiceField(queryset=Node.objects.all(), label="Конечная точка")