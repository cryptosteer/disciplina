from django import forms
from crispy_forms.helper import FormHelper
from .models import *


class TaskBulkForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TaskBulkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ajaxForm'
        self.helper.form_action = 'task_bulk'

    items = forms.CharField(label = "List of tasks", required = True, widget=forms.Textarea, )


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'ajaxForm'


    class Meta:
        model = Task
        fields = ('name', 'done', 'archived', 'working', 'description', )


class HabitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HabitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'ajaxForm'


    class Meta:
        model = Habit
        fields = ('name', 'working', 'archived', 'description', )
