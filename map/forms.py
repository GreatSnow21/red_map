from django import forms
from .models import Node, Type, Content_type

class RouteForm(forms.Form):
    start_node = forms.ModelChoiceField(queryset=Node.objects.all(), label="Начальная точка", required=False)
    end_node = forms.ModelChoiceField(queryset=Node.objects.all(), label="Конечная точка", required=False)

class RouteByTypeForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Тип объекта", required=False)
    content_type = forms.ModelChoiceField(queryset=Content_type.objects.none(), label="Название объекта", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'type' in self.data:
            try:
                type_id = self.data.get('type')
                self.fields['content_type'].queryset = Content_type.objects.filter(content_type_link=type_id)
            except (ValueError, TypeError):
                pass
