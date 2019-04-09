from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Topic, User, Post
from django.http import HttpResponse
from django.http import Http404
from .form import NewTopicForm, NewBoardForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

# Create your views here.

#######################
### Contoh ListView ###
#######################

### Tanpa argument / parameter ###
class BoardListView(ListView) :
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 5

### dengan 1 argument / parameter ###
class TopicListView(ListView) :
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs) :
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self) :
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.all()
        return queryset

class PostListView(ListView) :
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs) :
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False) :
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self) :
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('t_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

# Contoh UpdateView #
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView) :
    model = Post
    fields = ['message']
    template_name = 'edit_post.html'
    pk_url_kwarg = 'p_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form) :
        post = form.save(commit = False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        return redirect('topic_posts', pk=post.topic.board.pk, t_pk=post.topic.pk)

@login_required
def topic_reply(request, pk, t_pk):
    topic = get_object_or_404(Topic, board__pk = pk, pk = t_pk)

    if request.method == 'POST' :
        form = PostForm(request.POST)
        if form.is_valid() :
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 't_pk': t_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
            #return redirect('topic_posts', pk=pk, t_pk = t_pk)
    else :
        form = PostForm()

    return render(request, 'topic_reply.html', {'form': form, 'topic': topic})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board,pk=pk)

    if request.method == 'POST' :
        form = NewTopicForm(request.POST)
        if form.is_valid() :
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)
    else :
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'form': form, 'board': board})

@login_required
def new_board(request):

    if request.method == 'POST' :
        form = NewBoardForm(request.POST)
        if form.is_valid() :
            board = form.save(commit=False)
            board.save()
            return redirect('home')
    else:
        form = NewBoardForm()

    return render(request, 'new_board.html', {'form':form})

def about(request):
    return render(request, 'about.html')

def about_company(request):
    return render(request, 'about_company.html', {'company_name': 'Simple Complex'})

# obsolete views
"""
###############################
## Sudah diganti ke ListView ##
###############################

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards} )

def board_topics(request, pk):
    board = get_object_or_404(Board,pk=pk)
    queryset = board.topics.all()
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,5)
    topics = paginator.page(1)

    try :
        topics = paginator.page(page)
    except PageNotAnInteger :
        topics = paginator.page(1)
    except EmptyPage :
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})

def topic_posts(request, pk, t_pk):
    topic = get_object_or_404(Topic, board__pk=pk , pk=t_pk)
    topic.views += 1
    topic.save()
    queryset = topic.posts.all()

    page = request.GET.get('page',1)
    paginator = Paginator(queryset,3)
    posts = paginator.page(1)

    try :
        posts = paginator.page(page)
    except PageNotAnInteger :
        posts = paginator.page(1)
    except EmptyPage :
        posts = paginator.page(paginator.num_pages)

    return render(request, 'topic_posts.html', {'topic': topic, 'posts': posts})

"""
