# SEPTEMBER 23 2025
# SAMIP REGMI

# from django.http import StreamingHttpResponse
# from rest_framework.views import View
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework.parsers import MultiPartParser, FormParser
# from converter.image_sound_mapper import SoundToImage
# from rest_framework.views import APIView
# import os , uuid


# class FileUploadSerializer(serializers.Serializer):
#     file = serializers.FileField()

# UPLOAD_DIR = "uploads"
# RESULT_DIR = "results"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(RESULT_DIR, exist_ok=True)


# class SoundToImageView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request):
#         serializer = FileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             sound_file = serializer.validated_data['file']
#             unique_id = str(uuid.uuid4())
#             sound_path = os.path.join(UPLOAD_DIR, f"{unique_id}_uploaded.wav")

#             with open(sound_path, 'wb+') as destination:
#                 for chunk in sound_file.chunks():
#                     destination.write(chunk)
#             return Response({"id": unique_id}, status=201)
#         return Response(serializer.errors, status=400)


