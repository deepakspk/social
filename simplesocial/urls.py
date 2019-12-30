"""simplesocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from posts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name="index"),
    path('allposts', views.PostList.as_view(), name="all"),
    path('admin/', admin.site.urls),
    path('test/', views.TestPage.as_view(), name="test"),
    path('thanks/', views.ThanksPage.as_view(), name="thanks"),
    path('thank_you/', views.ThanksMsg.as_view(), name="thanksformsg"),
    path('nurses/', include("nursesApp.urls", namespace="nurses")),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('posts/', include("posts.urls", namespace="posts")),
    path('groups/',include("groups.urls", namespace="groups")),
    path('blog/',include("blog.urls", namespace="blog")),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
