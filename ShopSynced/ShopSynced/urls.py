"""
URL configuration for ShopSynced project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from core.views import FrontPageView, AboutPageView
from users.views import RegisterView, MyAccountView

urlpatterns = [
    # path('my-store/', include('users.urls')),
    path('login/', views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('myaccount/', MyAccountView.as_view(), name='myaccount'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('store.urls')),
    path('', FrontPageView.as_view(), name='frontpage'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
