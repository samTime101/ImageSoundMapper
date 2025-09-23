# SEPTEMBER 23 2025
# SAMIP REGMI

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import FileResponse
from converter.image_sound_mapper import SoundToImage
import os , uuid

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

class SoundToImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            sound_file = serializer.validated_data['file']
            unique_id = str(uuid.uuid4())
            sound_path = os.path.join(UPLOAD_DIR, f"{unique_id}_{sound_file.name}")
            image_path = os.path.join(RESULT_DIR, f"{unique_id}_output.png")

            with open(sound_path, 'wb+') as destination:
                for chunk in sound_file.chunks():
                    destination.write(chunk)

            sti = SoundToImage(sound_path, image_path)
            detected_chunks , detected_sr = sti.audio_file_to_chunks()
            detected_freqs = sti.sound_to_frequency(detected_chunks , detected_sr)
            sti.sound_to_image(detected_freqs)


            return FileResponse(open(image_path, "rb") , content_type='image/png')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)