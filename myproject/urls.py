from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view
from boards import views
from accounts import views as accounts_views

urlpatterns = [
    #  Admin url
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.BoardListView.as_view(), name='home'),
    url(r'^home', views.BoardListView.as_view(), name='home'), # Ganti listview

    #  Account url
    url(r'^signup/', accounts_views.signup, name='signup'),
    url(r'^logout/', auth_view.LogoutView.as_view(), name='logout'),
    url(r'^login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^settings/account/?', accounts_views.UserUpdateView.as_view(), name='my_account'),

    # Account password reset
    url(r'^settings/password/$', auth_view.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    url(r'^settings/password/done/$', auth_view.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    #  Board url
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/new', views.new_board, name='new_board'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    # Topic url
    url(r'^boards/(?P<pk>\d+)/topics/(?P<t_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<t_pk>\d+)/reply/$', views.topic_reply, name='topic_reply'),
    # Edit post / reply
    url(r'^boards/(?P<pk>\d+)/topics/(?P<t_pk>\d+)/posts/(?P<p_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post'),

    # About
    url(r'^about/$', views.about, name='about'),
    url(r'^about/company/$', views.about_company, name='about_company'),
]
