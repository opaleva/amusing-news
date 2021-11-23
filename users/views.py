from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import RewrittenCreationForm


class SignUpView(CreateView):
    form_class = RewrittenCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


# def logout_user(request):
#     logout(request)
#     return redirect('articles:index')