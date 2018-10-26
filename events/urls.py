from django.urls import path
from . import views

urlpatterns = [
    path('events', views.index, name='agenda-events-index'),
    path('all', views.all, name='agenda-events-all'),
    path('<int:id>', views.show, name='agenda-events-show'),
    path('<int:year>/<int:month>/<int:day>', views.day, name='agenda-events-day'),
    path('new', views.new, name='agenda-events-new'),
    path('delete/<int:id>', views.delete, name='agenda-events-delete'),
    path('edit', views.edit, name='agenda-events-edit'),

    path('peoples', views.people_list, name='people_list'),
    path('peoples/<int:pk>/', views.people_detail, name='people_detail'),
    path('peoples/new/', views.people_new, name='people_new'),
    path('peoples/<int:pk>/edit/', views.people_edit, name='people_edit'),
 ]