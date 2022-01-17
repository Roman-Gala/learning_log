"""URL paths for learning_logs"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Shows all topics
    path('topics/', views.topics, name='topics'),
    # Shows a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Adding new topic
    path('new_topic/', views.NewTopic.as_view(), name='new_topic'),
    # Adding new entry
    path('new_entry/<int:topic_id>/', views.NewEntry.as_view(),
         name='new_entry'),
    # Editing an existing entry
    path('edit_entry/<int:entry_id>/', views.EditEntry.as_view(),
         name='edit_entry'),
    # Deleting an entry
    path('delete_entry/<int:entry_id>/', views.delete_entry,
         name='delete_entry'),
    # Deleting a topic
    path('delete_topic/<int:topic_id>/', views.delete_topic,
         name='delete_topic'),
]
