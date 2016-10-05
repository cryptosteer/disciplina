from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .serializers import *
# from rest_framework import viewsets
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView
# from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import datetime, json


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    tasks = Task.objects.order_by('-creation')
    context = {'tasks': tasks}
    return render(request, 'website/dashboard.html', context)


def today_list(request):
    if request.method == "POST":
        filterargs = {}
        todayItems = []
        if(request.POST['type'] == "Active"):
            filterargs['archived'] = False
        queryset = Task.objects.all().order_by('order_today').filter(**filterargs)
        for item in queryset:
            todayItems.append(TodayItem(item.id, item.name, item.done, item.order_today, 'Task'))
        serializer = TodayItemsSerializer(todayItems, many=True)
    else:
        serializer = TaskSerializer()
    return JSONResponse(serializer.data)


def sort_today_items(request):
    if request.method == "POST":
        toupdate = json.loads(request.POST['toupdate'])
        for key, value in toupdate.items():
            tarea = Task.objects.get(pk=key)
            tarea.order_today = value
            tarea.save()
        return HttpResponse("Items sorted")


def sort_task_items(request):
    if request.method == "POST":
        toupdate = json.loads(request.POST['toupdate'])
        for key, value in toupdate.items():
            tarea = Task.objects.get(pk=key)
            tarea.order_task = value
            tarea.save()
        return HttpResponse("Items sorted")


def finish_item(request):
    if request.method == "POST":
        toggle = 0 if(request.POST['done'] == "true") else 1
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE website_task SET done = " + str(toggle) + " WHERE id = " + request.POST['id'])
        return HttpResponse('Task updated' + request.POST['done'])


def tasks(request):
    return render(request, 'website/tasks.html')


def task_list(request):
    if request.method == "POST":
        filterargs = {}
        if(request.POST['location'] == "Active"):
            filterargs['archived'] = False
        elif(request.POST['location'] == "Archived"):
            filterargs['archived'] = True
        if(request.POST['status'] == "Pending"):
            filterargs['done'] = False
        elif(request.POST['status'] == "Finished"):
            filterargs['done'] = True
        if(request.POST['working'] == "Not working"):
            filterargs['working'] = False
        elif(request.POST['working'] == "Working"):
            filterargs['working'] = True
        if(request.POST['date'] == "Yesterday"):
            filterargs['creation__gt'] = datetime.date.today() - datetime.timedelta(days=1)
        elif(request.POST['date'] == "Last week"):
            filterargs['creation__gt'] = datetime.date.today() - datetime.timedelta(weeks=1)
        elif(request.POST['date'] == "Last month"):
            filterargs['creation__gt'] = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        queryset = Task.objects.all().order_by('order_task').filter(**filterargs)
        serializer = TaskSerializer(queryset, many=True)
    else:
        serializer = TaskSerializer()
    return JSONResponse(serializer.data)


def habits(request):
    return render(request, 'website/habits.html')


def habit_list(request):
    if request.method == "POST":
        filterargs = {}
        if(request.POST['location'] == "Active"):
            filterargs['archived'] = False
        elif(request.POST['location'] == "Archived"):
            filterargs['archived'] = True
        if(request.POST['working'] == "Not working"):
            filterargs['working'] = False
        elif(request.POST['working'] == "Working"):
            filterargs['working'] = True
        queryset = Habit.objects.all().order_by('order_habit').filter(**filterargs)
        serializer = HabitSerializer(queryset, many=True)
    else:
        serializer = HabitSerializer()
    return JSONResponse(serializer.data)


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'website/modal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Task'
        context['name_btn'] = 'Create'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('Task ' + self.object.name + ' created')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'website/modal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Task'
        context['name_btn'] = 'Update'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse('Task <b>' + self.object.name + '</b> updated')


def delete_tasks(request):
    if request.method == "GET":
        return HttpResponse(render_to_string('website/modal_confirm.html', {'title': 'Delete Task(s)', 'name_btn': 'Delete'}, request=request))
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute("DELETE FROM website_task WHERE id in " +
                       request.POST['items'])
        return HttpResponse('<b>' + request.POST['items_count'] + '</b> task(s) deleted')


def finish_tasks(request):
    if request.method == "GET":
        return HttpResponse(render_to_string('website/modal_confirm.html', {'title': 'Finish Task(s)', 'name_btn': 'Finish'}, request=request))
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE website_task SET done = 1 WHERE id in " + request.POST['items'])
        return HttpResponse('<b>' + request.POST['items_count'] + '</b> task(s) finished')


def task_working(request):
    if request.method == "GET":
        return HttpResponse(render_to_string('website/modal_confirm.html', {'title': 'Task(s) Working On', 'name_btn': 'Working'}, request=request))
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE website_task SET working = 1 WHERE id in " + request.POST['items'])
        return HttpResponse('<b>' + request.POST['items_count'] + '</b> task(s) working on')


def task_archive(request):
    if request.method == "GET":
        return HttpResponse(render_to_string('website/modal_confirm.html',
                                             {'title': 'Archive Task(s)',
                                              'name_btn': 'Archive'},
                                             request=request))
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE website_task SET archived = 1 WHERE id in " +
            request.POST['items'])
        return HttpResponse('<b>' + request.POST['items_count'] +
                            '</b> task(s) Archived')


def task_bulk(request):
    if request.method == "GET":
        return HttpResponse(render_to_string(
            'website/modal_form.html',
            {'title': 'Create Multiple Task(s)',
             'name_btn': 'Create',
             'form': TaskBulkForm()}, request=request, ))
    if request.method == "POST":
        items = request.POST['items']
        items = items.strip()
        item_list = items.split('\n')
        items_count = len(item_list)
        for item in item_list:
            task = Task(name=item)
            task.save()
        return HttpResponse('<b>' + str(items_count) + '</b> task(s) created')


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all().order_by('order_task')  # .filter(archived=False)
#     serializer_class = TaskSerializer


class HabitCreateView(CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'website/modal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Habit'
        context['name_btn'] = 'Create'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('Habit ' + self.object.name + ' created')


class HabitUpdateView(UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'website/modal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Habit'
        context['name_btn'] = 'Update'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponse('Habit <b>' + self.object.name + '</b> updated')


def delete_habits(request):
    if request.method == "GET":
        return HttpResponse(render_to_string('website/modal_confirm.html', {'title': 'Delete Habit(s)', 'name_btn': 'Delete'}, request=request))
    if request.method == "POST":
        cursor = connection.cursor()
        cursor.execute("DELETE FROM website_habit WHERE id in " +
                       request.POST['items'])
        return HttpResponse('<b>' + request.POST['items_count'] + '</b> habit(s) deleted')
