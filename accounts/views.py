from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import login as auth_login
from .form import SignupForm

# untuk user update view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

def signup(request):
    # do something...
    if request.method == 'POST' :
        form = SignupForm(request.POST)
        if form.is_valid() :
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else :
        form = SignupForm()

    return render(request, 'signup.html', {"form":form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView) :
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self) :
        return self.request.user
