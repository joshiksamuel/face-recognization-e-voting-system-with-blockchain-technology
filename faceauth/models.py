from django.db import models
class UserImages(models.Model):
    face_image = models.ImageField(upload_to='user_faces/')
    def __str__(self):
        return f'UserImage {self.id}'