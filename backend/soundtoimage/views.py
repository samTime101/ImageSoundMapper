import os
import uuid
from django.http import StreamingHttpResponse , FileResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from converter.image_sound_mapper import SoundToImage 
from django.views import View
from rest_framework.response import Response
from rest_framework import status

class FileUploadSerializer(serializers.Serializer):
    audio = serializers.FileField()


class SoundToImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']
            unique_id = str(uuid.uuid4())
            
            upload_dir = os.path.join(unique_id,"uploads")
            os.makedirs(upload_dir, exist_ok=True)

            audio_path = os.path.join(upload_dir, f"audio.wav")
            with open(audio_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            return Response({"id": unique_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SoundToImageStreamLogs(View):
    def get(self, request):
        unique_id = request.GET.get("id")
        if not unique_id:
            return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        upload_dir = os.path.join(unique_id,"uploads")
        if not os.path.exists(upload_dir):
            return Response({"error": "Upload directory not found"}, status=status.HTTP_404_NOT_FOUND)
        audio_path = os.path.join(upload_dir, "audio.wav")
        if not os.path.exists(audio_path):
            return Response({"error": "Audio file not found"}, status=status.HTTP_404_NOT_FOUND)
        results_dir = os.path.join(unique_id, "results")
        result_file = os.path.join(results_dir, "reconstructed_image.png")
        os.makedirs(results_dir, exist_ok=True)

        sti = SoundToImage(audio_path, result_file)

        def log_generator():
            yield "data: 1. CONVERTING AUDIO TO CHUNKS\n\n"
            chunks,sr = sti.audio_file_to_chunks()
            yield "data: 2. EXTRACTING FREQUENCIES FROM CHUNKS\n\n"
            frequencies = sti.sound_to_frequency(chunks, sr)
            yield "data: 3. GENERATING IMAGE NOW\n\n"
            sti.sound_to_image(frequencies)
            yield "data: CONVERSION COMPLETED\n\n"
        return StreamingHttpResponse(log_generator(), content_type='text/event-stream')


class SoundToImagePreview(APIView):
    def get(self, request):
        unique_id = request.GET.get("id")
        if not unique_id:
            return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        results_dir = os.path.join(unique_id, "results")
        sound_path = os.path.join(results_dir, "reconstructed_image.png")
        print(f"Sound path->{sound_path}")

        if not os.path.exists(sound_path):
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(sound_path, 'rb'), content_type='image/png')