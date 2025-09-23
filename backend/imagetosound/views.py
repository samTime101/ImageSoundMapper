# SEPTEMBER 23 2025
# SAMIP REGMI

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import FileResponse
from converter.image_sound_mapper import ImageToSound
import os ,uuid

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

class ImageToSoundView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['file']
            unique_id = str(uuid.uuid4())
            image_path = os.path.join(UPLOAD_DIR, f"{unique_id}_{image_file.name}")
            grayscale_path = os.path.join(RESULT_DIR, f"{unique_id}_grayscale.png")
            resized_path = os.path.join(RESULT_DIR, f"{unique_id}_resized.png")
            sound_path = os.path.join(RESULT_DIR, f"{unique_id}_output.wav")

            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            its = ImageToSound(image_path, grayscale_path, resized_path, sound_path)
            its.compress_image_with_new_dimension((50, 50))
            its.image_to_grayscale()
            pixels = its.pixel_value_extractor()
            freqs = its.pixel_to_frequency(pixels)
            its.frequency_to_sound(freqs)


            return FileResponse(open(sound_path, "rb") , content_type='audio/wav')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
