from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """The home page for learning_log."""
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """Page that shows all the topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Single topic page."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        return HttpResponse(status=403)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


class NewTopic(View):
    """Add a new topic."""
    @method_decorator(login_required())
    def get(self, request):
        # No data submitted; render blank form.
        form = TopicForm()
        context = {'form': form}
        return render(request, 'learning_logs/new_topic.html', context)

    @method_decorator(login_required())
    def post(self, request):
        # Post data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        else:
            context = {'form': form}
            return render(request, 'learning_logs/new_topic.html', context)


class NewEntry(View):
    """Add a new entry"""
    @method_decorator(login_required())
    def get(self, request, topic_id):
        # No data submitted; render blank form.
        form = EntryForm()
        topic = Topic.objects.get(id=topic_id)
        context = {'topic': topic, 'form': form}
        return render(request, 'learning_logs/new_entry.html', context)

    @method_decorator(login_required())
    def post(self, request, topic_id):
        # Post data submitted; process data.
        form = EntryForm(data=request.POST)
        topic = Topic.objects.get(id=topic_id)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        else:
            context = {'topic': topic, 'form': form}
            return render(request, 'learning_logs/new_entry.html', context)


class EditEntry(View):
    """Edit an existing entry"""
    @method_decorator(login_required())
    def get(self, request, entry_id):
        # Initial request; render filled form.
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
        if topic.owner != request.user:
            return HttpResponse(status=403)
        form = EntryForm(instance=entry)
        context = {'entry': entry, 'topic': topic, 'form': form}
        return render(request, 'learning_logs/edit_entry.html', context)

    @method_decorator(login_required())
    def post(self, request, entry_id):
        # POST data submitted; process data.
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        else:
            context = {'entry': entry, 'topic': topic, 'form': form}
            return render(request, 'learning_logs/edit_entry.html', context)


@login_required()
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.user == topic.owner:
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)
    else:
        return HttpResponse(status=403)


@login_required()
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user == topic.owner:
        topic.delete()
        return redirect('learning_logs:topics')
    else:
        return HttpResponse(status=403)
