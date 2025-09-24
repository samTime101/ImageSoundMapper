import os
import uuid
from django.http import StreamingHttpResponse , FileResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from converter.image_sound_mapper import ImageToSound 
from django.views import View
from rest_framework.response import Response
from rest_framework import status

class FileUploadSerializer(serializers.Serializer):
    image = serializers.FileField()


class ImageToSoundView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            unique_id = str(uuid.uuid4())
            
            upload_dir = os.path.join(unique_id,"uploads")
            os.makedirs(upload_dir, exist_ok=True)

            image_path = os.path.join(upload_dir, f"image.png")
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            return Response({"id": unique_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ImageToSoundStreamLogs(View):
    def get(self, request):
        unique_id = request.GET.get("id")
        if not unique_id:
            return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        upload_dir = os.path.join(unique_id,"uploads")
        if not os.path.exists(upload_dir):
            return Response({"error": "Upload directory not found"}, status=status.HTTP_404_NOT_FOUND)

        image_path = os.path.join(upload_dir, "image.png")

        if not os.path.exists(image_path):
            return Response({"error": "Image file not found"}, status=status.HTTP_404_NOT_FOUND)

        results_dir = os.path.join(unique_id, "results")
        os.makedirs(results_dir, exist_ok=True)

        grayscale_path = os.path.join(results_dir, f"grayscale.png")
        resized_path = os.path.join(results_dir, f"resized.png")
        sound_path = os.path.join(results_dir, f"sound.wav")

        its = ImageToSound(
            image_path,
            grayscale_path,
            resized_path,
            sound_path
        )

        def log_generator():
            yield 'data: 1. RESIZING IMAGE \n\n'
            its.compress_image_with_new_dimension((50, 50))
            yield 'data: 2. IMAGE RESIZED \n\n'

            yield 'data: 3. CONVERTING TO GRAY SCALE \n\n'
            its.image_to_grayscale()
            yield 'data: 4. GRAYSCALE CONVERSION COMPLETE \n\n'

            yield 'data: 5. EXTRACTION OF PIXEL VALUES \n\n'
            pixels = its.pixel_value_extractor()
            yield 'data: 6. EXTRACTION COMPLETE \n\n'

            yield 'data: 7. CONVERTING PIXELS TO FREQUENCIES \n\n'
            freqs = its.pixel_to_frequency(pixels)
            yield 'data: 9. CONVERTING FREQUENCIES TO SOUND \n\n'
            its.frequency_to_sound(freqs)
            yield "data: CONVERSION COMPLETED\n\n"


        return StreamingHttpResponse(log_generator(), content_type='text/event-stream')



class ImageToSoundPreview(APIView):
    def get(self, request):
        unique_id = request.GET.get("id")
        if not unique_id:
            return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        results_dir = os.path.join(unique_id, "results")
        sound_path = os.path.join(results_dir, "sound.wav")
        print(f"Sound path->{sound_path}")

        if not os.path.exists(sound_path):
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(sound_path, 'rb'), content_type='audio/wav')
