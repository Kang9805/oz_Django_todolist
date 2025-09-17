from django import forms
from .models import Todo

# 할 일 생성 시 필요한 필드들을 포함한 폼
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']

# 할 일 수정할 때 사용하는 폼
class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']