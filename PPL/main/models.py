from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PeringkatFinal(models.Model):
    siswa = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    total_skor = models.IntegerField()
    total_waktu_detik = models.IntegerField()
    waktu_selesai = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.siswa.username} - {self.total_skor} Poin"