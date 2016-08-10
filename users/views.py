from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout, authenticate, login as django_login
from tweets.models import Tweet
from users.forms import LoginForm, UserSignUpForm, UserProfileSignUpForm, TweetForm
from users.models import UserProfile
from django.views.generic import View


class HomeView(View):
    def __init__(self):
        self.context = {
            'errors': [],
            'tweet_form': TweetForm(),
            'tweets': None
        }

    def get(self, request):
        if request.user.is_authenticated():
            tweet_list = Tweet.objects.filter(author=request.user).order_by('-date')
            page = request.GET.get('page', 1)
            paginator = Paginator(tweet_list, 3)

            try:
                self.context['tweets'] = paginator.page(page)
            except PageNotAnInteger:
                self.context['tweets'] = paginator.page(1)
            except EmptyPage:
                self.context['tweets'] = paginator.page(paginator.num_pages)

            return render(request, 'users/home.html', self.context)
        else:
            return render(request, 'users/home.html')

    def post(self, request):
        tweet_form = TweetForm(request.POST)
        current_user = request.user

        if tweet_form.is_valid() and current_user.is_authenticated():
            tweet = Tweet(author=current_user, text=tweet_form.cleaned_data.get('text'))
            tweet.save()
        else:
            self.context['errors'].append('something wrong')
            return render(request, 'users/home.html', self.context)

        return redirect('site_home')


class SignUpView(View):
    def get(self, request):
        context = {
            'user_signup_form': UserSignUpForm(),
            'user_profile_signup_form': UserProfileSignUpForm()
        }
        return render(request, 'users/create_user.html', context)

    def post(self, request):
        user_form = UserSignUpForm(request.POST)
        user_profile_form = UserProfileSignUpForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            user_profile = UserProfile(user=user)
            user_profile_form = UserProfileSignUpForm(request.POST, instance=user_profile)
            user_profile_form.save()

        return redirect('create_user')


class LoginView(View):
    def get(self, request):
        error_messages = []
        form = LoginForm()
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)

            if user is None:
                error_messages.append('user or password does not match')
            else:
                if user.is_active:
                    django_login(request, user)
                    url = request.GET.get('next', 'site_home')
                    return redirect(url)
                else:
                    error_messages.append('user is not active')
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, 'users/login.html', context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('site_home')
