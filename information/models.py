from django.db import models

# Create your models here.
class pdf_reader(models.Model):
    title=models.CharField(max_length=100)
    fiel=models.FileField(upload_to='pdf/')
    
    
    def __str__(self):
        f"{self.title}"