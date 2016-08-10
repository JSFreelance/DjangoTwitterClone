from django.conf.urls import include, url
from django.contrib import admin
from users import views as user_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'TwitterClone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', user_views.HomeView.as_view(), name='site_home'),
    url(r'^create_user$', user_views.SignUpView.as_view(), name='create_user'),
    url(r'^login$', user_views.LoginView.as_view(), name='user_login'),
    url(r'^logout$', user_views.LogoutView.as_view(), name='user_logout'),
    url(r'^admin/', include(admin.site.urls))
]
