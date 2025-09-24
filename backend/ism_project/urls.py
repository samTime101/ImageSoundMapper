from django.contrib import admin
from django.urls import path
from imagetosound.views import ImageToSoundStreamLogs , ImageToSoundView , ImageToSoundPreview
from soundtoimage.views import SoundToImageStreamLogs , SoundToImageView , SoundToImagePreview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('its/stream/', ImageToSoundStreamLogs.as_view(), name='image_to_sound_stream'),
    path('sti/stream/', SoundToImageStreamLogs.as_view(), name='sound_to_image_stream'),
    path('its/', ImageToSoundView.as_view(), name='image_to_sound'),
    path('sti/', SoundToImageView.as_view(), name='sound_to_image'),
    path('its/preview/', ImageToSoundPreview.as_view(), name='image_to_sound_preview'),
    path('sti/preview/', SoundToImagePreview.as_view(), name='sound_to_image_preview'),
]
