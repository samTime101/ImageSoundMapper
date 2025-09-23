"""
URL configuration for ism_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from soundtoimage.views import SoundToImageView
from imagetosound.views import ImageToSoundView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('encrypt/', ImageToSoundView.as_view(), name='image_to_sound'),
    path('decrypt/', SoundToImageView.as_view(), name='sound_to_image'),
]
