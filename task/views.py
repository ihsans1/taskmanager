from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import UserRegistrationForm, TaskForm
from .models import Task
from .models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.conf import settings

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request,"registration/register.html", {"form": form})
    def post(self, request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            verification_link= request.build_absolute_uri(
                reverse('activate',kwargs={'uidb64': uid, 'token': token})
            )
            send_mail(

               'verify your account',
                f'click the link to verify your account: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
)

            return HttpResponse("check your email to activate your account ")
        return render (request,"registration/register.html",{"form": form})
    
User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()   # uid ko decode karo
        user = User.objects.get(pk=uid)                # database se user fetch karo
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True   # account activate karo
        user.save()
        login(request, user)    # user ko login karao
        return redirect('task_list')  # task list page pe redirect karo
    else:
        return HttpResponse("Activation link is invalid!")  # agar link ghalat ho




@method_decorator(login_required, name="dispatch")
class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user).order_by("due_date")
        status_filter = request.GET.get("status")
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        return render(request, "tasks/task_list.html", {"tasks": tasks})


@method_decorator(login_required, name="dispatch")
class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, "tasks/task_form.html", {"form": form})

    def post(self, request):
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
        return render(request, "tasks/task_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "tasks/task_form.html", {"form": form})

    def post(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
        return render(request, "tasks/task_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class TaskDeleteView(View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        return render(request, "tasks/task_confirm_delete.html", {"task": task})

    def post(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        task.delete()
        return redirect("task_list")
