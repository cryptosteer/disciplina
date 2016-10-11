from django.conf.urls import url
from . import views

urlpatterns = [
    # Dashboard
    url(r'^$', views.index, name='index'),
    url(r'^today_list/$', views.today_list, name='today_list'),
    url(r'^sort_today_items/$', views.sort_today_items, name='sort_today_items'),
    url(r'^finish_item/$', views.finish_item, name='finish_item'),
    # Tasks
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^sort_task_items/$', views.sort_task_items, name='sort_task_items'),
    url(r'^task_create/$', views.TaskCreateView.as_view(),
        name='task_create'),
    url(r'^task_update/$', views.TaskUpdateView.as_view(),
        name='task_update'),
    url(r'^task_update/(?P<pk>[0-9]+)$',
        views.TaskUpdateView.as_view(), name='task_update'),
    url(r'^task_delete/$', views.delete_tasks, name='task_delete'),
    url(r'^task_finish/$', views.finish_tasks, name='task_finish'),
    url(r'^task_bulk/$', views.task_bulk, name='task_bulk'),
    url(r'^task_working/$', views.task_working, name='task_working'),
    url(r'^task_archive/$', views.task_archive, name='task_archive'),
    # Habits
    url(r'^habits/$', views.habits, name='habits'),
    url(r'^habit_list/$', views.habit_list, name='habit_list'),
    url(r'^habit_create/$', views.HabitCreateView.as_view(),
        name='habit_create'),
    url(r'^habit_update/$', views.HabitUpdateView.as_view(),
        name='habit_update'),
    url(r'^habit_update/(?P<pk>[0-9]+)$',
        views.HabitUpdateView.as_view(), name='habit_update'),
    url(r'^habit_delete/$', views.delete_habits, name='habit_delete'),
    url(r'^habit_schedule/$', views.habit_schedule, name='habit_schedule'),
    url(r'^habit_schedule/(?P<pk>[0-9]+)$', views.habit_schedule, name='habit_schedule'),
    # url(r'^habit_schedule_list/$', views.habit_schedule_list, name='habit_schedule_list'),
    # url(r'^habit_schedule_create/$', views.HabitCreateView.as_view(),
    #     name='habit_schedule_create'),
    # url(r'^habit_schedule_update/$', views.HabitUpdateView.as_view(),
    #     name='habit_schedule_update'),
    # url(r'^habit_update/(?P<pk>[0-9]+)$',
    #     views.HabitUpdateView.as_view(), name='habit_update'),
    # url(r'^habit_delete/$', views.delete_habits, name='habit_delete'),
    # Projects
    url(r'^projects/$', views.index, name='projects'),
    url(r'^testing/$', views.testing, name='testing'),
]
