import face_recognition
import base64
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import UserImages
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        face_image_data = request.POST['face_image']

        # Convert base64 image data to a file
        face_image_data = face_image_data.split(",")[1]  # Remove the "data:image/jpeg;base64," part
        face_image = ContentFile(base64.b64decode(face_image_data), name='face.jpg')

        # Save the face image in the database
        UserImages.objects.create(face_image=face_image)

        return JsonResponse({'status': 'success', 'message': 'Face image registered successfully!'})

    return render(request, 'face_register.html')


@csrf_exempt


def login_user(request):
    if request.method == 'POST':
        face_image_data = request.POST.get('face_image')

        if not face_image_data:
            return JsonResponse({'success': False, 'message': 'No image data provided.'})

        # Convert base64 image data to a file
        face_image_data = face_image_data.split(",")[1]
        uploaded_image = ContentFile(base64.b64decode(face_image_data), name='uploaded_face.jpg')

        # Load the uploaded face image
        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)

        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            user_images = UserImages.objects.all()

            for user_image in user_images:
                stored_face_image = face_recognition.load_image_file(user_image.face_image.path)
                stored_face_encoding = face_recognition.face_encodings(stored_face_image)

                if stored_face_encoding:
                    stored_face_encoding = stored_face_encoding[0]

                    # Compare the faces
                    match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)
                    if match[0]:
                        login_url = reverse('login')  # Adjust 'login' to your actual login URL name
                        return JsonResponse({
                            'success': True,
                            'message': 'Valid Voter',
                            'login_url': login_url
                        })

            return JsonResponse({'success': False, 'message': 'Invalid Voter'})

        return JsonResponse({'success': False, 'message': 'No face detected in the image.'})

    return render(request, 'face_login.html')


